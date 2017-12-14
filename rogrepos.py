from datetime import datetime
from github import Github
from threading import Thread
from queue import Queue
import click
import sys
from rcfile import rcfile


# Code snippet from https://gist.github.com/everilae/9697228
class ThreadedGenerator(object):
    """Helps generators run parallel."""
    def __init__(self, iterator, **kwargs):
        self._iterator = iterator
        self._sentinel = object()
        self._queue = Queue()
        self._thread = Thread(name=repr(iterator), target=self._run)
        self._kwargs = kwargs

    def _run(self):
        try:
            for value in self._iterator(**self._kwargs):
                self._queue.put(value)
        finally:
            self._queue.put(self._sentinel)

    def __iter__(self):
        self._thread.start()
        for value in iter(self._queue.get, self._sentinel):
            yield value

        self._thread.join()


def default(value, default):
    """Return default value when given value is None."""
    return value if value else default


def print_repo(repo):
    """Print basic information of given repository."""

    print(repo.full_name)

    if repo.description:
        print('\tDescription: {}'.format(repo.description))

    if repo.fork:
        print('\tForked     : from {}'.format(repo._parent.full_name))

    print('\tUpdated    : {} / {} day(s) ago'.format(repo.updated_at, repo.neglected_days))
    print('\tSize       : {} KB'.format(repo.size))


def delete_repo(repo):
    """Delete given repository."""

    repo.delete()
    print('{} was deleted.\n'.format(repo.full_name))


def gen_repos(g):
    """Generator of repositories."""

    now = datetime.now()
    user = g.get_user()

    for repo in user.get_repos():
        repo.neglected_days = (now - repo.updated_at).days

        if repo.fork:
            repo._parent = repo.parent

        yield repo


def gen_orgs(g):
    """Generator of orgs."""

    user = g.get_user()

    for org in user.get_orgs():
        print('\t{}, {} public repo(s), {} private repo(s)'.format(
            org.name, org.public_repos, org.total_private_repos))
        yield org


def get_total_repos(g):
    """Calculate total repository count."""

    user = g.get_user()
    total_repos = \
        default(user.public_repos, 0) + \
        default(user.total_private_repos, 0)

    print('Retrieving organizations from GitHub...')
    for org in gen_orgs(g):
        total_repos += \
            default(org.public_repos, 0) + \
            default(org.total_private_repos, 0)

    return total_repos


@click.command()
@click.option('--days', default=365, help='Find neglected repositories over given days.')
@click.option('--token', envvar='token', help='GitHub token to be used.')
def rogrepos(days, token):
    """Rogrepos helps you to remove outdated GitHub repositories."""

    if not token:
        args = rcfile('rogrepos')
        try:
            token = args['token']
        except KeyError:
            print('GitHub token is missing. Quitting...')
            return -1

    g = Github(token)

    total_repos = get_total_repos(g)
    print('Retrieving {} repositories from GitHub...'.format(total_repos))

    c = 0
    for repo in ThreadedGenerator(gen_repos, g=g):
        c += 1

        # We only care neglected repositories.
        if repo.neglected_days < days:
            continue

        print('{} of {}'.format(c, total_repos))
        print_repo(repo)

        # Ask twice when it's a source repository, not forked.
        if click.confirm('\tDo you really want to delete?', default=False):
            if not repo.fork:
                if click.confirm('\tThis is not a forked project. Are you sure?', default=False):
                    delete_repo(repo)
            else:
                delete_repo(repo)
        else:
            print('')

    return 0


if __name__ == '__main__':
    sys.exit(rogrepos())
