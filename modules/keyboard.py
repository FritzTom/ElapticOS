sys = __elaptic_registry__['sys']
time = __elaptic_registry__['time']
select = __elaptic_registry__['select']
_thread = __elaptic_registry__['_thread']

# --- Global State (Accessed by main program) ---
# The main program should read this variable.
last_key = ""

# A lock is necessary for thread safety when modifying 'last_key'
_lock = _thread.allocate_lock()

# --- Environment Specific Imports/Setup ---

# Import necessary OS-specific modules only if on desktop CPython
if sys.platform in ('linux', 'darwin'):
    # We need termios and tty for raw input mode on Posix systems
    import termios, tty

    _fd = sys.stdin.fileno()
    _old_settings = termios.tcgetattr(_fd)

elif sys.platform == 'win32':
    # We need msvcrt for immediate key detection on Windows
    import msvcrt


# --- Core Thread Function ---

def _keyboard_listener_thread():
    """
    This function runs continuously on a separate thread, detects key presses,
    and updates the global 'last_key' variable.
    """
    global last_key

    # Set terminal to raw mode if running on CPython desktop for immediate key capture
    if sys.platform in ('linux', 'darwin'):
        tty.setcbreak(sys.stdin.fileno())

    try:
        while True:
            char = None

            # --- Input Reading Logic (Specific to current environment) ---
            if sys.platform in ('linux', 'darwin'):
                # CPython Linux/macOS
                rlist, _, _ = select.select([sys.stdin], [], [], 0.01)
                if rlist:
                    char = sys.stdin.read(1)
                    if char == '\x1b': char += sys.stdin.read(2)

            elif sys.platform == 'win32':
                # CPython Windows
                if msvcrt.kbhit():
                    char = msvcrt.getch().decode('utf-8')
                    if char in ('\x00', '\xe0'): char += msvcrt.getch().decode('utf-8')

            else:
                # MicroPython (RP2, ESP32, etc.) serial input
                rlist, _, _ = select.select([sys.stdin], [], [], 0)
                if rlist:
                    char = sys.stdin.read(1)
                    if char == '\x1b': char += sys.stdin.read(2)

            # --- Process and Store the Key Safely ---
            if char:
                # Map ANSI sequences to standard names
                key_name = None
                if char == '\x1b[A':
                    key_name = "UP"
                elif char == '\x1b[B':
                    key_name = "DOWN"
                elif char == '\x1b[C':
                    key_name = "RIGHT"
                elif char == '\x1b[D':
                    key_name = "LEFT"
                elif char in ('\r', '\n'):
                    key_name = "ENTER"
                else:
                    key_name = char

                # Acquire lock before updating the shared variable
                with _lock:
                    last_key = key_name

            time.sleep(0.01)  # Small pause to prevent 100% CPU usage

    except Exception as e:
        # Simple error handling within the thread
        print(f"Keyboard input thread error: {e}")
    finally:
        # Ensure terminal mode is reset on desktop CPython when thread terminates (if it ever does)
        if sys.platform in ('linux', 'darwin'):
            termios.tcsetattr(_fd, termios.TCSADRAIN, _old_settings)


# --- Public Module Functions ---

def start_keyboard_monitoring():
    """Starts the background thread to monitor keyboard input."""
    # This is the function other OS components will call to activate the module
    print("Keyboard module starting input monitoring thread...")
    _thread.start_new_thread(_keyboard_listener_thread, ())


def get_last_key_pressed(clear_key=True):
    """
    Reads the last key pressed and optionally clears the internal buffer.
    Use this function from your main OS loop.
    """
    global last_key
    with _lock:
        key = last_key
        if clear_key:
            last_key = None  # Clear the key so it only registers once
        return key

