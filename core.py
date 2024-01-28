from functools import reduce


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


def get_all_dependencies(all_awailable_numbers: list[list[set]], main_x: int, main_y: int) -> set[tuple[int]]:
    main_numbers = all_awailable_numbers[main_y][main_x]
    result = set()

    for x in range(len(all_awailable_numbers[0])):
        numbers = all_awailable_numbers[main_y][x]
        if len(numbers) > 1 and len(numbers & main_numbers) > 0:
            result.add((x, main_y))

    for y in range(len(all_awailable_numbers)):
        numbers = all_awailable_numbers[y][main_x]
        if len(numbers) > 1 and len(numbers & main_numbers) > 0:
            result.add((main_x, y))

    for y in range(main_y // 3 * 3, main_y // 3 * 3 + 3):
        for x in range(main_x // 3 * 3, main_x // 3 * 3 + 3):
            numbers = all_awailable_numbers[y][x]
            if len(numbers) > 1 and len(numbers & main_numbers) > 0:
                result.add((x, y))
    return result


def remove_numbers_with_xy_wing(all_awailable_numbers: list[list[set[int]]]):
    all_dependencies = {}
    
    for y in range(len(all_awailable_numbers)):
        for x in range(len(all_awailable_numbers[y])):
            if len(all_awailable_numbers[y][x]) == 1:
                continue
            all_dependencies[(x, y)] = get_all_dependencies(all_awailable_numbers, x, y)

    for main_cell, main_cell_deps in all_dependencies.items():
        reversed_deps: dict[tuple, set[tuple[int]]] = {}
        for dep_cell in main_cell_deps:
            deps_of_dep = {d for d in all_dependencies[dep_cell] if d not in  [main_cell, *main_cell_deps]}
            for dep in deps_of_dep:
                if dep not in reversed_deps:
                    reversed_deps[dep] = set()
                reversed_deps[dep].add(dep_cell)

        for fork_cell, rev_deps in reversed_deps.items():
            main_x, main_y = main_cell[0], main_cell[1]

            fork_cell_numbers = all_awailable_numbers[fork_cell[1]][fork_cell[0]]
            if len(fork_cell_numbers) != 2:
                continue

            all_rev_deps_numbers = [all_awailable_numbers[c[1]][c[0]] for c in rev_deps]
            all_companions = {}
            for numbers in all_rev_deps_numbers:
                if len(numbers) != 2:
                    continue
                for number in numbers:
                    if number not in all_companions:
                        all_companions[number] = set()
                    all_companions[number].add(sum(numbers.difference({number})))
                            
            for number, companions in all_companions.items():
                if len(companions & fork_cell_numbers) >= 2 and number in all_awailable_numbers[main_y][main_x]:
                    all_awailable_numbers[main_y][main_x].remove(number)


def solve_step(field: GameField):
    awailable_numbers = [[get_awailable_numbers(field, x, y) for x in range(len(field[y]))] for y in range(len(field))]


    remove_numbers_with_xy_wing(awailable_numbers)

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
