import logging
import xml.etree.ElementTree as elementTree
import logging

from src.model.osm.node import Node
from src.model.osm.way import Way


class ParsingResult:
    """
    The result of parsing of the xml file
    """

    def __init__(self, node_list: list[Node], way_list: list[Way]):
        """
        :param node_list: The array of the nodes
        :param way_list: The list of the way
        """
        if node_list is None:
            node_list = []
        if way_list is None:
            way_list = []
        self.node_list = node_list
        self.way_list = way_list


class OSMXmlParser:
    """
    The parser of the open street model xml
    """

    def __init__(self):
        logging.debug('OSMXmlParser service initialed.')

    def parse_osm_xml(self, file, on_foot):
        """
        :param self:
        :param file: The file with
        :return:
        """
        logging.debug('Starting the parse of osm xml data..')
        tree = elementTree.parse(file)
        root = tree.getroot()
        logging.debug('Root of the data obtained.')

        # Parsing nodes
        node_dict = dict()
        logging.debug('Starting parsing of nodes..')
        for nodeElement in root.findall('node'):
            node = Node.from_osm_xml_element(nodeElement)
            node_dict.update({node.id_node: node})
        logging.debug('Parsing of nodes completed.')

        # Parsing ways
        logging.debug('Starting parsing of way..')
        ways = []
        for wayElement in root.findall('way'):
            way = Way.from_xlm_element(wayElement)
            ways.append(way)
        logging.debug('Parsing of way completed.')

        # Filtering data

        logging.debug('Filtering unused data..')
        logging.debug(f'Number of node before filtering {len(node_dict)} number of ways {len(ways)}')
        node_refs = set()
        node_cnt = dict()
        if on_foot:
            drivable_ways = ways
        else:
            drivable_ways = list(filter(lambda _: _.is_drivable(), ways))

        for w in drivable_ways:
            for node_id in w.node_list:
                if node_id not in node_cnt:
                    node_cnt[node_id] = 0
                node_cnt[node_id] = 1 + node_cnt[node_id]  # conta in quanti ways è presente il nodo
            node_refs.add(w.node_list[0])  # 2 estremi sempre
            node_refs.add(w.node_list[-1])

        for key, value in node_cnt.items():  # aggiungo nodi che sono condivisi da 2 o piu ways
            if value >= 2:
                node_refs.add(key)

        # uncomment to disable simplification
        #for w in drivable_ways:
        #    for n in w.node_list:
        #        node_refs.add(n)

        for w in drivable_ways:
            w.node_list = list(filter(lambda _: _ in node_refs, w.node_list))
            for i in range(0, len(w.node_list) - 1):
                if w.node_list[i] == w.node_list[i + 1]:
                    del(w.node_list[i])

        drivable_ways = list(filter(lambda _: len(_.node_list) > 1, drivable_ways))


        nodes = list(map(lambda id_node: node_dict.get(id_node), node_refs))
        logging.debug(f'Completed filtering of unused data. node found {len(nodes)}')
        return ParsingResult(nodes, drivable_ways)
