import csv
import doctest
from abc import ABC, abstractmethod


class GraphError(Exception):

    def __init__(self, message=''):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

    def __repr__(self):
        # canonical string representation of the error
        return f"GraphError({repr(str(self))})"


class Node:

    def __init__(self, identifier, **attributes):
        self._id = identifier
        self._attributes = attributes

    def identifier(self):
        return self._id

    def attributes(self):
        return self._attributes.copy()

    def __str__(self):
        sorted_dict = sorted(self._attributes.items())
        final = [f"Node [{self._id}]\n"]
        for x, y in sorted_dict:
            final.append(f"    {x} : {y}\n")
        return "".join(final)


class Edge:

    def __init__(self, node1, node2, **attributes):
        self._node1 = node1
        self._node2 = node2
        self._attributes = attributes

    def attributes(self):
        return self._attributes.copy()

    def nodes(self):
        return (self._node1, self._node2)

    def __str__(self):
        final = [f"Edge from node [{self._node1.identifier()}] to node [{self._node2.identifier()}]\n"]
        for x, y in sorted(self._attributes.items()):
            final.append(f"    {x} : {y}\n")
        return "".join(final)


class BaseGraph(ABC):

    def __init__(self):
        self._nodes = {}  # node id -> node obj
        self._edges = []  # list of edge objects
        self._adjacency = {}  # node id -> list of adjacent node ids

    def __len__(self):
        return len(self._nodes)

    def add_node(self, node_id, **prop):
        if node_id in self._nodes:
            raise GraphError(f"Node {node_id} already exists")
        self._nodes[node_id] = Node(node_id, **prop)
        self._adjacency[node_id] = []

    def node(self, node_id):
        if node_id not in self._nodes:
            raise GraphError(f"Node {node_id} not found")
        return self._nodes[node_id]

    def nodes(self):
        return [self._nodes[node_id] for node_id in sorted(self._nodes)]

    def add_edge(self, node1_id, node2_id, **prop):
        if node1_id not in self._nodes:
            raise GraphError(f"Node {node1_id} not found")
        if node2_id not in self._nodes:
            raise GraphError(f"Node {node2_id} not found")
        
        # Check if edge already exists
        for edge in self._edges:
            n1, n2 = edge.nodes()
            if n1.identifier() == node1_id and n2.identifier() == node2_id:
                raise GraphError(f"Edge ({node1_id},{node2_id}) already exists")

        # Create and add the edge
        node1 = self._nodes[node1_id]
        node2 = self._nodes[node2_id]
        new_edge = Edge(node1, node2, **prop)
        self._edges.append(new_edge)
        self._adjacency[node1_id].append(node2_id)

    def edge(self, node1_id, node2_id):
        for edge in self._edges:
            n1, n2 = edge.nodes()
            if n1.identifier() == node1_id and n2.identifier() == node2_id:
                return edge
        raise GraphError(f"Edge ({node1_id},{node2_id}) not found")

    def edges(self):
        sorted_edges = sorted(self._edges, 
                            key=lambda e: (e.nodes()[0].identifier(), e.nodes()[1].identifier()))
        return sorted_edges

    def __getitem__(self, key):
        try:
            return self.node(key)
        except GraphError:
            pass
        
        # Try edge lookup
        try:
            return self.edge(key[0], key[1])
        except (GraphError, TypeError, IndexError):
            pass
        
        raise GraphError(f"Key {key} not found")

    def __contains__(self, item):
        # Try node lookup first
        if item in self._nodes:
            return True
        
        # Try edge lookup
        try:
            self.edge(item[0], item[1])
            return True
        except (GraphError, TypeError, IndexError):
            return False

    def __str__(self):
        result = f'{type(self).__name__}:\n'
        for node in self.nodes():
            result += str(node)
        for edge in self.edges():
            result += str(edge)
        return result


class UndirectedGraph(BaseGraph):

    def __init__(self):
        super().__init__()

    def add_edge(self, node1_id, node2_id, **prop):
        if node1_id == node2_id:
            raise GraphError(f"Self-loops are not allowed in undirected graphs")
        
        if node1_id not in self._nodes:
            raise GraphError(f"Node {node1_id} not found")
        if node2_id not in self._nodes:
            raise GraphError(f"Node {node2_id} not found")
        
        # Check if edge already exists (in either direction)
        for edge in self._edges:
            n1, n2 = edge.nodes()
            if ((n1.identifier() == node1_id and n2.identifier() == node2_id) or
                (n1.identifier() == node2_id and n2.identifier() == node1_id)):
                raise GraphError(f"Edge ({node1_id},{node2_id}) already exists")

        # Create and add both directions of the edge
        node1 = self._nodes[node1_id]
        node2 = self._nodes[node2_id]
        edge1 = Edge(node1, node2, **prop)
        edge2 = Edge(node2, node1, **prop)
        self._edges.append(edge1)
        self._edges.append(edge2)
        self._adjacency[node1_id].append(node2_id)
        self._adjacency[node2_id].append(node1_id)

    def degree(self, node_id):
        if node_id not in self._nodes:
            raise GraphError(f"Node {node_id} not found")
        return len(self._adjacency[node_id])

    def __contains__(self, item):
        if item in self._nodes:
            return True
        
        try:
            self.edge(item[0], item[1])
            return True
        except (GraphError, TypeError, IndexError):
            try:
                self.edge(item[1], item[0])
                return True
            except (GraphError, TypeError, IndexError):
                return False


class DirectedGraph(BaseGraph):

    def __init__(self):
        super().__init__()

    def in_degree(self, node_id):
        if node_id not in self._nodes:
            raise GraphError(f"Node {node_id} not found")
        
        in_deg = 0
        for edge in self._edges:
            n1, n2 = edge.nodes()
            if n2.identifier() == node_id:
                in_deg += 1
        return in_deg

    def out_degree(self, node_id):
        if node_id not in self._nodes:
            raise GraphError(f"Node {node_id} not found")
        
        return len(self._adjacency[node_id])


def read_graph_from_csv(node_file, edge_file, directed=False):
    result = DirectedGraph() if directed else UndirectedGraph()
    for i, filename in enumerate((node_file, edge_file)):
        attr_start = i + 1
        with open(filename, 'r', encoding="utf8") as fo:
            ro = csv.reader(fo)
            header = next(ro)
            attr_names = header[attr_start:]
            for line in ro:
                identifier, attr_values = (line[:attr_start],
                                           line[attr_start:])
                attributes = {attr_names[i]: attr_values[i]
                              for i in range(len(attr_names))}
                if i == 0:
                    result.add_node(*identifier, **attributes)
                else:
                    result.add_edge(*identifier, **attributes)
    return result
