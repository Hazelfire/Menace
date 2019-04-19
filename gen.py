import json
from PIL import Image, ImageDraw


def reflect_board(board):
    return list(reversed(board))


def same_board(a, b):
    for i in range(3):
        for j in range(3):
            if a[i][j] != b[i][j]:
                return False
    return True


def rotate_board(a):
    new_board = []

    for i in range(3):
        new_row = []
        for j in range(3):
            new_row.append(a[2 - j][i])
        new_board.append(new_row)
    return new_board


def copy_board(board):
    return [row[:] for row in board]


def rotated_same_board(a, b):
    current_board = a
    for i in range(4):
        if same_board(current_board, b):
            return True
        current_board = rotate_board(current_board)
    return False


def symmetry_same_board(a, b):
    if rotated_same_board(a, b):
        return True
    reflected = reflect_board(a)
    if rotated_same_board(reflected, b):
        return True
    return False


def board_in_set(target, boards):
    for board in boards:
        if symmetry_same_board(target, board):
            return True
    return False


def row_wins(row, player):
    for cell in row:
        if row != player:
            return False
    return True


def wins_horizontally(board, player):
    for row in board:
        if row_wins(row, player):
            return True
    return False


def wins_vertically(board, player):
    rotated = rotate_board(board)
    return wins_horizontally(rotated, player)


def wins_major_diag(board, player):
    for i in range(3):
        if board[i][i] != player:
            return False
    return True


def wins_diagonally(board, player):
    return wins_major_diag(board, player) or wins_major_diag(rotate_board(board), player)


def wins_for(board, player):
    return wins_diagonally(board, player) or wins_vertically(board, player) or wins_horizontally(board, player)


def same_x_as_o(board):
    x_count = 0
    o_count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                x_count += 1
            if board[i][j] == 'O':
                o_count += 1
    return x_count == o_count


def gen_board(seed):
    possibilities = ["X", "O", " "]
    current_seed = int(seed)
    board = []
    for i in range(3):
        row = []
        for j in range(3):
            row.append(possibilities[current_seed % 3])
            current_seed = current_seed // 3
        board.append(row)
    return board


def x_o_count(board):
    count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == "X" or board[i][j] == "O":
                count += 1
    return count


def gen_route_tables(target, boards):
    blanks = []
    for i in range(3):
        for j in range(3):
            if target[i][j] == " ":
                blanks.append((j, i))

    route_tables = []
    new_board = copy_board(target)
    for i in range(len(blanks)):
        for j in range(len(blanks)):
            if i != j:
                x1, y1 = blanks[i]
                new_board[y1][x1] = "X"

                x2, y2 = blanks[j]
                new_board[y2][x2] = "O"

                board_index = 0
                for board in boards:
                    if symmetry_same_board(board, new_board):
                        route_tables.append({
                            "choices": (blanks[i], blanks[j]),
                            "index": board_index
                        })
                        break
                    board_index += 1
                new_board = copy_board(target)
    return route_tables


def draw_x(draw, position, size):
    start_x = position[0]
    start_y = position[1]
    end_x = position[0] + size
    end_y = position[1] + size

    draw.line((start_x, start_y, end_x, end_y), width=5, fill="black")

    start_x = position[0] + size
    start_y = position[1]
    end_x = position[0]
    end_y = position[1] + size

    draw.line((start_x, start_y, end_x, end_y), width=5, fill="black")


def draw_o(draw, position, size):
    start_x = position[0]
    start_y = position[1]
    end_x = position[0] + size
    end_y = position[1] + size

    draw.ellipse((start_x, start_y, end_x, end_y), width=5, outline="black")


def draw_plays(draw, board, start_offset, size):
    spacing = 10
    cell_size = size / 3
    line_size = cell_size - spacing * 2
    for i in range(3):
        for j in range(3):
            if board[j][i] == "X":
                start_x = (cell_size - line_size) / 2 + \
                    i * cell_size + start_offset
                start_y = (cell_size - line_size) / 2 + \
                    j * cell_size + start_offset
                draw_x(draw, (start_x, start_y), line_size)

            if board[j][i] == "O":
                start_x = (cell_size - line_size) / 2 + \
                    i * cell_size + start_offset
                start_y = (cell_size - line_size) / 2 + \
                    j * cell_size + start_offset

                draw_o(draw, (start_x, start_y), line_size)


def draw_grid(draw, start_offset, size):
    width = 5
    draw.line((start_offset[0], start_offset[1] + size / 3,
               start_offset[0] + size, start_offset[1] + size / 3), width=width, fill="black")

    draw.line((start_offset[0], start_offset[1] + 2 * size / 3,
               start_offset[0] + size, start_offset[1] + 2 * size / 3), width=width, fill="black")

    draw.line((start_offset[0] + size / 3, start_offset[1],
               start_offset[0] + size / 3, start_offset[1] + size), width=width, fill="black")

    draw.line((start_offset[0] + 2 * size / 3, start_offset[1],
               start_offset[0] + 2 * size / 3, start_offset[1] + size), width=width, fill="black")


def draw_guide(draw, board, routes, start_offset, size):
    draw_grid(draw, (start_offset, start_offset), size)
    draw_plays(draw, board, start_offset, size)
    draw_routes(draw, routes, board, start_offset, size)


COLORS = {
    (0, 0): "yellow",
    (1, 0): "lime",
    (2, 0): "black",
    (0, 1): "maroon",
    (1, 1): "pink",
    (2, 1): "orange",
    (0, 2): "green",
    (1, 2): "blue",
    (2, 2): "grey"
}


def draw_routes(draw, routes, board, start_offset, size):
    spacing = 10

    width = (size - spacing * 8) / 3
    internal_cell_size = width / 3
    cell_size = size / 3
    y = 0
    for row in board:
        x = 0
        for cell in row:
            if cell == " ":
                draw_grid(draw, (cell_size * x + spacing + start_offset,
                                 cell_size * y + spacing + start_offset), width)
            x += 1
        y += 1

    for i in range(len(routes)):
        route = routes[i]
        choices = route["choices"]
        my_choice = choices[0]
        their_choice = choices[1]
        cell_x = cell_size * my_choice[0] + spacing + start_offset
        cell_y = cell_size * my_choice[1] + spacing + start_offset
        internal_cell_x = cell_x + internal_cell_size * \
            their_choice[0] + 7
        internal_cell_y = cell_y + internal_cell_size * \
            their_choice[1] + internal_cell_size / 2
        draw.text((internal_cell_x, internal_cell_y),
                  str(route["index"]), align="center", fill="black")


def create_board(board, routes):
    im = Image.new("RGB", (450, 450), color="white")
    draw = ImageDraw.Draw(im)
    draw_guide(draw, board, routes, 25, 400)
    return im


def main():
    boards = []

    for i in range(int(3 ** 9)):
        board = gen_board(i)
        if same_x_as_o(board):
            if not wins_for(board, "X") and not wins_for(board, "Y"):
                if not board_in_set(board, boards):
                    print(board)
                    boards.append(board)
    boards.sort(key=x_o_count)

    routes = []
    for board in boards:
        route_tables = gen_route_tables(board, boards)
        routes.append(route_tables)

    i = 0
    for board, route in zip(boards, routes):
        im = create_board(board, route)
        im.save("images/{}.png".format(i))
        i += 1
        print(i)


if __name__ == "__main__":
    main()
