import reversi as r
import MCTS as mcts
import time as t
import math as m
import copy as c
from typing import Callable


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
    corners_captured = 2
    top_left_corner = [
        [100,80,40,30,20,15,10,100],
        [80, 90, 30, 20,15,10,0,0],
        [40, 30, 20,15,10,-1, 0,0],
        [30, 20, 15, 10, -1, 0, 0,0],
        [20, 15, 10, -1, 0, 0, 0,0],
        [15, 10, -1,  0, 0, 0, 0,0],
        [10, 0, 0,  0, 0, 0, 0,0],
        [100, 0, 0,  0, 0, 0, 0,100]
        ]
    top_right_corner = c.deepcopy(top_left_corner)
    for row in top_right_corner:
        row.reverse()

    bottom_right_corner = c.deepcopy(top_right_corner)
    bottom_right_corner.reverse()

    bottom_left_corner = c.deepcopy(bottom_right_corner)
    for row in bottom_left_corner:
        row.reverse()

    if board[0][0] != 0 :
        for row in range(len(board)):
            for col in range(len(board[0])):
                board_space_values[row][col] += top_left_corner[row][col]
        corners_captured += 1

    if board[7][0] != 0:
        for row in range(len(board)):
            for col in range(len(board[0])):
                board_space_values[row][col] += bottom_left_corner[row][col]
        corners_captured += 1
        
    if board[0][7] != 0:
        for row in range(len(board)):
            for col in range(len(board[0])):
                board_space_values[row][col] += top_right_corner[row][col]
        corners_captured += 1

    if board[7][7] != 0:
        for row in range(len(board)):
            for col in range(len(board[0])):
                board_space_values[row][col] += bottom_right_corner[row][col]
        corners_captured += 1

    for row_board, row_static in zip(board, board_space_values):
        for tile, tile_value in zip(row_board, row_static):
            board_value += tile * (tile_value/corners_captured)

    return board_value

def split(*arguments) -> int:
    occupied_tiles = 0
    for i in range(len(arguments[0].board)):
        for j in range(len(arguments[0].board)):
            if(arguments[0].board[i][j] != 0):
                occupied_tiles += abs(arguments[0].board[i][j])
    if occupied_tiles <= 20:
        return front_interior_heuristic(arguments[0], arguments[1]) + move_difference_heuristic(arguments[0],arguments[1])
    else:
        return board_space_heuristic(arguments[0])


# /m.sqrt(arguments[0].myPoints() + arguments[0].myPoints(False))
def all_heuristic(*arguments) -> int:
    # return (greedy_heuristic(arguments[0])*.5) + (move_difference_heuristic(arguments[0],arguments[1])) + (front_interior_heuristic(arguments[0],arguments[1])*1.2) + board_space_heuristic(arguments[0])
    return (front_interior_heuristic(arguments[0],arguments[1])*1.2) + board_space_heuristic(arguments[0])
    # return move_difference_heuristic(arguments[0],arguments[1]) + (front_interior_heuristic(arguments[0],arguments[1])*1.2) + board_space_heuristic(arguments[0])

def __is_frontier(board: list, x: int, y: int) -> bool:
    if x - 1 >= 0: #left check
        if board[x-1][y] == 0:
            return True
        
    if x + 1 <= 7: #right check
        if board[x+1][y] == 0:
            return True

    if y - 1 >= 0: #down check
       if board[x][y-1] == 0:
           return True
        
    if y + 1 <= 7: #up check
        if board[x][y+1] == 0 :
            return True
        
    if x - 1 >= 0 and y - 1 >= 0:
        if board[x-1][y-1] == 0 :
            return True
        
    if x - 1 >= 0 and y + 1 <= 7:    
        if board[x-1][y+1] == 0 :
            return True

    if x + 1 <= 7 and y - 1 >= 0:
        if board[x+1][y-1] == 0 :
            return True
    
    if x + 1 <= 7 and y + 1 <= 7:
        if board[x+1][y+1] == 0:
            return True

    return False



