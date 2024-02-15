from src.model.prolog.node import Node


class Edge:
    """
    The class that represents the edge
    """

    def __init__(self, node: Node, max_speed: int):
        """
        The edge returned by a prolog query
        :param node: The destination node
        :param max_speed: The speed in km for this edge
        """
        self.node = node
        self.max_speed = max_speed

    @classmethod
    def from_prolog_dictionary_result(cls, dictionary: dict) -> 'Edge':
        node = Node(dictionary['To_node'], float(dictionary['To_node_lat']), float(dictionary['To_node_lon']))
        return Edge(node, int(dictionary['Max_speed']))

