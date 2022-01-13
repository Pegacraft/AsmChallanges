import re

import virtualenv as vm


def interpret():
    content: list = read_file("asm-code")
    for line in content:
        if line != "\n":
            tokenized_line: tuple = tokenize_line(line)
            print(tokenized_line)
            compute_line(tokenized_line[0], tokenized_line[1])
            vm.debug_print()
            vm.program_counter += 1


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


def compute_line(tokenized_line: list, passed_num: int):
    def comment_remove():
        vm.program_counter -= 1

    def immediate_assignment():
        vm.reg_a = passed_num

    # Copy commands
    def reg_a_copy_reg_d():
        vm.reg_d = vm.reg_a

    def reg_d_copy_reg_a():
        vm.reg_a = vm.reg_d

    def reg_d_copy_ram():
        vm.ram_write(vm.reg_a, vm.reg_d)

    def reg_a_copy_ram():
        vm.ram_write(vm.reg_a, vm.reg_a)

    def ram_copy_reg_a():
        vm.reg_a = vm.ram_read(vm.reg_a)

    def ram_copy_reg_d():
        vm.reg_d = vm.ram_read(vm.reg_a)

    # Plus operation
    def reg_a_plus():
        vm.reg_a = vm.reg_a + vm.reg_d

    def reg_d_plus():
        vm.reg_d = vm.reg_a + vm.reg_d

    # Ram plus
    def reg_a_ram_plus():
        vm.reg_a = vm.ram_read(vm.reg_a) + vm.reg_d

    def reg_d_ram_plus():
        vm.reg_d = vm.ram_read(vm.reg_a) + vm.reg_d

    # Minus operation
    def reg_d_a_minus_d():
        vm.reg_d = vm.reg_a - vm.reg_d

    def reg_d_d_minus_a():
        vm.reg_d = vm.reg_d - vm.reg_a

    def reg_a_a_minus_d():
        vm.reg_a = vm.reg_a - vm.reg_d

    def reg_a_d_minus_a():
        vm.reg_a = vm.reg_d - vm.reg_a

    # Minus ram
    def reg_a_ram_minus_d():
        vm.reg_a = vm.ram_read(vm.reg_a) - vm.reg_d

    def reg_a_d_minus_ram():
        vm.reg_a = vm.reg_d - vm.ram_read(vm.reg_a)

    def reg_d_ram_minus_d():
        vm.reg_d = vm.ram_read(vm.reg_a) - vm.reg_d

    def reg_d_d_minus_ram():
        vm.reg_d = vm.reg_d - vm.ram_read(vm.reg_a)

    # And operation
    def reg_a_and():
        vm.reg_a = vm.reg_a & vm.reg_d

    def reg_d_and():
        vm.reg_d = vm.reg_a & vm.reg_d

    # Ram and operation
    def reg_a_ram_and():
        vm.reg_a = vm.ram_read(vm.reg_a) & vm.reg_d

    def reg_d_ram_and():
        vm.reg_d = vm.ram_read(vm.reg_a) & vm.reg_d

    # Or operation
    def reg_a_or():
        vm.reg_a = vm.reg_a | vm.reg_d

    def reg_d_or():
        vm.reg_d = vm.reg_a | vm.reg_d

    # Ram or operation
    def reg_a_ram_or():
        vm.reg_a = vm.ram_read(vm.reg_a) | vm.reg_d

    def reg_d_ram_or():
        vm.reg_d = vm.ram_read(vm.reg_a) | vm.reg_d

    if tokenized_line[0] == "COMMENT":
        comment_remove()
    # Copy operation
    if tokenized_line == ["REG_A", "EQUALS", "NUMBER", "END_LINE"]:
        immediate_assignment()
    if tokenized_line == ["REG_D", "EQUALS", "REG_A", "END_LINE"]:
        reg_a_copy_reg_d()
    if tokenized_line == ["REG_A", "EQUALS", "REG_D", "END_LINE"]:
        reg_d_copy_reg_a()
    # Ram copy operation
    if tokenized_line == ["ASTRIX", "REG_A", "EQUALS", "REG_A", "END_LINE"]:
        reg_a_copy_ram()
    if tokenized_line == ["ASTRIX", "REG_A", "EQUALS", "REG_D", "END_LINE"]:
        reg_d_copy_ram()
    if tokenized_line == ["REG_A", "EQUALS", "ASTRIX", "REG_A", "END_LINE"]:
        ram_copy_reg_a()
    if tokenized_line == ["REG_D", "EQUALS", "ASTRIX", "REG_A", "END_LINE"]:
        ram_copy_reg_d()
    # Plus operation
    if tokenized_line == ["REG_A", "EQUALS", "REG_A", "PLUS", "REG_D", "END_LINE"]:
        reg_a_plus()
    if tokenized_line == ["REG_D", "EQUALS", "REG_A", "PLUS", "REG_D", "END_LINE"]:
        reg_d_plus()
    if tokenized_line == ["REG_A", "EQUALS", "REG_D", "PLUS", "REG_A", "END_LINE"]:
        reg_a_plus()
    if tokenized_line == ["REG_D", "EQUALS", "REG_D", "PLUS", "REG_A", "END_LINE"]:
        reg_d_plus()
    # Plus ram operation
    if tokenized_line == ["REG_A", "EQUALS", "ASTRIX", "REG_A", "PLUS", "REG_D", "END_LINE"]:
        reg_a_ram_plus()
    if tokenized_line == ["REG_A", "EQUALS", "REG_D", "PLUS", "ASTRIX", "REG_A", "END_LINE"]:
        reg_a_ram_plus()
    if tokenized_line == ["REG_D", "EQUALS", "ASTRIX", "REG_A", "PLUS", "REG_D", "END_LINE"]:
        reg_d_ram_plus()
    if tokenized_line == ["REG_D", "EQUALS", "REG_D", "PLUS", "ASTRIX", "REG_A", "END_LINE"]:
        reg_d_ram_plus()
    # Minus operation
    if tokenized_line == ["REG_A", "EQUALS", "REG_A", "MINUS", "REG_D", "END_LINE"]:
        reg_a_a_minus_d()
    if tokenized_line == ["REG_D", "EQUALS", "REG_A", "MINUS", "REG_D", "END_LINE"]:
        reg_d_a_minus_d()
    if tokenized_line == ["REG_A", "EQUALS", "REG_D", "MINUS", "REG_A", "END_LINE"]:
        reg_a_d_minus_a()
    if tokenized_line == ["REG_D", "EQUALS", "REG_D", "MINUS", "REG_A", "END_LINE"]:
        reg_d_d_minus_a()
    # Ram minus operation
    if tokenized_line == ["REG_A", "EQUALS", "ASTRIX", "REG_A", "MINUS", "REG_D", "END_LINE"]:
        reg_a_ram_minus_d()
    if tokenized_line == ["REG_D", "EQUALS", "ASTRIX", "REG_A", "MINUS", "REG_D", "END_LINE"]:
        reg_d_ram_minus_d()
    if tokenized_line == ["REG_A", "EQUALS", "REG_D", "MINUS", "ASTRIX", "REG_A", "END_LINE"]:
        reg_a_d_minus_ram()
    if tokenized_line == ["REG_D", "EQUALS", "REG_D", "MINUS", "ASTRIX", "REG_A", "END_LINE"]:
        reg_d_d_minus_ram()
    # And operation
    if tokenized_line == ["REG_A", "EQUALS", "REG_A", "AND", "REG_D", "END_LINE"]:
        reg_a_and()
    if tokenized_line == ["REG_D", "EQUALS", "REG_A", "AND", "REG_D", "END_LINE"]:
        reg_d_and()
    # And ram operation
    if tokenized_line == ["REG_A", "EQUALS", "ASTRIX", "REG_A", "AND", "REG_D", "END_LINE"]:
        reg_a_ram_and()
    if tokenized_line == ["REG_D", "EQUALS", "ASTRIX", "REG_A", "AND", "REG_D", "END_LINE"]:
        reg_d_ram_and()
    # Or operation
    if tokenized_line == ["REG_A", "EQUALS", "REG_A", "OR", "REG_D", "END_LINE"]:
        reg_a_or()
    if tokenized_line == ["REG_D", "EQUALS", "REG_A", "OR", "REG_D", "END_LINE"]:
        reg_d_or()
    # Or ram operation
    if tokenized_line == ["REG_A", "EQUALS", "ASTRIX", "REG_A", "OR", "REG_D", "END_LINE"]:
        reg_a_ram_or()
    if tokenized_line == ["REG_D", "EQUALS", "ASTRIX", "REG_A", "OR", "REG_D", "END_LINE"]:
        reg_d_ram_or()
