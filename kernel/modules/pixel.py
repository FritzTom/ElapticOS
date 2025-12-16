# clever ahh text-based graphics

class Bitmap:
    def __init__(self, width, height, pixels):
        self.width = width
        self.height = height
        self.pixels = pixels[:]  # copy list
        # Fill with transparent pixels if not enough pixels provided
        # 0x000000 is now treated as the transparency key.
        missing = width * height - len(self.pixels)
        if missing > 0:
            self.pixels.extend([0x000000] * missing)
        self.visible = True
        self.x = 0
        self.y = 0
        self.z = 0  # z-height for layering

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def set_z(self, z):
        self.z = z


class Screen:
    def __init__(self, width_chars, height_chars):
        # width_chars, height_chars = size in character cells
        # each character cell = 2 vertical pixels
        self.width_chars = width_chars
        self.height_chars = height_chars
        self.width_pixels = width_chars
        self.height_pixels = height_chars * 2
        self.clear_color = 0x000000  # Clear color is transparent black
        self.sprites = []

    def add_sprite(self, sprite):
        self.sprites.append(sprite)
        self.sort_sprites()

    def remove_sprite(self, sprite):
        if sprite in self.sprites:
            self.sprites.remove(sprite)

    def sort_sprites(self):
        self.sprites.sort(key=lambda s: s.z)

    def clear(self):
        self.pixel_buffer = [
            [self.clear_color for _ in range(self.width_pixels)]
            for __ in range(self.height_pixels)
        ]

    def render(self):
        self.clear()
        # Draw sprites in z-order
        for sprite in self.sprites:
            if not sprite.visible:
                continue
            for py in range(sprite.height):
                screen_y = sprite.y + py
                if 0 <= screen_y < self.height_pixels:
                    for px in range(sprite.width):
                        screen_x = sprite.x + px
                        if 0 <= screen_x < self.width_pixels:
                            pixel_color = sprite.pixels[py * sprite.width + px]

                            # If the pixel is not the transparency key (0x000000), draw it.
                            if pixel_color != 0x000000:
                                self.pixel_buffer[screen_y][screen_x] = pixel_color

        # Now convert pixel_buffer to text lines using lower-half block chars
        lines = []
        for char_row in range(self.height_chars):
            line_chars = []
            top_row = char_row * 2
            bot_row = top_row + 1
            for char_col in range(self.width_chars):
                top_pixel = self.pixel_buffer[top_row][char_col]
                bot_pixel = (
                    self.pixel_buffer[bot_row][char_col]
                    if bot_row < self.height_pixels
                    else self.clear_color
                )

                # Compose ANSI escape for fg/bg color and lower half block char
                # For lower half block: top pixel becomes background, bottom pixel becomes foreground.
                fg = self.rgb_to_ansi(bot_pixel, background=False)
                bg = self.rgb_to_ansi(top_pixel, background=True)
                char = "\u2584"  # lower half block
                line_chars.append(f"{fg}{bg}{char}\033[0m")
            lines.append("".join(line_chars))
        return "\n".join(lines)

    @staticmethod
    def rgb_to_ansi(rgb, background=False):
        r = (rgb >> 16) & 0xFF
        g = (rgb >> 8) & 0xFF
        b = rgb & 0xFF
        return (
            f"\033[48;2;{r};{g};{b}m"
            if background
            else f"\033[38;2;{r};{g};{b}m"
        )
