reg_a: int = 0
reg_d: int = 0
ram: dict = {}
program_counter: int = 0


def debug_print():
    print(f"Reg_A: {reg_a} | Reg_D: {reg_d} | PC: {program_counter} | Memory: {ram}")


def save_a(val: int):
    global reg_a
    reg_a = val


def save_d(val: int):
    global reg_d
    reg_d = val


def load_a():
    global reg_a
    return reg_a


def load_d():
    global reg_d
    return reg_d


def save_pc(val: int):
    global program_counter
    program_counter = val


def load_pc():
    global program_counter
    return program_counter


def ram_write(addr: int, val: int):
    global ram
    ram[addr] = val


def ram_read(addr: int):
    global ram
    return ram.get(addr)
