"""
graph.py.

ADT definitions for directed and undirected graphs.

Project UID bd3b06d8a60861e18088226c3a1f0595e4426dcf
"""

import csv
import doctest
from abc import ABC,abstractmethod


class GraphError(Exception):
    """This class is used for raising exceptions in the graph ADTs.

    >>> e = GraphError()
    >>> str(e)
    ''
    >>> f = GraphError('some message')
    >>> str(f)
    'some message'
    >>> repr(e)
    "GraphError('')"
    >>> f # interpreter does the same thing as print(repr(f))
    GraphError('some message')
    """

    def __init__(self, message=''):
        self.message=message
        super().__init__(self.message)

    def __str__(self):
        return self.message

    def __repr__(self):
        #canonical string representation of the error
        return f"GraphError({repr(str(self))})"


class Node:
    r"""Represents a node in a graph.

    >>> n = Node('node1', weight=80, age=90)
    >>> n.identifier()
    'node1'
    >>> d = n.attributes()
    >>> d['age']
    90
    >>> d['weight']
    80
    >>> str(n)
    'Node [node1]\n    age : 90\n    weight : 80\n'
    """

    def __init__(self, identifier, **attributes):
        """Initialize this node with the given ID.

        The keyword arguments are optional node attributes.
        """
        self.id=identifier
        self.prop=attributes

    def identifier(self):
        """Return the identifier of this node."""
        return self.id

    def attributes(self):
        """Return a copy of this node's attribute dictionary."""
        return self.prop.copy()

    def __str__(self):
        """Return a string representation of this node.

        Produces a representation of this node and its attributes in
        sorted, increasing, lexicographic order.
        """
        sorted_dict=sorted(self.prop.items())
        final=[f"Node [{self.id}]\n"]
        for x,y in sorted_dict:
            final.append(f"    {x} : {y}\n")
        return "".join(final)

class Edge:
    r"""Represents a directed edge in a graph.

    >>> n1, n2 = Node('node1'), Node('node2')
    >>> e = Edge(n1, n2, size=3, cost=5)
    >>> d = e.attributes()
    >>> d['cost']
    5
    >>> d['size']
    3
    >>> e.nodes() == (n1, n2)
    True
    >>> str(e)
    'Edge from node [node1] to node [node2]\n    cost : 5\n    size : 3\n'
    """

    def __init__(self, node1, node2, **attributes):
        """Initialize this edge with the Nodes node1 and node2.

        The keyword arguments are optional edge attributes.
        """
        self.node1=node1
        self.node2=node2
        self.prop=attributes

    def attributes(self):
        """Return a copy of this edge's attribute dictionary."""
        return self.prop.copy()

    def nodes(self):
        """Return a tuple of the Nodes corresponding to this edge.

        The nodes are in the same order as passed to the constructor.
        """
        tup=(self.node1,self.node2)
        return tup
    
    def __str__(self):
        """Return a string representation of this edge.

        Produces a representation of this edge and its attributes in
        sorted, increasing, lexicographic order.
        """
        final=[f"Edge from node [{self.node1.identifier()}] to node [{self.node2.identifier()}]\n"]
        for x,y in sorted(self.prop.items()):
            final.append(f"    {x} : {y}\n")
        return "".join(final)

