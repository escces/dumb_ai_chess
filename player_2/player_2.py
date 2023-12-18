import random

from utils import get_legal_actions
# import xxx    # Here may be other package you want to import

class Player(): # please do not change the class name

    def __init__(self, side: str):
        """
        Variables:
            - self.side: specifies which side your agent takes. It must be "red" or "black".
            - self.history: records history actions.
            - self.move and self.move_back: when you do "search" or "rollout", you can utilize these two methods 
                to simulate the change of the board as the effect of actions and update self.history accordingly.
            - self.name : for you to set a name for your player. It is "Player" by default.

        Methods:
            - policy: the core method for you to implement. It must return a legal action according to the input 
                board configuration. Return values must be a four-element tuple or list in the form 
                of (old_x, old_y, new_x, new_y), with the x coordinate representing the column number 
                and the y coordinate representing the row number.
            - move: simulating movement, moving a piece from (old_x, old_y) to (new_x, new_y) 
                and eating a piece when overlap happens.
            - move_back: restoring the last move. You need to use it when backtracing along a path during a search,
                 so that both the board and self.history are reverted correctly.
        """

        self.side = side    # don't change
        self.opposite_side = "red" if side == "black" else "black"
        self.history = []   # don't change
        self.name = "Player_10"    # please change to your group name

    def policy(self, board: tuple): # the core method for you to implement
        """
        You should complement this method.

        Args:
            - board is a 10×9 matrix, showing current game state.
                board[i][j] > 0 means a red piece is on position (i,j)
                board[i][j] < 0 means a black piece is on position (i,j)
                board[i][j] = 0 means position (i,j) is empty.

        Returns:
            - Your return value is a four-element tuple (i,j,x,y), 
              which means your next action is to move your piece from (i,j) to (x,y).
            Note that your return value must be illegal. Otherwise you will lose the game directly.
        """
        
        # action_list = get_legal_actions(board, self.side, self.history) # get all actions that are legal to choose from
        return self.minimax_root(4, board, True) # LAYERS OF SEARCHING

    def move(self, board, old_x, old_y, new_x, new_y):  # don't change
        """utility function provided by us: simulate the effect of a movement"""

        eaten_id = board[new_x][new_y]
        board[new_x][new_y] = board[old_x][old_y]
        board[old_x][old_y] = 0
        self.history.append((old_x,old_y,new_x,new_y,eaten_id))

    def move_back(self, board, old_x, old_y, new_x, new_y): # don't change
        """utility function provided by us: restore or reverse the effect of a movement"""

        board[old_x][old_y] = board[new_x][new_y]
        board[new_x][new_y] = self.history[-1][4]
        self.history.pop()

    def update_history(self, current_game_history: list): 
        """to refresh your self.history after each actual play, which is taken care externally"""

        self.history = current_game_history
        
    def get_name(self):
        """used by the external logger"""

        return self.name
    def debug(self, board):
        conv_str=["將","車","砲","馬","象","士","卒","　","兵","仕","相","傌","炮","俥","帥"]
        for row in board:
            for item in row:
                print(conv_str[item+7], end="")
            print("")

    def minimax(self, depth, board, alpha, beta, is_maximizing: bool) :
        # positionCount += 1
        if depth == 0:
            return self.evaluate_board(board)
        k = 0
        for row in board:
            if 7 in row or -7 in row:
                k += 1
        if k < 2:
            return self.evaluate_board(board)
        
        new_game_moves = get_legal_actions(board, self.side if is_maximizing else self.opposite_side, self.history)
        
        if not new_game_moves:
            if is_maximizing:
                return -9999
            else:
                return 9999

        # print("here depth="+str(depth))
        # self.debug(board)

        if is_maximizing :
            best_move = -9999
            for move in new_game_moves:
                self.move(board, move[0], move[1], move[2], move[3])

                # print("moved")
                # self.debug(board)

                best_move = max(best_move, self.minimax(depth - 1, board, alpha, beta, not is_maximizing))

                # print("best"+str(best_move)+"unmoved")
                # self.debug(board)

                self.move_back(board, move[0], move[1], move[2], move[3])
                alpha = max(alpha, best_move)
                if beta <= alpha:
                    # print("pruned!")
                    return best_move
            return best_move
        else:
            best_move = 9999
            for move in new_game_moves:
                self.move(board, move[0], move[1], move[2], move[3])

                # print("moved")
                # self.debug(board)

                best_move = min(best_move, self.minimax(depth - 1, board, alpha, beta, not is_maximizing))

                
                # print("best: "+str(best_move)+" ,unmoved")
                # self.debug(board)

                self.move_back(board, move[0], move[1], move[2], move[3])
                beta = min(beta, best_move)
                if beta <= alpha:
                    # print("pruned!")
                    return best_move
            return best_move


    def minimax_root(self, depth, board, is_maximizing):
        new_game_moves = get_legal_actions(board, self.side, self.history)
        bestMove = -9999
        # bestMoveFound
        for new_game_move in new_game_moves:
            self.move(board, new_game_move[0], new_game_move[1], new_game_move[2], new_game_move[3])
            value = self.minimax(depth-1, board, -10000, 10000, not is_maximizing)
            self.move_back(board, new_game_move[0], new_game_move[1], new_game_move[2], new_game_move[3])
            if value >= bestMove:
                # print(value)
                # self.debug(board)
                bestMove = value
                bestMoveFound = new_game_move
        return bestMoveFound


    def evaluate_board(self, board):
        total_eval = 0
        for i in range(10):
            for j in range(9):
                total_eval = total_eval + self.get_piece_value(board[i][j], i ,j)
                # print (total_eval) ## debug
        return total_eval
    
    def get_piece_value(self, piece: int, x, y):
        if piece == 0:
            return 0
        absolute_value = piece_self_value[abs(piece)] + (pos_value[abs(piece)-1][x][y] if piece > 0 else pos_value[abs(piece)-1][8-x][y])
        return absolute_value if (piece < 0 and self.side == "black") or (piece > 0 and self.side == "red") else -absolute_value

