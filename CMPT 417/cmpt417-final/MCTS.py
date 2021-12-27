# Monte Carlo Tree Search
import numpy as numpy
import copy
from collections import defaultdict
''' Set num_simulation in main.py to a lower value if run time is too slow'''

class mcts:
    def __init__(self, state, parent=None, p_move = None):
        self.state = state
        self.player = None
        self.parent = parent
        self.p_move = p_move
        self.childNode = []
        self.visited = 0
        self.w = 0
        self.l = 0
        self.moves = []
        self.game = None
        return
        
    def possible_moves(self, player):
        ''' Grabs possible moves for current state'''
        ''' Calls Legal_moves from Reversi '''
        self.moves = self.state.legal_moves(player)
        return self.moves

    def q(self):
        ''' keeps track of score (wins - losses) '''
        ''' q value for UCT '''
        totalScore = self.w - self.l
        return totalScore
        
    def n(self):
        ''' how many times a node has been visited '''
        ''' n value for UCT '''
        return self.visited
    
    def is_terminal(self):
        '''Checks if the game is over '''
        return self.state.gameOver()[0]

    def is_finished(self):
        '''Checks if there are any valid moves left '''
        if self.moves:
            return False
        else:
            return True
            
    def expand(self):
        '''Expansion phase of MCTS '''
        '''Child nodes are created for each legal move from the current board state'''
        next_Move = self.moves
        child_Node = copy.deepcopy(self)
        play = child_Node.state.play_move(next_Move[0], next_Move[1], child_Node.player)
        child_Node.parent = self
        child_Node.player = not child_Node.player
        child_Node.p_move = next_Move
        child_Node.l = 0
        child_Node.w = 0
        self.childNode.append(child_Node)
        child_Node.childNode = []
        return child_Node
        
    def rollout(self, player):
        ''' Roll out phase of MCTS '''
        ''' From this phase, the game is played out from one of the child node states
            created in the Expansion phase. The game is played to the end -> until there is a winner
            or game results in a draw. Based on the results, rollout will return a 1, 0, or -1
            1 - if the player won
            -1 - if the player lost
            0 - if it resulted in a draw '''
            
        curr = self
        game_over = curr.state.gameOver()
        while not game_over[0]:
            legalMoves = curr.possible_moves(curr.player)
            if legalMoves:
                move = self.random_playout(legalMoves)
                temp = list(move)
                curr_move = curr.state.play_move(temp[0], temp[1], curr.player)
            curr.player = not curr.player
            game_over = curr.state.gameOver()
        winner = 0
        
        ''' depending on who the player is, it will return 1 or -1 accordingly '''
        
        if game_over[1] == game_over[2]:
            winner = 0
        elif game_over[2] > game_over[1]:
            if player == False:
                winner = 1
            else:
                winner = -1
        else:
            if player == False:
                winner = -1
            else:
                winner = 1
        return winner
        
    def backprop(self, scoreInd):
        ''' BackPropagation phase of MCTS '''
        ''' The node will record how many times it has been visited as well as how many
            wins/losses/draws resulted from this state. '''
        self.visited += 1.
        if scoreInd == 1:
            self.w += 1.
        elif scoreInd == -1:
            self.l += 1.
        if (self.parent):
            self.parent.backprop(scoreInd)


    def best_move(self, c = 0.1):
        '''Looks up the best move. Uses UCT formula to calculate '''
        next_action = [(node.q() + (c*numpy.sqrt(numpy.log(self.n())/node.n()))) for node in self.childNode]
        return self.childNode[numpy.argmax(next_action)]
        
    def random_playout(self, moves):
        '''Random Playout '''
        poss_moves = list(moves)
#        Tested Heuristic created from board space heuristic
#        best_h = [(1, 1), (1, 8), (8, 1), (8, 8)]
#
#        intersection_1 = [x for x in best_h if x in poss_moves]
#        if intersection_1:
#            return intersection_1[numpy.random.randint(len(intersection_1))]
#
#        better_h = [(1, 3), (1, 6), (3, 1), (3, 8), (6, 1), (6, 8), (8, 3), (8, 6)]
#        intersection_2 = [b for b in better_h if b in poss_moves]
#        if intersection_2:
#            return intersection_2[numpy.random.randint(len(intersection_2))]
#
#        mediocre_h = [(1, 4), (1, 5), (4, 1), (5, 1), (4, 8), (5, 8), (8, 4), (8, 5)]
#        intersection_3 = [y for y in mediocre_h if y in poss_moves]
#        if intersection_3:
#            return intersection_3[numpy.random.randint(len(intersection_3))]
#
#        neutral_h =[(1, 4), (1, 5), (4, 1), (5, 1), (4, 8), (5, 8), (8, 4), (8, 5
#                    ), (2, 3), (2, 4), (2, 5), (2, 6
#                    ), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7
#                    ), (4, 2), (4, 3), (4, 6), (4, 7
#                    ), (5, 2), (5, 3), (5, 6), (5, 7
#                    ), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7
#                    ), (7, 3), (7, 4), (7, 5), (7, 6)]
#        intersection_4 = [z for z in neutral_h if z in poss_moves]
#        if intersection_4:
#            return intersection_4[numpy.random.randint(len(intersection_4))]
#
#        bad_h = [(1, 2), (1, 7), (2, 1), (2, 8), (7, 1), (7, 7)]
#        intersection_5 = [q for q in bad_h if q in poss_moves]
#        if intersection_5:
#            return intersection_5[numpy.random.randint(len(intersection_5))]

        return poss_moves[numpy.random.randint(len(moves))]

    def tree_policy(self, current_move):
        curr = self
        curr.moves = current_move
        while not curr.is_terminal():
            if not curr.is_finished():
                return curr.expand()
            else:
                curr = curr.best_move()
        return curr
        
    def best_node(self, player, game_over, num_simulation):
        '''Returns node with best possible move. Runs expansion, simulation and backpropagation '''
        test = copy.deepcopy(self)
        test.game = game_over
        test.player = player
        test.moves = test.possible_moves(player)
        moves_to_test = len(test.moves)
        moves_list = test.moves
        for i in range(moves_to_test):
            if test.state.gameOver()[0]:
                continue
            next_move = moves_list.pop()
            t = test.tree_policy(next_move)
            temp = copy.deepcopy(t.state)
            for x in range(num_simulation):
                t.state = copy.deepcopy(temp)
                reward = t.rollout(player)
                t.backprop(reward)
        best = test.best_move(c = 0.)
        best_action = best.p_move
        return best_action
