import core


def test_solve_simple_one():
	field = [
		[0, 0, 0, 1, 0, 0, 0, 5, 0],
		[0, 7, 1, 9, 0, 2, 0, 0, 0],
		[3, 6, 0, 0, 0, 4, 0, 0, 2],
		[0, 1, 4, 8, 3, 0, 2, 6, 5],
		[0, 3, 0, 6, 7, 0, 0, 9, 0],
		[6, 8, 9, 2, 4, 0, 1, 0, 7],
		[1, 9, 0, 0, 0, 0, 5, 4, 0],
		[0, 0, 3, 0, 0, 6, 0, 0, 0],
		[0, 0, 0, 4, 0, 0, 3, 0, 1],
	]
	expected = [
		[9, 2, 8, 1, 6, 3, 7, 5, 4],
		[4, 7, 1, 9, 5, 2, 6, 8, 3],
		[3, 6, 5, 7, 8, 4, 9, 1, 2],
		[7, 1, 4, 8, 3, 9, 2, 6, 5],
		[5, 3, 2, 6, 7, 1, 4, 9, 8],
		[6, 8, 9, 2, 4, 5, 1, 3, 7],
		[1, 9, 7, 3, 2, 8, 5, 4, 6],
		[2, 4, 3, 5, 1, 6, 8, 7, 9],
		[8, 5, 6, 4, 9, 7, 3, 2, 1],
	]
	core.solve(field)
	assert field == expected


def test_solve_master_one():
    field = [
        [0, 8, 0, 2, 0, 0, 0, 1, 0],
        [0, 6, 0, 0, 0, 3, 0, 0, 0],
        [3, 0, 1, 0, 7, 0, 9, 0, 0],
        [4, 0, 2, 0, 0, 8, 0, 9, 0],
        [0, 0, 0, 5, 0, 0, 7, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0],
        [9, 0, 3, 0, 0, 4, 0, 2, 0],
        [0, 0, 0, 0, 8, 0, 0, 0, 4],
        [6, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    expected = [
        [7, 8, 4, 2, 9, 5, 3, 1, 6],
        [2, 6, 9, 8, 1, 3, 4, 5, 7],
        [3, 5, 1, 4, 7, 6, 9, 8, 2],
        [4, 3, 2, 7, 6, 8, 1, 9, 5],
        [8, 9, 6, 5, 2, 1, 7, 4, 3],
        [5, 1, 7, 3, 4, 9, 2, 6, 8],
        [9, 7, 3, 6, 5, 4, 8, 2, 1],
        [1, 2, 5, 9, 8, 7, 6, 3, 4],
        [6, 4, 8, 1, 3, 2, 5, 7, 9],
    ]
    core.solve(field)
    assert field == expected
