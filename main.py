import time
import os
import copy

import pytesseract
import pyautogui


from core import solve, GameField

GCOL = "\033[92m"  # gray
DCOL = "\033[39m"  # default


def print_game_field(field: GameField):
	for ys in ((0, 1, 2), (3, 4, 5), (6, 7, 8)):
		for y in ys:
			for xs in ((0, 1, 2), (3, 4, 5), (6, 7, 8)):
				for x in xs:
					print(f"{GCOL}[{DCOL}{field[y][x]}{GCOL}]{DCOL}", end="")
				print(" ", end="")
			print()
		print()


time.sleep(1.5)

image_region = list(map(int, os.popen('slop').read().replace('x', '+').strip().split('+')))
numpad_region = list(map(int, os.popen('slop').read().replace('x', '+').strip().split('+')))
field_w, field_h, field_x, field_y = tuple(image_region)
numpad_w, numpad_h, numpad_x, numpad_y = tuple(numpad_region)

image = pyautogui.screenshot()
image = image.crop((field_x, field_y, field_x+field_w, field_y+field_h))

left, right, top, bottom = 0, image.size[0], 0, image.size[1]
for x in range(image.size[0]):
	px = image.getpixel((x, image.size[1] // 2))
	if px != image.getpixel((0, image.size[1] // 2)):
		break
	left += 1

for x in reversed(range(image.size[0])):
	px = image.getpixel((x, image.size[1] // 2))
	if px != image.getpixel((image.size[0] - 1, image.size[1] // 2)):
		break
	right -= 1

for y in range(image.size[1]):
	px = image.getpixel((image.size[0] // 2, y))
	if px != image.getpixel((image.size[0] // 2, 0)):
		break
	top += 1

for y in reversed(range(image.size[1])):
	px = image.getpixel((image.size[0] // 2, y))
	if px != image.getpixel((image.size[0] // 2, image.size[1] - 1)):
		break
	bottom -= 1

image = image.crop((left, top, right, bottom))

game_field = [[0 for _ in range(9)] for _ in range(9)]

region_width = image.size[0] // 9
region_height = image.size[1] // 9
for rix in range(9):
	for riy in range(9):
		x = rix * region_width
		y = riy * region_height
		current_image = image.crop((x+5, y+5, x+region_width-5, y+region_height-5))
		text = pytesseract.image_to_string(current_image, config='--psm 6').strip()
		if text:
			game_field[riy][rix] = int(text)

initial_game_field = copy.deepcopy(game_field)
print(f"{GCOL}PARSED:{DCOL}")
print_game_field(game_field)
print()

solve(game_field)

print(f"{GCOL}SOLVED:{DCOL}")
print_game_field(game_field)

for y in range(len(game_field)):
    for x in range(len(game_field[y])):
        if initial_game_field[y][x]:
            continue

        pyautogui.click(
            field_x + left + image.size[0] / 9 * x + image.size[0] / 9 / 2,
            field_y + top + image.size[1] / 9 * y + image.size[1] / 9 / 2,
        )
        time.sleep(0.01)
        num = int(game_field[y][x])
        num_x = [0, 1, 2, 0, 1, 2, 0, 1, 2][num - 1]
        num_y = [0, 0, 0, 1, 1, 1, 2, 2, 2][num - 1]
        pyautogui.click(
            numpad_x + numpad_w / 3 * num_x + numpad_w / 3 / 2,
            numpad_y + numpad_h / 3 * num_y + numpad_h / 3 / 2,
        )
        time.sleep(0.01)