def minmax_alg(maximizing: bool, game: r, depth: int, heuristic: Callable, myColor: bool) -> tuple([any, int]):
    global nodes_generated

    copy_of_game = c.deepcopy(game)
    if(maximizing):
        possible_moves = list(copy_of_game.legal_moves())
        if len(possible_moves) == 0:
            return (-1,-1), -1
    else:
        possible_moves = list(copy_of_game.legal_moves(False))
        if len(possible_moves) == 0:
            return (-1,-1), -1
    if (copy_of_game.gameOver()[0] == True or depth == 0):
        return None, heuristic(game, myColor)
    move_taken = possible_moves[0]
    if maximizing:
        maximized_value = -m.inf
        for move in possible_moves:
            nodes_generated += 1
            temp_game = c.deepcopy(game)
            temp_game.play_move(move[0], move[1], True)
            current_value = minmax_alg(False, temp_game, depth-1, heuristic(temp_game, myColor), myColor)[1]
            if current_value > maximized_value:
                maximized_value = current_value
                move_taken = move
        return move_taken, maximized_value
    else:
        minimized_value = m.inf
        for move in possible_moves:
            nodes_generated += 1
            temp_game = c.deepcopy(game)
            temp_game.play_move(move[0], move[1], False)
            current_value = minmax_alg(True, temp_game, depth-1, heuristic(temp_game, myColor), myColor)[1]
            if current_value < minimized_value:
                minimized_value = current_value
                move_taken = move
        return move_taken, minimized_value


def minmax_alg_alphabeta(maximizing: bool, game: r, depth: int, heuristic: Callable, myColor: bool, alpha = -m.inf, beta = m.inf) -> tuple([any, int]):
    global nodes_generated

    copy_of_game = c.deepcopy(game)
    if(maximizing):
        possible_moves = list(copy_of_game.legal_moves())
        if len(possible_moves) == 0:
            return (-1,-1), -1
    else:
        possible_moves = list(copy_of_game.legal_moves(False))
        if len(possible_moves) == 0:
            return (-1,-1), -1
    if (copy_of_game.gameOver()[0] == True or depth == 0):
        return None, heuristic(game, myColor)

    move_taken = possible_moves[0]
    if maximizing:
        maximized_value = -m.inf
        for move in possible_moves:
            temp_game = c.deepcopy(game)
            temp_game.play_move(move[0], move[1], True)
            current_value = minmax_alg_alphabeta(False, temp_game, depth-1, heuristic, myColor, alpha, beta)[1]
            if current_value > maximized_value:
                maximized_value = current_value
                move_taken = move
            if current_value >= beta:
                return(move_taken, current_value)
            nodes_generated += 1
            alpha = max(alpha, current_value)
        return move_taken, maximized_value
    else:
        minimized_value = m.inf
        for move in possible_moves:
            temp_game = c.deepcopy(game)
            temp_game.play_move(move[0], move[1], False)
            current_value = minmax_alg_alphabeta(True, temp_game, depth-1, heuristic, myColor, alpha, beta)[1]
            if current_value < minimized_value:
                minimized_value = current_value
                move_taken = move
            if current_value <= alpha:
                return(move_taken, current_value)
            nodes_generated += 1
            beta = min(beta, current_value)
        return move_taken, minimized_value

game = r.reversi()
player_move = False
player_tile_color = True if not player_move else False
ai_tile_color = False if not player_move else True

game_over = game.gameOver()

heuristic_list = (greedy_heuristic, move_difference_heuristic, front_interior_heuristic, board_space_heuristic, split, all_heuristic)
heuristic_names = ('Greedy Heuristic', 'Move Difference Heuristic', 'Frontier vs Interior Heursitic', 'Board Space Heuristic', 'Split Heuristic','All Heuristic')
print("Which heuristic would you list to use:")

for name in heuristic_names:
    print("{}: {}".format(heuristic_names.index(name)+1, name))

choice = int(input()) - 1

