import os.path
from typing import Callable


def get_valid_string_input_with_predicates(string_input_specification_for_user: str, input_option_descriptions: list[str],
                                           option_validity_functions: list[Callable[[str], bool]]) -> tuple[int, str]:
    """
    Asks the user for a string via the command line till one of the given functions returns true when given the entered string as input.
    Returns the index of the first function which says the input is valid and the valid input itself.
    """
    default_indent = "    "
    print(string_input_specification_for_user)
    input_string = ""
    for i in range(len(input_option_descriptions)):
        if i < len(input_option_descriptions) - 1:
            print(default_indent + "<" + input_option_descriptions[i] + "> or")
        else:
            input_string = input(default_indent + "<" + input_option_descriptions[i] + ">: ")
    while True:
        for i in range(len(option_validity_functions)):
            if option_validity_functions[i](input_string):
                return i, input_string
        input_string = input(default_indent + "\"" + input_string + "\" isn't valid! Try another: ")


def get_valid_string_input_with_finite_valid_options_and_descriptions(string_input_specification_for_user: str, string_descriptions: list[str], valid_strings: list[str]) -> str:
    return get_valid_string_input_with_predicates(string_input_specification_for_user, string_descriptions, [SimpleEqualsFunction(x).get_function() for x in valid_strings])[1]


def get_valid_string_input_with_finite_valid_options(string_input_specification_for_user: str, valid_strings: list[str]) -> str:
    return get_valid_string_input_with_finite_valid_options_and_descriptions(string_input_specification_for_user, valid_strings, valid_strings)


def get_valid_yes_no_input(string_input_specification_for_user: str) -> bool:
    return True if get_valid_string_input_with_finite_valid_options_and_descriptions(string_input_specification_for_user, ["y", "Enter for no"], ["y", ""]) == "y" else False


def get_valid_file_path_input(file_input_specification: str) -> str:
    return get_valid_string_input_with_predicates(file_input_specification, ["Path to file"], [os.path.isfile])[1]


def get_valid_dir_path_input(file_input_specification: str) -> str:
    return get_valid_string_input_with_predicates(file_input_specification, ["Path to directory"], [os.path.isdir])[1]


def get_valid_int_input(int_input_specification: str) -> int:
    return int(get_valid_string_input_with_predicates(int_input_specification, ["int"], [str_is_int])[1])


def get_valid_float_input(float_input_specification: str) -> float:
    return float(get_valid_string_input_with_predicates(float_input_specification, ["float"], [str_is_float])[1])


def str_is_int(string_to_test: str):
    try:
        int(string_to_test)
        return True
    except Exception:
        return False


def str_is_float(string_to_test: str):
    try:
        float(string_to_test)
        return True
    except Exception:
        return False


class SimpleEqualsFunction:
    """
    Class as an encapsulation of a lambda to store its context.
    """

    def __init__(self, string_to_test: str):
        self.string_to_test = string_to_test

    def get_function(self):
        return lambda a: a == self.string_to_test
