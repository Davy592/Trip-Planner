import logging

class Node:
    """
    The node returned by a prolog query
    """

    def __init__(self, id: str, lat: float, lon: float):
        """

        :param id: The id of the node
        :param lat: The lattitude of the node
        :param lon: The longitude of the node
        """
        self.id = id
        self.lat = lat
        self.lon = lon

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return (self.id == other.id
                and self.lat == other.lat
                and self.lon == other.lon)

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return '{' + f"id: {self.id}, lat: {self.lat}, lon: {self.lon}" + '}'

    @classmethod
    def from_prolog_dictionary_result(cls, dictionary: dict) -> 'Node':
        """
        It returns a node from a prolog result query
        :param dictionary: The dictionary with all the keys
        :return: The node obtained
        """
        return Node(dictionary['Node'], float(dictionary['Lat']), float(dictionary['Lon']))
