# ansi.py

ansi = {
    # ---------- Foreground ----------
    "black":   "\x1b[38;2;0;0;0m",
    "red":     "\x1b[38;2;255;0;0m",
    "green":   "\x1b[38;2;0;255;0m",
    "yellow":  "\x1b[38;2;255;255;0m",
    "blue":    "\x1b[38;2;0;0;255m",
    "magenta": "\x1b[38;2;255;0;255m",
    "cyan":    "\x1b[38;2;0;255;255m",
    "white":   "\x1b[38;2;255;255;255m",

    # Bright / bold variants (often same as the normal colour but with “bold”)
    "bright_black":   "\x1b[38;2;128;128;128m",
    "bright_red":     "\x1b[38;2;255;85;85m",
    "bright_green":   "\x1b[38;2;85;255;85m",
    "bright_yellow":  "\x1b[38;2;255;255;85m",
    "bright_blue":    "\x1b[38;2;85;85;255m",
    "bright_magenta": "\x1b[38;2;255;85;255m",
    "bright_cyan":    "\x1b[38;2;85;255;255m",
    "bright_white":   "\x1b[38;2;255;255;255m",

    # ---------- Background ----------
    "on_black":   "\x1b[48;2;0;0;0m",
    "on_red":     "\x1b[48;2;255;0;0m",
    "on_green":   "\x1b[48;2;0;255;0m",
    "on_yellow":  "\x1b[48;2;255;255;0m",
    "on_blue":    "\x1b[48;2;0;0;255m",
    "on_magenta": "\x1b[48;2;255;0;255m",
    "on_cyan":    "\x1b[48;2;0;255;255m",
    "on_white":   "\x1b[48;2;255;255;255m",

    # Bright / bold background
    "on_bright_black":   "\x1b[48;2;128;128;128m",
    "on_bright_red":     "\x1b[48;2;255;85;85m",
    "on_bright_green":   "\x1b[48;2;85;255;85m",
    "on_bright_yellow":  "\x1b[48;2;255;255;85m",
    "on_bright_blue":    "\x1b[48;2;85;85;255m",
    "on_bright_magenta": "\x1b[48;2;255;85;255m",
    "on_bright_cyan":    "\x1b[48;2;85;255;255m",
    "on_bright_white":   "\x1b[48;2;255;255;255m",

    # ---------- Misc ----------
    "reset":      "\x1b[0m",          # reset all attributes
    "bold":       "\x1b[1m",
    "underline":  "\x1b[4m",
    "reverse":    "\x1b[7m",
    "clear":      "\x1b[2J\x1b[H",
}
