from pyswip import Prolog
from src.model.prolog.node import Node
import logging
import time


class PySwipClient:
    """
    The Client to interact with the knowledge base
    """

    def __init__(self, path_to_facts: str, path_to_rules: str):
        """
        :param path_to_facts: the path to the facts to import
        :param path_to_rules: the path to the rules to import
        """
        self.prolog = Prolog()
        self.prolog.consult(path_to_facts)
        self.prolog.consult(path_to_rules)
        logging.debug('Service PySwipClient initiated.')

    def ask_all_way_ids(self) -> list[str]:
        """
        It asks for all the ids of edges present
        :return: The list of ids of all the ways
        """
        result = self._query('get_all_way_ids(Way)')
        return list(map(lambda x: x['Way'], result))

    def ask_all_node(self) -> list[Node]:
        """
        It asks for all the ids of the nodes present
        :return: The list of ids of all the nodes
        """
        result = self._query('get_all_node(Node, Lat, Lon)')
        return list(map(lambda x: Node.from_prolog_dictionary_result(x), result))

    def ask_neighbours_of_node(self, from_node_id: str) -> list[Node]:
        """
        It asks for the neighbours of a node
        :param from_node_id: The node id
        :return: The list of neighbours
        """
        result = self._query(f"get_neighbours({from_node_id}, Node, Lat, Lon)")
        return list(map(lambda _: Node.from_prolog_dictionary_result(_), result))

    def get_distance_between_nodes(self, from_node_id: str, to_node_id: str) -> int:
        """
        It asks for the distance between two nodes
        :param from_node_id: The id of the starting node
        :param to_node_id: The id of the ending node
        :return: the distance between the two nodes
        """
        result = self._query(f"get_distance({from_node_id}, {to_node_id}, Distance)")
        return result[0]['Distance']


    def _query(self, query):
        """
        It wraps up the result of the query and returns the list
        :param query: The query to launch
        :return:
        """
        logging.debug(f"Executing query on prolog: '{query}'..")
        start_time = time.time()
        query_result = self.prolog.query(query)
        return_value = list(query_result)
        logging.debug(f"item size: {len(return_value)}")
        query_result.close()
        end_time = time.time()
        logging.debug(f'Time passed in prolog query {end_time - start_time}s')
        return return_value
