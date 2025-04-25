# Bad implementation, just here for a basic refrence

from dataclasses import dataclass
from enum import StrEnum
import sys
from typing import Any, Generator, Optional


END_OF_TOKEN = {" ", "\n"}
TOKENS = {"+", "-", "(", ")", "[", "]", ";"}


class TokenEnum(StrEnum):
    EOF = "EOF"

    PLUS = "PLUS"  # +
    SUB = "SUB"  # -

    INT = "INT"  # Integers

    PAREN_LEFT = "PAREN_LEFT"  # (
    PAREN_RIGHT = "PAREN_RIGHT"  # )

    STRING = "STRING"

    PRINT = "PRINT"  # print

    SEMICOLON = "SEMICOLON"  # ;

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

            if self.text[self.pointer] in TOKENS:
                break

        match content:
            case _ if content.isdigit():
                return Token(TokenEnum.INT, int(content))
            case "print":
                return Token(TokenEnum.PRINT)
            case "+":
                return Token(TokenEnum.PLUS)
            case "-":
                return Token(TokenEnum.SUB)
            case "(":
                return Token(TokenEnum.PAREN_LEFT)
            case ")":
                return Token(TokenEnum.PAREN_RIGHT)
            case ";":
                return Token(TokenEnum.SEMICOLON)
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

        with open(path.strip(".lush") + ".tok", mode="w") as write_target:
            for token in tokenizer:
                # print(token, end="")
                write_target.write(str(token))


if __name__ == "__main__":
    main(sys.argv[1])
