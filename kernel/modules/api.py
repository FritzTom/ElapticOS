# WARNING: USER PROGRAMS CAN ACCESS ANYTHING IMPORTED HERE, FIX ASAP
# TODO: confirm if fixed ^

dump_to_ede = True # Flag for programs to exit back to ede, if false it goes to the shell. should default to go back to ede

def lastkey(reset = False):
    keyboard = __elaptic_registry__['keyboard']
    last_key = keyboard.last_key
    if reset:
        keyboard.last_key = ""
    return last_key

def touch(path: str):
    with open(f"fs/{path}", "w") as f:
        pass
    return True

def rm(path: str):
    os = __elaptic_registry__['os']
    try:
        os.remove(f"fs/{path}")
        return True
    except:
        return False

def sleep(amount: int):
    time = __elaptic_registry__['time']
    time.sleep(amount)