class BaseGraph(ABC):
    r"""A graph where the nodes and edges have optional attributes.

    This class should not be instantiated directly by a user.

    >>> g = BaseGraph()
    >>> len(g)
    0
    >>> g.add_node(1, a=1, b=2)
    >>> g.add_node(3, f=6, e=5)
    >>> g.add_node(2, c=3)
    >>> g.add_edge(1, 2, g=7)
    >>> g.add_edge(3, 2, h=8)
    >>> len(g)
    3
    >>> str(g.node(2))
    'Node [2]\n    c : 3\n'
    >>> g.node(4)
    Traceback (most recent call last):
        ...
    GraphError: ...
    >>> str(g.edge(1, 2))
    'Edge from node [1] to node [2]\n    g : 7\n'
    >>> g.edge(1, 3)
    Traceback (most recent call last):
        ...
    GraphError: ...
    >>> len(g.nodes())
    3
    >>> g.nodes()[0].identifier()
    1
    >>> len(g.edges())
    2
    >>> str(g.edges()[1])
    'Edge from node [3] to node [2]\n    h : 8\n'
    >>> 1 in g, 4 in g
    (True, False)
    >>> (1, 2) in g, (2, 3) in g
    (True, False)
    >>> g[1].identifier()
    1
    >>> g[(1, 2)].nodes()[0].identifier()
    1
    >>> print(g)
    BaseGraph:
    Node [1]
        a : 1
        b : 2
    Node [2]
        c : 3
    Node [3]
        e : 5
        f : 6
    Edge from node [1] to node [2]
        g : 7
    Edge from node [3] to node [2]
        h : 8
    <BLANKLINE>
    """
    @abstractmethod
    def __init__(self):
        """Initialize this graph object."""
        self.node_dict={} #node id->node obj
        self.edge_set=set() #set of edge objects
        self.adj={} # node id -> adjNode id

    def __len__(self):
        """Return the number of nodes in the graph."""
        return len(self.node_dict)

    def add_node(self, node_id, **prop):
        """Add a node to this graph.

        Requires that node_id, the unique identifier for the node, is
        hashable and comparable to all identifiers for nodes currently
        in the graph. The keyword arguments are optional node
        attributes. Raises a GraphError if a node already exists with
        the given ID.
        """
        if node_id in self.node_dict.keys():
            raise GraphError(f"Node {node_id} already exists")
        self.node_dict[node_id]=Node(node_id,attributes=prop)
        self.adj[node_id]=[]

    def node(self, node_id):
        """Return the Node object for the node whose ID is node_id.

        Raises a GraphError if the node ID is not in the graph.
        """
        if node_id not in self.node_dict:
            raise GraphError(f"Node {node_id} not found")
        return self.node_dict[node_id]

    def nodes(self):
        """Return a list of all the Nodes in this graph.

        The nodes are sorted by increasing node ID.
        """
        list_nodes=[]
        for x in sorted(self.node_dict):
            list_nodes.append(x)
        return list_nodes

    def add_edge(self, node1_id, node2_id, **prop):
        """Add an edge between the nodes with the given IDs.

        The keyword arguments are optional edge attributes. Raises a
        GraphError if either node is not found, or if the graph
        already contains an edge between the two nodes.
        """
        if [node1_id,node2_id] in self.edge_set:
            raise GraphError(f"The edge ({node1_id},{node2_id}) already exists")
        
        self.edge_set.add(Edge(node1_id,node2_id,prop))
        self.adj[node1_id].append(node2_id)

    def edge(self, node1_id, node2_id):
        """Return the Edge object for the edge between the given nodes.

        Raises a GraphError if the edge is not in the graph.
        """
        flag=0
        res
        for p in self.edge_set:
           (n1,n2)=p.nodes()
           if((node1_id,node2_id)==(n1,n2)):
               flag=1
               res=p
               break
        if flag==0:
            raise GraphError(f"Edge ({node1_id},{node2_id}) already exists")
        return res

    def edges(self):
        """Return a list of all the edges in this graph.

        The edges are sorted in increasing, lexicographic order of the
        IDs of the two nodes in each edge.
        """
        final=[]
        for e in self.edge_set:
            final.append(e.nodes())
        final.sort()
        return final

    def __getitem__(self, key):
        """Return the Node or Edge corresponding to the given key.

        If key is a node ID, returns the Node object whose ID is key.
        If key is a pair of node IDs, returns the Edge object
        corresponding to the edge between the two nodes. Raises a
        GraphError if the node IDs or edge are not in the graph.
        """
        ans
        if isinstance(key,tuple) and len(key)>1:
            flag=0
            for e in self.edge_set:
                if(e.nodes()==key):
                    flag=1
                    ans=e
                    break
            if(flag):
                return ans
            else:
                raise GraphError(f"The given pair of edges ({key[0]},{key[1]}) does not exist")
        else:
            flag=0
            ans
            for x,y in self.node_dict.items():
                if(x==key):
                    flag=1
                    ans=y
                    break
            if(flag):
                return ans
            else:
                raise GraphError(f"The given node {key} does not exist")

    def __contains__(self, item):
        """Return whether the given node or edge is in the graph.

        If item is a node ID, returns True if there is a node in this
        graph with ID item. If item is a pair of node IDs, returns
        True if there is an edge corresponding to the two nodes.
        Otherwise, returns False.
        """
        if isinstance(item,tuple) and len(item)>1:
            for e in self.edge_set:
                if(item==e.nodes()):
                    return True
            return False
        else:
            return item in self.node_dict.keys()

    def __str__(self):
        """Return a string representation of the graph.

        The string representation contains the nodes in sorted,
        increasing order, followed by the edges in order.
        """
        result = f'{type(self).__name__}:\n'
        for node in self.nodes():
            result += str(node)
        for edge in self.edges():
            result += str(edge)
        return result


