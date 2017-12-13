from datetime import datetime
from github import Github
from threading import Thread
from queue import Queue
import click
import sys

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


def print_repo(repo):
    print(repo.full_name)

    if repo.description:
        print('\tDescription: {}'.format(repo.description))

    if repo.fork:
        print('\tForked     : from {}'.format(repo._parent.full_name))

    print('\tUpdated    : {} / {} day(s) ago'.format(repo.updated_at, repo.neglected_days))
    print('\tSize       : {} KB'.format(repo.size))


def delete_repo(repo):
    print('Deleted.')


def get_repos(g):
    now = datetime.now()
    user = g.get_user()

    for repo in user.get_repos():
        repo.neglected_days = (now - repo.updated_at).days

        if repo.fork:
            repo._parent = repo.parent

        yield repo


def main():
    g = Github("token")
    print('Retrieving repositories from GitHub...')

    for repo in ThreadedGenerator(get_repos, g=g):
        if repo.neglected_days < limit:
            continue

        print_repo(repo)

        if click.confirm('\tDo you really want to delete?', default=False):
            delete_repo(repo)
        else:
            print('')

    return 0


if __name__ == '__main__':
    sys.exit(main())
