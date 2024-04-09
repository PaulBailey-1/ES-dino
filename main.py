from src.game import Game
from src.agent import Agent
from src.optimizer import Optimizer

if (__name__ == "__main__"):

    game = Game(display=True)

    # Create agents
    agents = [Agent() for _ in range(2)]
    # agents[0].setParams([-0.008, 0, 1])
    game.addAgents(agents)

    initalParams = agents[0].getParams()
    for agent in agents:
        agent.setParams(initalParams)

    optimizer = Optimizer(initalParams, len(agents))

    generation = 0
    while True:

        print('Generation ', generation)

        for agent in agents:
            params, noiseIdx = optimizer.getParams()
            agent.setParams(params)

        # Rollout
        game.reset()
        while game.running:
            game.run()

        # Optimize
        rewards = game.getScores()
        print(rewards)
        optimizer.update(rewards)

        generation += 1