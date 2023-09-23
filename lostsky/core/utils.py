from math import ceil, log
import pygame

def format_number(n, accuracy=6):
    """Formats a number in a friendly manner
    (removes trailing zeros and unneccesary point."""

    fs = "%."+str(accuracy)+"f"
    str_n = fs % float(n)
    if '.' in str_n:
        str_n = str_n.rstrip('0').rstrip('.')
    if str_n == "-0":
        str_n = "0"
    return str_n


def lerp(a, b, i):
    """Linear enterpolate from a to b."""
    return a + (b - a) * i


def range2d(range_x, range_y):

    """Creates a 2D range."""

    range_x = list(range_x)
    return [(x, y) for y in range_y for x in range_x]


def xrange2d(range_x, range_y):

    """Iterates over a 2D range."""

    range_x = list(range_x)
    for y in range_y:
        for x in range_x:
            yield (x, y)


def saturate(value, low, high):
    return min(max(value, low), high)


def is_power_of_2(n):
    """Returns True if a value is a power of 2."""
    return log(n, 2) % 1.0 == 0.0


def next_power_of_2(n):
    """Returns the next power of 2 that is >= n"""
    return int(2 ** ceil(log(n, 2)))

def split_lines(string, max_length=90):
    """
    # THIS FUNCTION IS DEPRECATED: PLEASE USE DRAW ALIGNED TEXT
    # Function name: linesplitter
    # Purpose: Splits a single string into a list of strings of a defined maximum length
    # Inputs: string - A string that is to be split up
    #         max_length - maximum length of each line
    # Outputs: lines - The string broken up
    """

    print "This function is deprecated. Please use the draw_aligned_text function."

    next_word = ""
    lines = [""]
    linecount = 0
    # Iterates through each character in the string
    for i in xrange(0, len(string)):
        char = string[i]
        next_word += char
        # If the character is a space, we consider that a complete word
        # If the length of the word + length of the current line is shorter than the
        # Max length / line then we add it to the line. Otherwise we create a new line
        if char == " " or char == "-" or i == len(string)-1:
            if len(lines[linecount]) + len(next_word) < max_length:
                lines[linecount] += next_word
            else:
                linecount += 1
                lines.append("")
                lines[linecount] += next_word
            next_word = ""

    return lines

def set_transparency(surface, alpha_scaling):
    working_surface = surface.copy()
    working_surface.lock()
    for x in xrange(0, working_surface.get_width() - 1):
        for y in xrange(0, working_surface.get_height() - 1):
            r, g, b, a = working_surface.get_at((x, y))

            if a:
                working_surface.set_at((x, y), (r, g, b, alpha_scaling))
    working_surface.unlock()
    return working_surface

def padlib_rounded_rect(surface, color, rect, radius, width = 0):
    """
    Draws a rounded rectangle

    Credit: This function is from the PAdlib library created by Ian Mallett (Geometrian)
    http://www.geometrian.com/
    """

    if color[0] + color[1] + color[2] == 0:
        colorkey = (1,1,1)
    else:
        colorkey = (0,0,0)

    surf_temp = pygame.Surface((rect[2],rect[3]))
    surf_temp.fill(colorkey)

    pygame.draw.rect(surf_temp,color,(0,radius,rect[2],rect[3]-2*radius),0)
    pygame.draw.rect(surf_temp,color,(radius,0,rect[2]-2*radius,rect[3]),0)

    for point in [
        [radius,radius],
        [rect[2]-radius,radius],
        [radius,rect[3]-radius],
        [rect[2]-radius,rect[3]-radius]
    ]:
        pygame.draw.circle(surf_temp,color,point,radius,0)

    if width != 0:
        padlib_rounded_rect(surf_temp,colorkey,(width,width,rect[2]-2*width,rect[3]-2*width),radius-width,0)

    surf_temp.set_colorkey(colorkey)
    surface.blit(surf_temp,(rect[0],rect[1]))

def draw_aligned_text(surface, line, font, color, origin, width_limit):

    """
    draw_wrapped_text

    Draws evenly spaced text wrapped to a certain pixel radius

    Inputs:
        surface - target surface to render to
        line - a string of text
        font - a Pygame font object that does the rendering
        color - color to render font with
        origin - the origin coordinates for the object
        width_limit - the maximum width (in pixels) to draw to.

    """

    # Generates the text surfaces
    string_words = line.split(' ')
    rendered_words = [font.render(word, True, color) for word in string_words if word]

    current_x, current_y = origin

    # tracks the width of the words alone
    current_width = 0
    current_line = []

    # Size of a single space character is used to calibrate minimum spacing in x and vertical spacing
    font_x, font_y = font.size(' ')

    for index, word in enumerate(rendered_words):

        # If we are at the start of a list and the current word is greater than the width limit, just blit it
        if current_width == 0 and word.get_width() > width_limit:
            surface.blit(word, (current_x, current_y))
            current_y += font_y

        else:

            # If the addition of the current word exceeds the width limit, blit what's currently
            # in the current line and go to the new line
            if word.get_width() + current_width + len(current_line)*font_x > width_limit:

                space_pixels = width_limit - current_width
                delta_x = space_pixels / max(1, (len(current_line) - 1))

                # Draws each word with the appropriate spacing
                for word_to_draw in current_line:

                    surface.blit(word_to_draw, (current_x, current_y))
                    current_x += (word_to_draw.get_width() + delta_x)

                # Sets the rendering coordinates back to the original x position and down one line
                current_x = origin[0]
                current_y += font_y

                # Resets the width tracker and the current line
                current_width = word.get_width()
                current_line = [word]


            # Otherwise, append it to the current line
            else:
                current_line.append(word)
                current_width += word.get_width()

    # for the last line, do not justify to the edges and use the standard spacing
    for word_to_draw in current_line:

        surface.blit(word_to_draw, (current_x, current_y))
        current_x += (word_to_draw.get_width() + font_x)

def get_ui_panel(size, border_color, panel_color):
    """
    Generates a rounded rectangle panel commonly used in the UI

    Inputs: Size - an (x, y) tuple showing the size of the panel
                   border_color, panel_color - color to use for the border and interior respectively
    """

    panel = pygame.Surface(size, pygame.SRCALPHA)
    padlib_rounded_rect(panel, border_color, (0, 0, panel.get_width(), panel.get_height()), 5)
    padlib_rounded_rect(panel, panel_color, (2, 2, panel.get_width() - 4, panel.get_height() - 4), 3)

    return panel