import logging
from random import randint


class DynamicProgramming:
    def __init__(self, n):
        self.n = n
        self.interest, self.time, self.cost = [], [], []
        self.memo = {}

    def generate(self):
        logging.debug("Generating random values for the dp problem..")
        print("Generazione di valori casuali per il problema dp:")
        for i in range(self.n):
            self.interest.append(randint(0, 100))
            self.time.append(randint(30, 180))
            self.cost.append(randint(0, 35))
            logging.debug(f"Element {i}: interest {self.interest[i]}, time {self.time[i]}, cost {self.cost[i]}")
            print(f"    Elemento {i}: interesse {self.interest[i]}, tempo {self.time[i]}, costo {self.cost[i]}")
        logging.debug("Generation completed.")

    def calculate(self, i, t, b):  # Actual element, time left, budget left
        if i == self.n:
            return 0
        if (i, t, b) in self.memo:
            return self.memo[(i, t, b)]
        if self.time[i] > t or self.cost[i] > b:
            self.memo[(i, t, b)] = self.calculate(i + 1, t, b)
            return self.memo[(i, t, b)]
        self.memo[(i, t, b)] = max(self.calculate(i + 1, t, b),
                                   self.calculate(i + 1, t - self.time[i], b - self.cost[i]) + self.interest[i])
        return self.memo[(i, t, b)]

    def get_solution(self, i, t, b):
        logging.debug("Getting solution of the dp problem..")
        print("Soluzione del problema dp:")
        cnt = 0
        while i < self.n:
            if self.calculate(i, t, b) == self.calculate(i + 1, t, b):
                i += 1
            else:
                logging.debug(f"Selected {i} with interest {self.interest[i]}, time {self.time[i]} and cost {self.cost[i]}")
                print(f"    Selezionato {i} con interesse {self.interest[i]}, tempo {self.time[i]} e costo {self.cost[i]}")
                cnt += 1
                t -= self.time[i]
                b -= self.cost[i]
                i += 1
        logging.debug("Solution calculated.")
        return cnt