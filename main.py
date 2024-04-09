from src.game import Game
from src.agent import Agent

if (__name__ == "__main__"):

    game = Game(display=True)

    # Create agents
    agents = [Agent() for _ in range(2)]
    # agent.setParams([-0.008, 0, 1])
    # Rollout
    game.addAgents(agents)
    print('Running batch 1')
    while game.running:
        game.run()

    # Optimize them
    print(game.getScores())