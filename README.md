# Game-AI-Minimax-vs-Q-Learning
In this project, , I have implemented two classic games, Tic Tac Toe and Connect 4, and applied Minimax algorithm with alpha-beta pruning and tabular Q-learning reinforcement learning algorithm, to play against default opponents and each other. The objective of this project is to evaluate and compare compare their performance .
<br/>

Tic Tac Toe       |  Connect4
:-------------------------:|:-------------------------:
![](tic_tac_toe.png)  |  ![](connect4.png)

# Implementation of Algorithms
This project implements two classic games, Tic Tac Toe and Connect 4, and applies two well-known AI techniques, Minimax algorithm with alpha-beta pruning and tabular Q-learning reinforcement learning algorithm, to play against default opponents and each other. The objective of this project is to evaluate and compare the performance of these two algorithms in these two games.

## Minimax with alpha-beta pruning
The Minimax algorithm is a decision-making algorithm that searches through all possible moves and outcomes of a game to determine the best possible move for the current player. Alpha-beta pruning is used to optimize the Minimax algorithm by cutting off the search when it identifies a branch that is unlikely to lead to the best outcome.

## Q-Learning
Tabular Q-learning is a type of reinforcement learning technique that learns and improves with training. It assigns a Q-value to each possible action in a given state, which is updated over time as the algorithm interacts with the environment and learns which actions result in the highest rewards. The algorithm balances between exploration and exploitation by randomly selecting an action to explore new possibilities, or choosing the action with the highest Q-value to exploit its current knowledge.

## Default Agent Algorithm
A default agent is implemented for both Tic Tac Toe and Connect 4. This agent blocks the opponent’s next move if it is winning. Otherwise, it plays the winning move if there is one. If any of these scenarios are not possible, then it plays a random move.

## Design Decisions
For Tic Tac Toe, the following hyperparameters were chosen for Q-Learning: ε=0.3, α=0.2, γ=0.9. The reward function encourages the algorithm to learn to win the game while avoiding losing.

For Connect4, the following hyperparameters were chosen for Q-Learning: ε=0.3, α=0.5, γ=0.9. A 5x5 board was implemented to reduce the training time. The reward function was set to 1 if the Q-Agent (the AI) wins, -1 if the opponent (Minimax) wins, and a small positive value (1/25) if the game ends in a draw.

The choice of hyperparameters was based on examples from literature and fine-tuning through trial and error to achieve optimal performance.

# Results

This section presents the outcomes obtained from running 100 games for each scenario. The reason for choosing 100 games is because it good enough number for performance comparison and 100 games would not be too time-consuming, 100 games provide a good balance between accuracy and efficiency. I will analyze the performance of these algorithms by comparing their win/loss ratio and computational time when playing against default opponents and each other. The results provide insights into how the algorithms compare to each other when playing against default opponents as well as against each other in both Tic Tac Toe and Connect 4. 

## Tic Tac Toe – Performance comparison of algorithms against Default agent

I ran Tic Tac Toe 100 times for Minimax vs Default and Q-Learning vs Default. I observed the total time taken and the number of wins by each agent and the number of draws for each scenario.
The results achieved are shown below


### Minimax vs Default agent:

| Algorithms/Metrics                        | Wins | Total time take (sec) | Draws |
|-------------------------------------------|------|-----------------------|-------|
| Minimax (with alpha-beta pruning) agent   | 46   | 17.109375             | 19    |
| Default agent                             | 35   | 0.03125               | 19      |


### Q-Learning vs Default agent:

| Algorithms/Metrics | Wins | Total time take (sec) | Draws |
|--------------------|------|-----------------------|-------|
| Q-Learning agent   | 73   | 0.328125              | 15    |
| Default agent      | 12   | 0.046875              | 15   |


We can observe that in the 100 games of Tic Tac Toe, both Minimax and Q-learning algorithms outperformed the Default algorithms in the Win rate. The Minimax agent also took significantly more time to complete its moves than the default agent, with a total time of 17.109375 seconds compared to just 0.03125 seconds for the default agent. The Q-Learning agent also took a bit more time to complete its moves than the default agent, with a total time of 0.328125 seconds compared to 0.046875 seconds for the default agent.
In comparison, the Q-learning agent achieved a much higher win rate and also the Minimax agent took significantly more time to make its moves than the Q-Learning agent. Therefore, for Tic Tac Toe, Q-learning appears to be performing better than Minimax.

## Connect4 – Performance comparison of algorithms against Default agent
I ran Connect4 100 times for Minimax vs Default and Q-Learning vs Default. I observed the total time taken and the number of wins by each agent and the number of draws for each scenario.
The results achieved are shown below

### Minimax vs Default agent:

| Algorithms/Metrics                        | Wins | Total time take (sec) | Draws |
|-------------------------------------------|------|-----------------------|-------|
| Minimax (with alpha-beta pruning) agent   | 72   | 53.390625             | 19    |
| Default agent                             | 9    | 0.34375               |  19    |


### Q-Learning vs Default agent:

| Algorithms/Metrics | Wins | Total time take (sec) | Draws |
|--------------------|------|-----------------------|-------|
| Q-Learning agent   | 26   | 0.015625              | 5     |
| Default agent      | 69   | 0.28125               | 5      |


Based on the above results, we can see that Minimax with alpha-beta pruning was the strongest algorithm for playing Connect4, with 72 wins out of 100 games.