piece_self_value = [0, 10, 20, 20, 49, 52, 100, 1000]
pos_value = [
    [# 兵
        [ -2.0, -1.5, -1.0, -1.0, -1.0, -1.0, -1.0, -1.5, -2.0],
        [  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0],
        [  1.0,  1.0,  4.0,  4.0,  4.0,  4.0,  4.0,  1.0,  1.0],
        [  1.0,  2.0,  4.0,  2.0,  3.0,  2.0,  3.0,  2.0,  1.0],
        [  3.0,  2.0,  3.0,  3.0,  3.0,  3.0,  3.0,  2.0,  3.0],
        [ -0.1,  0.0, -0.1,  0.0, -0.5,  0.0, -0.1,  0.0, -0.1],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
    ],
    [ #士,
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  3.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
    ],
    [ #象
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0, -1.0,  0.0,  0.0,  0.0, -1.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [ -1.0,  0.0,  0.0,  0.0,  3.0,  0.0,  0.0,  0.0, -1.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
    ],
    [ #马
        [ -5.0, -4.0,  0.0,  0.0,  0.0,  0.0,  0.0, -4.0, -5.0],
        [ -4.0, -2.0,  2.0,  0.0,  0.0,  0.0,  2.0, -2.0, -4.0],
        [  0.0,  3.0,  3.0,  3.0,  2.0,  3.0,  3.0,  3.0,  0.0],
        [  0.0,  3.0,  3.0,  3.0,  3.0,  3.0,  3.0,  3.0,  0.0],
        [  0.0,  3.0,  3.0,  3.0,  2.0,  3.0,  3.0,  3.0,  0.0],
        [  0.0,  1.0,  1.0,  2.0,  2.0,  2.0,  1.0,  1.0,  0.0],
        [  0.0,  1.0,  1.0,  1.0,  2.0,  1.0,  1.0,  1.0,  0.0],
        [  0.0,  1.0,  1.0,  1.0,  2.0,  1.0,  1.0,  1.0,  0.0],
        [ -4.0, -2.0,  0.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
        [ -5.0, -4.0,  0.0,  0.0,  0.0,  0.0,  0.0, -4.0, -5.0]
    ],
    [# 炮
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  3.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
    ],
    [ # 车
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  4.0,  0.0],
        [  0.0,  3.0,  3.0,  3.0,  3.0,  3.0,  3.0,  3.0,  0.0],
        [  0.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  0.0],
        [  0.0,  1.5,  1.5,  1.5,  1.5,  1.5,  1.5,  1.5,  0.0],
        [  0.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.0],
        [  0.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
    ],
    [  #王
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0, -1.0, -1.0, -1.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0, -1.0, -1.0, -1.0,  0.0,  0.0,  0.0],
        [  0.0,  0.0,  0.0, -1.0,  1.0, -1.0,  0.0,  0.0,  0.0]
    ]
]