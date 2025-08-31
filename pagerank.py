import sys
import graph

def pagerank(digraph, num_iterations=40, damping_factor=.85):
    N=len(digraph)

    ranks={node.identifier():1/N for node in digraph.nodes()}


    for i in range(num_iterations):
        dangling_sum=0
        for node in digraph.nodes():
            if digraph.out_degree(node.identifier()) == 0:
                dangling_sum += ranks[node.identifier()]
        new_ranks={}
        for node in digraph.nodes():
            node_id=node.identifier()
            in_links=[edge.nodes()[0].identifier() for edge in digraph.edges()
                      if edge.nodes()[1].identifier()==node_id]
            rank_sum=0
            for in_node_id in in_links:
                out_degree=digraph.out_degree(in_node_id)
                if out_degree>0:
                    rank_sum+=ranks[in_node_id]/out_degree
            new_ranks[node_id]=(1-damping_factor)/N+damping_factor*(rank_sum+(dangling_sum/N))
        ranks=new_ranks
    return ranks

def print_ranks(ranks, max_nodes=20):
    if max_nodes not in range(len(ranks)):
        max_nodes = len(ranks)

    sorted_ids = sorted(ranks.keys(),
                        key=lambda node: (round(ranks[node], 5), node),
                        reverse=True)
    for node_id in sorted_ids[:max_nodes]:
        print(f'{node_id}: {ranks[node_id]:.5f}')
    if max_nodes < len(ranks):
        print('...')

    print(f'Sum: {(sum(ranks[n] for n in sorted_ids)):.5f}')

def pagerank_from_csv(node_file, edge_file, num_iterations):
    rgraph = graph.read_graph_from_csv(node_file, edge_file, True)
    ranks = pagerank(rgraph, num_iterations)
    print_ranks(ranks)