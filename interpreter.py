import re


def interpret():
    content: list = read_file("asm-code")
    for line in content:
        if line != "\n":
            print(tokenize_line(line))


def read_file(file_name: str):
    with open(file_name) as file:
        content: list = file.readlines()
        file.close()
        return content


def tokenize_line(command: str):
    existing_tokens: dict = {
        "=": "EQUALS",
        "A": "REG_A",
        "D": "REG_D",
        "#": "COMMENT",
        "\+": "PLUS",
        "-": "MINUS",
        "&": "AND",
        "~": "NEG",
        "\|": "OR",
        "\*": "ASTRIX",
        ";": "SEMICOLON",
        "JEQ": "JEQ",
        "JNE": "JNE",
        "JGT": "JGT",
        "JGE": "JGE",
        "JLT": "JLT",
        "JLE": "JLE",
        "JMP": "JMP",
        "[1-9][0-9_]*|0x[1-9A-F][0-9a-fA-F_]*|0b1[01_]*|0": "NUMBER",
        "\n": "END_LINE",
        ".+": "WORD"
    }
    tokenized_code: list = []
    number: int = -1
    command = command.replace(" ", "")
    while command != "":
        for token in existing_tokens:
            if re.search(token, command) is not None and re.search(token, command).start() == 0:
                tokenized_code.append(existing_tokens.get(token))
                if existing_tokens.get(token) == "NUMBER":
                    num_str: str = re.search(token, command).group()
                    if len(num_str) == 1:
                        number = int(num_str)
                    elif num_str[1] == "x":
                        number = int(num_str, 16)
                    elif num_str[1] == "b":
                        number = int(num_str, 2)
                    else:
                        number = int(num_str)
                command = command.replace(re.search(token, command).group(), "", 1)
                break
    return tokenized_code, number
