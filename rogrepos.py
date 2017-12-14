from datetime import datetime
from github import Github
from threading import Thread
from queue import Queue
import click
import sys
from rcfile import rcfile

limit = 365 * 2


# Code snippet from https://gist.github.com/everilae/9697228
class ThreadedGenerator(object):
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
    return value if value else default


def print_repo(repo):
    print(repo.full_name)

    if repo.description:
        print('\tDescription: {}'.format(repo.description))

    if repo.fork:
        print('\tForked     : from {}'.format(repo._parent.full_name))

    print('\tUpdated    : {} / {} day(s) ago'.format(repo.updated_at, repo.neglected_days))
    print('\tSize       : {} KB'.format(repo.size))


def delete_repo(repo):
    repo.delete()
    print('{} was deleted.\n'.format(repo.full_name))


def get_repos(g):
    now = datetime.now()
    user = g.get_user()

    for repo in user.get_repos():
        repo.neglected_days = (now - repo.updated_at).days

        if repo.fork:
            repo._parent = repo.parent

        yield repo


def get_orgs(g):
    user = g.get_user()

    for org in user.get_orgs():
        print('\t{}, {} public repo(s), {} private repo(s)'.format(
            org.name, org.public_repos, org.total_private_repos))
        yield org


def get_total_repos(g):
    user = g.get_user()
    total_repos = default(user.public_repos, 0) + default(user.total_private_repos, 0)

    print('Retrieving organizations from GitHub...')
    for org in get_orgs(g):
        total_repos += default(org.public_repos, 0) + default(org.total_private_repos, 0)

    return total_repos


def main():
    args = rcfile('rogrepos')
    g = Github(args['token'])

    total_repos = get_total_repos(g)

    print('Retrieving {} repositorie(s) from GitHub...'.format(total_repos))

    c = 0
    for repo in ThreadedGenerator(get_repos, g=g):
        c += 1

        if repo.neglected_days < limit:
            continue

        print('{} of {}'.format(c, total_repos))
        print_repo(repo)

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
    sys.exit(main())
