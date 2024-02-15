import logging
import time
from random import randint

from src.service.search.dp import DynamicProgramming
from src.external_libs.searchMPP import SearcherMPP
from src.service.search.floyd_warshall import FloydWarshall
from src.service.data.osm_xml_parser import OSMXmlParser
from src.service.data.facts_writer import FactsWriter
from src.service.prolog.pyswip_client import PySwipClient
from src.model.prolog.node import Node
from src.service.data.osm_xml_parser import ParsingResult

from src.service.search.my_search_problem import MySearchProblem


class Environment:
    """
    The class that store all the enviroment variabile for the run of the application
    """

    def __init__(self, path_to_prolog_facts: str, path_to_prolog_rules: str,
                 path_to_osm_data: str, on_foot: bool, total_time: int, total_budget: int, total_poi: int):
        self.path_to_prolog_facts = path_to_prolog_facts
        self.path_to_prolog_rules = path_to_prolog_rules
        self.path_to_osm_data = path_to_osm_data
        self.on_foot = on_foot
        self.total_time = total_time
        self.total_budget = total_budget
        self.total_poi = total_poi


def main(env: Environment):
    """
    The entry point of my application
    :param env: The environment variables
    :return:
    """
    # Bootstrapping the application
    # Set level=logging.CRITICAL to avoid logging messages
    logging.basicConfig(level=logging.CRITICAL)
    logging.info("Application started.")
    logging.debug("Initiating internal services..")
    # Initiating services
    parser_osm = OSMXmlParser()
    writer = FactsWriter()
    # Path to the file
    _update_facts_file(env.path_to_osm_data, parser_osm, env.path_to_prolog_facts, env.on_foot, writer)
    prolog_client = PySwipClient(env.path_to_prolog_facts, env.path_to_prolog_rules)
    # Setting up dp parameters
    dp = DynamicProgramming(total_poi_main)
    # Generating users preferences, time and cost for each poi
    dp.generate()
    # Calculating the best solution
    logging.info("Calculating the best solution..")
    dp.calculate(0, total_time_main, total_budget_main)
    logging.info("Solution calculated.")
    howmany = dp.get_solution(0, total_time_main, total_budget_main)
    # Calculating the map of the entire graph
    fw = FloydWarshall(prolog_client)
    # Picking up nodes
    selected_nodes = select_nodes(howmany + 1, fw.get_lsdb(), prolog_client)  # first is the start node
    # Finding the best path reordering nodes
    selected_nodes = fw.best_path(selected_nodes)
    for i in range(len(selected_nodes) - 1):
        problem = MySearchProblem(selected_nodes[i], selected_nodes[i + 1], fw.get_lsdb(), prolog_client)
        searcher = SearcherMPP(problem)
        path = searcher.search()
    problem = MySearchProblem(selected_nodes[len(selected_nodes)-1], selected_nodes[0], fw.get_lsdb(), prolog_client)
    searcher = SearcherMPP(problem)
    path = searcher.search()
    logging.info("Application has been shutdown")


def select_nodes(howmany: int, dist: dict, prolog_client: PySwipClient) -> list[Node]:
    logging.debug("Selecting nodes..")
    nodes = prolog_client.ask_all_node()
    selected_node = []
    different = False
    while not different:
        different = True
        selected_node = []
        for i in range(howmany):
            selected_node.append(nodes[randint(0, len(nodes) - 1)])
            for j in range(i):
                if selected_node[i] == selected_node[j] or not _is_connected(selected_node[i], selected_node[j], dist):
                    different = False
                    break
            if not different:
                break
    print("I nodi corrispondenti sono: ")
    for node in selected_node:
        logging.debug(f"Selected node {node}")
        print(f"    Il nodo {node.id} con latitudine {node.lat} e longitudine {node.lon}")
    logging.debug("Nodes selected.")
    return selected_node


def _update_facts_file(path_to_osm_data: str, parser: OSMXmlParser, path_to_prolog_facts: str, on_foot: bool,
                       writer: FactsWriter) -> ParsingResult:
    """
    A subroutine to parse data from the open street model and store the facts related on a file
    :param path_to_osm_data: The path of the file of the open street model
    :param parser: The parser of the xml
    :param path_to_prolog_facts: The path to store the prolog facts
    :param writer: The class that writes the facts on file
    :return:
    """
    logging.info(f"Importing open street data from:'{path_to_osm_data}'..")
    result = None
    with open(path_to_osm_data, 'r', encoding='utf-8') as file:
        result = parser.parse_osm_xml(file, on_foot)
    logging.info('Imported open street data completed.')
    assert result is not None, 'A parsing result should be produced'
    writer.write_facts(result, path_to_prolog_facts, on_foot)
    return result


def _is_connected(nodeA: Node, nodeB: Node, dist: dict) -> bool:
    """
    Checks if there is a path from nodeA to nodeB
    :param nodeA: the first node to check
    :param nodeB: the second node to check
    :return: True if the 2 nodes are connected
    """
    logging.debug(f'Checking {nodeA} and {nodeB}')
    return not (dist[nodeA.id][nodeB.id] == float('inf') or dist[nodeB.id][nodeA.id] == float('inf'))


if __name__ == "__main__":
    """
    Setting up environment variable
    """
    prolog_facts_path_main = '../resources/prolog/facts.pl'
    prolog_rules_path_main = '../resources/prolog/rules.pl'
    open_street_data_path_main = '../resources/open_street_map/molf.osm'
    on_foot_main = False
    total_poi_main = 100
    total_time_main = 300
    total_budget_main = 100
    env_main = Environment(prolog_facts_path_main, prolog_rules_path_main,
                           open_street_data_path_main, on_foot_main, total_time_main, total_budget_main, total_poi_main)
    main(env_main)
