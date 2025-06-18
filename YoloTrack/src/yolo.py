import cv2
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from scipy.ndimage import gaussian_filter
import os


class PitchTracker:
    def __init__(self):
        self.PITCH_LENGTH = 105
        self.PITCH_WIDTH = 68
        self.OUTPUT_SIZE = (800, 600)
        self.reference_points = None
        self.reference_features = None
        self.reference_frame = None
        self.orb = cv2.ORB_create(nfeatures=2000)
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        self.transform_matrix = None

    def initialize_reference(self, frame):
        """Initialize reference frame with feature points"""
        self.reference_frame = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        keypoints, descriptors = self.orb.detectAndCompute(gray, None)
        self.reference_features = (keypoints, descriptors)

        print("\nPitch Corner Selection Instructions:")
        print("Select 4 points that form a rectangle on the pitch:")
        print("1. Top-Left corner of visible pitch area")
        print("2. Top-Right corner of visible pitch area")
        print("3. Bottom-Left corner of visible pitch area")
        print("4. Bottom-Right corner of visible pitch area")

        points = []
        frame_copy = frame.copy()

        def mouse_callback(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                points.append([x, y])
                cv2.circle(frame_copy, (x, y), 5, (0, 255, 0), -1)
                if len(points) > 1:
                    cv2.line(frame_copy, tuple(points[-2]), tuple(points[-1]), (0, 255, 0), 2)
                cv2.imshow('Select Reference Points', frame_copy)

        cv2.imshow('Select Reference Points', frame_copy)
        cv2.setMouseCallback('Select Reference Points', mouse_callback)

        while len(points) < 4:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                cv2.destroyAllWindows()
                return False

        cv2.destroyAllWindows()
        self.reference_points = np.float32(points)
        return True

    def update_transform(self, frame):
        """Update transformation matrix based on feature matching"""
        if self.reference_features is None:
            return False

        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            keypoints, descriptors = self.orb.detectAndCompute(gray, None)
            if descriptors is None:
                return False

            matches = self.bf.match(self.reference_features[1], descriptors)
            matches = sorted(matches, key=lambda x: x.distance)
            good_matches = matches[:30]

            if len(good_matches) < 10:
                return False

            ref_pts = np.float32([self.reference_features[0][m.queryIdx].pt for m in good_matches])
            curr_pts = np.float32([keypoints[m.trainIdx].pt for m in good_matches])
            H, mask = cv2.findHomography(curr_pts, ref_pts, cv2.RANSAC, 5.0)
            if H is None:
                return False

            ref_corners = self.reference_points
            dst_corners = np.float32([
                [0, 0],
                [self.OUTPUT_SIZE[0], 0],
                [0, self.OUTPUT_SIZE[1]],
                [self.OUTPUT_SIZE[0], self.OUTPUT_SIZE[1]]
            ])

            transformed_corners = cv2.perspectiveTransform(
                ref_corners.reshape(-1, 1, 2),
                np.linalg.inv(H)
            ).reshape(-1, 2)

            self.transform_matrix = cv2.getPerspectiveTransform(
                transformed_corners,
                dst_corners
            )
            return True
        except Exception as e:
            print(f"Error in update_transform: {str(e)}")
            return False

    def transform_point(self, point):
        """Transform a point using current transformation matrix"""
        if self.transform_matrix is None:
            return None

        try:
            point_h = np.array([[[point[0], point[1]]]], dtype=np.float32)
            transformed = cv2.perspectiveTransform(point_h, self.transform_matrix)
            return (int(transformed[0][0][0]), int(transformed[0][0][1]))
        except Exception as e:
            print(f"Error in transform_point: {str(e)}")
            return None


def draw_2d_pitch(size=(800, 600)):
    """Draw 2D football pitch"""
    pitch = np.zeros((size[1], size[0], 3), dtype=np.uint8)
    pitch[...] = (0, 128, 0)  # Green background
    cv2.rectangle(pitch, (0, 0), (size[0] - 1, size[1] - 1), (255, 255, 255), 2)
    cv2.line(pitch, (size[0] // 2, 0), (size[0] // 2, size[1]), (255, 255, 255), 2)
    cv2.circle(pitch, (size[0] // 2, size[1] // 2), size[1] // 5, (255, 255, 255), 2)
    pen_area_width = size[0] // 5
    pen_area_height = size[1] // 3
    cv2.rectangle(pitch, (0, (size[1] - pen_area_height) // 2),
                  (pen_area_width, (size[1] + pen_area_height) // 2), (255, 255, 255), 2)
    cv2.rectangle(pitch, (size[0] - pen_area_width, (size[1] - pen_area_height) // 2),
                  (size[0], (size[1] + pen_area_height) // 2), (255, 255, 255), 2)
    return pitch


def assign_player_id(center, existing_players, max_distance=50):
    """Assign player ID based on proximity to previous positions"""
    closest_id = -1
    min_distance = float('inf')

    for player_id, positions in existing_players.items():
        if positions:
            last_pos = positions[-1]
            distance = np.sqrt((center[0] - last_pos[0]) ** 2 + (center[1] - last_pos[1]) ** 2)
            if distance < max_distance and distance < min_distance:
                min_distance = distance
                closest_id = player_id

    return closest_id if closest_id != -1 else max(existing_players.keys(), default=-1) + 1


def visualize_player_data(player_positions, player_colors, tracker):
    """Visualize player tracking data"""
    if not player_positions:
        print("No tracking data available")
        return

    print("\nAvailable Player IDs:", list(player_positions.keys()))
    while True:
        try:
            selected_id = int(input("Enter Player ID to visualize (or -1 to exit): "))
            if selected_id == -1:
                break
            if selected_id in player_positions:
                # Create figure with subplots
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

                # Plot movement trail
                pitch_img = draw_2d_pitch(tracker.OUTPUT_SIZE)
                ax1.imshow(cv2.cvtColor(pitch_img, cv2.COLOR_BGR2RGB))
                positions = np.array(player_positions[selected_id])
                ax1.plot(positions[:, 0], positions[:, 1], '-o',
                         color=np.array(player_colors[selected_id]) / 255.0,
                         linewidth=2, markersize=4)
                ax1.set_title(f"Player {selected_id} Movement Trail")

                # Plot heatmap
                heatmap_data = np.zeros(tracker.OUTPUT_SIZE[::-1])
                for (x, y) in player_positions[selected_id]:
                    if 0 <= x < tracker.OUTPUT_SIZE[0] and 0 <= y < tracker.OUTPUT_SIZE[1]:
                        heatmap_data[y, x] += 1

                heatmap_data = gaussian_filter(heatmap_data, sigma=10)
                ax2.imshow(cv2.cvtColor(pitch_img, cv2.COLOR_BGR2RGB))
                heatmap = ax2.imshow(heatmap_data, alpha=0.6, cmap='hot')
                plt.colorbar(heatmap, ax=ax2)
                ax2.set_title(f"Player {selected_id} Heatmap")

                plt.tight_layout()
                plt.show()
            else:
                print("Invalid player ID")
        except ValueError:
            print("Please enter a valid number")


def format_tracking_data(player_positions, player_colors):
    """Format tracking data for export"""
    return {
        'positions': dict(player_positions),
        'colors': {str(k): [int(c) for c in v] for k, v in player_colors.items()}
    }


def main():
    # Define paths to YOLO files
    yolo_weights = r"C:\Users\ayema\yolo project\yolov4.weights"
    yolo_cfg = r"C:\Users\ayema\yolo project\yolov4.cfg"
    # Check YOLO files
    if not os.path.isfile(yolo_weights) or not os.path.isfile(yolo_cfg):
        raise FileNotFoundError("YOLO files not found")

    # Load YOLO
    print("Loading YOLO model...")
    net = cv2.dnn.readNet(yolo_weights, yolo_cfg)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

    # Initialize video capture
    video_path = r"C:\Users\ayema\yolo project\D35bd9041_1 (25).mp4"
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError("Error opening video file")

    # Initialize tracker
    tracker = PitchTracker()

    # Read first frame for initialization
    ret, first_frame = cap.read()
    if not ret:
        raise ValueError("Could not read first frame")

    # Initialize tracker with first frame
    if not tracker.initialize_reference(first_frame):
        print("Initialization cancelled")
        return

    # Initialize tracking variables
    player_positions = defaultdict(list)
    player_colors = {}
    player_ids = [i for i in range(5)]  # Assign 5 stable player IDs
    frame_count = 0

    # Create window for camera view
    cv2.namedWindow('Camera View')

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Update transformation matrix
        transform_success = tracker.update_transform(frame)
        if not transform_success:
            print(f"Failed to update transform for frame {frame_count}")
            continue

        height, width = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        # Process detections
        boxes = []
        confidences = []
        centers = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.5 and class_id == 0:  # Only detect people
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    centers.append((center_x, center_y))

        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.4)

        if len(indices) > 0:
            for i in indices.flatten():
                center = centers[i]
                transformed_point = tracker.transform_point(center)

                if transformed_point is None:
                    continue

                # Check if point is within pitch bounds
                if (0 <= transformed_point[0] <= tracker.OUTPUT_SIZE[0] and
                        0 <= transformed_point[1] <= tracker.OUTPUT_SIZE[1]):

                    # Assign player ID
                    if len(player_ids) > 0:
                        player_id = player_ids.pop(0)
                    else:
                        player_id = assign_player_id(transformed_point, player_positions)

                    # Generate color for new players
                    if player_id not in player_colors:
                        player_colors[player_id] = tuple(np.random.randint(0, 255, 3).tolist())

                    color = player_colors[player_id]

                    # Store current position
                    player_positions[player_id].append(transformed_point)

                    # Draw on camera view
                    cv2.circle(frame, center, 5, color, -1)
                    cv2.putText(frame, f"Player {player_id}",
                                (center[0], center[1] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Show camera view
        cv2.imshow('Camera View', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('z'):  # Break loop if 'z' is pressed
            print("Video stopped. Proceeding to player selection.")
            break
        elif key == ord('q'):  # Exit entirely if 'q' is pressed
            print("Exiting program.")
            cap.release()
            cv2.destroyAllWindows()
            return

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

    # Format and visualize the tracking data after video processing
    tracking_data = format_tracking_data(player_positions, player_colors)
    visualize_player_data(player_positions, player_colors, tracker)


if __name__ == "__main__":
    main()