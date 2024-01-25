GameField = list[list[str]]


def count_numbers(field: GameField) -> int:
	result = 0
	for row in field:
		for s in row:
			if s and s != ' ':
				result += 1
	return result


def awailable_number(not_awailable_numbers: set[int]) -> int:
	for i in range(1, 10):
		if i not in not_awailable_numbers:
			return i


def solve_step(field: GameField):
	for main_y in range(len(field)):
		for main_x in range(len(field[0])):
			if field[main_y][main_x].isdigit():
				continue

			not_awailable_numbers = set()

			for x in range(len(field[0])):
				symbol = field[main_y][x]
				if symbol.isdigit():
					not_awailable_numbers.add(int(symbol))

			for y in range(len(field)):
				symbol = field[y][main_x]
				if symbol.isdigit():
					not_awailable_numbers.add(int(symbol))

			for y in range(main_y // 3 * 3, main_y // 3 * 3 + 3):
				for x in range(main_x // 3 * 3, main_x // 3 * 3 + 3):
					symbol = field[y][main_x]
					if symbol.isdigit():
						not_awailable_numbers.add(int(symbol))

			if len(not_awailable_numbers) == 8:
				field[main_y][main_x] = str(awailable_number(not_awailable_numbers))



def solve(field: GameField) -> GameField:
	while 1:
		count_before = count_numbers(field)
		solve_step(field)
		count_after = count_numbers(field)

		if count_before == count_after:
			break



