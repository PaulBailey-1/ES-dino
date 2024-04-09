import numpy as np

rng = np.random.default_rng()

class Optimizer:

    def __init__(self, params, mu):
        self.params = params
        self.n = len(params)
        self.mu = mu
        self.lamb = 70
        self.sigma = 0.01

        self.noise_table = []
        self.w = np.array([np.log(self.u + 0.5) - np.log(i) for i in range(1, self.u + 1)])
        self.w /= np.sum(self.w)

    def getParams(self):
        noise = rng.normal(size=self.n)
        self.noise_table.append(noise)
        params = self.params + self.sigma * noise
        return params, len(self.noise_table) - 1

    def update(self, rewards):
        sorting = np.array(rewards).argsort()[::-1][:self.mu]
        step = np.zeros(self.n)
        for i in range(self.n):
            step += self.w[i] * self.noise_table[sorting[i]]
        step *= self.sigma
        self.params += step
        self.noise_table.clear()