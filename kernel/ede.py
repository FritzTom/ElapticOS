# --------ELAPTIC DESKTOP ENVIRONMENT--------
# REQUIRED MODULES:
pixel = __elaptic_registry__['pixel']
ansi = __elaptic_registry__['ansi']
asyncio = __elaptic_registry__['asyncio']
time = __elaptic_registry__['time']
re = __elaptic_registry__['re']
os = __elaptic_registry__['os']
keyboard = __elaptic_registry__['keyboard']
interpreter = __elaptic_registry__['interpreter']
_thread = __elaptic_registry__['_thread']

def lastkey(reset = False):
    last_key = keyboard.last_key
    if reset:
        keyboard.last_key = ""
    return last_key

def get_program_icon(filepath):
    """Finds the first triple-quoted block in a file and evals it as a list."""
    try:
        with open(filepath, 'r') as f:
            # Only read the start of the file to save memory
            content = f.read(2048) 
            
            # Find content between first occurrence of """..."""
            # re.DOTALL allows the dot to match newlines
            match = re.search(r'"""(.*?)"""', content, re.DOTALL)
            
            if match:
                # Extract the string inside the quotes
                list_str = match.group(1).strip()
                # Evaluate the string into a Python list
                return eval(list_str)
    except Exception as e:
        print(f"Error loading icon from {filepath}: {e}")
    return None

def scan_directory(directory_path):
    """Scans fs/programs and sets icons."""
    icons = {}
    for filename in os.listdir(directory_path):
        if filename.endswith(".py"):
            path = os.path.join(directory_path, filename)
            icon_data = get_program_icon(path)
            icons[filename] = icon_data
    return icons

program_icons = scan_directory("fs/programs")
desktop_elements = ["selector", "icon1", "icon2"]
program_elements = ["selector", "icon1", "icon2"]

def showdesktop():
    for element in desktop_elements:
        eval(f"{element}.show()")
    for element in program_elements:
        eval(f"{element}.hide()")

def hidedesktop():
    for element in desktop_elements:
        eval(f"{element}.hide()")
    for element in program_elements:
        eval(f"{element}.show()")

def desktop_main():
    running_desktop = True # this controls the while loop, if it is set to false it should stop the display manager loop, which can be called again to restart
    selector_grid_x = 0
    selector_grid_y = 0
    
    screen = pixel.Screen(32, 16)
    background = pixel.Bitmap(32, 32, ([0x010101]) * 32 * 32)  # black background fill
    background.set_position(0, 0)
    screen.add_sprite(background)

    icon1 = pixel.Bitmap(8, 8, program_icons["program1.py"])
    icon1.set_position(1,1)
    screen.add_sprite(icon1)

    icon2 = pixel.Bitmap(8, 8, program_icons["program2.py"])
    icon2.set_position(12,1)
    screen.add_sprite(icon2)

    # add a terminal program eventually pretty please

    # Create selector
    selector = pixel.Bitmap(8, 8, [0x00ff11, 0x000000, 0x000000, 0x00ff11, 0x00ff11, 0x000000, 0x000000, 0x00ff11, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x00ff11, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x00ff11, 0x00ff11, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x00ff11, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x00ff11, 0x000000, 0x000000, 0x00ff11, 0x00ff11, 0x000000, 0x000000, 0x00ff11])
    screen.add_sprite(selector)

    while running_desktop:
        time.sleep(0.25)
        key = keyboard.get_last_key_pressed(True)

        if key == "RIGHT":
            if selector_grid_x < 2:
                selector_grid_x += 1

        elif key == "LEFT":
            if selector_grid_x > 0:
                selector_grid_x -= 1

        elif key == "DOWN":
            if selector_grid_y < 2:
                selector_grid_y += 1

        elif key == "UP":
            if selector_grid_y > 0:
                selector_grid_y -= 1


        elif key == "ENTER": # run the selected program
            running_desktop = False
            programselection = ""
            if selector_grid_x == 0 and selector_grid_y == 0: # we are hardcoding this because i don't know how else we should do it
                programselection = "1"
            if selector_grid_x == 1 and selector_grid_y == 0:
                programselection = "2"
            with open(f"fs/programs/program{programselection}.py", "r") as f:

                script_content = f.read()

                def script_wrapper():
                    # The interpreter.run_script function likely needs the content as an argument
                    interpreter.run_script(script_content)

                return _thread.start_new_thread(script_wrapper())

        selector.set_position(1 + (selector_grid_x * 11), 1 + (selector_grid_y * 11))
        print(f"\n\n\n\n{ansi.ansi['clear']}{screen.render()}")
