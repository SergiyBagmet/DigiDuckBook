from itertools import chain
import typing as t

from prompt_toolkit.lexers import Lexer
from prompt_toolkit.styles.named_colors import NAMED_COLORS
from prompt_toolkit.completion import NestedCompleter


class RainbowLexer(Lexer):
    """
    Lexer class for syntax highlighting with rainbow colors.

    This lexer is designed to apply rainbow colors to each line of text in a document.

    Attributes:
        None

    Methods:
        lex_document(self, document): Lex the document and apply rainbow colors.

    Example usage:
        lexer = RainbowLexer()
        tokens = lexer.lex_document(document)
    """
    def lex_document(self, document):
        """
        Lex the document and apply rainbow colors to each line.

        Args:
            document: The document to be lexed.

        Returns:
            Callable: A callable object for applying colors to lines in the document.
        """
        colors = list(sorted({"Teal": "#008080"}, key=NAMED_COLORS.get))

        def get_line(lineno):
            return [
                (colors[i % len(colors)], c)
                for i, c in enumerate(document.lines[lineno])
            ]

        return get_line


def get_completer(commands: t.Iterable[list[str]]) -> NestedCompleter:
    """
    Create a NestedCompleter based on a list of commands.

    Args:
        commands (Iterable[list[str]]): A list of command lists, 
        where each inner list contains alternative forms of a command.

    Returns:
        NestedCompleter: A NestedCompleter instance configured with the provided commands.
    """
    dict_commands: dict[str, None] = dict.fromkeys(chain.from_iterable(commands)) 
    return NestedCompleter.from_nested_dict(dict_commands)
    

