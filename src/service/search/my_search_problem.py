from src.external_libs.searchProblem import Search_problem
from src.service.prolog.pyswip_client import PySwipClient
from src.model.prolog.node import Node
from src.external_libs.searchProblem import Arc
import logging


class MySearchProblem(Search_problem):
    """
    My specialized problem to solve with the implementation of knowledge base
    """

    def __init__(self, from_node: Node, to_node: Node, dist: dict, pwswip_client: PySwipClient):
        self.from_node = from_node
        self.to_node = to_node
        self.dist = dist
        self.pwsip_client = pwswip_client
        self.cache = dict()
        logging.info(f"Problem to solve from {from_node.id} to {to_node.id}")
        print(f"Cerco il percorso da {from_node.id} a {to_node.id}")

    def start_node(self):
        return self.from_node

    def is_goal(self, node):
        return self.to_node == node

    def neighbors(self, node):
        if node not in self.cache:
            neighbors = self.pwsip_client.ask_neighbours_of_node(node.id)
            neighbors = list(map(lambda n: self._make_arc(node, n), neighbors))
            self.cache[node] = neighbors
        for w in self.cache[node]:
            assert node.id != w.to_node.id, "Can't be same node"
        return self.cache[node]

    def heuristic(self, n):
        return self.dist[n.id][self.to_node.id]

    def _make_arc(self, from_node: Node, to_node: Node) -> Arc:
        """
        It creates an arc from the given nodes
        :param from_node:
        :param edge: The edge with all the info
        :return:
        """
        return Arc(from_node, to_node, self.dist[from_node.id][to_node.id])