print("Ai using {}\n".format(heuristic_names[choice]))

ai_move_timestamps = []
nodes_generated = 0
number_of_moves = 0
depth_of_search = int(input("Depth is: "))

while not game_over[0]:
    game.print()
    valid_moves = game.legal_moves(player_move)
    
    if not len(valid_moves):
        player_move = not player_move
        continue
    
    print("Valid Moves: {}".format(valid_moves))
    
    if player_move:   
        print("Player  move: ")
        move = input().split(" ")
        while len(move) != 2:
            move = input().split(" ")

        while int(move[0]) > 8 or int(move[1]) > 8:
            move = input().split(" ")

        
        print("Player move ({},{})".format(move[0], move[1]))

        game.play_move(int(move[0]),int(move[1]), player_tile_color)
    else:
        start_time = t.time()
        move = minmax_alg_alphabeta(ai_tile_color, game, depth_of_search, heuristic_list[choice], ai_tile_color)[0]
        # print("Test:", nodes_generated)
        ai_move_timestamps.append(t.time() - start_time)
        number_of_moves += 1

        if move[0] != -1:
            print("AI move ({},{})".format(move[0], move[1]))
            game.play_move(int(move[0]),int(move[1]), ai_tile_color)
        else:
            print("AI makes no moves")
        
    player_move = not player_move
    game_over = game.gameOver()

game.print()
if game_over[1] == game_over[2]:
    winner = "No one!"
elif game_over[1] > game_over[2]:
    winner = "Their AI"
else:
    winner = "Our AI"

print("Depth for Minmax: {}".format(depth_of_search))
print("Run Time for Moves: ")
for time in range(len(ai_move_timestamps)):
    print("{}".format(ai_move_timestamps[time]))

print("Total nodes generated: {}".format(nodes_generated))
print("Total moves AI made: {}".format(number_of_moves))
print("Tile Difference: {}".format(game_over[2] - game_over[1])) # whoever goes first


print("Final score {} - {} for {}".format(game_over[1], game_over[2], winner))

# while not game_over[0]:
#     print("CURRENT PLAYER: ", player_1_move)
#     print("CURRENT BOARD STATE: ")
#     game.print()
# #    valid_moves = game.legal_moves(player_1_move)
# #    print("Valid Moves: {}".format(valid_moves))
# #    if not len(valid_moves):
# #         player_1_move = not player_1_move
# #         continue
# #    move = input().split(" ")
# #    print("Player 1's move: ") if player_1_move else print("Player 2's move: ")
# #    while not game.play_move(int(move[0]),int(move[1]),player_1_move):
# #         print("Enter a valid move: ")
# #         move = input().split(" ")
# #    game.print()
# #    player_1_move = not player_1_move
#     print("MCTS TURN  - PLAYER: ", player_1_move)
#     legalMoves = game.legal_moves(player_1_move)
#     print("CURRENT LEGAL MOVES FOR MCTS: ", legalMoves)
#     if not len(legalMoves):
#         print("NO MOVES AVAILBLE FOR MCTS: ", player_1_move, " SKIPPING")
#         player_1_move = not player_1_move
#         continue
#     root = mcts.mcts(game)
#     next_move = root.best_node(player_1_move, game_over)
#     print("IN MAIN, MCTS Next move: ", next_move)
#     temp = game.play_move(next_move[0], next_move[1], player_1_move)
#     player_1_move = not player_1_move
#
#     game_over = game.gameOver()
#
#if game_over[1] == game_over[2]:
#     winner = "No one!"
#elif game_over[1] > game_over[2]:
#     winner = "P1 MCTS"
#else:
#     winner = "P2"
#print("Final score {} - {} for {}".format(game_over[1], game_over[2], winner))
#print("Run Time for Moves: ")
#for time in range(len(ai_move_timestamps)):
#    print("{}".format(ai_move_timestamps[time]))
#print("Tile Difference: {}".format(game_over[2] - game_over[1])) # whoever goes first
