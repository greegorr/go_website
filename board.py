from PIL import Image, ImageDraw


def draw_board(pos):
    board = []
    r = pos[-361:]
    for i in range(0, 361, 19):
        board.append(list(r[i:i + 19]))
    board = chak(board, (len(pos) // 361) % 2)
    im = Image.open("static/img/board.jpg")
    drawer = ImageDraw.Draw(im)
    color = {
        "1": "#000000",
        "2": "#FFFFFF"
    }
    for y in range(19):
        for x in range(19):
            if board[y][x] != "0":
                drawer.ellipse(((16 + int(x * 10.4), 16 + int(y * 10.4)), (23 + int(x * 10.4), 23 + int(y * 10.4))),
                               color[board[y][x]])
    im.save("static/img/desk.jpg")
    ret = ""
    for y in range(19):
        ret += "".join(board[y])
    return ret


def chak(board, color):
    c_board = [['3' for i in range(21)] for j in range(21)]
    for i in range(19):
        for j in range(19):
            c_board[i + 1][j + 1] = board[i][j]
    black_list = [[True for i in range(21)] for j in range(21)]
    if color == 0:
        for i in range(1, 20):
            for j in range(1, 20):
                if black_list[i][j] and c_board[i][j] == '1':
                    black_list, live = group(black_list, i, j, c_board, color)
                    if not live:
                        c_board = kill(i, j, c_board, color)
    else:
        for i in range(1, 20):
            for j in range(1, 20):
                if black_list[i][j] and c_board[i][j] == '2':
                    black_list, live = group(black_list, i, j, c_board, color)
                    if not live:
                        c_board = kill(i, j, c_board, color)
    for i in range(19):
        for j in range(19):
            board[i][j] = c_board[i + 1][j + 1]

    return board


def group(bl, y, x, a, color):
    c = False
    bl[y][x] = False
    if a[y + 1][x] == "0" or a[y - 1][x] == "0" or a[y][x + 1] == "0" or a[y][x - 1] == "0":
        c = True
    if color == 0:
        if a[y + 1][x] == "1" and bl[y + 1][x]:
            bl, c1 = group(bl, y + 1, x, a, color)
            c = c or c1
        if a[y - 1][x] == "1" and bl[y - 1][x]:
            bl, c1 = group(bl, y - 1, x, a, color)
            c = c or c1
        if a[y][x + 1] == "1" and bl[y][x + 1]:
            bl, c1 = group(bl, y, x + 1, a, color)
            c = c or c1
        if a[y][x - 1] == "1" and bl[y][x - 1]:
            bl, c1 = group(bl, y, x - 1, a, color)
            c = c or c1
    if color == 1:
        if a[y + 1][x] == "2" and bl[y + 1][x]:
            bl, c1 = group(bl, y + 1, x, a, color)
            c = c or c1
        if a[y - 1][x] == "2" and bl[y - 1][x]:
            bl, c1 = group(bl, y - 1, x, a, color)
            c = c or c1
        if a[y][x + 1] == "2" and bl[y][x + 1]:
            bl, c1 = group(bl, y, x + 1, a, color)
            c = c or c1
        if a[y][x - 1] == "2" and bl[y][x - 1]:
            bl, c1 = group(bl, y, x - 1, a, color)
            c = c or c1
    return bl, c


def kill(y, x, a, color):
    if y == 10 and x == 10:
        print(*a, sep='\n')
    a[y][x] = "0"
    if y == 10 and x == 10:
        print(*a, sep='\n')
    if color == 0:
        if a[y + 1][x] == "1":
            a = kill(y + 1, x, a, color)
        if a[y - 1][x] == "1":
            a = kill(y - 1, x, a, color)
        if a[y][x + 1] == "1":
            a = kill(y, x + 1, a, color)
        if a[y][x - 1] == "1":
            a = kill(y, x - 1, a, color)
    if color == 1:
        if a[y + 1][x] == "2":
            a = kill(y + 1, x, a, color)
        if a[y - 1][x] == "2":
            a = kill(y - 1, x, a, color)
        if a[y][x + 1] == "2":
            a = kill(y, x + 1, a, color)
        if a[y][x - 1] == "2":
            a = kill(y, x - 1, a, color)
    return a


def move(s, pos):
    d = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "j": 8, "k": 9, "l": 10, "m": 11, "n": 12,
         "o": 13, "p": 14, "q": 15, "r": 16, "s": 17, "t": 18}
    st = list(pos[-361:])
    if s == "pass":
        return pos + pos[-361:]
    elif (len(s) != 2 and len(s) != 3) or st[d[s[0]] + (18 - (int(s[1:]) - 1)) * 19] != '0':
        return pos
    elif s[0] in "abcdefghjklmnopqrst" and s[1:].isdigit():
        if s[1] != 0:
            if len(pos) // 361 % 2 == 1:
                st[d[s[0]] + (18 - (int(s[1:]) - 1)) * 19] = "1"
            else:
                st[d[s[0]] + (18 - (int(s[1:]) - 1)) * 19] = "2"
            st = "".join(st)
            return pos + st


if __name__ == '__main__':
    # draw_board("1" * 180 + "0" + "1" * 180 + "1" * 180 + "2" + "1" * 180)
    # draw_board("2" * 180 + "1" + "2" * 180)

    pos = "0" * 361
    print(pos)
    print(move("g4", pos))
    draw_board(pos)
    for i in range(10):
        pos = move(input(), pos)
        draw_board(pos)
        # for j in range(38+i*19):
        #     print(pos[j*19:(j+1)*19])
