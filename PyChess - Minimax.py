
# PyChess by Lalith Roopesh
# Last updated: 1.8.2018

# TODO
# Fix checkmate detection
# Castling
# AI

board = [
    'BR','BN','BB','BQ','BK','BB','BN','BR',
    'BP','BP','BP','BP','BP','BP','BP','BP',
    'XX','XX','XX','XX','XX','XX','XX','XX',
    'XX','XX','XX','XX','XX','XX','XX','XX',
    'XX','XX','XX','XX','XX','XX','XX','XX',
    'XX','XX','XX','XX','XX','XX','XX','XX',
    'WP','WP','WP','WP','WP','WP','WP','WP',
    'WR','WN','WB','WQ','WK','WB','WN','WR'
    ]

rawpV = [ 0,  0,  0,  0,  0,  0,  0,  0,
       50, 50, 50, 50, 50, 50, 50, 50,
       10, 10, 20, 30, 30, 20, 10, 10,
       5,  5, 10, 25, 25, 10,  5,  5,
       0,  0,  0, 30, 30,  0,  0,  0,
       5, -5,  5,  0,  0,  5, -5,  5,
       5, 10, 10,-20,-20, 10, 10,  5,
       0,  0,  0,  0,  0,  0,  0,  0]
rawnV = [-50,-40,-30,-30,-30,-30,-40,-50,
      -40,-20,  0,  0,  0,  0,-20,-40,
      -30,  0, 10, 15, 15, 10,  0,-30,
      -30,  5, 15, 20, 20, 15,  5,-30,
      -30,  0, 15, 20, 20, 15,  0,-30,
      -30,  5, 10, 15, 15, 10,  5,-30,
      -40,-20,  0,  5,  5,  0,-20,-40,
      -50,-40,-30,-30,-30,-30,-40,-50]
rawbV = [-20,-10,-10,-10,-10,-10,-10,-20,
      -10,  0,  0,  0,  0,  0,  0,-10,
      -10,  0,  5, 10, 10,  5,  0,-10,
      -10,  5,  5, 10, 10,  5,  5,-10,
      -10,  0, 10, 10, 10, 10,  0,-10,
      -10, 10, 10, 10, 10, 10, 10,-10,
      -10,  5,  0,  0,  0,  0,  5,-10,
      -20,-10,-10,-10,-10,-10,-10,-20]
rawrV = [  0,  0,  0,  0,  0,  0,  0,  0,
        5, 10, 10, 10, 10, 10, 10,  5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        0,  0,  0,  5,  5,  0,  0,  0]
rawqV = [-20,-10,-10, -5, -5,-10,-10,-20,
      -10,  0,  0,  0,  0,  0,  0,-10,
      -10,  0,  5,  5,  5,  5,  0,-10,
      -5,  0,  5,  5,  5,  5,  0, -5,
      0,  0,  5,  5,  5,  5,  0, -5,
      -10,  5,  5,  5,  5,  5,  0,-10,
      -10,  0,  5,  0,  0,  0,  0,-10,
      -20,-10,-10, -5, -5,-10,-10,-20]
rawkV = [-30,-40,-40,-50,-50,-40,-40,-30,
      -30,-40,-40,-50,-50,-40,-40,-30,
      -30,-40,-40,-50,-50,-40,-40,-30,
      -30,-40,-40,-50,-50,-40,-40,-30,
      -20,-30,-30,-40,-40,-30,-30,-20,
      -10,-20,-20,-20,-20,-20,-20,-10,
      20, 20,  0,  0,  0,  0, 20, 20,
      20, 30, 10,  0,  0, 10, 30, 20]

notation = []

oldboard = list(board)

check = False
checkpoint = 64

checkmate = False
stalemate = False

wzones = []
bzones = []

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
numbers = ['1', '2', '3', '4', '5', '6', '7', '8']
promotepieces = ['Q', 'B', 'R', 'N']

