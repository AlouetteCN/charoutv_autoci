
def debug_normal(*args):
    print("- ", end='')
    for _ in args:
        print(f"{_}  ", end='')
    print("\n")


def dn(*args):
    debug_normal(*args)
