# --------SHELL WRAPPER--------

interpreter = __elaptic_registry__['interpreter']
api = __elaptic_registry__['api']
_thread = __elaptic_registry__['_thread']
ede = __elaptic_registry__['ede']

def run_shell_command(command: str, directory =  "/"):
    tokenized_command = command.split()
    try:
        if tokenized_command[0] == "help":
            print("""
            ElapticOS Guide:
                help                        | Displays the help menu.
                run <directory to .py file> | Runs a python program.
                rm  <file>                  | Deletes a file
            """)

        elif tokenized_command[0] == "run": # Run python program
            with open(f"fs/{tokenized_command[1]}", "r") as f:

                script_content = f.read()

                interpreter.run_script(script_content)

        elif tokenized_command[0] == "touch": # Create empty file
            api.touch(tokenized_command[1])

        elif tokenized_command[0] == "rm": # Remove file
            if api.rm(tokenized_command[1]):
                print(f"Removed file '{tokenized_command[1]}'")
            else:
                print(f"Failed to remove file '{tokenized_command[1]}'")

        elif tokenized_command[0] == "ede":
            ede.desktop_main()
            return 1

        elif tokenized_command[0] == "exit":
            quit()

        else:
            print(f"Invalid command: {command}")
    except:
        pass