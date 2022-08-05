#Known bugs:
# blows stuff up well beyond terminal dimensions :/ spaghetti
# truncates right edge of image under some conditions?
# for images with extreme aspect ratios, output sometimes too wide for terminal
#   !    This is happening because the script bases output size off of height
#        when it should be basing off width - simple fix!!
# transparency for nonRGB images turns white, should turn black (Image.convert)
#TODO
# choose ascii char based on brightness?
# refactor aggressively
# output array is way way longer than it should be, but it works so?????
# could effectively increase output "pixel" density by 2x as many column
#   samples as row samples?

from PIL import Image
from sys import argv
from os import get_terminal_size

def main():
    im_address = argv[1]
    im = Image.open(im_address).convert("RGB")
    old_width = im.size[0]
    old_height = im.size[1]
    max_height = get_terminal_size().lines
    max_width = get_terminal_size().columns // 2
    print("max height ", max_height, "max width ", max_width)
    
    # This needs refactored BAD bad
    if im.size[0] >= im.size[1]:
    #if max_width - old_width <= max_height - old_height: #base new dimensions on width
        print("using width to determine output size")
        max_width = get_terminal_size().columns // 2 # //2 accounts for char width
        new_width = max_width
        while old_width % new_width:
            new_width -= 1
        if new_width <= 1: # No factor for scaling, fit to term instead
            new_width = max_width
        new_height = int(new_width / old_width * old_height)
        pixels_per_char = old_width // new_width # Scale based on new_width
    else: #base new dimensions on height
        print("using height to determine output size")
        max_height = get_terminal_size().lines - 1 # -1 accounts for prompt line
        new_height = max_height
        new_width = max_width
        while old_height % new_height:
            new_height -= 1
        if new_height <= 1: # No factor for scaling, fit to term instead
            new_height = max_height
        new_width = int(new_height / old_height * old_width)
        pixels_per_char = old_width // new_width # Scale based on new_width

    output = []
    for j in range(new_height):
        for i in range(new_width): # one iteration for each char in output
            r_temp, b_temp, g_temp = 0, 0, 0
            denom = pixels_per_char**2
            for k in range(pixels_per_char): # row of subsample
                for l in range(pixels_per_char): # col of subsample
                    if j * pixels_per_char + l < old_height:
                        pix = im.getpixel((i * pixels_per_char + k,
                            j * pixels_per_char+ l))
                        r_temp += pix[0]
                        g_temp += pix[1]
                        b_temp += pix[2]
                    else:
                        denom -= 1
            r = r_temp // pixels_per_char**2
            g = g_temp // pixels_per_char**2
            b = b_temp // pixels_per_char**2
                        
            char = "#" #TODO
            output += f"\033[38;2;{r};{g};{b}m{char}" * 2 + "\033[38;2;255;255;255m"
        output += "\n" # line break at end of each row
    
    print(new_width * new_height)
    print(len(output)) # WHY??? TODO

    for c in output:
        print(c, end="")

if __name__ == "__main__":
    main()