pieces = {'WK': '♔', 'WQ': '♕', 'WR': '♖', 'WB': '♗', 'WN': '♘', 'WP': '♙',
          'BK': '♚', 'BQ': '♛', 'BR': '♜', 'BB': '♝', 'BN': '♞', 'BP': '♟',
          'XX': ' ', 'EE': ' ', 'EP': ' '}

values = {'K': 0, 'Q': 900, 'R': 500, 'B': 330, 'N': 320, 'P': 100}
connect = 0

def flip(raw):
    return list(reversed(raw))

# Flip values to black perspective
pV = flip(rawpV)
nV = flip(rawnV)
bV = flip(rawbV)
rV = flip(rawrV)
qV = flip(rawqV)
kV = flip(rawkV)

def printBoard(tboard):
#    for x in range(0, 20):
#        print()
    print()
    print('Write moves as following: ex. e2-e4 (e2 to e4)')
    print()
    print()
    if len(notation) % 2 == 0:
        for y in range(0,8):
            text = numbers[7 - y] + ' '
            for c in range(0,8):
                text += str(pieces[tboard[(y * 8) + c]])
            print(str(text))
        print('  a b c d e f g h')
    else:
        for y in range(0, 8):
            text = numbers[y] + ' '
            for c in range(0, 8):
                text += str(pieces[tboard[((7-y) * 8) + (7 - c)]])
            print(str(text))
        print('  h g f e d c b a')
    print()

def translate(l, n):
    py = 7 - numbers.index(n)
    px = letters.index(l)
    cdn = (py * 8) + px
    return cdn

def toLetter(n):
    px = numbers[7 - int(n/8)]
    py = letters[n - (int(n/8) * 8)]
    return (str(py) + str(px))

def checkMoveDirection(coord1, coord2, tboard):
    global wzones
    global bzones
    
    piece = tboard[coord1][1]
    color = tboard[coord1][0]
    ax = coord1 % 8
    ay = 7 - int(coord1 / 8)

    bx = coord2 % 8
    by = 7 - int(coord2 / 8)

    xd = abs(ax - bx)
    yd = abs(ay - by)
    
    if xd != 0:
        xp = -(ax - bx) / xd
    else:
        xp = 1
    if yd != 0:
        yp = -(ay - by) / yd
    else:
        yp = 1

    xs = []
    ys = []
    cpieces = []
    colors = []

    if color == tboard[coord2][0]:
        if color == 'W':
            wzones.append(coord2)
        else:
            bzones.append(coord2)
        return False

    if piece != 'N':
        if yd > 0 and xd == 0:
            for i in range(1, yd + 1):
                xs.append(ax)
                ys.append(ay + (i * yp))
        elif xd > 0 and yd == 0:
            for i in range(1, xd + 1):
                xs.append(ax + (i * xp))
                ys.append(ay)
        elif xd > 0 and yd > 0:
            for i in range(1, xd + 1):
                xs.append(ax + (i * xp))
                ys.append(ay + (i * yp))

    for x in range(0, len(xs)):
        cpieces.append(tboard[translate(letters[int(xs[int(x)])], numbers[int(ys[int(x)])])])
    for x in range(0, len(xs)):
        colors.append(cpieces[x][0])

    if color in colors:
        return False
    else:
        colors = colors[0:len(colors)-1]
        if color == 'W':
            if 'B' in colors:
                return False
            else:
                return True
        else:
            if 'W' in colors:
                return False
            else:
                return True

def doMove(coord1, coord2, tboard):
    tboard[coord2] = str(tboard[coord1])
    tboard[coord1] = 'XX'
    return tboard

def runSquares(coord1, tboard):
    squares = []  
    for x in range(0,64):
        if checkMovePiece(coord1, x, False, tboard) == True:
            if checkMoveDirection(coord1, x, tboard) == True:
                squares.append(x)

#    print(squares)
    return squares

def runZones(tboard):
    global wzones
    global bzones
    
    wzones = []
    bzones = []
    
    for x in range(0, 64):
        color = tboard[x][0]
        listram = set(runSquares(x, tboard))
        if color == 'W':
            wzones = set(wzones)
            wzones = list(wzones | listram)
        else:
            bzones = set(bzones)
            bzones = list(bzones | listram)
    
