import string
from enum import Enum
from xml.etree.ElementTree import Element
import json


class TagOSMEnum(Enum):
    """
    The enum containing the info of the keys of the attributes of tags osm xml node
    """
    K = 'k'
    """
    The attribute for the key 
    """

    V = 'v'
    """
    The attribute for the value
    """

    tag = 'tag'
    """
    The name of the xlm tag for the tag osm element
    """


class TagProprieties:
    """
    On open street view, the tag are a pair of key value that describe a property
    """

    def __init__(self):
        self.proprieties = dict()
        return

    def add_proprieties(self, key, value) -> set[string]:
        """
        It adds the new proprieties
        :param key: The new kay
        :param value: The new associated value
        :return All the value associated with the given key
        """
        current_set = self.proprieties.get(key)
        if current_set is None:
            current_set = set()
        current_set.add(value)
        self.proprieties[key] = current_set
        return current_set

    def get(self, key: string) -> set:
        """
        It returns the set of the key with associated property.
        :param key:
        :return: The set of values with the associated key. An empty set it's returned if the key it's not present.
        """
        values = self.proprieties.get(key)
        if values is None:
            values = set()
        values = set(values)
        return values



    @classmethod
    def from_osm_xml_element(cls, node_element: Element) -> 'TagProprieties':
        tag_proprieties = cls()
        for tag in node_element.findall(TagOSMEnum.tag.value):
            key = tag.get(TagOSMEnum.K.value)
            value = tag.get(TagOSMEnum.V.value)
            tag_proprieties.add_proprieties(key, value)
        return tag_proprieties
