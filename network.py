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

        # Add node with attributes if it doesn't exist, initialize pos as a list
        if not G.has_node(uri):
            G.add_node(uri, artist_name=artist_name, track_name=track_name,
                       duration_ms=duration_ms, album_name=album_name, pos=[pos])
        else:
            # If the node exists, append the new position to the existing list
            G.nodes[uri]['pos'].append(pos)
        
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
        for node in G.nodes:
            # Convert the list of positions to a string
            G.nodes[node]['pos'] = ','.join(map(str, G.nodes[node]['pos']))

        # Create a list of edges to iterate over, so you're not modifying the graph while iterating
        edges_to_check = list(G.edges(data=True))

        for u, v, data in edges_to_check:
            if data['weight'] < 3:
                G.remove_edge(u, v)  # Remove edge if its weight is below the threshold

        print(f"Remaining edges: {G.number_of_edges()}")

        # Create a list of nodes to check to avoid modifying the graph while iterating
        nodes_to_check = list(G.nodes())

        for node in nodes_to_check:
            if G.degree(node) <= 1:
                G.remove_node(node)  # Remove the node if its degree is 1
        print(f"Remaining nodes: {G.number_of_nodes()}")
        # Save the graph
        save_file_name = "spotify_AugWeek1.graphml"
        nx.write_graphml(G, save_file_name)

        end_time = time.time()  # End the timer
        duration = end_time - start_time
        print(f"Graph saved in GraphML format as '{save_file_name}'. Saving took {duration:.2f} seconds.")