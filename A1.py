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
    def __init__(self, root: Node):
        self.root = root

    def print_tree(self, node: Optional[Node] = None, level: int = 0) -> None:
        # If no node is provided, start from the root
        if node is None:
            node = self.root
                # Only print the three empty lines for the root (when level == 0)
        if level == 0:
            print("\n" * 3, end="")

        # Join the elements of the node to form a single string, using '_' as a separator
        node_str = "_".join(node.elem)

        # Print the current node with indentation based on the level in the tree
        if node_str !="":
            print("----" * level + node_str)

        # Recursively print each child node, increasing the level by 1
        for child in node.children:
            self.print_tree(child, level + 1)




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
    dot_opened_paren = False  # To track if a parenthesis was opened by a dot
    error_a = error_b = error_c = error_d = error_e = error_f = None  # Initialize error variables
    error_1 = error_2 = None

    while i < len(s):
        if s[i] == '\\':  # Lambda abstraction
            tokens.append('\\')
            last_token_was_lambda = True
            i += 1

            # Error E: Check if '\' is followed by a space
            if i < len(s) and s[i] == ' ':
                error_e = f"Invalid space inserted after \\ at index {i - 1}."
                break

            # Error F: Check if '\' is not followed by a valid variable
            if i < len(s) and s[i] not in alphabet_chars:
                error_f = f"Backslash not followed by a variable name at index {i - 1}."
                break

            # Proceed to parse variable if no errors so far
            var_start = i
            while i < len(s) and s[i] in var_chars:
                i += 1
            var_name = s[var_start:i]
            if not is_valid_var_name(var_name):
                error_c = f"Invalid variable name '{var_name}'."

            tokens.append(var_name)

            # Error D: Check if there's no valid expression after the variable
            if i >= len(s):  # If there's nothing after the variable
                error_d = f"Invalid lambda expression at {var_start - 1}."

            # Handle case with space after variable, then parentheses
            if i < len(s) and s[i] == ' ':
                i += 1
                if i < len(s) and s[i] == '(':  # Allow parentheses after space
                    continue
                elif i >= len(s):  # If there's nothing after the space
                    error_d = f"Invalid lambda expression at {var_start - 1}."

        elif s[i] in alphabet_chars:  # Variable name
            var_start = i
            while i < len(s) and s[i] in var_chars:
                i += 1
            var_name = s[var_start:i]
            if not is_valid_var_name(var_name):
                print(f"Invalid variable name '{var_name}'.")
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
                print(f"Missing expression for parenthesis at index {i - 1}.")
                return False

            # Check if the entire string will have a matching closing parenthesis
            if ')' not in s[i:]:
                print(f"Bracket ( at index {i - 1} is not matched with a closing bracket ')'.")
                return False

        elif s[i] == ')':  # Closing parenthesis
            if open_brackets == 0:
                print(f"Bracket ) at index {i} is not matched with an opening bracket '('.")
                return False
            tokens.append(')')
            open_brackets -= 1
            i += 1
            last_token_was_lambda = False

        

        elif s[i] == '.':  # Handle dot
            # Check if there's a space before the dot (invalid usage)
            if i > 0 and s[i - 1] == ' ':
                print(f"Must have a variable name before character '.' at index {i-1}.")
                return False
            elif i > 0 and s[i-1] not in alphabet_chars:
                print(f"Must have a variable name before character '.' at index {i-1}.")
                return False
            # A dot can only appear after a lambda abstraction variable, check if valid
            if not last_token_was_lambda:
                print(f"Encountered dot at invalid index {i}.")
                return False
            tokens.append('(')
            dot_opened_paren = True
            i += 1
            last_token_was_lambda = False
        
        elif s[i] == ' ':  # Ignore spaces, but check for invalid usage with a dot
            # If there's a space followed by a dot, raise an error
            if i + 1 < len(s) and s[i + 1] == '.':
                print(f"Must have a variable name before character '.' at index {i-1}.")
                return False
            i += 1


        else:
            if s[i] in numeric_chars:
                print(f"Error at index {i}, variables cannot begin with digits.")
            else:
                print(f"Error at index {i} with invalid character {s[i]}.")
            return False
    
    # Error A: Check if '\' is the last character
    if s[len(s)-1]== '\\': 
        print(f"Missing complete lambda expression starting at index {len(s)-1}.")
        return False

    # Centralized error handling
    if error_a:
        print(error_a)
        return False
    if error_b:
        print(error_b)
        return False
    if error_c:
        print(error_c)
        return False
    if error_d:
        print(error_d)
        return False
    if error_e:
        print(error_e)
        return False
    if error_f:
        print(error_f)
        return False
    if error_1:
        print(error_1)
        return False
    if error_2:
        print(error_2)
        return False
    
    # Ensure any open parentheses caused by dot are closed
    if dot_opened_paren:
        tokens.append(')')  # Close the parenthesis at the end if dot opened one


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


