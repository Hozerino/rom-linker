BACKUP_SUFFIX = "_bkp"


def print_cute_message(message):
    print("#" * len(message))
    print(message)
    print("#" * len(message))


def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        while input_string.endswith(suffix):
            input_string = input_string[:-len(suffix)]
    return input_string

def subtract(main, subtraction):
    new_list = []
    for entry in main:
        if entry not in subtraction:
            new_list.append(entry)
    return new_list


