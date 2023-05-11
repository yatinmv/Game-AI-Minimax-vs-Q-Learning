This is my project code for playing Connect 4 aganist different AI agents

In order to run the code , first install the necessary libraries using the following command in the project directory

> pip install -r requirements.txt

There are 3 functions in the main file :

default_vs_q_agent() - Plays 100 games of Connect 4 for Default agent vs Q-learning agent
minimax_vs_default() - Plays 100 games of Connect 4 for Minimax(with alpha beta pruning) agent vs Default agent
minimax_vs_q_agent() - Plays 100 games of Connect 4 for Minimax(with alpha beta pruning) agent vs Q-learning agent

By default, the number of games played is 100, you can change it by passing the number of games in the parameter of the function call. For eg: if you want to play 5 games of minimax vs default. Then we will call the function minimax_vs_default(5).

To run the code, in the project directory, open the terminal and enter

> python
> import main

> main.minimax_vs_q_agent() # to play minimax vs q-learning
> main.minimax_vs_default()  # to play minimax vs default
> main.default_vs_q_agent() # to play default vs q-learning.
