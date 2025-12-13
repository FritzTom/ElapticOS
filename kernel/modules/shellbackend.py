# kernel/shellbackend.py

builtins = __elaptic_registry__['builtins']
asyncio = __elaptic_registry__['asyncio']
sys = __elaptic_registry__['sys']
os = __elaptic_registry__['os']

api = __elaptic_registry__['api']


# --- The Sandbox Environment Setup ---

def _create_secure_execution_env(): # Only whitelisted builtins are allowed
    # Whitelist of safe Python built-ins
    whitelist_builtins = [
        'print', 'len', 'range', 'list', 'dict', 'tuple', 'str', 'int', 'float',
        'bool', 'type', 'isinstance', 'KeyError', 'ValueError', 'TypeError', 'Exception',
        'asyncio',  # We allow asyncio functions for task management
    ]

    safe_builtins = {}
    for name in whitelist_builtins:
        if hasattr(builtins, name):
            safe_builtins[name] = getattr(builtins, name)

    # The environment dictionary that user code can access
    secure_globals = {
        '__builtins__': safe_builtins,
        'api': api,  # Expose specific kernel functions directly
        # We can add a top-level 'api' object too if preferred:
    }

    return secure_globals


# Initialize the secure environment once when this module loads
_GLOBAL_SECURE_SCOPE = _create_secure_execution_env()

# A persistent local scope to maintain variables across shell commands
_SESSION_LOCAL_SCOPE = {}


# --- 2. API Functions for Execution (Exposed to the Kernel/Shell) ---

def run_shell_command(command: str):
    """
    Executes a single line of Python code in the sandbox.
    Uses exec() to allow variable assignment persistence in _SESSION_LOCAL_SCOPE.
    """
    try:
        # Use exec for single lines, preserving local state
        exec(command, _GLOBAL_SECURE_SCOPE, _SESSION_LOCAL_SCOPE)
        return "Command executed."
    except Exception as e:
        # Return error message to the shell UI
        return f"Execution Error: {e}"


def run_script(script_code: str):
    """
    Executes a multi-line Python script (e.g., from a file) in the sandbox.
    Uses a fresh local scope for a cleaner execution boundary if needed,
    or you can use the session local scope.
    """
    # Use the session scope here too to let scripts interact with shell vars
    local_scope_for_script = _SESSION_LOCAL_SCOPE.copy()

    try:
        # Use exec for multi-line scripts
        exec(script_code, _GLOBAL_SECURE_SCOPE, local_scope_for_script)
        # Update session locals after script finishes
        _SESSION_LOCAL_SCOPE.update(local_scope_for_script)
        return "Script executed successfully."
    except Exception as e:
        return f"Script Error: {e}"


async def run_background_task(async_function_to_run):
    """
    Starts an asynchronous task in the kernel's asyncio event loop.
    The user would call this via the shell like:
    `ls('dir')` or `api.run_background_task(my_async_func)`
    """
    # This requires that the 'asyncio' library is correctly available
    # in the main kernel environment where this function is ultimately called/awaited.
    try:
        task = asyncio.create_task(async_function_to_run())
        return f"Started background task: {task.get_name()}"
    except Exception as e:
        return f"Failed to start task: {e}"


# If you want to allow users to see their current local variables:
def get_session_variables():
    """Returns a dictionary of non-underscore session variables."""
    return {k: v for k, v in _SESSION_LOCAL_SCOPE.items() if not k.startswith('_')}

