class QLearner:
    def __init__(self):
        self.learning_rate = 0.1
        self.discount_factor = 0.1

    def qlearn(self, currentQ, r, sprime, aprime,  ):
        Qsa = model.predict()
        Q(s, a) = currentQ + self.learning_rate * (r + self.discount_factor * maxaQ(sprime, aprime) - currentQ)