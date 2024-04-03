# Network Analysis In Spotify Playlist Data

![Visualization of Network Analysis](https://github.com/KyoKii02/CPSC572-Project/assets/147207215/3d332caf-f29a-4461-b631-2e422183e5aa)

## Overview

This project delves into the public **Spotify Million Playlist Dataset** provided by AiCrowd, utilizing a network science approach to decipher the interconnectedness of humanity's musical experiences. Our goal is to explore the underlying commonalities among songs grouped in playlists, aiming to shed light on the psychological factors influencing playlist construction and the dynamics behind the popularity of certain tracks.

## Research Paper

For a comprehensive understanding of our findings and methodologies, refer to our research paper: [Research Paper](https://github.com/KyoKii02/CPSC572-Project/blob/main/Research%20Paper.pdf).
A summary can be found below.

### Objectives

- Construct a network model where songs co-occurring in playlists are interconnected.
- Perform comprehensive analyses to uncover playlist communities and the traits correlated with song popularity.
- Investigate the influence of genres, eras, artists, and cultural themes on playlist creation.

## Findings

Our analysis revealed a highly clustered network structure, showcasing:
- Distinct communities within playlists reflecting popular genres, music eras, artists, and thematic associations.
- A tendency for more popular songs to be positioned at the beginning of playlists and to have shorter durations.

These insights not only highlight the significant role of cultural and thematic associations in playlist creation but also hint at strategic song placement and duration in capturing listener attention.

## Limitations and Future Work

The study was constrained by computational resources, limiting our analysis to a week's worth of playlist data. Future investigations could expand on this by exploring how playlist networks evolve over time, offering deeper insights into the global music culture's influence and evolution.

## Repository Contents

This repository contains files and data related to the final project, offering insights into the network analysis of Spotify playlist data. Below is a detailed description of each file and its purpose:

- `Community_detection.ipynb`: Performs community detection and analysis to uncover distinct groups within the playlists that share common characteristics.

- `Graph_stats.ipynb`: Computes basic statistics, null models, and conducts deeper analysis of the dataset to understand the structural properties of the network.

- `graph_stats_Poly_regression.ipynb`: An experiment utilizing polynomial regression based on the analyses performed in `Graph_stats.ipynb`, aimed at uncovering more complex relationships within the data.

- `Vizualize_graph.py`: Provides a simple yet effective visualization tool to validate the construction of the network, helping to visually inspect the network's structure and the connections between nodes.

- `network.py`: The main code for constructing the network model where songs co-occurring in playlists are interconnected. This file lays the foundation for the network analysis.

- `spotify_AugWeek1.graphml`: The output file from `network.py`, representing the network model constructed from a week's worth of Spotify playlist data.

- `Network_with_communities.graphml`: An enhanced version of the `spotify_AugWeek1.graphml` file with community detection applied, showcasing the identified communities within the network.

These documents and files constitute the bulk of our original work. The analysis and visualization provided by these tools contribute significantly to our understanding of the complex dynamics within Spotify playlists and the factors influencing song popularity and playlist construction.


These documents constitute our original work, with the remaining data sourced from the [Spotify Million Playlist Dataset Challenge](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge/dataset_files) hosted by AiCrowd.
