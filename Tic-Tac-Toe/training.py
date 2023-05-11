import numpy as np 
import pandas as pd
from tqdm import tqdm

import matplotlib.pyplot as plt 

import agents
from agents import win_eval

def train_as_X(X_player,O_player,episodes,plot=False):
  ''' Similaire à game(), Q_learning est X '''
  t = tqdm(total=episodes,desc='Training')

  results = []
  for episode in range(episodes):
    board = np.zeros((3,3),int)   # On crée une matrice 3x3 vide

    while win_eval(board) == 0:   # Tant que la partie n'est pas finie   
      ################# X MOVE ######################
      move = X_player.move(board,2)

      S = np.copy(board)     
      A = move

      board[move[0],move[1]] = 2
      
      if win_eval(board) != 0:
        reward = agents.score_eval(board,2)
        prev = X_player.q(S,X_player.format(A))
        X_player.q_table[(X_player.encode(S),X_player.format(A))] = prev + X_player.alpha * (reward + X_player.gamma*reward - prev)
        break

      ################# O MOVE ######################
      move = O_player.move(board,1)
      board[move[0],move[1]] = 1

      S1 = np.copy(board)

      X_player.epsilon = 0    # Pour faire le move optimal (imaginaire)
      A1 = X_player.move(board,2)
      X_player.epsilon = 0.2 if episode <0.95*episodes else 0

      reward = agents.score_eval(board,2)
      X_player.learn(S,A,S1,A1,reward)
    
    results.append([episode,agents.score_eval(board,2)]) 

    t.update(1)
  t.close()
  
  win = []
  lose = []
  draw = []

  for el in results:
    if el[1] == 1:
      win.append([el[0],1])
      lose.append([el[0],0])
      draw.append([el[0],0])
    elif el[1] == -1:
      win.append([el[0],0])
      lose.append([el[0],1])
      draw.append([el[0],0])
    elif el[1] == 0:
      win.append([el[0],0])
      lose.append([el[0],0])
      draw.append([el[0],1])


  if plot:
    df = pd.DataFrame(results,columns=['Episode','Result'])
    dfwin = pd.DataFrame(win,columns=['Episode','Result'])
    dflose = pd.DataFrame(lose,columns=['Episode','Result'])
    dfdraw = pd.DataFrame(draw,columns=['Episode','Result'])

    import pickle
    pickle.dump([df,dfwin,dflose,dfdraw], open("train_stats.pkl","wb"))
    span = int(0.05*episodes)

    smaw = dfwin.rolling(window=span, min_periods=span).mean()[:span]
    smal = dfwin.rolling(window=span, min_periods=span).mean()[:span]
    smad = dfwin.rolling(window=span, min_periods=span).mean()[:span]

    restw = dfwin[span:]
    restl = dflose[span:]
    restd = dfdraw[span:]

    win = pd.concat([smaw, restw]).ewm(span=span, adjust=False).mean()
    lose = pd.concat([smal, restl]).ewm(span=span, adjust=False).mean()
    draw = pd.concat([smad, restd]).ewm(span=span, adjust=False).mean()

    plt.plot(win.Episode,win.Result, label='Win')
    plt.plot(lose.Episode,lose.Result, label='Loss')
    plt.plot(draw.Episode,draw.Result, label='Draw')
    plt.legend()
    plt.xlabel('Episode')
    plt.ylabel('Result')
    plt.ylim(0,1)
    plt.show()

  return(X_player.q_table)       # La fonction renvoie Q

def train_as_O(X_player,O_player,episodes,plot=False):
  ''' Similaire à game(), Q_learning est O '''
  t = tqdm(total=episodes,desc='Training')

  results = []
  for episode in range(episodes):
    board = np.zeros((3,3),int)   
   
    move = X_player.move(board,2)

    while win_eval(board) == 0:   
      ################# O MOVE ######################
      move = O_player.move(board,1)

      S = np.copy(board)     
      A = move

      board[move[0],move[1]] = 1
      
      if win_eval(board) != 0:
        reward = agents.score_eval(board,1)
        prev = O_player.q(S,O_player.format(A))
        O_player.q_table[(O_player.encode(S),O_player.format(A))] = prev + O_player.alpha * (reward + O_player.gamma*reward - prev)
        break

      ################# X MOVE ######################
      move = X_player.move(board,2)
      board[move[0],move[1]] = 2

      S1 = np.copy(board)

      O_player.epsilon = 0    
      A1 = O_player.move(board,1)
      O_player.epsilon = 0.2 if episode < 0.95*episodes else 0

      reward = agents.score_eval(board,1)
      O_player.learn(S,A,S1,A1,reward)
    
    results.append([episode,agents.score_eval(board,1)])  
    t.update(1)
  t.close()
  
  win = []
  lose = []
  draw = []

  for el in results:
    if el[1] == 1:
      win.append([el[0],1])
      lose.append([el[0],0])
      draw.append([el[0],0])
    elif el[1] == -1:
      win.append([el[0],0])
      lose.append([el[0],1])
      draw.append([el[0],0])
    elif el[1] == 0:
      win.append([el[0],0])
      lose.append([el[0],0])
      draw.append([el[0],1])


  if plot:
    df = pd.DataFrame(results,columns=['Episode','Result'])
    dfwin = pd.DataFrame(win,columns=['Episode','Result'])
    dflose = pd.DataFrame(lose,columns=['Episode','Result'])
    dfdraw = pd.DataFrame(draw,columns=['Episode','Result'])

    import pickle
    pickle.dump([df,dfwin,dflose,dfdraw], open("train_stats.pkl","wb"))
    span = int(0.05*episodes)

    smaw = dfwin.rolling(window=span, min_periods=span).mean()[:span]
    smal = dfwin.rolling(window=span, min_periods=span).mean()[:span]
    smad = dfwin.rolling(window=span, min_periods=span).mean()[:span]

    restw = dfwin[span:]
    restl = dflose[span:]
    restd = dfdraw[span:]

    win = pd.concat([smaw, restw]).ewm(span=span, adjust=False).mean()
    lose = pd.concat([smal, restl]).ewm(span=span, adjust=False).mean()
    draw = pd.concat([smad, restd]).ewm(span=span, adjust=False).mean()

    expw = dfwin.Result.ewm(span=span, adjust=False).mean()
    expl = dflose.Result.ewm(span=span, adjust=False).mean()    
    expd = dfdraw.Result.ewm(span=span, adjust=False).mean()

    plt.plot(lose.Episode,lose.Result, label='Win') 
    plt.plot(win.Episode,win.Result, label='Loss')
    plt.plot(draw.Episode,draw.Result, label='Draw')
    plt.legend()
    plt.xlabel('Episode')
    plt.ylabel('Result')
    plt.ylim(0,1)
    plt.show()

  return(O_player.q_table)     
