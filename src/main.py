from sys import argv
from lexer import lex

if __name__ == "__main__":
    if len(argv) < 2:
        exit(1)
    source_filename = argv[1];
    result, error = lex(source_filename)

    if error:
        print(error.as_string())
    else:
        print(result)

