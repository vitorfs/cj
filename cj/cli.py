#!/usr/bin/env python

import os
import sys
import subprocess
import datetime

from cj import VERSION


PRIMARY = '\033[94m'
SUCCESS = '\033[92m'
WARNING = '\033[93m'
DANGER = '\033[91m'
SECONDARY = '\033[90m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def get_str_date():
    date = datetime.datetime.now().strftime('%Y%m%d')
    return date


def compress(path, outfile=None):
    if outfile is None:
        outfile = 'archive_%s.tar.gz' % get_str_date()
    subprocess.call(['tar', '-zcf', outfile, path])


def dump_database(db_name, outfile=None):
    if outfile is None:
        outfile = 'database_%s.sql' % get_str_date()
    dump = subprocess.check_output(['mysqldump', '--add-drop-table', db_name])
    with open(outfile, 'w') as f:
        f.write(dump)
    return outfile


def wp(args):
    compress('/var/www/html')
    dump_file = dump_database('wordpress')
    if os.path.exists(dump_file):
        compress(dump_file, '%s.tar.gz' % dump_file)
        os.remove(dump_file)


def tar(args):
    PATH = 2
    if len(args) > 2:
        path = args[PATH]
        compress(path)
    else:
        sys.stderr.write('''{danger}The folder path is mandatory.{endcommand}
{bold}Usage:{endcommand} {primary}cj zip /path/to/folder{endcommand}
'''.format(danger=DANGER, bold=BOLD, primary=PRIMARY, endcommand=ENDC))


def tex(args):
    '''
    Wrapper of the `pandoc` program
    '''
    subprocess.call(['pandoc', 'main.tex', '--bibliography=ref.bib', '-S', '-o', 'main.docx'])


def pyc(self):
    subprocess.call(['find', '.', '-name', '\*.pyc', '-delete'])


COMMAND_NAME = 0
COMMAND_FUNCTION = 1
COMMAND_DESCRIPTION = 2
COMMANDS = (
    # command, function, description
    ('wp', wp, 'Wrapper of Wordpress utilities'),
    ('zip', tar, 'Compress file or folder'),
    ('tex', tex, 'Convert a LaTeX document to Word format'),
    ('pyc', pyc, 'Remove all .pyc files recursively'),
)


def help():
    HELP_COMMAND_PADDING = 15  # Spacing between the command name and the description
    str_commands = ''

    for command in COMMANDS:
        name = command[COMMAND_NAME]
        description = command[COMMAND_DESCRIPTION]
        padding = HELP_COMMAND_PADDING - len(name)
        if padding <= 0:
            padding = 1
        spacing = padding * ' '
        str_command = '  {name}{spacing}{secondary}{description}{endcommand}\n'.format(
            name=name,
            spacing=spacing,
            description=description,
            secondary=SECONDARY,
            endcommand=ENDC
        )
        str_commands = '{commands}{append}'.format(commands=str_commands, append=str_command)

    sys.stdout.write('''{bold}CJ {version}{endcommand}

Usage: {primary}cj COMMAND{endcommand}

For more details about the commands, type {primary}cj help TOPIC{endcommand} for more details:

{commands}
'''.format(bold=BOLD, version=VERSION, endcommand=ENDC, primary=PRIMARY, commands=str_commands))


def main():
    args = sys.argv
    if len(args) == 1:
        return help()
    else:
        command_name = args[1]
        command = list(filter(lambda c: c[COMMAND_NAME] == command_name, COMMANDS))
        if command:
            command = command[0]
            command_function = command[COMMAND_FUNCTION]
            return command_function(args)
        else:
            sys.stderr.write('{danger}Command not found.{endcommand}\n'.format(danger=DANGER, endcommand=ENDC))


if __name__ == '__main__':
    main()
