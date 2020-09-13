# Author: YJL
# Date: 05/28/2020
# Description: This script contains a class named GessGame that represets a board game called Gess. A Gess game is played by two players
# (black and white) on an 18x18 grid of a board. Each player has 43 stones at the beggining and takes turn to make a move, with black starting.
# A 3x3 group of stones moves as a piece, and how it moves is determined by the stones themselves: A direction is legal when there is a stone
# sitting at the corresponding spot of a piece's perimeter. The piece can move any unobstructed distance if there is a stone in the center.
# Otherwise up to 3 squares. Stones are removed when 1) being covered by the footprint of a piece 2) part of the piece moves beyond the
# board boundaries. A player doesn't lose until they have no remaining ring which is composed of eight stones being around an empty center. 

# When a GessGame object is created, the turn is initialized as 'black'. After black makes the first move, turn is updated to 'white', so
# on and so forth. Everytime when we intent to make a move, we pass in two strings that represents the center of the old piece and the new piece.
# The program will first check whether or not the move is legal based on several rules. If it's legal, makes the move, updates turn and game state
# if necessary. If the move is not legal, returns False and nothing gets updated/changed. Right after a move is made, the programs checks if
# the opponent still has ring. If not, the current player won; If yes, game continues. Player can also resign as long as the game is unfinished.


