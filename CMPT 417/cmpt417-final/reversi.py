class reversi:
    def __init__(self, size: int = 4) -> None: #default size is an 8x8 board
        #normalized to array indices
        self.maxRows = 2*size - 1
        self.maxCols = 2*size - 1

        '''
        Default board setup
        - Player 1 is tile 1
        - Player 2 is tile -1
        '''
        self.board = [[0 for y in range(2*size)] for x in range(2*size)]
        self.board[self.maxRows//2][self.maxCols//2] = 1
        self.board[self.maxRows//2][self.maxCols//2+1] = -1
        self.board[self.maxRows//2+1][self.maxCols//2] = -1
        self.board[self.maxRows//2+1][self.maxCols//2+1] = 1
    
    def print(self) -> None: #testing purpose only
        count = 1
        for row in self.board:
            print("{}|  ".format(count), end="")
            for cell in row:
                if cell == 0:
                    print("_          ",end="")
                else:
                    if cell == -1:
                        print("{}         ".format(cell),end="")
                    else:
                        print("{}          ".format(cell),end="")
            print("|\n")
            count += 1

    def play_move(self, x: int, y: int, player: bool = True) -> bool: 
        '''
        - Default is player 1
        - We can assume that the move is always valid, since the AI can only choose from a set of valid moves.
        '''
        x -= 1
        y -= 1
        if (x <= self.maxRows and x >= 0 ) and (y <= self.maxCols and y >= 0) and self.board[x][y] == 0:
            if self.__update(x, y, player) != 0: # potentially don't need this check since legal_moves should do it implicitly already
                self.board[x][y] = 1 if player else -1
                return True
        return False

    def __update(self, row: int, col: int, player: bool) -> int:
        tiles_conquered = 0

        myColor = 1 if player else -1
        opColor = -1 if player else 1

        if row < self.maxRows-1 and self.board[row + 1][col] == opColor: #downard check
            check = 2
            while row + check <= self.maxRows:
                if self.board[row + check][col] == 0:
                    break
                if self.board[row + check][col] == myColor:
                    for flip_tile in range(1,check):
                        self.board[row + flip_tile][col] = myColor
                        tiles_conquered += 1
                    break
                check += 1

        if row > 1 and self.board[row - 1][col] == opColor: #upward check
            check = 2
            while row - check >= 0:
                if self.board[row - check][col] == 0:
                    break
                if self.board[row - check][col] == myColor:
                    for flip_tile in range(1,check):
                        self.board[row - flip_tile][col] = myColor
                        tiles_conquered += 1
                    break
                check += 1

        if col < self.maxCols-1 and self.board[row][col + 1] == opColor: #right check
            check = 2
            while col + check <= self.maxCols:
                if self.board[row][col + check] == 0:
                    break
                if self.board[row][col + check] == myColor:
                    for flip_tile in range(1,check):
                        self.board[row][col + flip_tile] = myColor
                        tiles_conquered += 1
                    break
                check += 1

        if col > 1 and self.board[row][col - 1] == opColor: #left check
            check = 2
            while col - check >= 0:
                if self.board[row][col - check] == 0:
                    break
                if self.board[row][col - check] == myColor:
                    for flip_tile in range(1,check):
                        self.board[row][col - flip_tile] = myColor
                        tiles_conquered += 1
                    break
                check += 1

        if (row > 1 and col < self.maxCols-1) and self.board[row - 1][col + 1] == opColor: #top-right check
            check = 2
            while row - check >= 0 and col + check <= self.maxCols:
                if self.board[row - check][col + check] == 0:
                    break
                if self.board[row - check][col + check] == myColor:
                    for flip_tile in range(1,check):
                        self.board[row - flip_tile][col + flip_tile] = myColor
                        tiles_conquered += 1
                    break
                check += 1

        if (row > 1 and col > 1) and self.board[row - 1][col - 1] == opColor: #top-left check
            check = 2
            while row - check >= 0 and col - check >= 0:
                if self.board[row - check][col - check] == 0:
                    break
                if self.board[row - check][col - check] == myColor:
                    for flip_tile in range(1,check):
                        self.board[row - flip_tile][col - flip_tile] = myColor
                        tiles_conquered += 1
                    break
                check += 1

        if (row < self.maxRows-1 and col < self.maxCols-1) and self.board[row + 1][col + 1] == opColor: #bottom-right check
            check = 2
            while row + check <= self.maxRows and col + check <= self.maxCols:
                if self.board[row + check][col + check] == 0:
                    break
                if self.board[row + check][col + check] == myColor:
                    for flip_tile in range(1,check):
                        self.board[row + flip_tile][col + flip_tile] = myColor
                        tiles_conquered += 1
                    break
                check += 1

        if (row < self.maxRows-1 and col > 1) and self.board[row + 1][col - 1] == opColor: #bottom-left check
            check = 2
            while row + check <= self.maxRows and col - check >= 0:
                if self.board[row + check][col - check] == 0:
                    break
                if self.board[row + check][col - check] == myColor:
                    for flip_tile in range(1,check):
                        self.board[row + flip_tile][col - flip_tile] = myColor
                        tiles_conquered += 1
                    break
                check += 1

        return tiles_conquered

    def legal_moves(self, player: bool = True) -> set((int,int)):
        myColor = 1 if player else -1
        opColor = -1 if player else 1

        poss_moves = set() #we use a set to eliminate duplicates

        for row in range(self.maxRows+1):
            for col in range(self.maxCols+1):
                if self.board[row][col] == 0:
                    if row < self.maxRows-1 and self.board[row + 1][col] == opColor: #downward check
                        check = 2
                        while row + check <= self.maxRows:
                            if self.board[row + check][col] == myColor:
                                poss_moves.add((row + 1, col + 1))
                                break
                            elif self.board[row + check][col] == 0:
                                break
                            check += 1
                    
                    if row > 0 and self.board[row - 1][col] == opColor: #upward check
                        check = 2
                        while row - check >= 0:
                            if self.board[row - check][col] == myColor:
                                poss_moves.add((row + 1, col + 1))
                                break
                            elif self.board[row - check][col] == 0:
                                break
                            check += 1

                    if col < self.maxCols-1 and self.board[row][col + 1] == opColor: #right check
                        check = 2
                        while col + check <= self.maxCols:
                            if self.board[row][col + check] == myColor:
                                poss_moves.add((row + 1, col + 1))
                                break
                            elif self.board[row][col + check] == 0:
                                break
                            check += 1

                    if col > 0 and self.board[row][col - 1] == opColor: #left check
                        check = 2
                        while col - check >= 0:
                            if self.board[row][col - check] == myColor:
                                poss_moves.add((row + 1, col + 1))
                                break
                            elif self.board[row][col - check] == 0:
                                break
                            check += 1

                    if row > 0 and col < self.maxCols-1 and self.board[row-1][col+1] == opColor: #top-right check
                        check = 2
                        while row - check >= 0 and col + check <= self.maxCols:
                            if self.board[row - check][col + check] == myColor:
                                poss_moves.add((row + 1, col + 1))
                                break
                            elif self.board[row - check][col + check] == 0:
                                break
                            check += 1

                    if row > 0 and col > 0 and self.board[row-1][col-1] == opColor: #top-left check
                        check = 2
                        while row - check >= 0 and col - check >= 0:
                            if self.board[row - check][col - check] == myColor:
                                poss_moves.add((row + 1, col + 1))
                                break
                            elif self.board[row - check][col - check] == 0:
                                break
                            check += 1

                    if row < self.maxRows-1 and col > 0 and self.board[row+1][col-1] == opColor: #bottom-left check
                        check = 2
                        while row + check <= self.maxRows and col - check >= 0:
                            if self.board[row + check][col - check] == myColor:
                                poss_moves.add((row + 1, col + 1))
                                break
                            elif self.board[row + check][col - check] == 0:
                                break
                            check += 1

                    if row < self.maxRows-1 and col < self.maxCols-1 and self.board[row+1][col+1] == opColor: #bottom-right check
                        check = 2
                        while row + check <= self.maxRows and col + check <= self.maxCols:
                            if self.board[row + check][col + check] == myColor:
                                poss_moves.add((row + 1, col + 1))
                                break
                            elif self.board[row + check][col + check] == 0:
                                break
                            check += 1

        return poss_moves

    def gameOver(self) -> tuple([bool, int, int]):
        p1 = self.legal_moves()
        p2 = self.legal_moves(False)
        if not len(p1) and not len(p2): #Maybe should be or? Please give it a check
     #       print("-------GAME OVER-------")
            return True, self.myPoints(), self.myPoints(False)
        else:
            return False, 0, 0
                
    def myPoints(self, player: bool = True) -> int:
        myColor = 1 if player else -1
        points = 0
        for row in self.board:
            for cell in row:
                if cell == myColor:
                    points += 1
        return points