import numpy as np
import math
import time
import sys
from dict import *
global_width = 15
global_height = 15

# Gomoku board class
class Board():
    # create constructor (init board class instance)
    def __init__(self, board=None, width = 15, height = 15, play_first = "human"):
        # define players, NO SWAP
        if(play_first =="human"):
            self.player_1 = 1 #'x'
            self.player_2 = -1 #'o', player 2 always computer
        else:
            self.player_1 = -1 # 'o'
            self.player_2 = 1  # 'x'

        self.empty_square = 0 #'.'
        self.width = width
        self.height = height
        # define board position
        self.position = np.zeros((self.height,self.width))



    
    # make move
    def make_move(self, row, col, player):
        # create new board instance that inherits from the current state
        # make move
        self.position[row, col] = player



    # get whether the game is drawn
    def is_draw(self):
        # loop over board squares
        if(np.sum(np.abs(self.position))==self.width*self.height):
            return True
        return False
    
    # get whether the game is won
    def is_win(self):
        board = self.position
        for i in range(self.height):
            for j in range(self.width):
                if j >= 2 and j < self.width - 2:
                    row_sum = np.sum(board[i, j - 2:j + 3])
                    if row_sum == 5 or row_sum == -5:
                        return True
                if i >= 2 and i < self.height - 2:
                    col_sum = np.sum(board[i - 2:i + 3, j])
                    if col_sum == 5 or col_sum == -5:
                        return True
                if i >= 2 and i < self.height - 2 and j >= 2 and j < self.width - 2:
                    diagonal1 = board[i - 2:i + 3, j - 2:j + 3]
                    diagonal2 = board[i - 2:i + 3, j + 2:j - 3:-1]
                    diagonal1_sum = np.sum(np.diagonal(diagonal1))
                    diagonal2_sum = np.sum(np.diagonal(diagonal2))
                    if diagonal1_sum == 5 or diagonal1_sum == -5 or diagonal2_sum == 5 or diagonal2_sum == -5:
                        return True
        return False

    # check if position is satisfied
    def satify_position(self, row,col):
        # Not be occupied
        if(self.position[row, col]!=self.empty_square):
            return False
        up = max(0, row-2)
        left = max(0, col-2)
        down=min(self.height, row+3)
        right = min(self.width, col+3)

        # Go not too far
        if(np.trace(np.abs(np.fliplr(self.position[up:down,left:right])))<1 and np.trace(np.abs(self.position[up:down,left:right]))<1
            and np.sum(np.abs(self.position[up:down,col]))<1 and np.sum(np.abs(self.position[row, left:right]))<1):
            return False
        return True

    # get heuristic value 
    def heuristic_value(self, min_height= 0 , min_width = 0, max_height =global_height, max_width = global_width, intense=False):
        # Save current status
        # Loop through every element
        # Sequence: Radius, direction, check
        if not intense:
            score = np.sum([self.check_in_current_pos(i, j) for i in range(min_height,max_height) for j in range(min_width,max_width)])
        else:
            # Get center
            score = 0
            center_x = math.floor((max_width+min_width)/2)
            center_y = math.floor((max_height+min_height)/2)
            for i in range(min_height,max_height):
                for j in range(min_width, max_width):
                    if(i!= center_y and j != center_x and abs(i*1.0/center_y)!=abs(j*1.0/center_x)):
                        continue
                    else:
                        score+= self.check_in_current_pos(i, j)
        # Score is prefer for player_1
       
        return score


    # print(''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in self.position[ i - 2:i + 3,j].reshape((-1,))))
    def get_score_from_dict(self, temp, best_score, worst_score):
        if (temp in PB_MY_HEURISTICS_DICT ):
            if PB_MY_HEURISTICS_DICT[temp] > best_score:
                best_score = PB_MY_HEURISTICS_DICT[temp]
            if (PB_MY_HEURISTICS_DICT[temp] < worst_score):
                worst_score = PB_MY_HEURISTICS_DICT[temp]
        elif (temp[::-1] in PB_MY_HEURISTICS_DICT):
            if PB_MY_HEURISTICS_DICT[temp[::-1]] > best_score:
                best_score = PB_MY_HEURISTICS_DICT[temp[::-1]]
            if PB_MY_HEURISTICS_DICT[temp[::-1]] < worst_score:
                worst_score = PB_MY_HEURISTICS_DICT[temp[::-1]]

        return best_score, worst_score
    def check_in_current_pos(self, i, j, intense=False):
        if not intense:
            a = max(0,i-2)
            b =min(self.height,i+2)
            c= max(0,j-2)
            d =min(self.width,j+2)
            if np.sum(self.position[a:b,c:d])==0:
                return 0
        # if intense:
        #     a = max(0, i - 6)
        #     b = min(self.height, i + 7)
        #     c = max(0, j - 6)
        #     d = min(self.width, j + 7)
        #     return self.check_in_current_pos()
        best_honri = 0
        best_verti = 0
        best_diag = 0
        best_diagfl = 0

        worst_honri = 0
        worst_verti = 0
        worst_diag = 0
        worst_diagfl = 0

        # i mean honri, j mean verti (sorry...)
        if (i >= 2 and i + 2 <= self.height - 1):

            temp = self.position[i - 2:i + 3, j].reshape((-1,))
            temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            best_honri, worst_honri = self.get_score_from_dict(temp,best_honri, worst_honri)

        if (i >= 2 and i + 3 <= self.height - 1):
            temp = self.position[i - 2:i + 4, j].reshape((-1,))
            temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            best_honri, worst_honri = self.get_score_from_dict(temp,best_honri, worst_honri)

        if (i >= 3 and i + 3 <= self.height - 1):
            temp = self.position[i - 3:i + 4, j].reshape((-1,))
            temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            best_honri, worst_honri = self.get_score_from_dict(temp,best_honri, worst_honri)

        if (j >= 2 and j + 2 <= self.width - 1):
            temp = self.position[i, j - 2:j + 3].reshape((-1,))
            temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            best_verti, worst_verti = self.get_score_from_dict(temp,best_verti, worst_verti)

        if (j >= 2 and j + 3 <= self.width - 1):
            temp = self.position[i, j - 2:j + 4].reshape((-1,))
            temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            best_verti, worst_verti = self.get_score_from_dict(temp,best_verti, worst_verti)

        if (j >= 3 and j + 3 <= self.width - 1):
            temp = self.position[i, j - 3:j + 4].reshape((-1,))
            temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            best_verti, worst_verti = self.get_score_from_dict(temp,best_verti, worst_verti)

        if (j >= 2 and i >= 2 and j + 2 <= self.width - 1 and i + 2 <= self.height - 1):
            temp = np.diag(self.position[i - 2:i + 3, j - 2:j + 3]).reshape((-1,))
            temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            best_diag, worst_diag = self.get_score_from_dict(temp,best_diag, worst_diag)

        if (j >= 2 and i >= 2 and j + 3 <= self.width - 1 and i + 3 <= self.height - 1):
            temp = np.diag(self.position[i - 2:i + 4, j - 2:j + 4]).reshape((-1,))
            temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            best_diag, worst_diag = self.get_score_from_dict(temp,best_diag, worst_diag)

        if (j >= 3 and i >= 3 and j + 3 <= self.width - 1 and i + 3 <= self.height - 1):
            temp = np.diag(self.position[i - 3:i + 4, j - 3:j + 4]).reshape((-1,))
            temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            best_diag, worst_diag = self.get_score_from_dict(temp,best_diag, worst_diag)

        if (j >= 2 and i >= 2 and j + 2 <= self.width - 1 and i + 2 <= self.height - 1):
            temp = np.diag(np.fliplr(self.position[i - 2:i + 3, j - 2:j + 3])).reshape((-1,))
            temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            best_diagfl, worst_diagfl = self.get_score_from_dict(temp,best_diagfl, worst_diagfl)

        if (j >= 2 and i >= 2 and j + 3 <= self.width - 1 and i + 3 <= self.height - 1):
            temp = np.diag(np.fliplr(self.position[i - 2:i + 4, j - 2:j + 4])).reshape((-1,))
            temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)

            best_diagfl, worst_diagfl = self.get_score_from_dict(temp,best_diagfl, worst_diagfl)


        if (j >= 3 and i >= 3 and j + 3 <= self.width - 1 and i + 3 <= self.height - 1):
            temp = np.diag(np.fliplr(self.position[i - 3:i + 4, j - 3:j + 4])).reshape((-1,))
            temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            best_diagfl, worst_diagfl = self.get_score_from_dict(temp,best_diagfl, worst_diagfl)

        # if intense:
            # # 10h
            # if (i >= 6 and j >= 6):
            #     temp = np.diag(self.position[i - 6:i + 1, j - 6:j+1]).ravel()
            #     temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            #     best_diag, worst_diag = self.get_score_from_dict(temp, best_diag, worst_diag)
            #
            # if (i >= 5 and j >= 5):
            #     temp = np.diag(self.position[i - 5:i + 1, j - 5:j+1]).ravel()
            #     temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            #     best_diag, worst_diag = self.get_score_from_dict(temp, best_diag, worst_diag)
            #
            # if (i >= 4 and j >= 4):
            #     temp = np.diag(self.position[i - 4:i + 1, j - 4:j+1]).ravel()
            #     temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            #     best_diag, worst_diag = self.get_score_from_dict(temp, best_diag, worst_diag)
            #
            #
            # # 12h
            # # i mean honri, j mean verti (sorry...)
            # if (i>=6):
            #     temp = self.position[i - 6:i + 1, j ].ravel()
            #     temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            #     best_honri, worst_honri = self.get_score_from_dict(temp, best_honri, worst_honri)
            #
            # if (i >= 5):
            #     temp = self.position[i - 5:i + 1, j].ravel()
            #     temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            #     best_honri, worst_honri = self.get_score_from_dict(temp, best_honri, worst_honri)
            #
            # if (i >= 4):
            #     temp = self.position[i - 4:i + 1, j].ravel()
            #     temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            #     best_honri, worst_honri = self.get_score_from_dict(temp, best_honri, worst_honri)
            # # 2h
            # if (i>=6 and j<=self.width-6-1):
            #     temp = np.diag(np.fliplr(self.position[i - 6:i + 1, j :j + 7])).ravel()
            #     temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            #     best_diagfl, worst_diagfl = self.get_score_from_dict(temp, best_diagfl, worst_diagfl)
            #
            # if (i >= 5 and j <= self.width - 5 - 1):
            #     temp = np.diag(np.fliplr(self.position[i - 5:i + 1, j:j + 6])).ravel()
            #     temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            #     best_diagfl, worst_diagfl = self.get_score_from_dict(temp, best_diagfl, worst_diagfl)
            #
            # if (i >= 4 and j <= self.width - 4 - 1):
            #     temp = np.diag(np.fliplr(self.position[i - 4:i + 1, j:j + 5])).ravel()
            #     temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            #     best_diagfl, worst_diagfl = self.get_score_from_dict(temp, best_diagfl, worst_diagfl)
            #
            # # 3h
            #
            # if(j<= self.width - 6-1):
            #     temp = self.position[i, j :j + 7].ravel()
            #     temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            #     best_verti, worst_verti = self.get_score_from_dict(temp, best_verti, worst_verti)
            #
            # if(j<=self.width -5-1):
            #     temp = self.position[i, j:j + 6].ravel()
            #     temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            #     best_verti, worst_verti = self.get_score_from_dict(temp, best_verti, worst_verti)
            #
            # if( j<= self.width - 4- 1):
            #     temp = self.position[i, j:j + 5].ravel()
            #     temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            #     best_verti, worst_verti = self.get_score_from_dict(temp, best_verti, worst_verti)
            #
            # # 4h
            # if (i<= self.height - 6-1 and j<= self.width - 6-1):
            #     temp = np.diag(self.position[i : i + 7, j: j +7]).ravel()
            #     temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            #     best_diag, worst_diag = self.get_score_from_dict(temp, best_diag, worst_diag)
            #
            # if (i<= self.height - 5-1 and j<= self.width - 5-1):
            #     temp = np.diag(self.position[i : i + 6, j: j +6]).ravel()
            #     temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            #     best_diag, worst_diag = self.get_score_from_dict(temp, best_diag, worst_diag)
            #
            # if (i<= self.height - 4-1 and j<= self.width - 4-1):
            #     temp = np.diag(self.position[i : i + 5, j: j +5]).ravel()
            #     temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            #     best_diag, worst_diag = self.get_score_from_dict(temp, best_diag, worst_diag)
            #
            # # 6h
            # if (i<= self.height - 6-1):
            #     temp = self.position[i :i +7, j ].ravel()
            #     temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            #     best_honri, worst_honri = self.get_score_from_dict(temp, best_honri, worst_honri)
            #
            # if (i<= self.height - 5-1):
            #     temp = self.position[i :i +6, j].ravel()
            #     temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            #     best_honri, worst_honri = self.get_score_from_dict(temp, best_honri, worst_honri)
            #
            # if (i<= self.height - 4-1):
            #     temp = self.position[i :i +5, j].ravel()
            #     temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            #     best_honri, worst_honri = self.get_score_from_dict(temp, best_honri, worst_honri)
            #
            # # 8h
            # if (j>=6 and i<=self.height-6-1):
            #     temp = np.diag(np.fliplr(self.position[i:i+7, j-6: j+1])).ravel()
            #     temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            #     best_diagfl, worst_diagfl = self.get_score_from_dict(temp, best_diagfl, worst_diagfl)
            #
            # if (j >= 5 and i <= self.height - 5 - 1):
            #     temp = np.diag(np.fliplr(self.position[i:i+6, j-5: j+1])).ravel()
            #     temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            #     best_diagfl, worst_diagfl = self.get_score_from_dict(temp, best_diagfl, worst_diagfl)
            #
            # if (j >= 4 and i <= self.height - 4 - 1):
            #     temp = np.diag(np.fliplr(self.position[i:i+5, j-4: j+1])).ravel()
            #     temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            #     best_diagfl, worst_diagfl = self.get_score_from_dict(temp, best_diagfl, worst_diagfl)
            #
            # # 9h
            # if (j >=6):
            #     temp = self.position[i, j-6:j + 1].ravel()
            #     temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            #     best_verti, worst_verti = self.get_score_from_dict(temp, best_verti, worst_verti)
            #
            # if (j >=5):
            #     temp = self.position[i, j-5:j + 1].ravel()
            #     temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            #     best_verti, worst_verti = self.get_score_from_dict(temp, best_verti, worst_verti)
            #
            # if (j >=4):
            #     temp = self.position[i, j-4:j + 1].ravel()
            #     temp = ''.join(('o' if i == self.player_1 else 'x' if i == self.player_2 else '-') for i in temp)
            #     best_verti, worst_verti = self.get_score_from_dict(temp, best_verti, worst_verti)


        best_honri = max(0, best_honri)
        best_verti = max(0, best_verti)
        best_diag = max(0, best_diag)
        best_diagfl = max(0, best_diagfl)
        worst_honri = min(0, worst_honri)
        worst_verti = min(0, worst_verti)
        worst_diag = min(0, worst_diag)
        worst_diagfl = min(0, worst_diagfl)
        max_best = max(best_diag,best_verti,best_diagfl,best_honri)
        min_worst = min(worst_diag,worst_diagfl,worst_verti,worst_honri)
        # New:
        if(min_worst<=-10000 and max_best<=10000):
            return -10000

        return best_honri + best_verti + best_diag + best_diagfl + worst_honri + worst_verti + worst_diag + worst_diagfl

    def get_available_move(self):
        # Get best move for player 2
        # 1. Get available moves
        moves = []
        for i in range(self.height):
            for j in range(self.width):
                if self.satify_position(i,j):
                    moves.append((i,j))
        return moves

    def get_score_for_moves(self, moves, player, lite=False):
        scores = np.array([])
        # for i,j in moves:
        #     self.position[i,j]=player
        #     if not lite:
        #         post_score= self.heuristic_value()
        #     else:
        #         post_score= self.check_in_current_pos(i,j,intense=True)
        #
        #     scores = np.append(scores, post_score)
        #
        #
        #     self.position[i,j] = self.empty_square

        init_heu = self.heuristic_value()
        for i,j in moves:
            a = max(0, i - 6)
            b = min(self.height, i + 7)
            c = max(0, j - 6)
            d = min(self.width, j + 7)
            init_score = self.heuristic_value(a,c,b,d,intense=True)
            self.position[i,j]=player
            post_score = self.heuristic_value(a,c,b,d,intense=True)
            if(post_score<=-10000):
                scores = np.append(scores, init_heu+post_score)
            else:
                scores = np.append(scores, init_heu-init_score+post_score)
            self.position[i, j] = self.empty_square
        return scores

    def get_best_move(self,depth):
        # Auto get best move
        players = [self.player_1, self.player_2]
        idx = 1 # Player 2 first in get move
        moves = self.get_available_move()
        moves_score = np.array([])
        for i,j in moves:
            
            next_moves = [(i,j)]
            self.position[i,j] = players[idx]
            init_heu_value = self.heuristic_value()
            move_score =  init_heu_value
          
            idx = 1-idx
            for d in range(depth):

                # check cond
                if self.is_win() or self.is_draw():
                    break
                # get move with highest score
                depth_avai_move = self.get_available_move()

                depth_scores = self.get_score_for_moves(depth_avai_move,players[idx], lite=False)

                # depth_scores+=init_heu_value
                if players[idx] == self.player_1:
                    move_position = np.argmax(depth_scores)
                else:
                    move_position = np.argmin(depth_scores)
                # move
                row, col = depth_avai_move[move_position]
                self.position[row,col] = players[idx]
                # append to next moves to delete afternath
                next_moves.append((row,col))
                # cumulate score
                if players[idx] == self.player_1:
                    move_score+= depth_scores[move_position]
               
                idx = 1-idx
            moves_score = np.append(moves_score, move_score)
            # get board like before
            for row, col in next_moves:
                self.position[row,col] = self.empty_square

        #reshape
        # scores_log = scores_log.reshape((-1,depth+1))
     
        return moves[np.argmin(moves_score)]

        # 3. Return



    # main game loop
    def game_loop(self):


        print('  Type "exit" to quit the game')
        print('  Move format [x,y]: 1,2 where 1 is column and 2 is row')
        init_play_first = int(input("1 to play first, 0 to let computer play first "))
        players = [self.player_1, self.player_2]
        idx = 0
        if(init_play_first==0):
            idx = 0
            # Init
            self.player_1= -1
            self.player_2=1
            # Get move in center
            self.position[round(self.height/2), round(self.width/2)] = players[idx]
            idx = 1- idx
        else:
            self.player_1=1
            self.player_2=-1
            idx =0
        
        # print board
        print(self)

       
        count = 0
        # game loop
        while True:
            # get user input
            user_input = input('> ')
        
            # escape condition
            if user_input == 'exit': break
            
            # skip empty input
            if user_input == '': continue
            count+=1
            try:

                # parse user input (move format [col, row]: 1,2)
                row = int(user_input.split(',')[0])
                col = int(user_input.split(',')[1])

                # check move legality
                if self.position[row, col] != self.empty_square:
                    print(' Illegal move!')
                    continue

                # make move on board
                self.make_move(row, col, players[idx])
                idx = 1-idx


                if self.is_win():
                    print('player "%s" has won the game!\n' % self.player_2)
                    break
                if self.is_draw():
                    print("Game draw")
                    break
                start = time.time()
                # search for the best move
                best_move_row, best_move_col = self.get_best_move(depth=3)
                print("Time: ", time.time()-start)
                # legal moves available
                try:
                    # make AI move here
                    self.make_move(best_move_row,best_move_col, players[idx])
                    idx= 1-idx

                # game over
                except:
                    pass


                # print board
                print(self)


                # check if the game is won
                if self.is_win():
                    print('player "%s" has won the game!\n' % self.player_2)
                    break

                # check if the game is drawn
                elif self.is_draw():
                    print('Game is drawn!\n')
                    break
            
            except Exception as e:
                print('  Error:', e)
                print('  Illegal command!')
                print('  Move format [x,y]: 1,2 where 1 is column and 2 is row')

    # print board state
    def __str__(self):
        # define board string representation
        board_string = '  0 1 2 3 4 5 6 7 8 9 1011121314\n'
        str = ' 0123456789      '
        # loop over board rows
        for row in range(self.height):
            board_string +=str[row+1]
            # loop over board columns
            for col in range(self.width):
                if self.position[row, col]==1:
                    board_string += ' %s' % 'x'
                elif self.position[row, col]==-1:
                    board_string += ' %s' % 'o'
                else:
                    board_string += ' %s' % '.'
            
            # print new line every row
            board_string += '\n'
        
        # prepend side to move
        if self.player_1 == 1:
            board_string = '\n--------------\n "x" to move:\n--------------\n\n' + board_string
        
        elif self.player_1 == -1:
            board_string = '\n--------------\n "o" to move:\n--------------\n\n' + board_string
                        
        # return board string
        return board_string

    
    
        
        
        
    
    
    
    
    
    
    
    
