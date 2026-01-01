# -------- ELAPTIC OS KERNEL (Universal Compatibility) --------
import _thread
# We need the 'sys' library to manually manage imports within the module registry
# I just like having high level access to imports in the environment of an operating system :p
import sys

# This dictionary will hold references to all loaded modules, shared globally
module_registry = {}


# --- Helper Function for Dynamic Loading ---
def load_module_to_registry(module_path: str, important: bool):
    """
    Dynamically loads a module using standard Python import mechanism
    and stores it in the shared module_registry dictionary.
    """
    module_short_name = module_path.split('.')[-1]

    # We load ANSI first to use its colors
    if 'ansi' in module_registry:
        print(
            f"{module_registry['ansi'].ansi['green']}--Loading {module_path} as {module_short_name}{module_registry['ansi'].ansi['reset']}")
    else:
        # Fallback print if ansi isn't loaded yet
        print(f"--Loading {module_path} as {module_short_name}")

    try:
        # Manually import the module. Python caches this automatically.
        __import__(module_path)
        loaded_module = sys.modules[module_path]

        # Store the module object reference in our central dictionary
        module_registry[module_short_name] = loaded_module

        if 'ansi' in module_registry:
            print(
                f"{module_registry['ansi'].ansi['green']}--Successfully registered {module_short_name}{module_registry['ansi'].ansi['reset']}")
        else:
            print(
                f"--Successfully registered {module_short_name}")

    except ImportError as e:
        if important:
            if 'ansi' in module_registry:
                print(
                    f"{module_registry['ansi'].ansi['red']}KERNEL PANIC: Module '{module_path}' failed to load. Halting. ({e}){module_registry['ansi'].ansi['reset']}")
            else:
                print(f"KERNEL PANIC: Module '{module_path}' failed to load. Halting. ({e})")
            quit()
        else:
            if 'ansi' in module_registry:
                print(f"{module_registry['ansi'].ansi['yellow']}Module '{module_path}' failed to load, but is not required. This may cause issues later. ({e}){module_registry['ansi'].ansi['reset']}")
            else:
                print(f"Module '{module_path}' failed to load, but is not required. This may cause issues later. ({e})")

# --- OS Startup Logic ---

# Literals:
kernel_version = "Beta 0.0.3"

print(f"Kernel loaded! Version: {kernel_version}")

import builtins
builtins.__elaptic_registry__ = module_registry

# Load modules
load_module_to_registry("kernel.modules.ansi", True)
load_module_to_registry("sys", True)
load_module_to_registry("os", False)
load_module_to_registry("re", True)
load_module_to_registry("select", False)
load_module_to_registry("builtins", True)
load_module_to_registry("_thread", False)
load_module_to_registry("asyncio", True)
load_module_to_registry("time", True)
load_module_to_registry("kernel.modules.keyboard", True)
load_module_to_registry("kernel.modules.api", True)
load_module_to_registry("kernel.modules.pixel", False)
load_module_to_registry("kernel.modules.interpreter", True)
load_module_to_registry("kernel.ede", False)
load_module_to_registry("kernel.modules.shellwrapper", True)

# Set variable names to module
ansi = module_registry['ansi']
asyncio = module_registry['asyncio']
ede = module_registry['ede']
time = module_registry['time']
sys = module_registry['sys']
interpreter = module_registry['interpreter']
shellwrapper = module_registry['shellwrapper']
keyboard = module_registry['keyboard']
environment = sys.implementation.name

print("\n\n\n")

# --------KERNEL SYSTEM--------
def mainloop():
    while True:
        time.sleep(3)

def shell_interface(start_command = ""):
    if start_command != "":
        shellwrapper.run_shell_command(start_command)
    print(f"--------ElapticOS Version {kernel_version} running under '{environment}'--------")
    while True:
        keyboard.stop_keyboard_monitoring() #make sure keyboard monitoring doesn't interact with inputs
        command = input("$> ")
        shellwrapper.run_shell_command(command)


# Start the kernel :D
_thread.start_new_thread(mainloop, ())
shell_interface() #start with ede
