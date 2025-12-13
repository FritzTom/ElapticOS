shell = __elaptic_registry__['shellbackend']
def run_shell_command(command: str, directory =  "/"):
    tokenized_command = command.split()
    if tokenized_command[0] == "help":
        print("""
        ElapticOS Guide:
            run <directory to .py file> | Runs a python program.
        """)
    elif tokenized_command[0] == "run":
        with open(f"fs/{tokenized_command[1]}", "r") as f:
            shell.run_script(f.read())