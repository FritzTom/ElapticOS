import sys
import time
import select
import _thread

# --- Global State ---
last_key = "none"
_lock = _thread.allocate_lock()
_monitoring_active = False  # Added flag to control the thread

# --- Environment Specific Imports ---
if sys.platform in ('linux', 'darwin'):
    import termios, tty

    _fd = sys.stdin.fileno()
    _old_settings = termios.tcgetattr(_fd)
elif sys.platform == 'win32':
    import msvcrt


def _keyboard_listener_thread():
    global last_key, _monitoring_active

    # Set terminal to cbreak mode (non-canonical)
    if sys.platform in ('linux', 'darwin'):
        tty.setcbreak(_fd)

    try:
        # Check the flag instead of 'True'
        while _monitoring_active:
            char = None

            if sys.platform in ('linux', 'darwin'):
                rlist, _, _ = select.select([sys.stdin], [], [], 0.1)  # Increased timeout slightly for efficiency
                if rlist:
                    char = sys.stdin.read(1)
                    if char == '\x1b':
                        char += sys.stdin.read(2)

            elif sys.platform == 'win32':
                if msvcrt.kbhit():
                    raw_char = msvcrt.getch()
                    if raw_char in (b'\x00', b'\xe0'):
                        raw_char += msvcrt.getch()
                    char = raw_char

            else:
                rlist, _, _ = select.select([sys.stdin], [], [], 0)
                if rlist:
                    char = sys.stdin.read(1)
                    if char == '\x1b':
                        char += sys.stdin.read(2)

            if char:
                key_name = None
                # Windows Byte Sequence Mapping
                if char == b'\xe0H':
                    key_name = "UP"
                elif char == b'\xe0P':
                    key_name = "DOWN"
                elif char == b'\xe0M':
                    key_name = "RIGHT"
                elif char == b'\xe0K':
                    key_name = "LEFT"
                elif char == b'\r':
                    key_name = "ENTER"
                # POSIX/ANSI String Mapping
                elif char == '\x1b[A':
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
                    try:
                        key_name = char.decode('utf-8') if isinstance(char, bytes) else char
                    except:
                        key_name = str(char)

                with _lock:
                    last_key = key_name

            time.sleep(0.01)

    except Exception as e:
        pass  # Handle errors silently in kernel
    finally:
        # IMPORTANT: This restores the terminal to "Normal" mode (Cooked mode)
        # This allows standard input() to see characters and backspaces again.
        if sys.platform in ('linux', 'darwin'):
            termios.tcsetattr(_fd, termios.TCSADRAIN, _old_settings)


def start_keyboard_monitoring():
    global _monitoring_active
    if _monitoring_active:
        return  # Already running

    _monitoring_active = True
    _thread.start_new_thread(_keyboard_listener_thread, ())


def stop_keyboard_monitoring():
    global _monitoring_active
    _monitoring_active = False
    # Small sleep to give the thread time to hit the 'finally' block and reset the terminal
    time.sleep(0.1)


def get_last_key_pressed(clear_key=True):
    global last_key
    with _lock:
        key = last_key
        if clear_key:
            last_key = None
        return key