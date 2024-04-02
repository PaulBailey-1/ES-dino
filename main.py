from src.game import Game
from src.agent import Agent

if (__name__ == "__main__"):

    game = Game()

    # Create agents
    agent = Agent()
    # Rollout
    game.addAgent(agent)
    while game.running:
        game.run()
    # Optimize them
    