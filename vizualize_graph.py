# visualize_graph.py
import sys
import networkx as nx
import matplotlib.pyplot as plt
import time

def load_graph(graph_file):
    print(f"Loading graph from {graph_file}...")
    start_time = time.time()
    G = nx.read_graphml(graph_file)
    end_time = time.time()
    print(f"Graph loaded in {end_time - start_time:.2f} seconds. It has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
    return G

def visualize_graph(G, output_file, edge_weight_threshold=1):

    print("Starting graph visualization...")
    plt.figure(figsize=(12, 12), dpi=300)

    print("Computing layout...")
    start_time = time.time()
    pos = nx.spring_layout(G, k=0.15, iterations=20)
    end_time = time.time()
    print(f"Layout computed in {end_time - start_time:.2f} seconds.")

    print("Drawing graph... This might take a while for large graphs.")
    start_time = time.time()
    nx.draw(G, pos, node_size=20, edge_color='gray', alpha=0.4, with_labels=False)
    end_time = time.time()
    print(f"Graph drawn in {end_time - start_time:.2f} seconds.")

    plt.title("Filtered Spotify Playlist Graph")
    plt.savefig(output_file)
    print(f"Graph visualization saved to {output_file}")

    # Display the graph
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python vizualize_graph.py <filename>")
        sys.exit(1)
    try:
        graph_file = sys.argv[1]
        with open(graph_file, 'r'):
            pass
    except FileNotFoundError:
        print(f"File not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
    output_file = "spotify_playlist_graph.png"  # Specify the output file name
    G = load_graph(graph_file)
    visualize_graph(G, output_file)
