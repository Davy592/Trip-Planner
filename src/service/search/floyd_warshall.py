import itertools
import logging

from src.service.prolog.pyswip_client import PySwipClient


class FloydWarshall:
    def __init__(self, prolog: PySwipClient):
        self.prolog = prolog
        self.dist = self._create_matrix()

    def _create_matrix(self) -> dict:
        nodes = self.prolog.ask_all_node()
        self.dist = dict()
        for node in nodes:
            self.dist[node.id] = dict()
            for node2 in nodes:
                if node.id == node2.id:
                    self.dist[node.id][node2.id] = 0
                else:
                    self.dist[node.id][node2.id] = float('inf')
        for node in nodes:
            for neighbour in self.prolog.ask_neighbours_of_node(node.id):
                self.dist[node.id][neighbour.id] = self.prolog.get_distance_between_nodes(node.id, neighbour.id)
        for k in nodes:
            for i in nodes:
                for j in nodes:
                    self.dist[i.id][j.id] = min(self.dist[i.id][j.id], self.dist[i.id][k.id] + self.dist[k.id][j.id])
        return self.dist

    def best_path(self, nodes):
        logging.debug("Calculating best path..")
        start = nodes[0]
        goals = nodes[1:]

        perms = list(itertools.permutations(goals))

        best = None
        minimum = float('inf')
        for perm in perms:
            prev = start

            path_cost = 0

            for node in perm:
                path_cost += self.dist[prev.id][node.id]
                prev = node

            path_cost += self.dist[prev.id][start.id]

            if path_cost <= minimum:
                minimum = path_cost
                best = perm

        best = list(best)
        best.insert(0, start)
        logging.debug("The best path is: " + str(best))
        print("La strada migliore da seguire è: ")
        for i in range(len(best)):
            print(f"  Nodo {i+1}: {best[i]}")
        logging.debug("Best path calculated.")
        return best

    def get_lsdb(self):
        return self.dist
