class QLearner():
    def __init__(self):
        self.lambda = 0.1

    def qlearn(self, currentQ, r, sprime, aprime,  ):
        Q(s, a) = currentQ + alpha * (r + self.lambda * maxaQ(sprime, aprime) - currentQ)