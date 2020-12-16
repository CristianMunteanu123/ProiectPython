from sys import argv
import random
import string


class ProgramArguments:
    use_dict_arg = '-use_dict'
    help_arg = '-help'

    use_dict_arg_description = 'generates a password including the words found in the given dictionary' \
                               '. Will only use valid words (max 18 characters)'
    use_dict_arg_param_file_path = 'file_path'

    help_arg_description = 'prints the help section'

    file_name = _file_
    python_executable = 'python3'


class PasswordCharacteristics:
    minimum_length = 12
    maximum_length = 18

    required_character = ['!', '?', '#', '@']
    min_required_characters = 1
    max_required_characters = 6

    dict_info = (False, None)


def print_help():
    print(f'Usage : {ProgramArguments.python_executable} {ProgramArguments.file_name} [ {ProgramArguments.use_dict_arg}'
          f' | {ProgramArguments.help_arg} ]')
    print(f'\t{ProgramArguments.use_dict_arg} <{ProgramArguments.use_dict_arg_param_file_path}> - '
          f'{ProgramArguments.use_dict_arg_description}')
    print(f'\t{ProgramArguments.help_arg} - {ProgramArguments.help_arg_description}')


def check_use_dict_option():
    try:
        PasswordCharacteristics.dict_info = (True, argv[argv.index(ProgramArguments.use_dict_arg) + 1])
    except ValueError as DictOptionNotUsed:
        pass
    except IndexError as DictOptionNoParam:
        print('When using -use_dict, provide a file path for the dictionary')
        exit(1)


def check_help_option():
    try:
        argv.index(ProgramArguments.help_arg)
        print_help()
        exit(0)
    except ValueError as HelpOptionNotUsed:
        pass


def generate_password():
    password = ''
    characters = dict()