class UndirectedGraph(BaseGraph):
    """An undirected graph where nodes/edges have optional attributes.

    >>> g = UndirectedGraph()
    >>> g.add_node(1, a=1)
    >>> g.add_node(2, b=2)
    >>> g.add_edge(1, 2, c=3)
    >>> len(g)
    2
    >>> g.degree(1)
    1
    >>> g.degree(2)
    1
    >>> g.edge(1, 2).nodes() == (g.node(1), g.node(2))
    True
    >>> g.edge(2, 1).nodes() == (g.node(2), g.node(1))
    True
    >>> 1 in g, 4 in g
    (True, False)
    >>> (1, 2) in g, (2, 1) in g
    (True, True)
    >>> (2, 3) in g
    False
    >>> g[1].identifier()
    1
    >>> g[(1, 2)].nodes()[0].identifier()
    1
    >>> g.add_edge(1, 1, d=4)
    Traceback (most recent call last):
        ...
    GraphError: ...
    >>> print(g)
    UndirectedGraph:
    Node [1]
        a : 1
    Node [2]
        b : 2
    Edge from node [1] to node [2]
        c : 3
    Edge from node [2] to node [1]
        c : 3
    <BLANKLINE>
    """

    def __init__(self):
        """Initialize this UndirectedGraph object."""
        # add your code here or remove this method

    def degree(self, node_id):
        """Return the degree of the node with the given ID.

        Raises a GraphError if the node ID is not found.
        """
        # add your code here

    # Add whatever overridden or new methods you need here


class DirectedGraph(BaseGraph):
    """A directed graph where nodes/edges have optional attributes.

    >>> g = DirectedGraph()
    >>> g.add_node(1, a=1)
    >>> g.add_node(2, b=2)
    >>> g.add_edge(1, 2, c=3)
    >>> len(g)
    2
    >>> g.in_degree(1), g.out_degree(1)
    (0, 1)
    >>> g.in_degree(2), g.out_degree(2)
    (1, 0)
    >>> g.edge(1, 2).nodes() == (g.node(1), g.node(2))
    True
    >>> g.edge(2, 1)
    Traceback (most recent call last):
        ...
    GraphError: ...
    >>> 1 in g, 4 in g
    (True, False)
    >>> (1, 2) in g, (2, 1) in g
    (True, False)
    >>> g[1].identifier()
    1
    >>> g[(1, 2)].nodes()[0].identifier()
    1
    >>> g.add_edge(1, 1, d=4)
    >>> g.in_degree(1), g.out_degree(1)
    (1, 2)
    >>> g.in_degree(-1)
    Traceback (most recent call last):
        ...
    GraphError: ...
    >>> g.out_degree(-1)
    Traceback (most recent call last):
        ...
    GraphError: ...
    >>> print(g)
    DirectedGraph:
    Node [1]
        a : 1
    Node [2]
        b : 2
    Edge from node [1] to node [1]
        d : 4
    Edge from node [1] to node [2]
        c : 3
    <BLANKLINE>
    """

    def __init__(self):
        """Initialize this DirectedGraph object."""
        # add your code here or remove this method

    def in_degree(self, node_id):
        """Return the in-degree of the node with the given ID.

        Raises a GraphError if the node is not found.
        """
        # add your code here

    def out_degree(self, node_id):
        """Return the out-degree of the node with the given ID.

        Raises a GraphError if the node is not found.
        """
        # add your code here

    # Add whatever overridden or new methods you need here


def read_graph_from_csv(node_file, edge_file, directed=False):
    """Read a graph from CSV node and edge files.

    Refer to the project specification for the file formats.
    """
    result = DirectedGraph() if directed else UndirectedGraph()
    for i, filename in enumerate((node_file, edge_file)):
        attr_start = i + 1
        with open(filename, 'r', encoding="utf8") as csv_data:
            reader = csv.reader(csv_data)
            header = next(reader)
            attr_names = header[attr_start:]

            for line in reader:
                identifier, attr_values = (line[:attr_start],
                                           line[attr_start:])
                attributes = {attr_names[i]: attr_values[i]
                              for i in range(len(attr_names))}
                if i == 0:
                    result.add_node(*identifier, **attributes)
                else:
                    result.add_edge(*identifier, **attributes)
    return result


def _test():
    """Run this module's doctests."""
    doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)


if __name__ == '__main__':
    # Run the doctests
    _test()
