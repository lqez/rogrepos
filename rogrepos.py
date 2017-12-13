from github import Github
from datetime import datetime
import click

g = Github("token")
limit = 365 * 2

now = datetime.now()


def display_info(repo, not_updated_in_days):
    print(repo.full_name)

    if repo.description:
        print(repo.description)

    if repo.fork:
        print('\tForked from {}'.format(repo.parent.full_name))

    print('\tUpdated at {} / {} day(s) ago'.format(repo.updated_at, not_updated_in_days))

    events = list(repo.get_events())
    if events:
        print('\t{} event(s) found'.format(len(events)))
        for event in events:
            print('\t\t- {}, {} by {} ({})'.format(event.created_at, event.type, event.actor.login, event.actor.name))


for repo in g.get_user().get_repos():
    not_updated_in_days = (now - repo.updated_at).days

    if not_updated_in_days >= limit:
        display_info(repo, not_updated_in_days)
        if click.confirm('\tDo you really want to delete?', default=False):
            print('Deleted.')
        else:
            print('')
