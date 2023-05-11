
This is my project code for playing Tic Tac Toe aganist different AI agents

In order to run the code , first install the necessary libraries using the following command in the project directory

``` pip install -r requirements.txt

There are 3 functions in the main file :

qLearning_vs_default() - Plays 100 games of Tic Tac Toe for Default agent vs Q-learning agent
minimax_vs_default() - Plays 100 games of Tic Tac Toe for Minimax(with alpha beta pruning) agent vs Default agent
minimax_vs_qLearning() - Plays 100 games of Tic Tac Toe for Minimax(with alpha beta pruning) agent vs Q-learning agent

By default, the number of games played is 100, you can change it by passing the number of games in the parameter of the function call. For eg: if you want to play 5 games of minimax vs default. Then we will call the function minimax_vs_default(5).

To run the code, in the project directory, open the terminal and enter

> python
> import main

> main.minimax_vs_qLearning() # to play minimax vs q-learning
> main.minimax_vs_default()  # to play minimax vs default
> main.qLearning_vs_default() # to play default vs q-learning.
