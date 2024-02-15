import sys
import json
import codecs
import networkx as nx
import time
import matplotlib.pyplot as plt

cache = {}
G = nx.Graph()  # Initialize an undirected graph for the network

def process_playlist(playlist):
    tracks = playlist['tracks']
    for track in tracks:
        # Extracting track details
        uri = track['track_uri']
        artist_name = track['artist_name']
        track_name = track['track_name']
        duration_ms = track['duration_ms']
        album_name = track['album_name']
        pos = track['pos']

        # Add node with attributes if it doesn't exist
        if not G.has_node(uri):
            G.add_node(uri, artist_name=artist_name, track_name=track_name,
                       duration_ms=duration_ms, album_name=album_name, pos=pos)
        
    # Create edges with weights
    for i, track1 in enumerate(tracks):
        for j, track2 in enumerate(tracks):
            if i < j:  # Ensure that each pair is counted only once
                uri1 = track1['track_uri']
                uri2 = track2['track_uri']
                if not G.has_edge(uri1, uri2):
                    G.add_edge(uri1, uri2, weight=1)
                else:
                    G[uri1][uri2]['weight'] += 1

def show_playlist(prefix, pid):
    low = 1000 * int(pid / 1000)
    high = low + 999
    offset = pid - low
    path = prefix + "/mpd.slice." + str(low) + "-" + str(high) + ".json"
    if path not in cache:
        f = codecs.open(path, "r", "utf-8")
        js = f.read()
        f.close()
        playlist_data = json.loads(js)
        cache[path] = playlist_data

    playlist = cache[path]["playlists"][offset]
    
    # Check if playlist's last modification time is within the first week of August 2016
    august_1_2016_start = 1470009600
    august_7_2016_end = 1470614399
    if august_1_2016_start <= playlist["modified_at"] <= august_7_2016_end:
        print(f"Playlist {playlist['pid']} is from the first week of August 2016.")
        process_playlist(playlist)  # Update the graph with this playlist



def show_playlists_in_range(prefix, start, end):
    try:
        istart = int(start)
        iend = int(end)
        total_playlists = iend - istart + 1
        if istart <= iend and istart >= 0 and iend <= 1000000:
            for i, pid in enumerate(range(istart, iend), start=1):
                show_playlist(prefix, pid)
                if i % 1000 == 0:  # print progress every 100 playlists
                    print(f"Processed {i}/{total_playlists} playlists.")
    except ValueError:
        print("bad pid")

def filter_and_save_graph(G, output_file, edge_weight_threshold=1):
    # Filter the graph to include edges above a certain weight threshold
    print(f"Filtering graph to include only edges with weight > {edge_weight_threshold}...")
    start_time = time.time()
    edges_to_keep = [(u, v) for u, v, d in G.edges(data=True) if d['weight'] > edge_weight_threshold]
    H = G.edge_subgraph(edges_to_keep).copy()
    print(f"Filtered graph has {H.number_of_nodes()} nodes and {H.number_of_edges()} edges. Took {time.time() - start_time:.2f} seconds.")
    nx.write_graphml(H, output_file)
    print(f"Filtered graph saved to {output_file}")

if __name__ == "__main__":
    args = sys.argv[1:]
    path = None
    start_pid = None
    end_pid = None

    while args:
        arg = args.pop(0)
        if arg == "--path":
            path = args.pop(0)
        elif "-" in arg:
            fields = arg.split("-")
            if len(fields) == 2:
                start_pid = fields[0]
                end_pid = fields[1]
        else:
            pid = int(arg)
            start_pid = pid
            end_pid = pid

    if path and start_pid is not None and end_pid is not None:
        show_playlists_in_range(path, start_pid, end_pid)
        
        print("Processing complete. Starting to save the graph...")
        start_time = time.time()  # Start the timer

        # Save the graph
        filter_and_save_graph(G, "spotify_AugWeek1.graphml")

        end_time = time.time()  # End the timer
        duration = end_time - start_time
        print(f"Graph saved in GraphML format as 'spotify_graph.graphml'. Saving took {duration:.2f} seconds.")