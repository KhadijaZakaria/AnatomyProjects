
# Anatomy Projects

Welcome to the **Anatomy Projects** repository, a collection of diverse projects developed by **Bassel Shaheen**, **Ahmed AbdelMo3ty**, **Aya Emad**, **Khadija Zakaria**. This repository showcases my work on **AI-based models**, **game development**, **medical image processing**, **Dealing with Dicom files** and **innovative research** in anatomy-related fields. Below you'll find the different projects included in this repository.

## 📚 Projects

### 🎮 [OrganPuzzleGame](OrganPuzzleGame)
A **Unity-based puzzle game** designed to help players learn about the human **larynx** and other organs through interactive gameplay.

### 🤖 [YoloTrack](YoloTrack)
An **AI-powered player tracking model** that assigns unique IDs to players, generates heatmaps, and converts camera views into a **2D planar view**.

### 🧠 [OrgoVision]https://github.com/BasselShaheen06/OrgoVision)
An **organ classification model** built using **LeNet architecture** to identify various human organs from images.

### 🧬 [NOPIS](NOPIS)
A **research proposal** for a new **imaging modality** that aims to improve anatomical visualization in medical imaging.

### 🧪 [MPRViewer](MPRViewer)
A **MRI scan viewer** for **NIFTI files**, featuring various diagnostic tools and a simple, clean user interface.

### 🖼️ [MediPixel](MediPixel)
An **image processing application** that allows denoising, adding artificial noise, and adjusting various parameters like resolution and field of view.

### 🖥️ [DicomShow](DicomShow)
A **DICOM file viewer** built using **PyQt5** and **VTK**, designed to provide an interactive and straightforward interface for viewing **DICOM images**. This viewer allows users to adjust window leveling, zoom, and scroll through image slices, making it a useful tool for medical professionals.

## 🛠️ Technologies Used

This repository combines a range of tools and technologies:

- **Machine Learning**: TensorFlow, YOLO, LeNet
- **Game Development**: Unity3D, C#
- **Medical Imaging**: PyQt5, VTK, NIFTI, OpenCV
- **Libraries**: NumPy, Matplotlib, Scikit-learn, PIL

## 🚀 Installation

To get started with any of these projects, clone the repository and follow the installation instructions specific to each project:

1. Clone the repository:

   ```bash
   git clone https://github.com/BasselShaheen06/Anatomy_Projects.git
   cd Anatomy_Projects
   ```

2. For each project, refer to its **README** for detailed installation and setup instructions.

---

## 📂 Individual Project Details

### 🎮 [OrganPuzzleGame](OrganPuzzleGame)

A game made using **Unity3D** for educational purposes, where users assemble puzzle pieces of the **larynx** (and other organs) to learn about human anatomy.

#### Features:
- Interactive learning tool
- Organ-based puzzles with a focus on the **larynx**

#### Getting Started:
1. Download Unity and open the project folder.
2. Play the game and solve the organ puzzle!

### 🤖 [YoloTrack](YoloTrack)

This AI model tracks players in a video, generates heatmaps, and assigns each player a unique ID. The system also converts the camera view into a **2D planar view**.

#### Features:
- Real-time player tracking
- Heatmap visualization
- Camera view transformation

#### Getting Started:
1. Navigate to `YoloTrack` directory:
   ```bash
   cd YoloTrack
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the model on a video:
   ```bash
   python yolo.py --video YoloTrack\video\screen_record.mp4
   ```

### 🧠 [OrgoVision](OrgoVision)

A **LeNet-based AI model** for organ classification from images. This project demonstrates how machine learning can assist in **medical diagnosis**.

#### Features:
- Organ classification with high accuracy
- Built using **LeNet architecture**

#### Getting Started:
1. Navigate to `OrgoVision` directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Train or test the model:
   look on how to run the notebook cells in the project repo

### 🧬 [NOPIS](NOPIS)

A **research proposal** for a novel imaging modality, aiming to revolutionize the field of **medical imaging** and visualization techniques.

#### Getting Started:
This project is in the form of a proposal document that outlines a new imaging technique.

### 🧪 [MPRViewer](MPRViewer)

A viewer tool to interact with **MRI NIFTI files**, providing essential diagnostic tools for medical professionals.

#### Features:
- Window leveling for MRI images
- Interactive scroll through 3D data
- Clean, simple UI

#### Getting Started:
1. Navigate to `MPRViewer` directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Open and view your MRI scan:
   ```bash
   python MPR_Viewer.py  --make sure to load a nifti file
   ```

### 🖼️ [MediPixel](MediPixel)

A comprehensive **image processing tool** for denoising, adding noise, and adjusting the field of view and resolution of images.

#### Features:
- Noise addition and denoising
- Field of view and resolution controls

#### Getting Started:
1. Navigate to `MediPixel` directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the image processing tool:
   ```bash
   python Medical_Image_Viewer.py 
   ```

---

### 🖥️ [DICOMShow](Dicomshow)

A **DICOM file viewer** built using **PyQt5** and **VTK**, designed to provide an interactive and straightforward interface for viewing **DICOM images**. This viewer allows users to adjust window leveling, zoom, and scroll through image slices, making it a useful tool for medical professionals.

#### Features:
- Window leveling for DICOM images
- Interactive scroll through image slices
- Simple, intuitive UI for viewing medical images

#### Getting Started:
1. Navigate to `DicomShow` directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Open and view your DICOM image:
   ```bash
   python DICOM_Viewer.py  --make sure to load a dicom file
   ```
---

## ✍️ Contributing

Feel free to contribute to any of the projects! Here's how you can help:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes and commit (`git commit -am 'Add feature'`).
4. Push to your fork (`git push origin feature-name`).
5. Create a **pull request**.

## 📄 License

This repository is open-source and available under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---

Thank you for visiting the **Anatomy Projects** repository! Feel free to explore the individual projects, learn, and contribute. 🚀
