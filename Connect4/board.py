import time
from copy import deepcopy
import DefaultOpponent
from random import choice
from sys import exit as sys_exit
from numpy import NINF, flip, random, zeros
from pygame import MOUSEBUTTONDOWN, MOUSEMOTION, QUIT, display, draw
from pygame import event as pygame_event
from pygame import font
from pygame import init as pygame_init
from pygame import time as pygame_time
from alpha_beta_pruning import (Q_children, best_move, children, minimax,
                                moves, static)

# Constants
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)


class Connect4:
    '''Some methods assume that the board has a 5 X 5 size'''

    def __init__(self, nb_rows=5, nb_cols=5):
        self.rows = nb_rows
        self.cols = nb_cols
        self.board = zeros((nb_rows, nb_cols))
        self.game_over = False
        self.turn = 0
        self.winner = None

    def play_move(self, row, col, piece):
        self.board[row][col] = piece

    def move_is_valid(self, col):
        return self.board[self.rows-1][col] == 0

    def get_available_row(self, col):
        for r in range(self.rows):
            if self.board[r][col] == 0:
                return r

    def print_board(self):
        '''Flips the board to match the real game'''
        print(flip(self.board, 0))

    def check_wins(self, piece):
        # Check horizontal locations for win
        for c in range(self.cols-3):
            for r in range(self.rows):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(self.cols):
            for r in range(self.rows-3):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(self.cols-3):
            for r in range(self.rows-3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(self.cols-3):
            for r in range(3, self.rows):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    return True

    def draw_board(self, screen):
        height = (self.rows+1) * SQUARESIZE

        for c in range(self.cols):
            for r in range(self.rows):
                draw.rect(
                    screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
                draw.circle(screen, BLACK, (int(
                    c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

        for c in range(self.cols):
            for r in range(self.rows):
                if self.board[r][c] == 1:
                    draw.circle(screen, RED, (int(
                        c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
                elif self.board[r][c] == 2:
                    draw.circle(screen, YELLOW, (int(
                        c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
        display.update()

    def play(self):
        '''Allows you to play as Player 2 against Minimax'''

        pygame_init()

        width = self.cols * SQUARESIZE
        height = (self.rows+1) * SQUARESIZE
        size = (width, height)

        screen = display.set_mode(size)
        self.draw_board(screen)
        display.update()

        myfont = font.Font('sweet purple.ttf', 75)

        while not self.game_over:
            i =0
            for event in pygame_event.get():
                if event.type == QUIT:
                    sys_exit()
                if event.type == MOUSEMOTION:
                    draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    posx = event.pos[0]
                    if self.turn == 0:
                        col = best_move(self)
                        row = self.get_available_row(col)
                        self.play_move(row, col, 1)

                        if self.check_wins(1):
                            label = myfont.render("Minimax wins!", 1, RED)
                            screen.blit(label, (width/4, 10))
                            self.game_over = True
                            self.draw_board(screen)
                            break
                        self.draw_board(screen)
                        self.turn = 1 - self.turn

                    else:
                        draw.circle(
                            screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
                    display.update()

                if event.type == MOUSEBUTTONDOWN:
                    draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

                    # Asks for Player's input
                    if not self.turn:
                        # Turn = 0
                        pass

                    else:
                        # Turn = 1
                        posx = event.pos[0]
                        col = int(posx/SQUARESIZE)
                        if self.move_is_valid(col):
                            row = self.get_available_row(col)
                            self.play_move(row, col, 2)

                            if self.check_wins(2):
                                label = myfont.render(
                                    "Player wins!", 1, YELLOW)
                                screen.blit(label, (width/4, 10))
                                self.game_over = True
                                self.draw_board(screen)
                                break

                        self.draw_board(screen)
                        self.turn = 1 - self.turn

        pygame_time.wait(5000)

    def board_to_string(self):
        ''' Returns ndarray board as string'''
        s = ''

        for row in range(self.rows):
            for col in range(self.cols):
                s += str(int(self.board[row][col]))

        return s

    def string_to_board(self, board_string):
        ''' Transforms board string into ndarray'''
        for row in range(self.rows):
            for col in range(self.cols):
                self.board[row][col] = float(board_string[self.cols*row+col])

    def train_q_learning(self, qdict, eps_0):
        '''Modifies winner attribute'''
        ALPHA = 0.5
        GAMMA = 0.9
        while not self.game_over:
            hasExplored = False
            if not self.turn:
                # Minimax plays as Player 1
                col = self.default_opponent_move(self,self.turn)
                row = self.get_available_row(col)
                self.play_move(row, col, 1)
                if self.check_wins(1):
                    self.game_over = True
                    self.winner = 0
                self.turn = 1
            else:
                # Chosen move has the highest q-value
                state = self.board_to_string()
                coups = moves(self)
                minimax_moves = Q_children(self)[1]

                max_q_value = NINF
                chosen_column = 0

                try:
                    qdict[state]
                except:
                    # State gets added to the table 
                    qdict[state] = [0]*self.cols

                # Current state q-value
                Q_list = deepcopy(qdict[state])
                # Random number to allow some exploitation
                eps = random.uniform(0, 1)

                if eps < eps_0:
                    # Exploration
                    hasExplored = True
                    chosen_column = choice(list(coups))
                else:
                    # Exploitation
                    for col in range(self.cols):
                        if col not in coups:
                            Q_list[col] = NINF
                    chosen_column = Q_list.index(max(Q_list))

                previous_q_value = (1-ALPHA)*Q_list[chosen_column]

                # Q-Agent plays
                row = self.get_available_row(chosen_column)
                self.play_move(row, chosen_column, 2)
                self.turn = 0

                if self.check_wins(2):
                    # Checks for Q-Agent's victory
                    qdict[state][chosen_column] = 1
                    self.winner = 1
                    self.game_over = True
                elif not minimax_moves:
                    self.game_over = True
                    reward = 1/42
                    if not hasExplored:
                        update_value = previous_q_value + ALPHA*reward
                        qdict[state][chosen_column] = float(
                            f'{update_value:.5f}')
                else:
                    move = minimax_moves[str(chosen_column)]
                    row = self.get_available_row(move)
                    self.play_move(row, move, 1)
                    self.turn = 1
                    if self.check_wins(1):
                        # Checks for Minimax's victory
                        qdict[state][chosen_column] = -1
                        self.winner = 0
                        self.game_over = True
                    else:
                        # Computes the estimate of optimal future value
                        try:
                            max_q_value = max(
                                [qdict[self.board_to_string()][col] for col in moves(self)])
                        except:
                            qdict[state] = [0]*self.cols
                            max_q_value = 0
                        reward = 1/42
                        if not hasExplored:
                            update_value = previous_q_value + ALPHA*reward + ALPHA*GAMMA*max_q_value
                            qdict[state][chosen_column] = float(
                                f'{update_value:.5f}')

    def minimax_vs_q_play(self, qdict):
        '''Allows you to play as Player 1 against our trained model'''
        winner = 0  # 0- draw, 1 - minimax, 2- Qlearning
        pygame_init()

        width = self.cols * SQUARESIZE
        height = (self.rows+1) * SQUARESIZE
        size = (width, height)

        screen = display.set_mode(size)
        self.draw_board(screen)
        display.update()
        q_time = 0
        minmax_time = 0

        myfont = font.Font('sweet purple.ttf', 75)

        while not self.game_over:
            if "0" not in self.board_to_string():
                label = myfont.render("It's a Draw", 1, BLUE)
                screen.blit(label, (width / 4, 10))
                self.draw_board(screen)
                winner = 0
                break
            # for event in pygame_event.get():
            #     if event.type == QUIT:
            #         sys_exit()
            draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            if self.turn == 1:
                start  = time.process_time()
                state = self.board_to_string()

                try:
                    score = qdict[state]
                    if(max(score) == 0):
                        for i in range(len(score)):
                            if(self.move_is_valid(i)):
                                col = i
                    else:
                        col = score.index(max(score))
                except:
                    col = choice(list(moves(self)))

                row = self.get_available_row(col)
                self.play_move(row, col, 2)
                q_time += time.process_time() - start
                if self.check_wins(2):
                    label = myfont.render("Q-Agent wins!", 1, YELLOW)
                    screen.blit(label, (width / 4, 10))
                    self.game_over = True
                    self.draw_board(screen)
                    winner = 2
                    break
                self.draw_board(screen)
                self.turn = 1 - self.turn
                # display.update()
                time.sleep(0.1)
            else:
                start = time.process_time()
                col = best_move(self)
                row = self.get_available_row(col)
                self.play_move(row, col, 1)
                minmax_time += time.process_time() - start
                if self.check_wins(1):
                    label = myfont.render("Minimax wins!", 1, RED)
                    screen.blit(label, (width / 4, 10))
                    self.game_over = True
                    self.draw_board(screen)
                    winner = 1
                    break

                self.draw_board(screen)
                self.turn = 1 - self.turn
                time.sleep(0.1)

        pygame_time.wait(2000)
        return winner, q_time, minmax_time

    
   

    def default_opponent_move(self, connect4, turn):
        if(turn == 0):
            other_player = 2
        else:
            other_player = 1
        for col in range(connect4.cols):
            row = connect4.get_available_row(col)
            if row is None:
                continue
            connect4.board[row][col] = turn+1
            if connect4.check_wins(turn+1):
                connect4.board[row][col] = 0
                return col
            connect4.board[row][col] = 0

        # If no winning move, block the opponent's winning move
        for col in range(connect4.cols):
            row = connect4.get_available_row(col)
            if row is None:
                continue
            connect4.board[row][col] = other_player
            if connect4.check_wins(other_player):
                connect4.board[row][col] = 0
                return col
            connect4.board[row][col] = 0

        # If no winning or blocking move, choose a random column
        return choice(list(moves(self)))


    def default_vs_q_play(self, qdict):
        '''Allows you to play as Player 1 against our trained model'''
        winner = 0  # 0- draw, 1 - minimax, 2- Qlearning
        pygame_init()

        width = self.cols * SQUARESIZE
        height = (self.rows+1) * SQUARESIZE
        size = (width, height)
        q_time = 0
        default_time = 0

        screen = display.set_mode(size)
        self.draw_board(screen)
        display.update()

        myfont = font.Font('sweet purple.ttf', 75)

        while not self.game_over:
            if "0" not in self.board_to_string():
                label = myfont.render("It's a Draw", 1, BLUE)
                screen.blit(label, (width / 4, 10))
                self.draw_board(screen)
                winner = 0
                break
            # for event in pygame_event.get():
            #     if event.type == QUIT:
            #         sys_exit()
            draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            if self.turn == 1:
                start = time.process_time()
                state = self.board_to_string()

                try:
                    score = qdict[state]
                    if(max(score) == 0):
                        for i in range(len(score)):
                            if(self.move_is_valid(i)):
                                col = i
                    else:
                        col = score.index(max(score))
                except:
                    col = choice(list(moves(self)))

                row = self.get_available_row(col)
                self.play_move(row, col, 2)
                q_time += time.process_time() - start
                print(self.board)
                if self.check_wins(2):
                    label = myfont.render("Q-Agent wins!", 1, YELLOW)
                    screen.blit(label, (width / 4, 10))
                    self.game_over = True
                    self.draw_board(screen)
                    winner = 2
                    break
                self.draw_board(screen)
                self.turn = 1 - self.turn
                # display.update()
                time.sleep(0.1)
            else:
                start = time.process_time()
                col = self.default_opponent_move(self,self.turn)
                row = self.get_available_row(col)
                self.play_move(row, col, 1)
                default_time += time.process_time() - start
                print(self.board)
                if self.check_wins(1):
                    label = myfont.render("Defaut op wins!", 1, RED)
                    screen.blit(label, (width / 4, 10))
                    self.game_over = True
                    self.draw_board(screen)
                    winner = 1
                    break

                self.draw_board(screen)
                self.turn = 1 - self.turn
                time.sleep(0.1)

        pygame_time.wait(2000)
        return winner, q_time, default_time

    def minimax_vs_default(self):
        '''Allows you to play as Player 1 against our trained model'''
        winner = 0  # 0- draw, 1 - minimax, 2- Qlearning
        pygame_init()

        width = self.cols * SQUARESIZE
        height = (self.rows+1) * SQUARESIZE
        size = (width, height)

        screen = display.set_mode(size)
        self.draw_board(screen)
        display.update()
        minmax_time = 0
        default_time = 0
        myfont = font.Font('sweet purple.ttf', 75)

        while not self.game_over:
            if "0" not in self.board_to_string():
                label = myfont.render("It's a Draw", 1, BLUE)
                screen.blit(label, (width / 4, 10))
                self.draw_board(screen)
                winner = 0
                break
     
            draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            if self.turn == 1:
                start = time.process_time()
                state = self.board_to_string()

                col = best_move(self)
                # if (col not in moves(self)):
                #     col = choice(list(moves(self)))

                row = self.get_available_row(col)
                self.play_move(row, col, 2)
                minmax_time += time.process_time() - start
                print(self.board)
                if self.check_wins(2):
                    # print(self.board)
                    label = myfont.render("Minimax wins!", 1, YELLOW)
                    screen.blit(label, (width / 4, 10))
                    self.game_over = True
                    self.draw_board(screen)
                    winner = 2
                    break
                self.draw_board(screen)
                self.turn = 1 - self.turn
                # display.update()
                time.sleep(0.1)
            else:
                start = time.process_time()
                col = self.default_opponent_move(self,self.turn)
                row = self.get_available_row(col)
                self.play_move(row, col, 1)
                default_time += time.process_time() - start
                print(self.board)
                if self.check_wins(1):
                    # print(self.board)
                    label = myfont.render("Default Op wins!", 1, RED)
                    screen.blit(label, (width / 4, 10))
                    self.game_over = True
                    self.draw_board(screen)
                    winner = 1
                    break

                self.draw_board(screen)
                self.turn = 1 - self.turn
                time.sleep(0.1)

        pygame_time.wait(2000)
        print("-------------------------")
        return winner, minmax_time, default_time

