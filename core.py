GameField = list[list[str]]


def count_numbers(field: GameField) -> int:
	result = 0
	for row in field:
		for s in row:
			if s and s != ' ':
				result += 1
	return result


def get_awailable_numbers(field: GameField, main_x: int, main_y: int) -> set[int]:
	if field[main_y][main_x].isdigit():
		return {int(field[main_y][main_x])}

	result = set(range(1, 10))

	for x in range(len(field[0])):
		symbol = field[main_y][x]
		if symbol.isdigit() and int(symbol) in result:
			result.remove(int(symbol))

	for y in range(len(field)):
		symbol = field[y][main_x]
		if symbol.isdigit() and int(symbol) in result:
			result.remove(int(symbol))

	for y in range(main_y // 3 * 3, main_y // 3 * 3 + 3):
		for x in range(main_x // 3 * 3, main_x // 3 * 3 + 3):
			symbol = field[y][x]
			if symbol.isdigit() and int(symbol) in result:
				result.remove(int(symbol))

	return result


def solve_step(field: GameField):
	awailable_numbers = [[get_awailable_numbers(field, x, y) for x in range(len(field[y]))] for y in range(len(field))]

	for main_y in range(len(field)):
		for main_x in range(len(field[main_y])):
			current_awailable_numbers = awailable_numbers[main_y][main_x]

			if field[main_y][main_x].isdigit():
				continue

			if len(current_awailable_numbers) == 1 and not field[main_y][main_x].isdigit():
				field[main_y][main_x] = str(sum(current_awailable_numbers))
				return

			for number in current_awailable_numbers:
				finded_count = 0
				for search_numbers in awailable_numbers[main_y]:
					if number in search_numbers:
						finded_count += 1
				if finded_count < 2:
					field[main_y][main_x] = str(number)
					return

			for number in current_awailable_numbers:
				finded_count = 0
				for y in range(len(awailable_numbers)):
					search_numbers = awailable_numbers[y][main_x]
					if number in search_numbers:
						finded_count += 1
				if finded_count < 2:
					field[main_y][main_x] = str(number)
					return

			for number in current_awailable_numbers:
				finded_count = 0
				for y in range(main_y // 3 * 3, main_y // 3 * 3 + 3):
					for x in range(main_x // 3 * 3, main_x // 3 * 3 + 3):
						search_numbers = awailable_numbers[y][x]
						if number in search_numbers:
							finded_count += 1
				if finded_count < 2:
					field[main_y][main_x] = str(number)
					return


def solve(field: GameField):
	while 1:
		count_before = count_numbers(field)
		solve_step(field)
		count_after = count_numbers(field)

		if count_before == count_after:
			break


