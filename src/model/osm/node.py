from enum import Enum
from xml.etree.ElementTree import Element
from src.model.osm.tag_proprieties import TagProprieties
import json


class NodeOSMEnum(Enum):
    """
    The enum containing the tags attribute of the node
    """

    ID = 'id'
    """
    The tag used on xml on osm to identify the id of the node
    """

    LAT = 'lat'
    """
    The tag used on xml on osm to identify the latitude of the node
    """

    LON = 'lon'
    """
    The tag used on xml of osm to identify the longitude of the node
    """


class Node:
    """
    A class representing a node on open street map model
    """

    def __init__(self, id_node: int, lat: float, lon: float, tag_proprieties: TagProprieties = None):
        """
        :param id_node: The id of the node
        :param lat: The latitude coord
        :param lon: The longitude coord
        """
        if tag_proprieties is None:
            tag_proprieties = TagProprieties()
        self.id_node = id_node
        self.lat = lat
        self.lon = lon
        self.tag_proprieties = tag_proprieties
        return

    @classmethod
    def from_osm_xml_element(cls, node_element: Element) -> 'Node':
        """
        It builds the node from the xml element
        :param node_element: The node element of the xml osm
        """
        id_node = int(node_element.get(NodeOSMEnum.ID.value))
        lon = float(node_element.get(NodeOSMEnum.LON.value))
        lat = float(node_element.get(NodeOSMEnum.LAT.value))
        tag_proprieties = TagProprieties.from_osm_xml_element(node_element)
        return cls(id_node, lon, lat, tag_proprieties)
