# WARNING: USER PROGRAMS CAN ACCESS ANYTHING IMPORTED HERE, FIX ASAP
os = __elaptic_registry__['os']
time = __elaptic_registry__['time']
keyboard = __elaptic_registry__['keyboard']



def lastkey(reset = False):
    last_key = keyboard.last_key
    if reset:
        keyboard.last_key = ""
    return last_key

def touch(path: str):
    with open(f"fs/{path}", "w") as f:
        pass
    return True

def rm(path: str):
    try:
        os.remove(f"fs/{path}")
        return True
    except:
        return False

def sleep(amount: int):
    time.sleep(amount)