class GessGame:
    """ 
    Represents a board game called Gess that's played by two players (black and white) on an 18x18 grid of a board.
    Each player has 43 stones at the beggining and takes turn to make a move, with black starting.
    A 3x3 group of stones moves as a piece, and how it moves is determined by the stones themselves:
    Direction each stone on the perimeter of a piece allows the piece to move in that direction.
    Distance: the piece can move any unobstructed distance if there is a stone in the center. Otherwise up to 3 squares.
    Stones are removed when 1) being covered by the footprint of a piece 2) part of the piece gets moved beyond the board boundaries.
    A player doesn't lose until they have no remaining ring which is composed of eight stones being around an empty center.

    Totally 11 methods are implemented:
        1) __init__ ()
        2) make_move(stone, from_location, to_location)
        3) is_move_legal(stone, from_location, to_location)
        4) move_and_capture(stone, from_location, to_location)
        5) has_ring(stone)
        6) resign_game()
        7) get_game_state()
        8) set_game_state(winner)
        9) set_turn(turn)
        For debugging:
        10) get_turn()  
        11) print_board()

    """
    def __init__(self):
        """
        Takes no parameters and initializes a GessGame object with 3 private data members: state, turn and board.
        board is initialized as a 20x20 nested list, each outerlist represents a row, each element of the innerlist 
        represents a square.
        """
        self._state = 'UNFINISHED'
        self._turn = 'black'
        self._board = [['','','','','','','','','','','','','','','','','','','',''],
                       ['','','○','','○','','○','○','○','○','○','○','○','○','','○','','○','',''],
                       ['','○','○','○','','○','','○','○','○','○','','○','','○','','○','○','○',''],
                       ['','','○','','○','','○','○','○','○','○','○','○','○','','○','','○','',''],
                       ['','','','','','','','','','','','','','','','','','','',''],
                       ['','','','','','','','','','','','','','','','','','','',''],
                       ['','','○','','','○','','','○','','','○','','','○','','','○','',''],
                       ['','','','','','','','','','','','','','','','','','','',''],
                       ['','','','','','','','','','','','','','','','','','','',''],
                       ['','','','','','','','','','','','','','','','','','','',''],
                       ['','','','','','','','','','','','','','','','','','','',''],
                       ['','','','','','','','','','','','','','','','','','','',''],
                       ['','','','','','','','','','','','','','','','','','','',''],
                       ['','','●','','','●','','','●','','','●','','','●','','','●','',''],
                       ['','','','','','','','','','','','','','','','','','','',''],
                       ['','','','','','','','','','','','','','','','','','','',''],
                       ['','','●','','●','','●','●','●','●','●','●','●','●','','●','','●','',''],
                       ['','●','●','●','','●','','●','●','●','●','','●','','●','','●','●','●',''],
                       ['','','●','','●','','●','●','●','●','●','●','●','●','','●','','●','',''],
                       ['','','','','','','','','','','','','','','','','','','','']]
       
         
    
    def make_move(self, from_location, to_location):
        """
        Takes two parameters that respectively represents the center of the piece being moved and the center of the desired new piece.
        If the move is legal, makes the move, updates turn and returns True, updates game_state if necessary.
        if the move is illegal, returns False.
        """
        # check game state
        if self._state != 'UNFINISHED':
            return False
        
        # define stone, opponent's stone and next_turn based on the current turn
        if self._turn == 'black':
            stone = '●'
            opponent_stone = '○'
            next_turn = 'white'
        else:
            stone = '○'
            opponent_stone = '●'
            next_turn = 'black'
        
        # check if the move is legal
        if not self.is_move_legal(stone, from_location, to_location):
            return False
       
        # make the move if it's legal 
        self.move_and_capture(stone, from_location, to_location)

        # check opponent's ring, if no ring then the current turn won. Update game_state
        if not self.has_ring(opponent_stone):
            self.set_game_state(self._turn) 
            return True
            
        # game continues, update turn
        self.set_turn(next_turn)
        
        return True


    def is_move_legal(self, stone, from_location, to_location):
        """
        Takes 3 parameters and check if the stone is allowed to make such move based on following rules:
            1) not legal if the center of the from_location or to_location is out of bound
            2) not legal if the 3x3 grid contains something else besides the right stone and empty squares
            3) not legal to move if it would leave no ring
            4) not legal to move in such direction that no stone in the corresponding spot on the piece's perimeter
            5) not legal to move the over 3 squares if the piece center is empty
            6) not legal to move when there's obstructed stone in between
            
        Returns False if the move is illegal, otherwise returns True.
        """
        
        # convert location from the format like 'm3' to 2 integers that repectively represents column and row of the board
        column_range = ['b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s']
        row_range = ['2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19']
        column_lookup_table = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10,
                               'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19}
        from_row = from_location[1:]
        from_column = from_location[0]
        from_location_board_row = 20 - int(from_row) 
        from_location_board_column = column_lookup_table[from_column]  # get the corresponding column integer from the look up table
        
        to_row = to_location[1:]
        to_column = to_location[0]
        to_location_board_row = 20 - int(to_row)
        to_location_board_column = column_lookup_table[to_column]   # get the corresponding column integer from the look up table
        
        # 1) not legal if the center of the from_location or to_location is out of bound
        if from_column not in column_range or from_row not in row_range:
            return False
        if to_column not in column_range or to_row not in row_range:
            return False
        
        # 2) not legal if the 3x3 grid contains something else besides the right stone and empty squares
        for r in range(from_location_board_row-1, from_location_board_row+2):
            for c in range(from_location_board_column-1, from_location_board_column+2):
                if self._board[r][c] != stone and self._board[r][c] != '':
                    return False
        
        # 3) not legal to move if it would leave no ring 
        temp_board = []  
        for outerlist in self._board:
            temp_board.append(list(outerlist))  # save the current board in a temporary variable      

        self.move_and_capture(stone, from_location, to_location)  # make the move

        # change the board back to the previous board, then return False if there would be no ring 
        if not self.has_ring(stone):
            self._board = []
            for outerlist in temp_board:
                self._board.append(list(outerlist))
            return False
        
        # change the board back to the previous board
        self._board = []
        for outerlist in temp_board:
            self._board.append(list(outerlist))  
        
        # 4) not legal to move in such direction that no stone in the corresponding spot on the piece's perimeter
        # 4.1) horizontally
        if from_location_board_row == to_location_board_row:
            # West
            if from_location_board_column > to_location_board_column and self._board[from_location_board_row][from_location_board_column-1] == '':
                return False
            # East  
            if from_location_board_column < to_location_board_column and self._board[from_location_board_row][from_location_board_column+1] == '':
                return False
       
        # 4.2) vertically
        if from_location_board_column == to_location_board_column:
            # North
            if from_location_board_row > to_location_board_row and self._board[from_location_board_row-1][from_location_board_column] == '':
                return False
            # South
            if from_location_board_row < to_location_board_row and self._board[from_location_board_row+1][from_location_board_column] == '':
                return False
        
        # 4.3) West-diagonally
        if from_location_board_column > to_location_board_column:
            # North-West
            if from_location_board_row > to_location_board_row:
                # check if it's 45 degree diagnoal
                if from_location_board_column - to_location_board_column != from_location_board_row - to_location_board_row:
                    return False
                if self._board[from_location_board_row-1][from_location_board_column-1] == '':
                    return False
            # South-West
            if from_location_board_row < to_location_board_row:
                # check if it's 45 degree diagnoal
                if from_location_board_column - to_location_board_column != to_location_board_row - from_location_board_row:
                    return False
                if self._board[from_location_board_row+1][from_location_board_column-1] == '':
                    return False
                
        # 4.4) East-diagonally
        if from_location_board_column < to_location_board_column:
            # North-East
            if from_location_board_row > to_location_board_row:
                # check if it's 45 degree diagnoal
                if to_location_board_column - from_location_board_column != from_location_board_row - to_location_board_row:                    
                    return False
                if self._board[from_location_board_row-1][from_location_board_column+1] == '':
                    return False
            # South-East
            if from_location_board_row < to_location_board_row:
                # check if it's 45 degree diagnoal
                if to_location_board_column - from_location_board_column != to_location_board_row - from_location_board_row:    
                    return False
                if self._board[from_location_board_row+1][from_location_board_column+1] == '':
                    return False

        # 5) not legal to move over 3 squares if the piece center is empty
        if self._board[from_location_board_row][from_location_board_column] == '':  # empty center
            if abs(to_location_board_column - from_location_board_column) > 3 or abs(to_location_board_row - from_location_board_row) > 3:
                return False
        
        # 6) not legal to move when there's obstructed stone in between
        # 6.1) horizontally
        if from_location_board_row == to_location_board_row:
            # West
            if from_location_board_column > to_location_board_column:
                for r in range(from_location_board_row-1, from_location_board_row+2):
                    for c in range(to_location_board_column, from_location_board_column-1):
                        if self._board[r][c] != '':
                            return False          
            # East 
            if from_location_board_column < to_location_board_column:
                for r in range(from_location_board_row-1, from_location_board_row+2):
                    for c in range(from_location_board_column+2, to_location_board_column+1):
                        if self._board[r][c] != '':
                            return False 
                                     
        # 6.2) vertically
        if from_location_board_column == to_location_board_column:
            # North
            if from_location_board_row > to_location_board_row: 
                for r in range(to_location_board_row, from_location_board_row-1):
                    for c in range(from_location_board_column-1, from_location_board_column+2):
                        if self._board[r][c] != '':
                            return False
                                                 
            # South
            if from_location_board_row < to_location_board_row:
                for r in range(from_location_board_row+2, to_location_board_row+1):
                    for c in range(from_location_board_column-1, from_location_board_column+2):
                        if self._board[r][c] != '':
                            return False              
                    
        # 6.3) West-diagonally
        if from_location_board_column > to_location_board_column:
            # North-West
            if from_location_board_row > to_location_board_row:
                mobile_row = from_location_board_row-1
                mobile_column = from_location_board_column-1
                while mobile_row >  to_location_board_row:
                    for r in range(mobile_row-1, mobile_row+2):
                        if self._board[r][mobile_column-1] != '':
                            return False
                    for c in range(mobile_column-1, mobile_column+2):
                        if self._board[mobile_row-1][c] != '':
                            return False
                    mobile_row -= 1
                    mobile_column -= 1                   
            
            # South-West
            if from_location_board_row < to_location_board_row:
                mobile_row = from_location_board_row+1
                mobile_column = from_location_board_column-1
                while mobile_row < to_location_board_row:
                    for r in range(mobile_row-1, mobile_row+2):
                        if self._board[r][mobile_column-1] != '':
                            return False
                    for c in range(mobile_column-1, mobile_column+2):
                        if self._board[mobile_row+1][c] != '':
                            return False
                    mobile_row += 1
                    mobile_column -= 1
                    
        # 6.4) East-diagonally
        if from_location_board_column < to_location_board_column:
            # North-East
            if from_location_board_row > to_location_board_row:
                mobile_row = from_location_board_row-1
                mobile_column = from_location_board_column+1
                while mobile_row >  to_location_board_row:
                    for r in range(mobile_row-1, mobile_row+2):
                        if self._board[r][mobile_column+1] != '':
                            return False
                    for c in range(mobile_column-1, mobile_column+2):
                        if self._board[mobile_row-1][c] != '':
                            return False
                    mobile_row -= 1
                    mobile_column += 1
                    
            # South-East
            if from_location_board_row < to_location_board_row:
                mobile_row = from_location_board_row+1
                mobile_column = from_location_board_column+1
                while mobile_row < to_location_board_row:
                    for r in range(mobile_row-1, mobile_row+2):
                        if self._board[r][mobile_column+1] != '':
                            return False
                    for c in range(mobile_column-1, mobile_column+2):
                        if self._board[mobile_row+1][c] != '':
                            return False
                    mobile_row += 1
                    mobile_column += 1
                  
        return True
    

    def move_and_capture(self, stone, from_location, to_location):
        """
        Takes 3 parameters (stone, from_location, to_location), empties the old piece and restores the same contents in the new 
        piece. Empties out-of-boundary squares.
        Simply return.
        """
        # convert location from the format like 'm3' to 2 integers that repectively represents column and row of the board
        column_lookup_table = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8,
                               'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16,
                               'r': 17, 's': 18, 't': 19}
        
        from_row = from_location[1:]
        from_column = from_location[0]
        from_location_board_row = 20 - int(from_row)
        from_location_board_column = column_lookup_table[from_column]
        
        to_row = to_location[1:]
        to_column = to_location[0]
        to_location_board_row = 20 - int(to_row)
        to_location_board_column = column_lookup_table[to_column]
        
        temp = []       # used to store the old piece
        
        # empty old piece
        for r in range(from_location_board_row-1, from_location_board_row+2):
            for c in range(from_location_board_column-1, from_location_board_column+2):
                temp.append(self._board[r][c])  # save the each square in the temporary list
                self._board[r][c] = ''          # empty each square
        
        # restore the same squares in the new piece
        index_temp = 0 
        for r in range(to_location_board_row-1, to_location_board_row+2):
            for c in range(to_location_board_column-1, to_location_board_column+2):
                self._board[r][c] = temp[index_temp]  # assign each square of the new piece with each square of the old piece
                index_temp += 1
         
        # empty out of boundary
        for i in range(20):
            self._board[0][i] = ''   # empty row '20'
            self._board[19][i] = ''  # empty row '1'
            self._board[i][0] = ''   # empty column 'a'
            self._board[i][19] = ''  # empty column 't'
            
        return


    def has_ring(self, stone):
        """
        Takes stone as parameter, loops through the board to see if there is a ring for the passed stone
        Returns True if there is at least a ring, otherwise False.
        """
        for row in range(19):
            for column in range(19):
                if stone == self._board[row][column] == self._board[row][column+1] == self._board[row][column+2]:
                    if stone == self._board[row+1][column] == self._board[row+1][column+2] and self._board[row+1][column+1] == '':
                        if stone == self._board[row+2][column] == self._board[row+2][column+1] == self._board[row+2][column+2]:
                            return True
        return False


    def get_game_state(self):
        """
        Takes no parameter and returns a GessGame object's game_state
        """
        return self._state
    

    def resign_game(self):
        """ 
        Takes no parameter.
        If the game is finsihed, returns False indicating it's not allowed to resign.
        Otherwise updates game_state as the opponent won the game based on whose turn it currently is, then returns True.
        """
        # if someone already won, no resign is allowed
        if self._state != 'UNFINISHED':
            return False
        
        # check who is the current turn, update game state as the opponent won
        if self._turn == 'black':
            winner = 'white'
        else:
            winner = 'black'
        
        # set game state by calling the set_game_state() method
        self.set_game_state(winner)
        
        return True
                    

    def set_game_state(self, winner):
        """
        Takes a parameter winner and updates game_state.
        No return.
        """
        if winner == 'black':
            self._state = 'BLACK_WON'
        else:
            self._state = 'WHITE_WON'


    def set_turn(self, new_turn):
        """
        Takes a parameter turn and makes it the GessGame object's self._turn.
        No return.
        """
        self._turn = new_turn
  

    def get_turn(self):
        """
        Takes no parameter and returns whose turn it currently is
        """
        return self._turn          

    
    def print_board(self):
        """
        Takes no parameter and displays the board one row at a time.
        Each row is constructed as a string that contains 20 squares being separated by | and a row number added at the end
        No return.
        """
        row_number = 20
        
        for row in self._board:
            print('-' * 81)
            row_string = '| '            # each row_string starts with |
            for stone in row:
                if stone:
                    row_string += stone  # if the square contains a stone, concatenate row_string with the stone
                else:
                    row_string += ' '    # if the square is empty, concatenate row_string with a space
                row_string += ' | '
            print(row_string, end = f'{row_number}\n')
            row_number -= 1
            
        print('-' * 81)
        print('  a    b   c   d   e   f   g   h   i   j   k   l   m   n   o   p   q   r   s   t')


# game = GessGame()
# game.print_board()