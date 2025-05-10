# README: Predicting User Internet Activity from Encrypted Network Traffic Patterns

## Overview
This repository contains the code and resources for the research paper *"Predicting User Internet Activity from Encrypted Network Traffic Patterns"*, which investigates whether encrypted web traffic metadata (packet size, timing, and direction) can reveal user browsing activity. The study demonstrates that machine learning models can predict visited websites with **72% accuracy** using only encrypted traffic patterns.

## Key Findings
- **Privacy Implications**: Even with encryption, metadata leaks meaningful information about user behavior.
- **Feature Engineering**: Statistical summaries of packet data (e.g., average size, inter-packet timing) enable accurate classification.
- **Model Performance**: 
  - Random Forest: **68% accuracy**  
  - K-Nearest Neighbors (KNN) with PCA: **72% accuracy**


## Repository Structure (Updated)
```
.
├── data/                           # Raw packet capture logs
│   ├── chat_gpt_packet_log.csv
│   ├── instagram_packet_log.csv
│   ├── reddit_packet_log.csv
│   ├── spotify_packet_log.csv
│   ├── tetris_packet_log.csv
│   ├── wikipedia_packet_log.csv
│   ├── wouldyourather_packet_log.csv
│   ├── youtube_browsing_packet_log.csv
│   └── youtube_packet_log.csv
│
├── src/                            # Data processing and analysis code
│   ├── shark_data_collection.py    # Primary packet capture script
│   ├── port_shark_data_collection.py
│   ├── sharkless_data_collection.py
│   ├── data_creation.ipynb         # Dataset generation notebook
│   ├── data_analysis.ipynb         # Feature analysis notebook
│   ├── packet_log.csv              # Consolidated raw data
│   └── network_traffic_features.csv # Processed features
│
├── vis/                            # Generated visualizations
│   ├── boxplots.png                # Feature distributions by website
│   ├── corrheatmap.png             # Feature correlation matrix
│   ├── randomforrest.png           # Decision tree visualization
│   ├── smoothedsurfacemap.png      # KNN-PCA accuracy surface
│   ├── spotify_data.png            # Spotify traffic pattern
│   ├── surfacemap.png              # 3D accuracy plot
│   └── tetris_data.png             # Tetris traffic pattern
│
└── README.md                       # This document
```

## Requirements
- Python 3.8+
- Libraries: `pyshark`, `scikit-learn`, `pandas`, `numpy`, `matplotlib`, `seaborn`
- Wireshark/tshark (for packet capture)

## Dataset
- **Websites**: Spotify, Wikipedia, ChatGPT, Instagram, Reddit, YouTube, Tetris, Would You Rather.
- **Features**: 
  - Packet sizes (incoming/outgoing averages)  
  - Inter-packet timings  
  - Packet count ratios  
  - Directionality (inferred from host IPs).

## Results
- **Best Model**: KNN with PCA (6 components, *k*=3) achieved **72% accuracy**.
- **Interpretability**: Random Forest revealed key discriminative features (e.g., Tetris had distinct outgoing packet patterns).
- Visualization highlights:
  - PCA reduced feature space while preserving class separation.
  - Boxplots showed clear differences in packet counts across sites.

## Citation
If this work aids your research, please cite our paper (BibTeX forthcoming).

## Contact
- Nishk Patel: `nishkdp2@illinois.edu`  
- Ethan Mathew: `ethmth2@illinois.edu`  

---

**Note**: This research underscores privacy risks in encrypted traffic. Use responsibly and ethically.
