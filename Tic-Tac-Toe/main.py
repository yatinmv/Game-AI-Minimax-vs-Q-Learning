import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import agents

def win_eval(board):
  ''' Fonction qui évalue une grille et renvoie : 0 si la partie n'est pas finie, 1 si O gagne, 2 si X gagne ou 3 si match nul '''
  for x in range(3):
    if board[x,0] == board[x,1] == board[x,2] != 0: return board[x,0]    # -
    elif board[0,x] == board[1,x] == board[2,x] != 0: return board[0,x]  # |
    elif board[0,0] == board[1,1] == board[2,2] != 0: return board[0,0]  # \
    elif board[0,2] == board[1,1] == board[2,0] != 0: return board[0,2]  # /
  if np.count_nonzero(board) < 9: return 0  # Pas fini
  return 3                                  # Match nul

def game(X_player,O_player,show_end_state=True,return_time=False):
    ''' La fonction principale, renvoie le résultat d'une partie entre 2 joueurs '''
    board = np.zeros((3,3),int)   
    turn = 2                      
    X_player_time = 0
    O_player_time = 0
    while win_eval(board) == 0:     
      if turn == 2: 
        start = time.process_time() 
        move = X_player.move(board,turn)
        board[move[0],move[1]] = 2
        turn = 1
        X_player_time += time.process_time() - start

      else:
        start = time.process_time()
        move = O_player.move(board,turn)
        board[move[0],move[1]] = 1
        turn = 2
        O_player_time += time.process_time() - start

    if show_end_state:           
      agents.Human().show_end_state(board)  
      agents.Human().show_end_state(np.zeros((3,3),int))  
    if not return_time:
      return(agents.score_eval(board,2))
    return(agents.score_eval(board,2),X_player_time,O_player_time)       

from training import train_as_X, train_as_O

def minimax_vs_default(i=100):
    X_player = agents.Minimax()   # Epsilon = 0 pour avoir un joueur parfait
    O_player = agents.DefaultOpponent()
    default_wins = 0
    minimax_wins = 0
    X_player_time = 0
    O_player_time = 0
    draws = 0
    while i>0:
      res,t1,t2 = game(X_player,O_player,True,True)
      if res == 1:
        minimax_wins += 1
      elif res == -1:
        default_wins += 1
      else:
        draws += 1
      i -= 1
      X_player_time += t1
      O_player_time += t2

    print("Default wins: ", default_wins)
    print("Minimax wins: ", minimax_wins)
    print("Draws: ", draws)
    print("Minimax player time: ", X_player_time)
    print("Default player time: ", O_player_time)

def qLearning_vs_default(i=100):

  Q = train_as_X(agents.Q_learning(),agents.Random(),7000)

  X_player = agents.Q_learning(Q,0)   # Epsilon = 0 
  O_player = agents.Random()

  results = []
  for j in range(1000):
    results.append([j,game(X_player,O_player,False)])

  df = pd.DataFrame(results,columns=['Episode','Result'])
  exp = df.Result.ewm(span=(1000)//10, adjust=False).mean()

  plt.plot(df.Episode,df.Result, 'ro')
  plt.plot(df.Episode,exp, label='EMA')
  plt.xlabel('Episode')
  plt.ylabel('Result (1= X win/-1= O win)')
  plt.show()

  O_player = agents.DefaultOpponent()
  
  qlearning_wins = 0
  default_wins = 0
  X_player_time = 0
  O_player_time = 0
  draws = 0
  while i>0:
    res,t1,t2 = game(X_player,O_player,True,True)
    if res == 1:
      qlearning_wins += 1
    elif res == -1:
      default_wins += 1
    else:
      draws += 1
    i -= 1
    X_player_time += t1
    O_player_time += t2
    print(i)

  print("Qlearning wins: ", qlearning_wins)
  print("Default wins: ", default_wins)
  print("Draws: ", draws)
  print("QLearning player time: ", X_player_time)
  print("Default time: ", O_player_time)

def minimax_vs_qLearning(i=100):
    Q = train_as_O(agents.Random(),agents.Q_learning(),7000)

    O_player = agents.Q_learning(Q,0)   # Epsilon = 0 
    X_player = agents.Minimax()

    # results = []
    # for j in range(1000):
    #   results.append([j,game(X_player,O_player,False)])

    # df = pd.DataFrame(results,columns=['Episode','Result'])
    # exp = df.Result.ewm(span=(1000)//10, adjust=False).mean()

    # plt.plot(df.Episode,df.Result, 'ro')
    # plt.plot(df.Episode,exp, label='EMA')
    # plt.xlabel('Episode')
    # plt.ylabel('Result (1= X win/-1= O win)')
    # plt.show()

    qlearning_wins = 0
    minimax_wins = 0
    X_player_time = 0
    O_player_time = 0
    draws = 0
    while i>0:
      res,t1,t2 = game(X_player,O_player,True,True)
      if res == 1:
        minimax_wins += 1
      elif res == -1:
        qlearning_wins += 1
      else:
        draws += 1
      i -= 1
      X_player_time += t1
      O_player_time += t2
      print(i)

    print("Qlearning wins: ", qlearning_wins)
    print("Minimax wins: ", minimax_wins)
    print("Draws: ", draws)
    print("QLearning player time: ", O_player_time)
    print("Minimax player time: ", X_player_time)

if __name__ == "__main__":
  
  minimax_vs_default()