#    print(wzones)
#    print(bzones)

def checkMovePiece(coord1, coord2, move, tboard):
    global connect
    
    piece = tboard[coord1][1]
    color = tboard[coord1][0]
    squares = []
    
    ax = coord1 % 8
    ay = 7 - int(coord1 / 8)
    
    bx = coord2 % 8
    by = 7 - int(coord2 / 8)
    
    xd = abs(ax - bx)
    yd = abs(ay - by)

    # Chess piece-moving rules
    if piece == 'K':
        if color == 'W' and coord2 in bzones:
            return False
        elif color == 'B' and coord2 in wzones:
            return False
        elif xd == 0 and yd == 1:
            return True
        elif xd == 1 and yd == 0:
            return True
        elif xd == 1 and yd == 1:
            return True
        else:
            return False
    if piece == 'Q':
        if xd > 0 and yd > 0:
            if xd/yd == 1:
                return True
            else:
                return False
        elif xd == 0 or yd == 0:
            return True
        else:
            return False
    if piece == 'B':
        if xd == 0 or yd == 0:
            return False
        elif xd/yd == 1:
            return True
        else:
            return False
    if piece == 'N':
        if xd == 2 and yd == 1:
            return True
        elif xd == 1 and yd == 2:
            return True
        else:
            return False
    if piece == 'R':
        if xd == 0 and yd > 0:
            return True
        elif xd > 0 and yd == 0:
            return True
        else:
            return False
    if piece == 'P':
        if color == 'W' and ay - by > 0:
            return False
        elif color == 'B' and ay - by < 0:
            return False
        elif xd == 1 and yd == 1:
            if tboard[coord2][0] == color:
                connect += 1
            if tboard[coord2][0] != color and tboard[coord2][0] != 'X' and tboard[coord2][0] != 'E':
                return True
            elif tboard[coord2] == 'EE':
                if move == True:
                    tboard[coord2 - 8] = 'XX'
                return True
            elif tboard[coord2] == 'EP':
                if move == True:
                    tboard[coord2 + 8] = 'XX'
                return True
            else:
                return False
        elif yd == 2 and xd == 0:
            if color == 'W' and coord1 > 47 and coord1 < 56:
                if move == True:
                    tboard[coord2 + 8] = 'EE'
                return True
            elif color == 'B' and coord1 > 7 and coord1 < 16:
                if move == True:
                    tboard[coord2 - 8] = 'EP'
                return True
            else:
                return False
        elif xd == 0 and yd == 1 and tboard[coord2][1] == 'X':
            return True
        else:
            return False

def printNotation():
    print()
    print('   W   |   B   ')
    print('---------------')
    for x in range(0, int(len(notation) / 2)):
        print(' ' + notation[2 * x] + ' | ' + notation[(2 * x) + 1] + ' ')
    print()

def detectPromotion():
    wpieces = []
    bpieces = []
    
    for x in range(0,8):
        wpieces.append(board[x][1])
    for x in range(56, 64):
        bpieces.append(board[x][1])

    if 'P' in wpieces:
        num = wpieces.index('P')
        while True:
            promote = str(input('What to promote to? Q, B, N, R? '))
            if promote in promotepieces:
                board[num] = ('W' + promote)
                printBoard()
                break
            else:
                print('Invalid Choice')
    if 'P' in bpieces:
        num = bpieces.index('P')
        while True:
            promote = str(input('What to promote to? Q, B, N, R? '))
            if promote in promotepieces:
                board[num] = ('B' + promote)
                printBoard()
                break
            else:
                print('Invalid choice')

def detectEscape(coord1, tboard):
    global wzones
    global bzones
    global checkpoint
    
    squares = runSquares(coord1, tboard)
    color = board[coord1][0]
    runZones(tboard)
    if color == 'W' and checkpoint in wzones:
        return False
    elif color == 'B' and checkpoint in bzones:
        return False
    
    for x in range(0,len(squares)):
        if color == 'W' and squares[x] not in bzones:
            return False
        elif color == 'B' and squares[x] not in wzones:
            return False
    return True

