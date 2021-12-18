import argparse
from commands.dispatch import dispatch


parser = argparse.ArgumentParser(description='Crawl League of Legends match data')
subparsers = parser.add_subparsers(help='command specific help')

# TODO: Check that the session doesn't already exists.
# Sessions are unique according to their root summoner.
# TODO: Add way to override/delete an existing session?
start_traversal = subparsers.add_parser('start', help='start a new traversal')
start_traversal.add_argument(
    'root_summoner',
    metavar='ROOT_SUMMONER',
    type=str,
    help='The summoner to start the traversal from.'
)
start_traversal.set_defaults(cmd='start')

resume_traversal = subparsers.add_parser('resume', help='resume an old traversal')
resume_traversal.add_argument(
    'session_id',
    metavar='SESSION_ID',
    type=str,
    help='The session to resume'
)
resume_traversal.set_defaults(cmd='resume')

list_sessions_cmd = subparsers.add_parser('list', help='list active sessions')
list_sessions_cmd.set_defaults(cmd='list')

if __name__ == '__main__':
    fathom_args = vars(parser.parse_args())
    print(f"Args are {fathom_args}")
    dispatch(fathom_args)
