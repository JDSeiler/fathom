from typing import Dict, Any
import commands.list_sessions
import commands.start_traversal
import commands.resume_traversal


def dispatch(args: Dict[str, Any]):
    command_name = args['cmd']

    if command_name == 'list':
        commands.list_sessions.run()
    elif command_name == 'start':
        root = args['root_summoner']
        commands.start_traversal.run(root)
    elif command_name == 'resume':
        session_id = args['session_id']
        commands.resume_traversal.run(session_id)
    else:
        raise Exception(f"Unknown command {command_name}")