def detectStalemate(coord1, tboard):
    global wzones
    global bzones
    
    squares = runSquares(coord1, tboard)
    color = board[coord1][0]
    pieces = []
    moves = []

    for x in range(0, 64):
        if board[x][0] == color and tboard[x][1] != 'K':
            pieces.append(x)
    
    for x in range(0, len(pieces)):
        moves.extend(runSquares(pieces[x], tboard))
        if len(moves) > 0:
            return False
    
    for x in range(0,len(squares)):
        if color == 'W' and squares[x] not in bzones:
            return False
        elif color == 'B' and squares[x] not in wzones:
            return False

def checkTurn(coord1):
    color = board[coord1][0]
    if len(notation) % 2 == 0 and color == 'W':
        return True
    elif len(notation) % 2 == 1 and color == 'B':
        return True
    else:
        return False

def resetEP():
    color = len(notation) % 2

    for x in range(0, 64):
        if color == 0:
            if board[x] == 'EP':
                board[x] = 'XX'
        else:
            if board[x] == 'EE':
                board[x] = 'XX'

# White is the maximizer, black is the minimizer
def boardValue(tboard):
    value = 0

    # Materialistic advantage
    for x in range(0, 64):
        if tboard[x][0] == 'B':
            value -= values[tboard[x][1]] * 5
        elif tboard[x][0] == 'W':
            value += values[tboard[x][1]] * 5

    # Placement value
    for x in range(0, 64):
        if tboard[x][0] == 'B':
            p = tboard[x][1]
            if p == 'P':
                value -= pV[x]/2
            elif p == 'N':
                value -= nV[x]*2
            elif p == 'B':
                value -= bV[x]*2
            elif p == 'R':
                value -= rV[x]
            elif p == 'Q':
                value -= qV[x]
            elif p == 'K':
                value -= kV[x]
    for x in range(0, 64):
        if tboard[x][0] == 'W':
            p = tboard[x][1]
            if p == 'P':
                value += rawpV[x]/2
            elif p == 'N':
                value += rawnV[x]*2
            elif p == 'B':
                value += rawbV[x]*2
            elif p == 'R':
                value += rawrV[x]
            elif p == 'Q':
                value += rawqV[x]
            elif p == 'K':
                value += rawkV[x]

    # Determine board control
    runZones(tboard)
    value -= len(bzones)
    value += len(wzones)
    
    # King protection
    value -= len(runSquares(tboard.index('WK'), tboard)) / 5
    value += len(runSquares(tboard.index('BK'), tboard)) / 5

    # Check status
    if tboard.index('WK') in bzones:
        value -= 10
    elif tboard.index('BK') in wzones:
        value += 10

    # Checkmate status
    if board.index('WK') in bzones and detectEscape(board.index('WK'), tboard) == True:
        value -= 1000000
    if board.index('BK') in wzones and detectEscape(board.index('BK'), tboard) == True:
        value += 1000000
    return value

def generateMoves(tboard, color):
    moves = []
    for x in range(0, 64):
        if tboard[x][0] == color:
            if x < 10:
                s = '0' + str(x)
            else:
                s = str(x)
            sl = runSquares(x, tboard)
            for y in range(0, len(sl)):
                moves.append(s + str(sl[y]))
    return moves

def detectBlock(dPiece, aPiece, tboard):
    dColor = tboard[dPiece][0]
    aColor = tboard[aPiece][0]

    if tboard[aPiece][1] == 'N':
        return False
    

# AI MINIMAX
# ----------------------------------------------------------------------------------------------------

