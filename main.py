import time
import os
from pprint import pp

import pytesseract
import pyautogui
from PIL import Image


from core import solve


# time.sleep(1.5)

# slop_region = list(map(int, os.popen('slop').read().replace('x', '+').strip().split('+')))
# width, height, x, y = tuple(slop_region)

# image = pyautogui.screenshot()
# image = image.crop((x, y, x+width, y+height))

image = Image.open('image.png')

left, width, top, height = 0, image.size[0], 0, image.size[1]
for x in range(image.size[0]):
	px = image.getpixel((x, image.size[1] // 2))
	if sum(px) < 250:
		break
	left += 1

for x in reversed(range(image.size[0])):
	px = image.getpixel((x, image.size[1] // 2))
	if sum(px) < 250:
		break
	width -= 1

for y in range(image.size[1]):
	px = image.getpixel((image.size[0] // 2, y))
	if sum(px) < 250:
		break
	top += 1

for y in reversed(range(image.size[1])):
	px = image.getpixel((image.size[0] // 2, y))
	if sum(px) < 250:
		break
	height -= 1

image = image.crop((left, top, width, height))

game_field = [[' ' for _ in range(9)] for _ in range(9)]

region_width = image.size[0] // 9
region_height = image.size[1] // 9
for rix in range(9):
	for riy in range(9):
		x = rix * region_width
		y = riy * region_height
		current_image = image.crop((x+5, y+5, x+region_width-5, y+region_height-5))
		# current_image.save(f"{rix}_{riy}.png")
		text = pytesseract.image_to_string(current_image, config='--psm 6').strip()
		if text:
			game_field[riy][rix] = text



print("-"*18, "NOT SOLVED", "-"*18)
pp(game_field)
print()

solve(game_field)

print("-"*20, "SOLVED", "-"*20)
pp(game_field)

