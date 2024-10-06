import os
from typing import Union, List, Optional

alphabet_chars = list("abcdefghijklmnopqrstuvwxyz") + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
numeric_chars = list("0123456789")
var_chars = alphabet_chars + numeric_chars
all_valid_chars = var_chars + ["(", ")", ".", "\\"]
valid_examples_fp = "./valid_examples.txt"
invalid_examples_fp = "./invalid_examples.txt"


def read_lines_from_txt(fp: [str, os.PathLike]) -> List[str]:
    """
    :param fp: File path of the .txt file.
    :return: The lines of the file path removing trailing whitespaces
    and newline characters.
    """
    # TODO
    return []


def is_valid_var_name(s: str) -> bool:
    """
    :param s: Candidate input variable name
    :return: True if the variable name starts with a character,
    and contains only characters and digits. Returns False otherwise.
    """
    # TODO
    return False


class Node:
    """
    Nodes in a parse tree
    Attributes:
        elem: a list of strings
        children: a list of child nodes
    """
    def __init__(self, elem: List[str] = None):
        self.elem = elem
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
        # TODO
        print("")



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

    s = s_[:]  #  Don't modify the original input string
    # TODO

    return []


def read_lines_from_txt_check_validity(fp: [str, os.PathLike]) -> None:
    """
    Reads each line from a .txt file, and then
    parses each string  to yield a tokenized list of strings for printing, joined by _ characters
    In the case of a non-valid line, the corresponding error message is printed (not necessarily within
    this function, but possibly within the parse_tokens function).
    :param fp: The file path of the lines to parse
    """
    lines = read_lines_from_txt(fp)
    valid_lines = []
    for l in lines:
        tokens = parse_tokens(l)
        if tokens:
            valid_lines.append(l)
            print(f"The tokenized string for input string {l} is {'_'.join(tokens)}")
    if len(valid_lines) == len(lines):
        print(f"All lines are valid")



def read_lines_from_txt_output_parse_tree(fp: [str, os.PathLike]) -> None:
    """
    Reads each line from a .txt file, and then
    parses each string to yield a tokenized output string, to be used in constructing a parse tree. The
    parse tree should call print_tree() to print its content to the console.
    In the case of a non-valid line, the corresponding error message is printed (not necessarily within
    this function, but possibly within the parse_tokens function).
    :param fp: The file path of the lines to parse
    """
    lines = read_lines_from_txt(fp)
    for l in lines:
        tokens = parse_tokens(l)
        if tokens:
            print("\n")
            parse_tree2 = build_parse_tree(tokens)
            parse_tree2.print_tree()




def build_parse_tree_rec(tokens: List[str], node: Optional[Node] = None) -> Node:
    """
    An inner recursive inner function to build a parse tree
    :param tokens: A list of token strings
    :param node: A Node object
    :return: a node with children whose tokens are variables, parenthesis, slashes, or the inner part of an expression
    """

    #TODO
    return Node()


def build_parse_tree(tokens: List[str]) -> ParseTree:
    """
    Build a parse tree from a list of tokens
    :param tokens: List of tokens
    :return: parse tree
    """
    pt = ParseTree(build_parse_tree_rec(tokens))
    return pt


if __name__ == "__main__":

    print("\n\nChecking valid examples...")
    read_lines_from_txt_check_validity(valid_examples_fp)
    read_lines_from_txt_output_parse_tree(valid_examples_fp)

    print("Checking invalid examples...")
    read_lines_from_txt_check_validity(invalid_examples_fp)