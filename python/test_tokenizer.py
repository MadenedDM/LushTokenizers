from py_tok import *


def tok(code: str) -> str:
    cont = ""

    for token in Tokenizer(code):
        cont += str(token)

    return cont


def test_number_tokens():
    assert (
        tok("1 2 30 4570 8914 ")
        == "INT\t1;\nINT\t2;\nINT\t30;\nINT\t4570;\nINT\t8914;\nEOF;\n"
    )


def test_semicolon():
    assert tok(";") == "SEMICOLON;\nEOF;\n"


def test_colon():
    assert tok(":") == "COLON;\nEOF;\n"


def test_print():
    assert tok("print ( ) ;") == "PRINT;\nPAREN_LEFT;\nPAREN_RIGHT;\nSEMICOLON;\nEOF;\n"
    assert tok("print( );") == "PRINT;\nPAREN_LEFT;\nPAREN_RIGHT;\nSEMICOLON;\nEOF;\n"
    assert (
        tok("print(5);")
        == "PRINT;\nPAREN_LEFT;\nINT\t5;\nPAREN_RIGHT;\nSEMICOLON;\nEOF;\n"
    )


def test_math_text():
    assert (
        tok("10024 + 489 - 702;")
        == "INT\t10024;\nPLUS;\nINT\t489;\nSUB;\nINT\t702;\nSEMICOLON;\nEOF;\n"
    )

def test_strings():
    assert tok('"Greetings!"') == "STRING\t'Greetings!';\nEOF;\n"
    assert tok('"Hello World!"') == "STRING\t'Hello World!';\nEOF;\n"