os = __elaptic_registry__['os']
def touch(path="/"):
    with open(f"fs/{path}", "w") as f:
        pass