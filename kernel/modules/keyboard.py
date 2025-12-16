import sys
import time
import select
import _thread

# --- Global State ---
last_key = "none"
_lock = _thread.allocate_lock()

# --- Environment Specific Imports ---
if sys.platform in ('linux', 'darwin'):
    import termios, tty
    _fd = sys.stdin.fileno()
    _old_settings = termios.tcgetattr(_fd)
elif sys.platform == 'win32':
    import msvcrt

def _keyboard_listener_thread():
    global last_key

    if sys.platform in ('linux', 'darwin'):
        tty.setcbreak(sys.stdin.fileno())

    try:
        while True:
            char = None

            if sys.platform in ('linux', 'darwin'):
                rlist, _, _ = select.select([sys.stdin], [], [], 0.01)
                if rlist:
                    char = sys.stdin.read(1)
                    if char == '\x1b':
                        char += sys.stdin.read(2)

            elif sys.platform == 'win32':
                if msvcrt.kbhit():
                    # Read as raw bytes to avoid UTF-8 decode errors on prefix bytes
                    raw_char = msvcrt.getch()
                    if raw_char in (b'\x00', b'\xe0'):
                        # Arrow keys on Windows are two bytes; second byte defines direction
                        raw_char += msvcrt.getch()
                    char = raw_char

            else:
                # MicroPython / Generic
                rlist, _, _ = select.select([sys.stdin], [], [], 0)
                if rlist:
                    char = sys.stdin.read(1)
                    if char == '\x1b':
                        char += sys.stdin.read(2)

            if char:
                key_name = None
                
                # Windows Byte Sequence Mapping
                if char == b'\xe0H': key_name = "UP"
                elif char == b'\xe0P': key_name = "DOWN"
                elif char == b'\xe0M': key_name = "RIGHT"
                elif char == b'\xe0K': key_name = "LEFT"
                elif char == b'\r':   key_name = "ENTER"
                
                # POSIX/ANSI String Mapping
                elif char == '\x1b[A': key_name = "UP"
                elif char == '\x1b[B': key_name = "DOWN"
                elif char == '\x1b[C': key_name = "RIGHT"
                elif char == '\x1b[D': key_name = "LEFT"
                elif char in ('\r', '\n'): key_name = "ENTER"
                
                # Default character handling
                else:
                    try:
                        key_name = char.decode('utf-8') if isinstance(char, bytes) else char
                    except:
                        key_name = str(char)

                with _lock:
                    last_key = key_name

            time.sleep(0.01)

    except Exception as e:
        print(f"Keyboard input thread error: {e}")
    finally:
        if sys.platform in ('linux', 'darwin'):
            termios.tcsetattr(_fd, termios.TCSADRAIN, _old_settings)

def start_keyboard_monitoring():
    print("Keyboard module starting input monitoring thread...")
    _thread.start_new_thread(_keyboard_listener_thread, ())

def get_last_key_pressed(clear_key=True):
    global last_key
    with _lock:
        key = last_key
        if clear_key:
            last_key = None
        return key
