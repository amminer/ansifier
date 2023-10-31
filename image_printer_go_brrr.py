# Known bugs:
# at large terminal sizes (very zoomed out) image takes on diamond-shaped
#   rgb artifacting?
# at extreme terminal aspect ratios similar artifacting occurs as the image is
#   very slightly stretched along the long axis of the terminal window...
# lame and obfuscated behind PIL as these bugs are, this is kinda better than
#   the earlier version.
# transparency for nonRGB images turns white, should turn black (Image.convert)
# TODO
# Re-write with classes, then tackle old bugs if they still exist:
# choose ascii char based on brightness?
# output array is way way longer than it should be, but it works so?????
# could effectively increase output "pixel" density by 2x as many column
#   samples as row samples?

from PIL import Image
from sys import argv, exit
from os import get_terminal_size


class outputChar:  # Not yet in use
    def __init__(self, r, g, b, maxBrightness) -> None:
        self.possibleChars = ["'", '"', "*", "!", "?", "%", "#"]
        self.char = self.getChar(r, g, b, maxBrightness)
        self.printString = (
            f"\033[38;2;{r};{g};{b}m{self.char}" * 2 + "\033[38;2;255;255;255m"
        )

    def getChar(self, r, g, b, maxBrightness):
        brightness = r + g + b  # out of 765...
        interval = (
            maxBrightness * 0.8 / len(self.possibleChars)
        )  # 0.8 to fill out upper bound more
        bLevel = 0
        ret = "_"
        for charIndex in range(len(self.possibleChars)):
            if brightness >= bLevel:
                ret = self.possibleChars[charIndex]
            bLevel += interval
        return ret

    def __str__(self) -> str:
        return self.printString


class output:  # Not yet in use
    def __init__(self, image, max_w, max_h) -> None:
        self.chars = []
        self.max_width = max_w
        self.max_height = max_h
        self.resize_method = Image.LANCZOS
        self.image = self.resizeToTerminal(image, max_w, max_h)

        self.generateChars(self.getMaxBrightness())

    def resizeToTerminal(self, im, w, h):
        problem_dim = min(w, h)
        im.thumbnail((problem_dim-1, problem_dim-1), self.resize_method)
        if im.size[0] <= self.max_width and im.size[1] <= self.max_height:
            return im
        else:
            return self.resizeToTerminal(im, w, h)

    def generateChars(self, maxBrightness):
        for j in range(self.image.size[1]):
            for i in range(self.image.size[0]):  # one iteration for each char in output
                pix = self.image.getpixel((i, j))
                self.chars.append(outputChar(pix[0], pix[1], pix[2], maxBrightness))
            self.chars.append("\n")  # line break at end of each row

    def getMaxBrightness(self):
        maxBrightness = 0
        for j in range(self.image.size[1]):
            for i in range(self.image.size[0]):
                pix = self.image.getpixel((i, j))
                brightness = pix[0] + pix[1] + pix[2]  # out of 765...
                if brightness > maxBrightness:
                    maxBrightness = brightness
        return maxBrightness

    def __str__(self):
        return ''.join([str(e) for e in self.chars])


def main():
    max_width = get_terminal_size().columns // 2  # //2 accounts for char width
    max_height = get_terminal_size().lines - 1  # -1 accounts for prompt line
    img_path = argv[1]
    image_file = Image.open(img_path).convert("RGB")
    toPrint = output(image_file, max_width, max_height)
    print(toPrint)
    image_file.close()


"""
def main():
    resize_method = Image.LANCZOS
    max_height = get_terminal_size().lines - 1  # -1 accounts for prompt line
    max_width = get_terminal_size().columns // 2  # //2 accounts for char width
    new_height, new_width = max_height, max_width
    img_path = argv[1]
    im = Image.open(img_path).convert("RGB")
    # reduce contrast for char selection effect?
    problem_dim = max(new_width, new_height)
    im.thumbnail((problem_dim, problem_dim), resize_method)
    while im.size[0] > max_width or im.size[1] > max_height:  # img sz > terminal
        problem_dim = max(new_width, new_height)
        im.thumbnail((problem_dim, problem_dim), resize_method)
        new_height -= 1
        new_width -= 1

    output = []
    for j in range(im.size[1]):
        for i in range(im.size[0]):  # one iteration for each char in output
            pix = im.getpixel((i, j))
            r = pix[0]
            g = pix[1]
            b = pix[2]
            brightness = r + g + b

            char = "#"  # TODO
            output += f"\033[38;2;{r};{g};{b}m{char}" * 2 + "\033[38;2;255;255;255m"
        output += "\n"  # line break at end of each row

    # print(new_width * new_height)
    # print(len(output)) # WHY??? TODO

    for c in output:
        print(c, end="")
"""


if __name__ == "__main__":
    main()
