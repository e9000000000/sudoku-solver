import copy


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


def minimal_split(field: GameField) -> list[GameField]:
    min_x = 0
    min_y = 0
    min_len = 9999
    for y in range(len(field)):
        for x in range(len(field[y])):
            numbers = get_awailable_numbers(field, x, y)
            if len(numbers) < min_len and len(numbers) > 1:
                min_x = x
                min_y = y
                min_len = len(numbers)

    variants = []
    for cell_variant in get_awailable_numbers(field, min_x, min_y):
        field_variant = copy.deepcopy(field)
        field_variant[min_y][min_x] = str(cell_variant)
        variants.append(field_variant)
    return variants


def solve(field: GameField, depth=0):
    if depth > 6:
        return

    cell_amount = len(field) * len(field[0])

    while 1:
        count_before = count_numbers(field)
        solve_step(field)
        count_after = count_numbers(field)

        if count_after == cell_amount:
            break

        if count_before == count_after:
            variants = minimal_split(field)
            for variant in variants:
                solve(variant, depth=depth+1)
                if count_numbers(variant) == cell_amount:
                    # write success variant into our game field
                    for i in range(len(field)):
                        field[i] = variant[i]
                    return
            break