def read_lines_from_txt_output_parse_tree(fp: [str, os.PathLike]) -> None:
    lines = read_lines_from_txt(fp)
    for l in lines:
        tokens = parse_tokens(l)
        if tokens:
            print("\n")
            parse_tree2 = build_parse_tree(tokens)
            parse_tree2.print_tree()


def build_parse_tree_rec(tokens: List[str]) -> Node:
    # Root node with all tokens
    root = Node(elem=tokens.copy())  # Copy tokens to avoid modifying the original list

    def parse(tokens: List[str], node: Node):
        while tokens:
            token = tokens.pop(0)
            
            if token.isalnum():  # Case of variable like 'a'
                var = Node([token])
                node.add_child_node(var)

                # Check if the next token is a lambda expression '\' 
                if tokens and tokens[0] == '\\':
                    # All remaining tokens after 'a' (including '\') become the second child node
                    lambd = Node(tokens.copy())
                    node.add_child_node(lambd)
                    
                    # Recursively parse the rest of the expression
                    parse(tokens, lambd)
                else:
                    parse(tokens,node)
                return  # Stop parsing after handling the first token and the lambda expression
            
            elif token == '\\':  # Handling the lambda expression if it appears first
                
                lvar = tokens.pop(0)  # The variable after '\'

                # Add '\' and 'lvar' as separate child nodes
                node.add_child_node(Node([token]))  # '\' as a child
                node.add_child_node(Node([lvar]))  # 'x' (the variable) as a child

                # After lambda expression, process all subsequent tokens as separate nodes
                while tokens and tokens[0] != '(':  # Process until we reach a '(' or run out of tokens
                    next_token = tokens.pop(0)
                    if next_token:  # Ensure we don't process empty tokens
                        node.add_child_node(Node([next_token]))  # Add each token as a separate node

                if tokens and tokens[0] == '(':  # Check for parentheses after the lambda expression
                    i = []
                    d = 0
                    while tokens:
                        t = tokens.pop(0)
                        if t == '(':
                            d += 1
                        elif t == ')':
                            d -= 1
                        i.append(t)
                        if d == 0:
                            break
                    # Recursively parse the inside of the parentheses

                    inner = build_parse_tree_rec(i)  # Remove outer parentheses
                    node.add_child_node(inner)
                    
                else:
                    # If no parentheses, parse the rest of the expression
                    expr_node = build_parse_tree_rec(tokens)
                    node.add_child_node(expr_node)
            
            # first is (
            elif token == '(':  # Handling parentheses expression
                # Collect the content inside the parentheses
                i = ['(']
                d = 1
                while tokens:
                    t = tokens.pop(0)
                    i.append(t)
                    if t == '(':
                        d += 1
                    elif t == ')':
                        d -= 1
                    if d == 0:
                        break

                # Create a node for the entire parenthesis expression
                paren_exp = Node(i)
                node.add_child_node(paren_exp)

                # Special case: if the subexpression has only one token inside parentheses
                if len(i[1:-1]) == 1:  # This means it's like '(a)'
                    leftp= Node(['('])
                    rightp=Node([')'])
                    paren_exp.add_child_node(leftp)
                    paren_exp.add_child_node(Node([i[1]]))
                    paren_exp.add_child_node(rightp)
                else:
                    # Recursively process the content inside parentheses
                    leftp= Node(['('])
                    rightp=Node([')'])
                    paren_exp.add_child_node(leftp)
                    inner = build_parse_tree_rec(i[1:-1])  # Remove outer parentheses
                    paren_exp.add_child_node(inner)
                    paren_exp.add_child_node(rightp)

    # Start parsing the tokens for the root node
    parse(tokens, root)
    
    return root









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
