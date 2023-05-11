from board import *
from pandas import read_csv
import ast



def default_vs_q_agent(iterations = 100):
# Upload values from table
    Q_table = {}
    table = read_csv('q_learning_table.csv')
    for i in range(len(table['states'])):
        Q_table[table['states'][i]] = ast.literal_eval(table['scores'][i])

    q_count = 0
    default_count = 0
    q_time = 0
    default_time = 0
    draws = 0
    while(iterations):
        
        game = Connect4()
        response,t1,t2 = game.default_vs_q_play(Q_table)
        if(response == 1 ):
            default_count+=1
        elif (response == 2):
            q_count+=1
        else:
            draws+=1     
        iterations-=1
        q_time+=t1
        default_time+=t2
    print('-------------------------------')
    print("Q-Learning won : " + str(q_count)+" times")
    print("Default Op won : " + str(default_count)+" times")
    print("Draws : " + str(draws)+" times")
    print("Q-Learning took : " + str(q_time)+" seconds")
    print("Default Op took : " + str(default_time)+" seconds")
    print('-------------------------------')

def minimax_vs_default(iterations = 100):
    
    minimax_count = 0
    default_count = 0
    minmax_time = 0
    default_time = 0
    draws = 0
    while(iterations):
        
        game = Connect4()
        response,t1,t2 = game.minimax_vs_default()
        if(response == 1 ):
            default_count+=1
        elif (response == 2):
            minimax_count+=1
        else:
            draws+=1     
        iterations-=1
        minmax_time+=t1
        default_time+=t2
    print('-------------------------------')
    print("Minimax won : " + str(minimax_count)+" times")
    print("Default Op won : " + str(default_count)+" times")
    print("Draws : " + str(draws)+" times")
    print("Minimax took : " + str(minmax_time)+" seconds")
    print("Default Op took : " + str(default_time)+" seconds")
    print('-------------------------------')

def minimax_vs_q_agent(iterations = 100):
    # Upload values from table
    Q_table = {}
    table = read_csv('q_learning_table.csv')
    for i in range(len(table['states'])):
        Q_table[table['states'][i]] = ast.literal_eval(table['scores'][i])

    q_count = 0
    minimax_count = 0
    q_time = 0
    minmax_time = 0
    draws = 0
    while(iterations):
        
        game = Connect4()
        response,t1,t2 = game.minimax_vs_q_play(Q_table)
        if(response == 1 ):
            minimax_count+=1
        elif (response == 2):
            q_count+=1
        else:
            draws+=1     
        iterations-=1
        q_time+=t1
        minmax_time+=t2
    print('-------------------------------')
    print("Q-Learning won : " + str(q_count)+" times")
    print("Minimax won : " + str(minimax_count)+" times")
    print("Draws : " + str(draws)+" times")
    print("Q-Learning took : " + str(q_time)+" seconds")
    print("Minimax took : " + str(minmax_time)+" seconds")
    print('-------------------------------')

if __name__ == "__main__":

    default_vs_q_agent(5)
    