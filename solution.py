
assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows,cols)
row_units = [cross(r,cols) for r in rows]
cols_units = [cross(rows,c) for c in cols]
square_units = [cross(r,c) for r in ('ABC','DEF','GHI') for c in ('123','456','789')]
# New for Diagonal sudoku
diag_units = [[rows[i] + cols[i] for i in range(9)],[rows[8-i] + cols[i] for i in range(9)]]
unit_list = row_units + cols_units + square_units + diag_units
units =  dict((b, [u for u in unit_list if b in u]) for b in boxes)
peers =  dict((b, set(sum(units[b],[]))-set([b])) for b in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    assert len(values) == 81

    #Re compute based on new information found i.e. naked twins & elimination basically this matches solution 2 in the unittest
    rerun = True
    while rerun:
        rerun = False
        # Evalurate each unit
        for unit in unit_list:
            naked_twins_dict = {}
            # Find all instances of naked twins
            for box in unit:
                if len(values[box]) == 2:
                    naked_twins_dict[values[box]] = naked_twins_dict.get(values[box], 0) + 1
            # Eliminate the naked twins as possibilities for their peers
            for twin in naked_twins_dict.keys():
                if naked_twins_dict[twin] == 2:
                    for box in unit:
                        # Ignore self & values of 1
                        if (values[box] != twin) and (len(values[box]) >= 2):
                            #Only rerun if something changed
                            if(values[box] != values[box].replace(twin[0], '')) or (values[box] != values[box].replace(twin[1], '')):
                                rerun = True
                            #Change the values
                            assign_value(values, box, values[box].replace(twin[0], ''))
                            assign_value(values, box, values[box].replace(twin[1], ''))

    return values

# Test for hidden twins
# values_hidden_twin = {'A1': '56', 'A2': '4', 'A3': '9', 'A4': '1', 'A5': '3', 'A6': '2', 'A7': '67', 'A8': '578',
#                       'A9': '678', 'B1': '56', 'B2': '8', 'B3': '1', 'B4': '4', 'B5': '7', 'B6': '9', 'B7': '236',
#                       'B8': '235', 'B9': '26', 'C1': '3', 'C2': '2', 'C3': '7', 'C4': '6', 'C5': '8',
#                       'C6': '5', 'C7': '9', 'C8': '1', 'C9': '4', 'D1': '24', 'D2': '9', 'D3': '6',
#                       'D4': '37', 'D5': '5', 'D6': '1', 'D7': '8', 'D8': '2347', 'D9': '27', 'E1': '14',
#                       'E2': '7', 'E3': '5', 'E4': '39', 'E5': '2', 'E6': '8', 'E7': '1346', 'E8': '349', 'E9': '169',
#                       'F1': '12', 'F2': '3', 'F3': '8', 'F4': '79', 'F5': '4', 'F6': '6', 'F7': '127',
#                       'F8': '279', 'F9': '5', 'G1': '8', 'G2': '5', 'G3': '2', 'G4': '2', 'G5': '6',
#                       'G6': '7', 'G7': '14', 'G8': '49', 'G9': '19', 'H1': '7', 'H2': '1', 'H3': '2', 'H4': '8',
#                       'H5': '9', 'H6': '4', 'H7': '5', 'H8': '6', 'H9': '3', 'I1': '9', 'I2': '6', 'I3': '4',
#                       'I4': '5', 'I5': '1', 'I6': '3', 'I7': '27', 'I8': '278', 'I9': '278'}
#
# possible_after = {'A1': '56', 'A2': '4', 'A3': '9', 'A4': '1', 'A5': '3', 'A6': '2', 'A7': '67', 'A8': '578',
#                   'A9': '678', 'B1': '56', 'B2': '8', 'B3': '1', 'B4': '4', 'B5': '7', 'B6': '9', 'B7': '236',
#                   'B8': '235', 'B9': '26', 'C1': '3', 'C2': '2', 'C3': '7', 'C4': '6', 'C5': '8',
#                   'C6': '5', 'C7': '9', 'C8': '1', 'C9': '4', 'D1': '24', 'D2': '9', 'D3': '6',
#                   'D4': '37', 'D5': '5', 'D6': '1', 'D7': '8', 'D8': '2347', 'D9': '27', 'E1': '14',
#                   'E2': '7', 'E3': '5', 'E4': '39', 'E5': '2', 'E6': '8', 'E7': '1346', 'E8': '349', 'E9': '19',
#                   'F1': '12', 'F2': '3', 'F3': '8', 'F4': '79', 'F5': '4', 'F6': '6', 'F7': '127',
#                   'F8': '279', 'F9': '5', 'G1': '8', 'G2': '5', 'G3': '2', 'G4': '2', 'G5': '6',
#                   'G6': '7', 'G7': '14', 'G8': '49', 'G9': '19', 'H1': '7', 'H2': '1', 'H3': '2', 'H4': '8',
#                   'H5': '9', 'H6': '4', 'H7': '5', 'H8': '6', 'H9': '3', 'I1': '9', 'I2': '6', 'I3': '4',
#                   'I4': '5', 'I5': '1', 'I6': '3', 'I7': '27', 'I8': '278', 'I9': '278'}


def hidden_twin(values):
    """Eliminate values using the hidden twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    assert len(values) == 81

    for unit in unit_list:
        dict_digit_keys = {}
        for digit in '123456789':
            box_list = [box for box in unit if digit in values[box]]
            #unsolved boxes
            if len(box_list) > 1:
                dict_digit_keys[digit] = box_list
        # check if there are any twins
        for key1 in dict_digit_keys.keys():
            for key2 in dict_digit_keys.keys():
                # key1 < key2 key check so that ordering is maintained e.g. 19 instead of 91
                # key1 != key2 skip if key is the same.
                # dict_digit_keys.get(key1) == dict_digit_keys.get(key2) --> occur in the same boxes
                if key1 < key2 and key1 != key2 and dict_digit_keys.get(key1) == dict_digit_keys.get(key2) and len(dict_digit_keys.get(key1)) == 2:
                    # We found a hidden twin Change the values
                    assign_value(values, dict_digit_keys.get(key1)[0], key1+key2)
                    assign_value(values, dict_digit_keys.get(key1)[1], key1+key2)
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    assert len(values) == 81
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        for peer in peers[box]:
            #values[peer] = values[peer].replace(values[box],'')
            assign_value(values, peer, values[peer].replace(values[box],''))

    return values

def only_choice(values):
    assert len(values) == 81
    for unit in unit_list:
        #box_list = []
        for digit in '123456789':
            box_list = [box for box in unit if digit in values[box]]
            if len(box_list) == 1:
                #values[box_list[0]] = digit
                assign_value(values, box_list[0], digit)
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after

        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values

def search(values):

    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[box])== 1 for box in boxes):
        return values
    value,box = min((len(values[box]),box)for box in boxes if len(values[box]) > 1)

    for digit in values[box]:
        new_sudoku = values.copy()
        #new_sudoku[box] = digit
        assign_value(new_sudoku, box, digit)
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
