import sys
import json
import codecs
import datetime
import networkx as nx
import time
import matplotlib.pyplot as plt

pretty = True
compact = False
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

def print_playlist(playlist):
    if pretty:
        print("===", playlist["pid"], "===")
        print(playlist["name"])
        print("  followers", playlist["num_followers"])
        print(
            "  modified",
            datetime.datetime.fromtimestamp(playlist["modified_at"]).strftime(
                "%Y-%m-%d"
            ),
        )
        print("  edits", playlist["num_edits"])
        print()
        if not compact:
            for track in playlist["tracks"]:
                print(
                    "%3d %s - %s"
                    % (track["pos"], track["track_name"], track["album_name"])
                )
            print()
    else:
        print(json.dumps(playlist, indent=4))

def show_playlist(prefix, pid):
    if pid >= 0 and pid < 1000000:
        low = 1000 * int(pid / 1000)
        high = low + 999
        offset = pid - low
        path = prefix + "/mpd.slice." + str(low) + "-" + str(high) + ".json"
        if path not in cache:
            f = codecs.open(path, "r", "utf-8")
            js = f.read()
            f.close()
            playlist = json.loads(js)
            cache[path] = playlist

        playlist = cache[path]["playlists"][offset]
        process_playlist(playlist)  # Update the graph with this playlist

def show_playlists_in_range(prefix, start, end):
    try:
        istart = int(start)
        iend = int(end)
        total_playlists = iend - istart + 1
        if istart <= iend and istart >= 0 and iend <= 1000000:
            for i, pid in enumerate(range(istart, iend), start=1):
                show_playlist(prefix, pid)
                if i % 100 == 0:  # print progress every 100 playlists
                    print(f"Processed {i}/{total_playlists} playlists.")
    except ValueError:
        print("bad pid")


def usage():
    print(f"{sys.argv[0]} --path mpd --pretty --compact --raw pid")
    print(f"{sys.argv[0]} --path mpd --pretty --compact --raw pid1-pid2")

if __name__ == "__main__":
    args = sys.argv[1:]
    path = None
    start_pid = None
    end_pid = None

    while args:
        arg = args.pop(0)
        if arg == "--pretty":
            pretty = True
        elif arg == "--path":
            path = args.pop(0)
        elif arg == "--compact":
            compact = True
        elif arg == "--help":
            usage()
        elif arg == "--raw":
            pretty = False
        elif "-" in arg:
            fields = arg.split("-")
            if len(fields) == 2:
                start_pid = fields[0]
                end_pid = fields[1]
        else:
            try:
                pid = int(arg)
                start_pid = pid
                end_pid = pid
            except ValueError:
                usage()

    if path and start_pid is not None and end_pid is not None:
        show_playlists_in_range(path, start_pid, end_pid)
        
        print("Processing complete. Starting to save the graph...")
        start_time = time.time()  # Start the timer

        # Save the graph
        nx.write_graphml(G, "spotify_graph.graphml")

        end_time = time.time()  # End the timer
        duration = end_time - start_time
        print(f"Graph saved in GraphML format as 'spotify_graph.graphml'. Saving took {duration:.2f} seconds.")
    else:
        usage()

# After processing all playlists, you can use G for analysis or visualization
