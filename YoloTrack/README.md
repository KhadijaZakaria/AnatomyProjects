# Football Player Detection and Tracking using YOLO and OpenCV

This Python script utilizes OpenCV and YOLO (You Only Look Once) for detecting and tracking football players in match videos. It processes video frames, aligns them with a 2D football pitch, and visualizes player movements and heatmaps.

## Features

- **Player Detection and Tracking**:
  - Detects players in video frames using YOLO.
  - Assigns unique IDs to players based on proximity in consecutive frames.

- **Football Pitch Alignment**:
  - Allows manual selection of reference points on the pitch for coordinate alignment.
  - Computes a transformation matrix to map video coordinates to a standard 2D football pitch.

- **Data Visualization**:
  - Generates movement trails on a 2D football pitch for individual players.
  - Creates heatmaps to highlight high-activity zones for each player.

- **Video Processing**:
  - Processes video frame-by-frame with Non-Maximum Suppression (NMS) for optimized detections.
  - Displays video with overlays showing detected players and their IDs.

- **Exportable Data**:
  - Formats player tracking data for export or further analysis.

## Requirements

1. **YOLO Model Files**:
   - `yolov4.weights`
   - `yolov4.cfg`

2. **A Video File**:
   - A football match video to analyze.

3. **Python Dependencies**:
   - OpenCV
   - NumPy
   - Matplotlib
   - SciPy
## Heatmap 
 is a visual representation that shows the density or frequency of events across a specific area. In the context of this project, the heatmap illustrates where a player has spent the most time on the football pitch. Here's a simple explanation:

- Purpose:

The heatmap helps identify areas on the pitch where the player was most active. It shows the intensity of the player's presence, with hotter (brighter) areas indicating more frequent visits.
- How It Works:

Every time the player is detected in a certain position on the pitch, that position's value on the heatmap increases.
The heatmap accumulates these values over time, creating a visual trail of the player's movements.
- Color Representation:

The heatmap uses colors to show activity levels:
Red or bright colors indicate areas where the player spent a lot of time.
Cooler colors (like blue) represent less activity.
- Benefits:

This visual tool helps coaches and analysts understand player behavior, such as preferred zones, movement patterns, and overall involvement on the pitch.

![Screenshot 2025-01-02 174605](https://github.com/user-attachments/assets/e794ab2d-925c-4ae7-b8bc-8b0a971df92a)

## video
https://github.com/user-attachments/assets/4de3adbc-ebd8-4a8a-8a03-9bfbf894cd22

## license
This project is licensed under the MIT License


## Install dependencies using:
```bash
pip install opencv-python-headless numpy matplotlib scipy
Usage
Clone the repository and ensure all required files are in place.

python yolo.py
Manually select four reference points on the pitch:
Top-left corner of the visible pitch area.
Top-right corner of the visible pitch area.
Bottom-left corner of the visible pitch area.
Bottom-right corner of the visible pitch area.
Watch the processed video with player tracking displayed in real-time.
After video processing, visualize player data:
Movement trails on a 2D pitch.
Heatmaps of activity zones.
Suggested Improvements
Enhance player ID assignment to handle occlusions and abrupt stops.
Add detection for other objects, like the football.
Automate data saving in formats like JSON or CSV.
