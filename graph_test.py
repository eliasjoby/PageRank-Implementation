import graph

def undirected_test():
    ugraph = graph.read_graph_from_csv('data/characters-nodes.csv','data/characters-edges.csv')
    assert ugraph.degree('0') == 6
    assert '0' in ugraph
    assert len(ugraph) == 10
    assert ('0', '2') in ugraph
    assert ('2', '0') in ugraph
    print(', '.join(n.identifier() for n in ugraph.nodes()))
    print(ugraph)


def simple_directed_graph():
    dgraph = graph.DirectedGraph()
    dgraph.add_node(0, airport_name='DTW')
    dgraph.add_node(1, airport_name='AMS', country='The Netherlands')
    dgraph.add_node(2, airport_name='ORD', city='Chicago')
    dgraph.add_node(3)
    dgraph.add_node(4)
    dgraph.add_edge(0, 1, flight_time_in_hours=8)
    dgraph.add_edge(0, 2, flight_time_in_hours=1)
    dgraph.add_edge(1, 0, airline_name='KLM')
    dgraph.add_edge(3, 4)
    return dgraph


def directed_test():
    dgraph = simple_directed_graph()
    assert dgraph.in_degree(2) == 1
    assert dgraph.out_degree(0) == 2
    print(dgraph)


if __name__ == '__main__':
    undirected_test()
    directed_test()