def minimaxRoot(depth, tboard, isMaxing):
    if isMaxing == True:
        c = 'W'
    else:
        c = 'B'
    allMoves = generateMoves(tboard, c)
    bestValue = -9999
    bestMove = ''

    for x in range(0, len(allMoves)):
        selectMove = allMoves[x]
        boardState = list(tboard)
        tboard = doMove(int(selectMove[0:2]), int(selectMove[2:4]), tboard)
        value = minimax(depth - 1, tboard, -10000, 10000, not(isMaxing))
        tboard = list(boardState)
        if value >= bestValue:
            bestValue = value
            bestMove = selectMove
    return bestMove

def minimax(depth, tboard, alpha, beta, isMaxing):
    if depth == 0:
        return boardValue(tboard)
    if isMaxing == True:
        c = 'W'
    else:
        c = 'B'
    allMoves = generateMoves(tboard, c)
    
    if isMaxing == True:
        bestValue = -9999
        for x in range(0, len(allMoves)):
            selectMove = allMoves[x]
            boardState = list(tboard)
            tboard = doMove(int(selectMove[0:2]), int(selectMove[2:4]), tboard)
            bestValue = minimax(depth - 1, tboard, alpha, beta, not(isMaxing))
            tboard = list(boardState)
            alpha = max(alpha, bestValue)
            if beta <= alpha:
                return bestValue
        return bestValue
    else:
        bestValue = 9999
        for x in range(0, len(allMoves)):
            selectMove = allMoves[x]
            boardState = list(tboard)
            tboard = doMove(int(selectMove[0:2]), int(selectMove[2:4]), tboard)
            bestValue = min(bestValue, minimax(depth - 1, tboard, alpha, beta, not(isMaxing)))
            tboard = list(boardState)
            beta = min(beta, bestValue)
            if beta <= alpha:
                return bestValue
        return bestValue

def createMove(depth, tboard):
    move = minimaxRoot(depth, tboard, False)
    p1 = int(move[0:2])
    p2 = int(move[2:4])
    return (toLetter(p1) + '-' + toLetter(p2))
# ----------------------------------------------------------------------------------------------------
        
# Main "run" code

printBoard(board)

while True:
    while True:
        if len(notation) % 2 == 0:
            user = str(input('-> '))
            move = list(user)
        else:
            print('Calculating... ')
            move = createMove(2, list(board))
            print(move)
            print(str(boardValue(board)))
        runZones(board)
        if ''.join(move) == 'undo':
            board = list(oldboard)
            notation = notation[0:len(notation-1)]
            break
        elif ''.join(move) == 'notation':
            printNotation()
            print('Press ENTER to continue')
            u = input()
            break
        elif len(move) == 5 and move[2] == "-" and move[0] in letters and move[1] in numbers and move[3] in letters and move[4] in numbers and checkTurn(translate(move[0], move[1])) == True and checkMoveDirection(translate(move[0], move[1]), translate(move[3], move[4]), board) == True and checkMovePiece(translate(move[0], move[1]), translate(move[3], move[4]), True, board) == True and translate(move[0], move[1]) != translate(move[3], move[4]) and board[translate(move[0], move[1])] != 'XX':
            oldboard = list(board)
            board = doMove(translate(move[0], move[1]), translate(move[3], move[4]), board)
            resetEP()
            notation.append(''.join(move))
            runZones(board)
            if board.index('WK') in bzones:
                check = True
                checkpoint = translate(move[3], move[4])
                checkmate = detectEscape(board.index('WK'), board)
            elif board.index('BK') in wzones:
                check = True
                checkpoint = translate(move[3], move[4])
                checkmate = detectEscape(board.index('BK'), board)
            else:
                check = False
                checkpoint = 64
                stalemate = detectStalemate(board.index('WK'), board)
                stalemate = detectStalemate(board.index('BK'), board)
            break
        else:
            print("Invalid move")
            break
    printBoard(board)
    if stalemate == True:
        printNotation()
        print("STALEMATE")
        break
    elif checkmate == True:
        printNotation()
        print("CHECKMATE")
        break
    elif check == True:
        u = input("CHECK. Press ENTER to continue ")
        printBoard(board)
    detectPromotion()

