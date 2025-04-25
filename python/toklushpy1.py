# Bad implementation, just here for a basic refrence

from dataclasses import dataclass
from enum import StrEnum
import sys
from typing import Any, Generator, Optional


END_OF_TOKEN = {" ", "\n"}
TOKENS = {
    "+",
    "-",
    "(",
    ")",
    "[",
    "]",
    "{",
    "}",
    ";",
    ",",
    ":",
}  # Single Character Tokens Only
letters = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "z",
]


class TokenEnum(StrEnum):
    EOF = "EOF"

    PLUS = "PLUS"  # +
    SUB = "SUB"  # -

    INT = "INT"  # Integers

    PAREN_LEFT = "PAREN_LEFT"  # (
    PAREN_RIGHT = "PAREN_RIGHT"  # )

    BRACE_LEFT = "BRACE_LEFT"  # {
    BRACE_RIGHT = "BRACE_RIGHT"  # }

    CHAR = "CHAR"  # ''
    STRING = "STRING"  # ""

    PRINT = "PRINT"  # print
    EXIT = "EXIT"  # exit

    SEMICOLON = "SEMICOLON"  # ;
    COLON = "COLON"
    COMMA = "COMMA"  #  ,

    FUNCTION = "FUNCTION"  # fn
    REFRENECE = "REFERENCE"

    TYPE_DEC = "TYPE_DEC"  # Type Declarations (int32, int64, str, bool, ...)


@dataclass
class Token:
    token: TokenEnum
    data: Optional[Any] = None

    """
    def __str__(self):
        return f"[{self.token}{"" if self.data is None else (": " + str(self.data))}]"
    """

    def __str__(self):
        return f"{self.token}{"" if self.data is None else "\t" + (str(self.data))};\n"


class Tokenizer:
    def __init__(self, text: str):
        self.pointer = 0
        self.text = text
        self.identifiers = set()

    def pull_next(self) -> Token:
        content = ""  # Content is local to each run

        if self.pointer == len(self.text):  # EOF Token
            return Token(TokenEnum.EOF)

        while (self.text[self.pointer] in END_OF_TOKEN) and (
            self.pointer < len(self.text)
        ):  # Whitespace trim
            self.pointer += 1

            if self.pointer == len(self.text):  # EOF Token
                return Token(TokenEnum.EOF)

        while (self.text[self.pointer] not in END_OF_TOKEN) and (
            self.pointer < len(self.text)
        ):
            content += self.text[self.pointer]

            self.pointer += 1

            if self.pointer >= (len(self.text) - 1):
                break

            if content in TOKENS:
                break

            if content == "'":  # Chars
                char = self.text[self.pointer]

                self.pointer += 1

                if self.text[self.pointer] == "'":
                    self.pointer += 1
                    return Token(TokenEnum.CHAR, char)
                else:
                    print("Error Occured While Processing:")
                    print("Unclosed Char")
                    exit(4)

            if content == '"':  # Strings
                string_content = ""

                self.pointer -= 1

                while self.pointer < len(self.text):
                    self.pointer += 1
                    if self.text[self.pointer] == '"':
                        self.pointer += 1
                        return Token(TokenEnum.STRING, f"'{string_content}'")
                    string_content += self.text[self.pointer]

                print("Error Occured While Processing:")
                print("Unclosed String")
                exit(3)

            if self.text[self.pointer] in TOKENS:
                break

        match content:
            case _ if content.isdigit():
                return Token(TokenEnum.INT, int(content))
            case _ if content in self.identifiers:
                return Token(TokenEnum.REFRENECE, str(content))
            case "print":
                return Token(TokenEnum.PRINT)
            case "exit":
                return Token(TokenEnum.EXIT)
            case "fn":
                identifier = ""
                while (self.text[self.pointer] in END_OF_TOKEN) and (
                    self.pointer < len(self.text)
                ):  # Whitespace trim
                    self.pointer += 1

                    if self.pointer == len(self.text):  # EOF Token
                        print("Error Occured While Processing:")
                        print("Undefined Funtion")
                        exit(5)

                while (
                    (self.text[self.pointer] not in END_OF_TOKEN)
                    and (self.pointer < len(self.text))
                    and (self.text[self.pointer].lower() in letters)
                ):
                    identifier += self.text[self.pointer]
                    self.pointer += 1

                self.identifiers.add(identifier)
                return Token(TokenEnum.FUNCTION, identifier)
            case "+":
                return Token(TokenEnum.PLUS)
            case "-":
                return Token(TokenEnum.SUB)
            case "(":
                return Token(TokenEnum.PAREN_LEFT)
            case ")":
                return Token(TokenEnum.PAREN_RIGHT)
            case "{":
                return Token(TokenEnum.BRACE_LEFT)
            case "}":
                return Token(TokenEnum.BRACE_RIGHT)
            case ";":
                return Token(TokenEnum.SEMICOLON)
            case ":":
                return Token(TokenEnum.COLON)
            case ",":
                return Token(TokenEnum.COMMA)
            case _:  # Unspecified token
                print("Error Occured While Processing:")
                print(f"Unrecognized token at character {self.pointer}: {content}")
                print("Exiting")
                exit(2)

    def __iter__(self) -> Generator[Token, None, None]:
        while (token := self.pull_next()).token != TokenEnum.EOF:
            yield token
        yield token


def main(path: str):
    print(f"Tokenizing {path} \n")

    with open(path, mode="r") as file:
        content = file.read()
        tokenizer = Tokenizer(content)
        tokcount = 0

        with open(path.strip(".lush") + ".tok", mode="w") as write_target:
            for token in tokenizer:
                # print(token, end="")
                tokcount += 1
                write_target.write(str(token))
        print(f"Total Tokens: {tokcount}")


if __name__ == "__main__":
    main(sys.argv[1])
