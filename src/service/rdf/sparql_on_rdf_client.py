from rdflib import Graph, Namespace


class sparql_client():
    def __init__(self, path):
        self.path = path
        self.graph = Graph()
        self.graph.parse(self.path, format="turtle")

    def ask_range_of_prop(self, prop):
        query = f"""
                PREFIX osm: <https://w3id.org/openstreetmap/terms#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                
                SELECT ?domain ?range
                WHERE {{
                  osm:{prop}
                    rdfs:label "{prop}=*"@en;
                    rdfs:domain ?domain;
                    rdfs:range ?range .
                }}
                """
        rows = self.graph.query(query)
        osm = "https://w3id.org/openstreetmap/terms#"
        for row in rows:
            range = str(row['range']).replace(osm, "")
            return range

    def ask_label_for_meaning_in_range(self, mean, range):
        query = f"""
                PREFIX osm: <https://w3id.org/openstreetmap/terms#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                
                SELECT ?label
                WHERE {{
                  osm:{mean}
                    a osm:{range};
                    rdfs:label ?label.
                }}
                """
        rows = self.graph.query(query)
        osm = "https://w3id.org/openstreetmap/terms#"
        for row in rows:
            label = str(row['label']).replace(osm, "")
            return label