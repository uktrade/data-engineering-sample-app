from app.commands.dev import cmd_group as dev_cmd_group


def get_command_groups():
    return [dev_cmd_group]
