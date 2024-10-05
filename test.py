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
    Reads lines from a .txt file and returns a list of stripped strings.
    """
    with open(fp, 'r') as file:
        return [line.rstrip('\n') for line in file.readlines()]  # Use rstrip to preserve empty lines


def is_valid_var_name(s: str) -> bool:
    """
    Checks if a string is a valid variable name.
    """
    if not s or s[0] not in alphabet_chars:
        return False
    return all(c in var_chars for c in s)


def is_digit_start_var(s: str) -> bool:
    """
    Checks if a variable starts with a digit.
    """
    return s and s[0] in numeric_chars


def parse_tokens(s_: str) -> Union[List[str], bool]:
    """
    Tokenizes the input string based on lambda calculus syntax rules.
    """
    s = s_[:]  # Don't modify the original input string
    tokens = []
    i = 0
    paren_stack = []
    last_token_is_backslash = False
    expected_next = None
    has_error = False

    while i < len(s):
        if s[i] == "\\":
            # Lambda must be followed by a valid variable name, no space allowed
            if i + 1 < len(s) and s[i + 1].isspace():
                print(f"Invalid space inserted after \\ at index {i}")
                has_error = True
                break
            if i + 1 == len(s):
                print(f"Missing complete lambda expression starting at index {i}")
                has_error = True
                break
            tokens.append("\\")
            last_token_is_backslash = True
            expected_next = 'variable'
            i += 1

        elif s[i] == "(":
            if expected_next == 'variable':
                print(f"Backlashes not followed by a variable name at {i - 1}.")
                has_error = True
                break
            tokens.append("(")
            paren_stack.append(i)
            last_token_is_backslash = False
            expected_next = None
            i += 1
            # Check for empty parentheses
            if i < len(s) and s[i] == ")":
                print(f"Missing expression for parenthesis at index {i - 1}.")
                has_error = True
                break
        elif s[i] == ")":
            if not paren_stack:
                print(f"Bracket ) at index: {i} is not matched with an opening bracket '('.")
                has_error = True
                break
            paren_stack.pop()
            tokens.append(")")
            last_token_is_backslash = False
            expected_next = None
            i += 1
        elif s[i].isalnum():
            var = ""
            start_idx = i
            while i < len(s) and s[i].isalnum():
                var += s[i]
                i += 1
            if is_digit_start_var(var):
                print(f"Error at index {start_idx}, variables cannot begin with digits.")
                has_error = True
                break
            tokens.append(var)
            last_token_is_backslash = False
            if expected_next == 'variable':
                expected_next = 'dot'
            elif expected_next == 'expression':
                expected_next = None
        elif s[i].isspace():
            if last_token_is_backslash:
                print(f"Invalid space inserted after \\ at index {i - 1}")
                has_error = True
                break
            i += 1  # Skip spaces
        else:
            if s[i] == '.':
                if expected_next != 'dot' and i==0:
                    print(f"Encountered dot at invalid index {i}.")
                else:
                    print(f"Must have a variable name before character '.' at index {i-1}")
            else:
                print(f"Error at index {i} with invalid character {s[i]}.")
            has_error = True
            break

    if not has_error:
        if paren_stack:
            idx = paren_stack.pop()
            print(f"Bracket ( at index: {idx} is not matched with a closing bracket ')'.")
            has_error = True
        elif last_token_is_backslash:
            print(f"Invalid lambda expression at {i - 1}.")
            has_error = True
        elif expected_next == 'dot':
            print(f"Invalid lambda expression at {i - 1}.")
            has_error = True
        elif expected_next == 'expression':
            print(f"Missing expression after '.' at index {i - 1}.")
            has_error = True

    if has_error:
        return False
    else:
        return tokens


def read_lines_from_txt_check_validity(fp: Union[str, os.PathLike]) -> None:
    """
    Reads each line from a .txt file and checks its validity.
    """
    lines = read_lines_from_txt(fp)
    print("Checking invalid examples...")
    for l in lines:
        if l.strip() == '':
            # Handle empty lines to ensure correct line count
            print("Empty line detected.")
            continue
        tokens = parse_tokens(l)
        if tokens:
            pass  # Valid line, but we don't need to output anything
        # Ensure only one error message is printed per line


if __name__ == "__main__":
    read_lines_from_txt_check_validity(invalid_examples_fp)



