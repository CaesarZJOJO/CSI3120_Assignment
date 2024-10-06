import os
from typing import Union, List, Optional

alphabet_chars = list("abcdefghijklmnopqrstuvwxyz") + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
numeric_chars = list("0123456789")
var_chars = alphabet_chars + numeric_chars
all_valid_chars = var_chars + ["(", ")", ".", "\\"]
valid_examples_fp = "./valid_examples.txt"
invalid_examples_fp = "./invalid_examples.txt"


def read_lines_from_txt(fp: Union[str, os.PathLike]) -> List[str]:
    """
    :param fp: File path of the .txt file.
    :return: The lines of the file path removing trailing whitespaces
    and newline characters.
    """
    with open(fp, "r") as f:
        return [line.strip() for line in f.readlines()]


def is_valid_var_name(s: str) -> bool:
    """
    :param s: Candidate input variable name
    :return: True if the variable name starts with a character,
    and contains only characters and digits. Returns False otherwise.
    """
    if not s or s[0] not in alphabet_chars:
        return False
    for char in s:
        if char not in var_chars:
            return False
    return True

def parse_tokens(s_: str) -> Union[List[str], bool]:
    """
    Gets the final tokens for valid strings as a list of strings, only for valid syntax,
    where tokens are (no whitespace included)
    \\ values for lambdas
    valid variable names
    opening and closing parenthesis
    Note that dots are replaced with corresponding parenthesis
    :param s_: the input string
    :return: A List of tokens (strings) if a valid input, otherwise False
    """
    s = s_.strip()  # Trim leading and trailing spaces
    tokens = []
    i = 0
    open_brackets = 0  # To track open parentheses
    last_token_was_lambda = False  # To track if the last token was a lambda

    while i < len(s):
        if s[i] == '\\':  # Lambda abstraction
            tokens.append('\\')
            last_token_was_lambda = True
            i += 1
            if i >= len(s) or s[i] not in alphabet_chars:
                print(f"Invalid lambda expression at index {i - 1}")
                return False
            var_start = i
            while i < len(s) and s[i] in var_chars:
                i += 1
            var_name = s[var_start:i]
            if not is_valid_var_name(var_name):
                print(f"Invalid variable name '{var_name}'")
                return False
            tokens.append(var_name)

                        # After parsing the variable, we must check for a valid expression or parentheses
            if i >= len(s):  # If there's nothing after the variable
                print(f"Invalid lambda expression at index {var_start - 1}")
                return False

            # If there's a space after the variable, skip it and check for valid expression or parentheses
            if s[i] == ' ':
                i += 1
                if i < len(s) and s[i] == '(':  # Allow parentheses after space
                    continue
                elif i >= len(s):  # If there's nothing after the space
                    print(f"Invalid lambda expression at index {var_start - 1}")
                    return False
            

        elif s[i] in alphabet_chars:  # Variable name
            var_start = i
            while i < len(s) and s[i] in var_chars:
                i += 1
            var_name = s[var_start:i]
            if not is_valid_var_name(var_name):
                print(f"Invalid variable name '{var_name}'")
                return False
            tokens.append(var_name)
            last_token_was_lambda = False

        elif s[i] == '(':  # Opening parenthesis
            open_brackets += 1
            tokens.append('(')
            i += 1
            last_token_was_lambda = False

            # Check if the next character is a closing parenthesis, indicating empty parentheses
            if i < len(s) and s[i] == ')':
                print(f"Missing expression for parenthesis at index {i - 1}")
                return False

            # Check if the entire string will have a matching closing parenthesis
            if ')' not in s[i:]:
                print(f"Bracket ( at index {i - 1} is not matched with a closing bracket ')'")
                return False

        elif s[i] == ')':  # Closing parenthesis
            if open_brackets == 0:
                print(f"Bracket ) at index {i} is not matched with an opening bracket '('")
                return False
            tokens.append(')')
            open_brackets -= 1
            i += 1
            last_token_was_lambda = False

        elif s[i] == '.':  # Handle dot
            # Check if there's a space before the dot (invalid usage)
            if i > 0 and s[i - 1] == ' ':
                print(f"Must have a variable name before character '.' at index {i}")
                return False
            # A dot can only appear after a lambda abstraction variable, check if valid
            if not last_token_was_lambda:
                print(f"Encountered dot at invalid index {i}")
                return False
            tokens.append('(')
            i += 1
            last_token_was_lambda = False

        elif s[i] == ' ':  # Ignore spaces, but check for invalid usage with a dot
            # If there's a space followed by a dot, raise an error
            if i + 1 < len(s) and s[i + 1] == '.':
                print(f"Must have a variable name before character '.' at index {i + 1}")
                return False
            i += 1

        else:
            print(f"Error at index '{i}' with invalid character +.")
            return False

    # Check if all open parentheses are closed
    if open_brackets > 0:
        print(f"Unmatched opening bracket '('")
        return False

    # Handle dot-based grouping by closing parenthesis at the end
    if '.' in s:
        tokens.append(')')

    return tokens







def read_lines_from_txt_check_validity(fp: Union[str, os.PathLike]) -> None:
    """
    Reads each line from a .txt file, and then
    parses each string to yield a tokenized list of strings for printing, joined by _ characters
    In the case of a non-valid line, the corresponding error message is printed.
    :param fp: The file path of the lines to parse
    """
    lines = read_lines_from_txt(fp)
    valid_lines = []
    for l in lines:
        tokens = parse_tokens(l)
        if tokens:
            valid_lines.append(l)
            print(f"The tokenized string for input string '{l}' is {'_'.join(tokens)}")
    if len(valid_lines) == len(lines):
        print(f"All lines are valid")
    else:
        print(f"Some lines are invalid")


if __name__ == "__main__":

    print("\n\nChecking valid examples...")
    read_lines_from_txt_check_validity(valid_examples_fp)

    print("Checking invalid examples...")
    read_lines_from_txt_check_validity(invalid_examples_fp)
