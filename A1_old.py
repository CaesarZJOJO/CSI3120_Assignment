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
    with open(fp, 'r') as file:
        return [line.strip() for line in file.readlines()]


def is_valid_var_name(s: str) -> bool:
    """
    :param s: Candidate input variable name
    :return: True if the variable name starts with a character,
    and contains only characters and digits. Returns False otherwise.
    """
    if not s or s[0] not in alphabet_chars:
        return False
    return all(c in var_chars for c in s)


class Node:
    """
    Nodes in a parse tree
    Attributes:
        elem: a list of strings
        children: a list of child nodes
    """
    def __init__(self, elem: List[str] = None):
        self.elem = elem if elem else []
        self.children = []

    def add_child_node(self, node: 'Node') -> None:
        self.children.append(node)

class ParseTree:
    """
    A full parse tree, with nodes
    Attributes:
        root: the root of the tree
    """
    def __init__(self, root):
        self.root = root

    def print_tree(self, node: Optional[Node] = None, level: int = 0) -> None:
        """
        Prints the parse tree in a structured, indented format
        """
        if node is None:
            node = self.root
        print(" " * level + "-".join(node.elem))
        for child in node.children:
            self.print_tree(child, level + 4)


def parse_tokens(s_: str) -> Union[List[str], bool]:
    """
    Lexical analysis for tokenizing the input string based on lambda calculus.
    :param s_: the input string
    :return: A List of tokens (strings) if a valid input, otherwise False
    """
    s = s_[:]  # Don't modify the original input string
    tokens = []
    i = 0
    parentheses_count = 0
    last_token_is_backslash = False

    while i < len(s):
        if s[i] == "\\":
            # Lambda must be followed by a valid variable name, no space allowed
            if i + 1 < len(s) and s[i + 1].isspace():
                print(f"Invalid space inserted after \\ at index {i}")
                return False
            if i + 1 == len(s):
                print(f"Missing complete lambda expression starting at index {i}")
                return False
            tokens.append("\\")
            last_token_is_backslash = True
            i += 1
        elif s[i] == ".":
            # Ensure there's a valid token before "."
            if not tokens or tokens[-1] == "\\":
                print(f"Must have a variable name before character '.' at index {i}")
                return False
            tokens.append(".")
            i += 1
        elif s[i] == "(":
            tokens.append("(")
            parentheses_count += 1
            i += 1
        elif s[i] == ")":
            parentheses_count -= 1
            if parentheses_count < 0:
                print(f"Bracket ) at index {i} is not matched with an opening bracket '('")
                return False
            tokens.append(")")
            i += 1
        elif s[i].isalnum():
            var = ""
            while i < len(s) and s[i].isalnum():
                var += s[i]
                i += 1
            if is_valid_var_name(var):
                tokens.append(var)
                last_token_is_backslash = False
            else:
                print(f"Invalid variable name {var} at index {i - len(var)}")
                return False
        elif s[i].isspace():
            if last_token_is_backslash:
                print(f"Invalid space inserted after \\ at index {i-1}")
                return False
            i += 1  # skip spaces
        else:
            print(f"Invalid character {s[i]} at index {i}")
            return False

    if parentheses_count > 0:
        print(f"Bracket ( at index {len(s)-1} is not matched with a closing bracket ')'.")
        return False

    if parentheses_count < 0:
        print(f"Bracket ) at index {len(s)-1} is not matched with an opening bracket '('.")
        return False
    
    if last_token_is_backslash:
        print(f"Backlashes not followed by a variable name at {i-1}.")
        return False

    return tokens

def build_parse_tree_rec(tokens: List[str], node: Optional[Node] = None) -> Node:
    """
    Recursively build a parse tree from the list of tokens.
    :param tokens: A list of token strings
    :param node: A Node object representing the current node
    :return: a Node with children representing sub-expressions, variables, or operators
    """
    if node is None:
        node = Node()

    while tokens:
        token = tokens.pop(0)
        if token == "(":
            # Create a new child node for the content within parentheses
            child_node = Node(["("])
            node.add_child_node(build_parse_tree_rec(tokens, child_node))
        elif token == ")":
            return node
        else:
            # Add token as a new child node
            child_node = Node([token])
            node.add_child_node(child_node)

    return node

def build_parse_tree(tokens: List[str]) -> ParseTree:
    """
    Build a full parse tree from a list of tokens.
    :param tokens: List of tokens
    :return: A ParseTree object
    """
    root = build_parse_tree_rec(tokens)
    return ParseTree(root)



def read_lines_from_txt_check_validity(fp: Union[str, os.PathLike]) -> None:
    """
    Reads each line from a .txt file, and then parses each string to yield
    a tokenized list of strings for printing.
    """
    lines = read_lines_from_txt(fp)
    valid_lines = []
    for l in lines:
        tokens = parse_tokens(l)
        if tokens:
            valid_lines.append(l)
            print(f"The tokenized string for input string {l} is {'_'.join(tokens)}")
        else:
            print(f"Invalid lambda expression: {l}")
    if len(valid_lines) == len(lines):
        print(f"All lines are valid")


def read_lines_from_txt_output_parse_tree(fp: Union[str, os.PathLike]) -> None:
    """
    Reads each line from a .txt file, parses each string to yield a tokenized output string,
    and builds a parse tree. The parse tree should call print_tree() to print its content to the console.
    :param fp: The file path of the lines to parse
    """
    lines = read_lines_from_txt(fp)
    for l in lines:
        tokens = parse_tokens(l)
        if tokens:
            print(f"\nThe tokenized string for input string {l} is {'_'.join(tokens)}")
            parse_tree = build_parse_tree(tokens)
            parse_tree.print_tree()
        else:
            print(f"Invalid expression, unable to build parse tree: {l}")


if __name__ == "__main__":
    print("\n\nChecking valid examples...")
    read_lines_from_txt_check_validity(valid_examples_fp)
    read_lines_from_txt_output_parse_tree(valid_examples_fp)

    print("Checking invalid examples...")
    read_lines_from_txt_check_validity(invalid_examples_fp)

