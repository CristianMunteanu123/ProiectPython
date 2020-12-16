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

    file_name = __file__
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

    first_charachter = random.choice(string.ascii_uppercase)
    characters[0] = first_charachter

    first_character = random.choice(string.ascii_uppercase)
    characters[0] = first_character

    length = random.randint(PasswordCharacteristics.minimum_length, PasswordCharacteristics.maximum_length)
    special_characters_count = random.randint(PasswordCharacteristics.min_required_characters,
                                              PasswordCharacteristics.max_required_characters)
    special_characters_indices = random.sample(population=[i for i in range(1, length)],
                                               k=special_characters_count)

    for i in special_characters_indices:
        characters[i] = random.choice(PasswordCharacteristics.required_character)

    for i in range(1, length):
        if i not in characters:
            characters[i] = random.choice(string.ascii_letters)
    for key in characters:
        password += characters[key]

    return password


def filter_words_by_length(file_name):
    try:
        words_by_len = []
        with open(file_name) as dict_file:
            for line in dict_file.readlines():
                line = line.rstrip().capitalize()
                if len(line) >= 18:
                    continue
                words_by_len.append((len(line), line))
            dict_file.close()

            return sorted(words_by_len, key=lambda t: t[0])
    except IOError as FileOpenError:
        print('File given is invalid / cannot be opened')
        exit(2)


def assign_in_buckets(words_by_len):
    buckets = dict()
    for len_word_tuple in words_by_len:
        if len_word_tuple[0] not in buckets:
            buckets[len_word_tuple[0]] = [len_word_tuple[1]]
        else:
            buckets[len_word_tuple[0]].append(len_word_tuple[1])

    for key in buckets:
        buckets[key].sort()

    return buckets


def gen_word_lengths(total_length):
    current_len = random.randint(3, 8)
    while current_len < total_length and total_length - current_len > 3:
        total_length -= current_len
        yield current_len
        yield total_length

def generate_password_dict():
    words_by_len = assign_in_buckets(filter_words_by_length(PasswordCharacteristics.dict_info[1]))

    password = ''
    length = random.randint(PasswordCharacteristics.minimum_length, PasswordCharacteristics.maximum_length)
    special_characters_count = random.randint(PasswordCharacteristics.min_required_characters,
                                              PasswordCharacteristics.max_required_characters)
    other_characters_count = random.randint(0, special_characters_count - 1)
    special_characters_count -= other_characters_count

    words_total_length = length - special_characters_count

    selected_words = []

    for word_len in gen_word_lengths(words_total_length):
        selected_words.append(random.choice(words_by_len[word_len]))

    print(selected_words)
    print(special_characters_count)
    print(other_characters_count)
    print(length)

    start_with_word = True if other_characters_count == 0 else bool(random.randint(0, 1))
    if not start_with_word:
        other_characters_count -= 1
        password += random.choice(string.ascii_uppercase)
    else:
        password += selected_words.pop(selected_words.index(random.choice(selected_words)))

    while len(selected_words) > 0 or other_characters_count > 0 or special_characters_count > 0:
        if len(selected_words) >= other_characters_count and len(selected_words) >= special_characters_count and \
                len(selected_words) > 0:
            password += selected_words.pop(selected_words.index(random.choice(selected_words)))
        elif other_characters_count >= len(selected_words) and other_characters_count >= special_characters_count and \
                other_characters_count > 0:
            password += random.choice(string.ascii_letters)
            other_characters_count -= 1
        elif special_characters_count > 0:
            password += random.choice(PasswordCharacteristics.required_character)
            special_characters_count -= 1

    return password



def start_script() -> object:
    random.seed()

    check_use_dict_option()
    check_help_option()

    if PasswordCharacteristics.dict_info[0] is False:
        password = generate_password()
    else:
        password = generate_password_dict()

    print(password)


if __name__ == '_main_':
    start_script()