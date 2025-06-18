import tkinter as tk
from tkinter import *
from tkinter import simpledialog
from ttkthemes import ThemedTk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import pydicom
import nibabel as nib
import numpy as np
import threading
import time
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QWidget, QMessageBox, QTabWidget, QTextEdit, QDialog, QScrollArea, QGridLayout, 
    QLabel, QLineEdit, QSlider, QComboBox, QSpinBox, QGroupBox, QStatusBar, QShortcut
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QIcon, QPalette, QColor, QKeySequence
import pyqtgraph as pg
from pyqtgraph import ImageView
import sys
import random
import string

class DICOMViewerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DICOM Viewer")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set dark theme
        self.setup_dark_theme()
        
        # Initialize variables
        self.init_variables()
        
        # Setup UI
        self.setup_ui()
        
        # Setup shortcuts
        self.setup_shortcuts()
        
        # Show status bar
        self.statusBar().showMessage("Ready")

    def setup_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.black)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.black)
        palette.setColor(QPalette.ToolTipText, Qt.black)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.black)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(palette)

    def init_variables(self):
        self.dicom_file = None
        self.pixel_array = None
        self.image_type = None
        self.playing_cine = False
        self.current_frame = 0
        self.total_frames = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_cine_frame)  # Connect timer to update function
        self.zoom_level = 1.0
        self.brightness = 0
        self.contrast = 1.0
        self.frame_rate = 15  # Default frame rate


    def setup_ui(self):
        # Main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)

        # Create toolbar
        self.create_toolbar()
        
        # Create content area
        self.create_content_area()
        
        

    def create_toolbar(self):
        # Toolbar containing all control buttons
        toolbar_widget = QWidget()
        self.toolbar_layout = QHBoxLayout(toolbar_widget)
        
        # File operations group
        file_group = QGroupBox("File Operations")
        file_layout = QHBoxLayout()
        
        self.load_button = self.create_button("Load File", self.load_file, "folder-open")
        self.save_button = self.create_button("Save", self.save_file, "save")
        self.anonymize_button = self.create_button("Anonymize", self.anonymize, "Anonymize")
        file_layout.addWidget(self.load_button)
        file_layout.addWidget(self.save_button)
        file_layout.addWidget(self.anonymize_button)
        file_group.setLayout(file_layout)
        
        # Image control group
        image_group = QGroupBox("Image Controls")
        image_layout = QHBoxLayout()
        
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(-100, 100)
        self.brightness_slider.valueChanged.connect(self.update_brightness)
        
        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setRange(0, 200)
        self.contrast_slider.setValue(100)
        self.contrast_slider.valueChanged.connect(self.update_contrast)
        
        image_layout.addWidget(QLabel("Brightness:"))
        image_layout.addWidget(self.brightness_slider)
        image_layout.addWidget(QLabel("Contrast:"))
        image_layout.addWidget(self.contrast_slider)
        image_group.setLayout(image_layout)
        
        # Playback control group
        playback_group = QGroupBox("Playback")
        playback_layout = QHBoxLayout()
        
        self.play_button = self.create_button("Play/Pause", self.toggle_cine_play, "play")
        
        # Add frame rate control
        frame_rate_layout = QHBoxLayout()
        frame_rate_layout.addWidget(QLabel("FPS:"))
        self.frame_rate_spinbox = QSpinBox()
        self.frame_rate_spinbox.setRange(1, 60)
        self.frame_rate_spinbox.setValue(self.frame_rate)
        self.frame_rate_spinbox.valueChanged.connect(self.update_frame_rate)
        self.frame_rate_spinbox.setStyleSheet("""
            QSpinBox {
                background-color: white;  
            }
        """)
        
        frame_rate_layout.addWidget(self.frame_rate_spinbox)
        
        # Frame control layout
        frame_control_layout = QVBoxLayout()
        
        # Frame slider with labels
        slider_layout = QHBoxLayout()
        self.frame_slider = QSlider(Qt.Horizontal)
        self.frame_slider.setRange(0, 0)  # Will be updated when file is loaded
        self.frame_slider.valueChanged.connect(self.update_frame)
        
        # Frame control layout
        frame_control_layout = QVBoxLayout()
        
        # Frame slider with labels
        slider_layout = QHBoxLayout()
        self.frame_slider = QSlider(Qt.Horizontal)
        self.frame_slider.setRange(0, 0)
        self.frame_slider.valueChanged.connect(self.update_frame)
        
        self.current_frame_label = QLabel("0")
        self.total_frames_label = QLabel("/ 0")
        
        slider_layout.addWidget(self.current_frame_label)
        slider_layout.addWidget(self.frame_slider, stretch=1)
        slider_layout.addWidget(self.total_frames_label)
        
        frame_control_layout.addLayout(slider_layout)
        
        playback_layout.addWidget(self.play_button)
        playback_layout.addLayout(frame_rate_layout)
        playback_layout.addLayout(frame_control_layout)
        playback_group.setLayout(playback_layout)
        
        # Add all groups to toolbar
        self.toolbar_layout.addWidget(file_group)
        self.toolbar_layout.addWidget(image_group)
        self.toolbar_layout.addWidget(playback_group)
        
        self.main_layout.addWidget(toolbar_widget)

    def create_content_area(self):
        # Content area with image view and metadata
        content_widget = QWidget()
        self.content_layout = QHBoxLayout(content_widget)
        
        # Left side: Image view with tools
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # Image view
        self.image_view = ImageView()
        self.image_view.ui.histogram.hide()
        self.image_view.ui.roiBtn.hide()
        self.image_view.ui.menuBtn.hide()
        left_layout.addWidget(self.image_view)
        
        # Tools under image view
        tools_layout = QHBoxLayout()
        tools_layout.addWidget(self.create_button("Reset View", self.reset_view, "refresh"))
        tools_layout.addWidget(self.create_button("Save Screenshot", self.save_screenshot, "camera"))
        tools_layout.addWidget(self.create_button("Show 3D tiles", self.show_3d_slices, "cube"))
        left_layout.addLayout(tools_layout)
        
        self.content_layout.addWidget(left_widget, stretch=2)
        
        # Right side: Metadata tabs
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Search bar for metadata
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search metadata...")
        self.search_bar.textChanged.connect(self.filter_all_attributes)
        right_layout.addWidget(self.search_bar)
        
        # Style the search bar explicitly
        self.search_bar.setStyleSheet("""
            QLineEdit {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #555555;
                padding: 5px;
                border-radius: 3px;
            }
            QLineEdit:focus {
                border: 1px solid #666666;
                background-color: #333333;
            }
        """)
        
        right_layout.addWidget(self.search_bar)

        
        # Tabs
        self.tabs = QTabWidget()
        self.limited_tab = QTextEdit()
        self.limited_tab.setReadOnly(True)
        self.all_tab = QTextEdit()
        self.all_tab.setReadOnly(True)
        
        self.tabs.addTab(self.limited_tab, "Limited Metadata")
        self.tabs.addTab(self.all_tab, "All Metadata")
        right_layout.addWidget(self.tabs)
        
        self.content_layout.addWidget(right_widget, stretch=1)
        
        self.main_layout.addWidget(content_widget)

    def create_button(self, text, callback, icon_name=None):
        btn = QPushButton(text)
        if icon_name:
            btn.setIcon(QIcon(f"icons/{icon_name}.png"))
        btn.clicked.connect(callback)
        return btn

    def setup_shortcuts(self):
        # Add keyboard shortcuts
        self.shortcuts = {
            'Ctrl+O': self.load_file,
            'Ctrl+S': self.save_file,
            'Space': self.toggle_cine_play,
            'Ctrl+R': self.reset_view,
            'Ctrl+P': self.save_screenshot
        }
        
        for key, callback in self.shortcuts.items():
            QShortcut(QKeySequence(key), self).activated.connect(callback)

    # Add these new methods
    def save_file(self):
        if self.dicom_file:
            filepath = QFileDialog.getSaveFileName(self, "Save DICOM File", "", "DICOM Files (*.dcm)")[0]
            if filepath:
                try:
                    self.dicom_file.save_as(filepath)
                    self.statusBar().showMessage(f"File saved: {filepath}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")

    def update_zoom(self, value):
        self.zoom_level = value / 100.0
        self.refresh_image()

    def update_brightness(self, value):
        self.brightness = value / 100.0
        self.refresh_image()

    def update_contrast(self, value):
        self.contrast = value / 100.0
        self.refresh_image()

    def update_frame(self, value):
        """Update the display when frame slider value changes."""
        if self.pixel_array is not None:
            self.current_frame = value
            self.current_frame_label.setText(str(value))
            self.display_image(value)


    def update_frame_rate(self, value):
        """Update the timer interval when frame rate changes."""
        if self.timer.isActive():
            self.timer.stop()
            self.timer.start(1000 // value)  # Convert fps to milliseconds
    
    def reset_view(self):
        self.zoom_level = 1.0
        self.brightness = 0
        self.contrast = 1.0
        self.brightness_slider.setValue(0)
        self.contrast_slider.setValue(100)
        self.current_frame = 0
        self.frame_slider.setValue(0)
        self.refresh_image()

    def save_screenshot(self):
        if self.image_view.image is not None:
            filepath = QFileDialog.getSaveFileName(self, "Save Screenshot", "", "PNG Files (*.png)")[0]
            if filepath:
                self.image_view.export(filepath)
                self.statusBar().showMessage(f"Screenshot saved: {filepath}")

    def refresh_image(self):
        """Update the displayed image with brightness, contrast, and zoom applied."""
        if self.pixel_array is not None:
            image_data = self.pixel_array[self.current_frame] if self.image_type == "M2D" else self.pixel_array
            
            # Normalize pixel values
            image_data = self.normalize_pixel_data(image_data)

            # Apply brightness and contrast
            adjusted_image = np.clip(
                image_data * self.contrast + self.brightness * 255,
                0, 255
            ).astype(np.uint8)

            # Zoom and update the image view
            height, width = adjusted_image.shape
            scaled_image = adjusted_image[:int(height * self.zoom_level), :int(width * self.zoom_level)]
            self.image_view.setImage(scaled_image.T)



    def load_file(self):
        """Load and process a DICOM file."""
        filepath = QFileDialog.getOpenFileName(self, "Open DICOM file", "", "DICOM files (*.dcm)")[0]
        if not filepath:
            return

        try:
            # Read the DICOM file
            self.dicom_file = pydicom.dcmread(filepath)
            
            # Extract pixel data and determine type
            self.pixel_array = self.dicom_file.pixel_array
            
            # Update frame slider range and labels based on image type
            if hasattr(self.dicom_file, 'NumberOfFrames'):
                self.total_frames = self.dicom_file.NumberOfFrames
                self.frame_slider.setRange(0, self.total_frames - 1)
                self.total_frames_label.setText(f"/ {self.total_frames - 1}")
                self.image_type = "M2D"
            else:
                self.total_frames = 1
                self.frame_slider.setRange(0, 0)
                self.total_frames_label.setText("/ 0")
                self.image_type = "2D"
            
            # Reset current frame
            self.current_frame = 0
            self.frame_slider.setValue(0)
            self.current_frame_label.setText("0")
            
            # Display the first frame/image
            self.display_image(0)
            
            # Populate DICOM information tabs
            self.populate_metadata()
            
            # Update status
            self.statusBar().showMessage(f"Loaded file: {filepath}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file:\n{e}")


    def populate_metadata(self):
        """Populate metadata into the limited and all attributes tabs."""
        if self.dicom_file is None:
            self.limited_tab.setText("No file loaded.")
            self.all_tab.setText("No file loaded.")
            return

        try:
            # Fetch and format limited attributes
            limited_info = "--- Patient Information ---\n"
            limited_info += f"Patient Name: {self.dicom_file.get('PatientName', 'N/A')}\n"
            limited_info += f"Patient ID: {self.dicom_file.get('PatientID', 'N/A')}\n"
            limited_info += f"Patient Sex: {self.dicom_file.get('PatientSex', 'N/A')}\n"
            limited_info += f"Patient Birth Date: {self.dicom_file.get('PatientBirthDate', 'N/A')}\n\n"

            limited_info += "--- Study Information ---\n"
            limited_info += f"Study Date: {self.dicom_file.get('StudyDate', 'N/A')}\n"
            limited_info += f"Study Time: {self.dicom_file.get('StudyTime', 'N/A')}\n"
            limited_info += f"Study Description: {self.dicom_file.get('StudyDescription', 'N/A')}\n\n"

            limited_info += "--- Series Information ---\n"
            limited_info += f"Series Description: {self.dicom_file.get('SeriesDescription', 'N/A')}\n"
            limited_info += f"Modality: {self.dicom_file.get('Modality', 'N/A')}\n"
            limited_info += f"Series Number: {self.dicom_file.get('SeriesNumber', 'N/A')}\n"

            # Display the limited attributes
            self.limited_tab.setText(limited_info)

            # Fetch and format all attributes
            all_info = ""
            for tag in self.dicom_file.keys():
                value = self.dicom_file.get(tag, "N/A")
                all_info += f"{value}\n"

            self.all_tab.setText(all_info)

        except Exception as e:
            self.limited_tab.setText(f"Error populating limited attributes: {e}")
            print(f"Error populating limited attributes: {e}")



    def update_dicom_tags(self):
        """Update the all attributes tab based on the search term."""
        if self.dicom_file is None:
            return

        search_term = self.search_bar.text().lower()
        matching_tags = [
            f"{self.dicom_file.get(tag, 'N/A')}"
            for tag in self.dicom_file.keys()
            if search_term in str(self.dicom_file.get(tag, 'N/A')).lower()
        ]
        self.all_tab.setText("\n".join(matching_tags))


    def update_dicom_tags(self, event):
        """Update the tags based on search input."""
        search_term = self.search_var.get().lower()
        self.all_attributes_text.configure(state="normal")
        self.all_attributes_text.delete(1.0, "end")

        for tag in self.dicom_file.keys():
            tag_name = self.dicom_file.get(tag, "N/A")
            if search_term in str(tag_name).lower():
                self.all_attributes_text.insert("end", f"{tag_name}\n")

        self.all_attributes_text.configure(state="disabled")


    def display_image(self, frame_index=0):
        """Display a 2D image, a frame from M2D data, or a slice from 3D data."""
        if self.pixel_array is None:
            return

        try:
            # Select the appropriate frame/slice
            if self.image_type == "3D":
                # If you're displaying a single slice from a 3D volume (e.g., the first slice)
                frame_index = 0
                image_data = self.pixel_array[frame_index]  # Get the first slice from 3D data
            elif self.image_type == "M2D":
                frame_index = max(0, min(frame_index, self.total_frames - 1))  # Bound frame_index to total frames
                image_data = self.pixel_array[frame_index]  # Get the specified frame from M2D data
            else:  # 2D
                image_data = self.pixel_array  # Use the full 2D image

            # Normalize the pixel data
            normalized_data = self.normalize_pixel_data(image_data)

            # Convert and display the image
            if normalized_data.ndim == 3 and normalized_data.shape[-1] == 3:  # RGB
                self.image_view.setImage(normalized_data.transpose(2, 0, 1))  # PyQtGraph expects (channels, height, width)
            else:  # Grayscale
                self.image_view.setImage(normalized_data.T)  # Transpose for correct orientation

        except Exception as e:
            print(f"Error displaying image: {e}")
            QMessageBox.critical(self, "Error", f"Failed to display image:\n{e}")


    def anonymize(self):
        """Anonymize the opened DICOM file using random values with a user-provided prefix."""
        if not self.dicom_file:
            messagebox.showerror("Error", "No DICOM file loaded.")
            return

        try:
            # Prompt the user for a prefix
            prefix = simpledialog.askstring(
                "Enter Prefix",
                "Enter a prefix to use for anonymization:"
            )
            if not prefix:
                messagebox.showerror("Error", "Anonymization prefix is required.")
                return

            # Helper function to generate random strings with the prefix
            def generate_random_value():
                random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                return f"{prefix}{random_suffix}"

            # List of critical fields to anonymize
            fields_to_anonymize = [
                "PatientName", "PatientID", "PatientBirthDate", "AccessionNumber",
                "StudyInstanceUID", "SeriesInstanceUID", "SOPInstanceUID",
                "PatientAddress", "PatientPhoneNumbers", "OtherPatientIDs",
                "ReferringPhysicianName", "PerformingPhysicianName",
                "PhysiciansOfRecord", "InstitutionName", "InstitutionAddress"
            ]

            # Anonymize each field
            for field in fields_to_anonymize:
                if field in self.dicom_file:
                    setattr(self.dicom_file, field, generate_random_value())

            # Save the anonymized file
            save_file_path = filedialog.asksaveasfilename(
                defaultextension=".dcm",
                filetypes=[("DICOM Files", "*.dcm")],
                title="Save Anonymized File"
            )
            if not save_file_path:
                messagebox.showinfo("Info", "Operation canceled.")
                return

            self.dicom_file.save_as(save_file_path)
            messagebox.showinfo("Success", f"Anonymized file saved to:\n{save_file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to anonymize the file:\n{e}")

    def toggle_cine_play(self):
        """Toggle cine play for multi-frame images."""
        if self.pixel_array is None or self.total_frames <= 1:
            QMessageBox.warning(self, "Warning", "Cine Play is only available for multi-frame files.")
            return

        if self.playing_cine:
            self.timer.stop()
            self.playing_cine = False
            self.play_button.setText("Play")
        else:
            interval = int(1000 / self.frame_rate_spinbox.value())  # Convert fps to milliseconds
            self.timer.start(interval)
            self.playing_cine = True
            self.play_button.setText("Pause")

    def update_frame_rate(self, value):
        """Update the timer interval when frame rate changes."""
        self.frame_rate = value
        if self.playing_cine:
            self.timer.stop()
            interval = int(1000 / value)  # Convert fps to milliseconds
            self.timer.start(interval)
    
    def update_cine_frame(self):
        """Update frame during cine play."""
        if self.pixel_array is not None and self.total_frames > 1:
            next_frame = (self.current_frame + 1) % self.total_frames
            self.frame_slider.setValue(next_frame)
    
    def show_3d_slices(self):
        if len(self.pixel_array.shape) != 3:
            QMessageBox.critical(self, "Error", "Not a 3D file.")
            return

        # Create a new dialog window for 3D slices
        dialog = QDialog(self)
        dialog.setWindowTitle("3D Slices")
        dialog.resize(800, 600)

        # Create a layout for the dialog
        layout = QVBoxLayout(dialog)

        # Scroll area to make slices scrollable
        scroll_area = QScrollArea(dialog)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        # Widget to hold the grid of slices
        scroll_content = QWidget()
        scroll_layout = QGridLayout(scroll_content)
        scroll_area.setWidget(scroll_content)

        # Get the number of slices
        num_slices = self.pixel_array.shape[0]

        # Calculate grid dimensions
        num_columns = 5
        #num_rows = 7

        for i in range(num_slices):
            slice_data = self.pixel_array[i]
            
            # Normalize the slice
            normalized_slice = self.normalize_pixel_data(slice_data)
            
            # Convert numpy array to QImage
            height, width = normalized_slice.shape
            bytes_per_line = width
            q_img = QImage(normalized_slice.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
            
            # Convert QImage to QPixmap
            pixmap = QPixmap.fromImage(q_img)
            
            # Scale pixmap to a reasonable size
            scaled_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # Create a label to display the slice
            label = QLabel()
            label.setPixmap(scaled_pixmap)
            label.setAlignment(Qt.AlignCenter)
            
            # Add label to the grid layout
            scroll_layout.addWidget(label, i // num_columns, i % num_columns)

        dialog.setLayout(layout)
        dialog.exec_()
    
    def filter_all_attributes(self):
        """Filter the attributes in the 'All Attributes' tab based on the search term."""
        if self.dicom_file is None:
            self.all_tab.setText("No file loaded.")
            return

        search_term = self.search_bar.text().lower()  # Get the search term
        filtered_attributes = [
            f"{self.dicom_file.get(tag, 'N/A')}"
            for tag in self.dicom_file.keys()
            if search_term in str(self.dicom_file.get(tag, 'N/A')).lower()  # Match case-insensitive
        ]
        
        # Set the filtered text in the "All Attributes" tab
        self.all_tab.setText("\n".join(filtered_attributes))  # Display the filtered tags
    
    def normalize_pixel_data(self, pixel_array):
        """Normalize pixel data for 2D and 3D arrays."""
        try:
            # Check if the pixel_array is 2D or 3D
            if len(pixel_array.shape) == 2:
                # For 2D array (single slice)
                normalized_array = (pixel_array / np.max(pixel_array) * 255).astype(np.uint8)
            elif len(pixel_array.shape) == 3:
                # For 3D array (volume of slices)
                normalized_array = np.zeros_like(pixel_array, dtype=np.uint8)
                for i in range(pixel_array.shape[0]):  # Loop through each slice
                    normalized_array[i] = (pixel_array[i] / np.max(pixel_array) * 255).astype(np.uint8)
            else:
                raise ValueError("Unsupported pixel array shape")

            return normalized_array

        except Exception as e:
            print(f"Error in normalization: {e}")
            return pixel_array  # Fallback to unprocessed array



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DICOMViewerApp()
    window.show()
    sys.exit(app.exec_())

