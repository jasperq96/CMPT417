import math
import copy
from typing import Callable
import reversi as r

def greedy_heuristic(*arguments) -> int:
    occupied_tiles = 0
    for i in range(len(arguments[0].board)):
        for j in range(len(arguments[0].board)):
            if(arguments[0].board[i][j] != 0):
                occupied_tiles += arguments[0].board[i][j]
    return occupied_tiles

def move_difference_heuristic(game: r, myColor: bool) -> int:
    return len(game.legal_moves(myColor)) - len(game.legal_moves(not myColor))

def front_interior_heuristic(game: r, myColor: bool) -> int:
    myTile = 1 if myColor else -1
    frontier = 0
    interior = 0
    board = game.board

    for x in range(game.maxRows + 1):
        for y in range(game.maxCols + 1):
            if board[x][y] == myTile:
                if __is_frontier(board, x, y):
                    frontier += 1
                else:
                    interior += 1
    return interior - frontier

def board_space_heuristic(*arguments) -> int:
    board_space_values = [
        [100,-30,6,2,2,6,-30,100],
        [-30,-50,0,0,0,0,-50,-30],
        [6,0,0,0,0,0,0,6],
        [2,0,0,3,3,0,0,2],
        [2,0,0,3,3,0,0,2],
        [6,0,0,0,0,0,0,6],
        [-30,-50,0,0,0,0,-50,-30],
        [100,-30,6,2,2,6,-30,100]
    ]
    board = arguments[0].board
    board_value = 0

    for row_board, row_static in zip(board, board_space_values):
        for tile, tile_value in zip(row_board, row_static):
            board_value += tile * tile_value

    return board_value

def __is_frontier(board: list, x: int, y: int) -> bool:
    if board[x-1][y] == 0 or board[x+1][y] == 0 or board[x][y-1] == 0 or board[x][y+1] == 0 or board[x-1][y-1] == 0 or board[x-1][y+1] == 0 or board[x+1][y-1] == 0 or board[x+1][y+1] == 0:
        return True
    return False

nodes_generated = 0

def minmax_alg(maximizing: bool, game: r, depth: int, heuristic: Callable, myColor: bool) -> tuple([any, int]):
    # copy_of_game = r.reversi(dimensions)
    copy_of_game = copy.deepcopy(game)
    if(maximizing):
        possible_moves = list(copy_of_game.legal_moves())
    else:
        possible_moves = list(copy_of_game.legal_moves(False))
    if (copy_of_game.gameOver()[0] == True or depth == 0):
        return None, heuristic(game, myColor)
    move_taken = possible_moves[0]
    if maximizing:
        maximized_value = -math.inf
        for move in possible_moves:
            # temp_game = r.reversi(dimensions)
            temp_game = copy.deepcopy(game)
            temp_game.play_move(move[0], move[1], True)
            current_value = minmax_alg(False, temp_game, depth-1, heuristic, myColor)[1]
            if current_value > maximized_value:
                maximized_value = current_value
                move_taken = move
        return move_taken, maximized_value
    else:
        minimized_value = math.inf
        for move in possible_moves:
            # temp_game = r.reversi(dimensions)
            temp_game = copy.deepcopy(game)
            temp_game.play_move(move[0], move[1], False)
            current_value = minmax_alg(True, temp_game, depth-1, heuristic, myColor)[1]
            if current_value < minimized_value:
                minimized_value = current_value
                move_taken = move
            return move_taken, minimized_value


def minmax_alg_alphabeta(maximizing: bool, game: r, depth: int, heuristic: Callable, myColor: bool, alpha = -math.inf, beta = math.inf) -> tuple([any, int]):
    # copy_of_game = r.reversi(dimensions)
    copy_of_game = copy.deepcopy(game)
    if(maximizing):
        possible_moves = list(copy_of_game.legal_moves())
    else:
        possible_moves = list(copy_of_game.legal_moves(False))
    if (copy_of_game.gameOver()[0] == True or depth == 0):
        return None, heuristic(game, myColor)
    move_taken = possible_moves[0]
    if maximizing:
        maximized_value = -math.inf
        for move in possible_moves:
            # temp_game = r.reversi(dimensions)
            temp_game = copy.deepcopy(game)
            temp_game.play_move(move[0], move[1], True)
            current_value = minmax_alg_alphabeta(False, temp_game, depth-1, heuristic, myColor, alpha, beta)[1]
            if current_value > maximized_value:
                maximized_value = current_value
                move_taken = move
            if current_value >= beta:
                return(move_taken, current_value)
            alpha = max(alpha, current_value)
        return move_taken, maximized_value
    else:
        minimized_value = math.inf
        for move in possible_moves:
            # temp_game = r.reversi(dimensions)
            temp_game = copy.deepcopy(game)
            temp_game.play_move(move[0], move[1], False)
            current_value = minmax_alg_alphabeta(True, temp_game, depth-1, heuristic, myColor, alpha, beta)[1]
            if current_value < minimized_value:
                minimized_value = current_value
                move_taken = move
            if current_value <= alpha:
                return(move_taken, current_value)
            beta = min(beta, current_value)
            return move_taken, minimized_value


'''
test = [[0 for y in range(3)] for x in range(3)]
# test[1][1]=0
testlist = [1, 2, 3]
testvalue = testlist.pop()
print(testvalue)
mm = minmax(test)
testcopy = copy.deepcopy(mm.board)
testcopy[1][1] = 1
print(mm.initial_nodes())
print(mm.board_count(test))
print(len(mm.board))
for i in testcopy:
    for j in i:
        print(j)
'''
'''
test = [[0 for y in range(3)] for x in range(3)]
test[0][1] = 1
test[0][0] = 1
test[0][2] = -1
board_size = board_count(test)
print(test)
print("this is the board size")
print(board_size)
'''
# game = r.reversi(2)
# game.print()
# test_run = minmax_alg_alphabeta(True, game, 2, greedy_heuristic, True)
# print(test_run)
# game.play_move(test_run[0][0], test_run[0][1], True)
# game.print()
# test_run2 = minmax_alg(False, game, 2, 2, greedy_heuristic)
# print(test_run2)
# game.play_move(test_run2[0][0], test_run2[0][1], False)
# game.print()
# print(game)
# print(game.legal_moves())
# test_run3 = minmax_alg(True, game, 2, 2, greedy_heuristic)
# print(test_run3)
# game.play_move(test_run3[0][0], test_run3[0][1], True)
# game.print()
# test_run4 = minmax_alg(False, game, 2, 2, greedy_heuristic)
# print(test_run4)
# game.play_move(test_run4[0][0], test_run4[0][1], False)
# game.print()
# test_run5 = minmax_alg(True, game, 2, 2, greedy_heuristic)
# print(test_run5)
# game.play_move(test_run5[0][0], test_run5[0][1], True)
# game.print()
# test_run6 = minmax_alg(False, game, 2, 2, greedy_heuristic)
# print(test_run6)
# print(game.legal_moves(False))
# game.play_move(test_run6[0][0], test_run6[0][1], False)
# game.print()
