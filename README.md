# Network Analysis In Spotify Playlist Data

![Visualization of Network Analysis](https://github.com/KyoKii02/CPSC572-Project/assets/147207215/3d332caf-f29a-4461-b631-2e422183e5aa)

## Overview

This project delves into the public **Spotify Million Playlist Dataset** provided by AiCrowd, utilizing a network science approach to decipher the interconnectedness of humanity's musical experiences. Our goal is to explore the underlying commonalities among songs grouped in playlists, aiming to shed light on the psychological factors influencing playlist construction and the dynamics behind the popularity of certain tracks.

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

This repository contains files and data related to the final project:
- `network.py`
- `graph_stats.ipynb`
- `community_detection.py`

These documents constitute our original work, with the remaining data sourced from the [Spotify Million Playlist Dataset Challenge](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge/dataset_files) hosted by AiCrowd.

## Dataset Source

For further information on the dataset used for this project, please visit the [Spotify Million Playlist Dataset Challenge](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge/dataset_files) on AiCrowd.
