import graph
import pagerank

def test_doctest_example():
    print("Testing doctest example...")
    
    g = graph.DirectedGraph()
    g.add_node(0, airport_name='DTW')
    g.add_node(1, airport_name='AMS', country='The Netherlands')
    g.add_node(2, airport_name='ORD', city='Chicago')
    g.add_edge(0, 1, flight_time_in_hours=8)
    g.add_edge(0, 2, flight_time_in_hours=1)
    g.add_edge(1, 0, airline_name='KLM')
    
    ranks_1 = pagerank.pagerank(g, 1)
    ranks_40 = pagerank.pagerank(g, 40)
    
    print(f"After 1 iteration: {ranks_1}")
    print(f"After 40 iterations: {ranks_40}")
    
    total_1 = sum(ranks_1.values())
    total_40 = sum(ranks_40.values())
    print(f"Sum after 1 iteration: {total_1:.6f}")
    print(f"Sum after 40 iterations: {total_40:.6f}")
    
    assert abs(total_1 - 1.0) < 0.001, f"Sum should be 1.0, got {total_1:.6f}"
    assert abs(total_40 - 1.0) < 0.001, f"Sum should be 1.0, got {total_40:.6f}"
    
    assert all(rank > 0 for rank in ranks_1.values()), "All ranks should be positive"
    assert all(rank > 0 for rank in ranks_40.values()), "All ranks should be positive"
    
    print("✓ Doctest example test passed\n")


def test_single_node():
    print("Testing single node...")
    
    g = graph.DirectedGraph()
    g.add_node(42)
    
    ranks = pagerank.pagerank(g)
    print(f"Single node rank: {ranks}")
    
    assert abs(ranks[42] - 1.0) < 0.001, f"Expected 1.0, got {ranks[42]:.6f}"
    print("✓ Single node test passed\n")

def test_triangle_graph():
    print("Testing symmetric triangle...")
    
    g = graph.DirectedGraph()
    g.add_node(0)
    g.add_node(1)
    g.add_node(2)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    
    ranks = pagerank.pagerank(g, num_iterations=50)
    print(f"Triangle ranks: {ranks}")
    expected = 1.0 / 3
    for node_id in [0, 1, 2]:
        assert abs(ranks[node_id] - expected) < 0.001, \
            f"Node {node_id}: got {ranks[node_id]:.6f}, expected {expected:.6f}"
    
    total = sum(ranks.values())
    assert abs(total - 1.0) < 0.001, f"Sum should be 1.0, got {total:.6f}"
    print(f"Sum: {total:.6f}")
    print("✓ Triangle test passed\n")


def test_dangling_node():
    print("Testing dangling node...")
    
    g = graph.DirectedGraph()
    g.add_node(0)
    g.add_node(1)
    g.add_node(2)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    
    ranks = pagerank.pagerank(g, num_iterations=20)
    print(f"Dangling node ranks: {ranks}")
    
    assert ranks[2] > ranks[0] and ranks[2] > ranks[1], \
        "Dangling node should have highest PageRank"
    
    total = sum(ranks.values())
    assert abs(total - 1.0) < 0.001, f"Sum should be 1.0, got {total:.6f}"
    print(f"Sum: {total:.6f}")
    print("✓ Dangling node test passed\n")


def test_two_node_cycle():
    print("Testing two-node cycle...")
    
    g = graph.DirectedGraph()
    g.add_node(0)
    g.add_node(1)
    g.add_edge(0, 1)
    g.add_edge(1, 0)
    
    ranks = pagerank.pagerank(g, num_iterations=20)
    print(f"Two-node cycle ranks: {ranks}")
    
    assert abs(ranks[0] - 0.5) < 0.001, f"Node 0: got {ranks[0]:.6f}, expected 0.5"
    assert abs(ranks[1] - 0.5) < 0.001, f"Node 1: got {ranks[1]:.6f}, expected 0.5"
    
    total = sum(ranks.values())
    assert abs(total - 1.0) < 0.001, f"Sum should be 1.0, got {total:.6f}"
    print(f"Sum: {total:.6f}")
    print("✓ Two-node cycle test passed\n")


def test_print_ranks():
    print("Testing print_ranks function...")
    
    ranks = {0: 0.4, 1: 0.35, 2: 0.15, 3: 0.1}
    
    print("Top 2 nodes:")
    pagerank.print_ranks(ranks, max_nodes=2)
    
    print("\nAll nodes:")
    pagerank.print_ranks(ranks)
    
    print("✓ print_ranks test passed\n")


def run_all_tests():
    print("Running PageRank Tests\n\n")
    
    tests = [
        test_doctest_example,
        test_triangle_graph,
        test_single_node,
        test_dangling_node,
        test_two_node_cycle,
        test_print_ranks
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"{test_func.__name__} FAILED: {e}\n")
    print(f"Results: {passed}/{total} tests passed")
    if passed == total:
        print("All tests passed!")
    else:
        print("Some tests failed - check implementation")

if __name__ == '__main__':
    run_all_tests()