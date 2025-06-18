# OrgoVision 🔬

OrgoVision is a powerful desktop application designed to identify and classify organ images using advanced machine learning techniques. Built with Python and TensorFlow, it provides medical professionals and researchers with a user-friendly interface for quick and accurate organ recognition.

## UI Overview

The OrgoVision UI is designed to be simple and intuitive, featuring easy-to-navigate buttons and real-time feedback. Users can quickly upload images, view predictions, and access detailed confidence metrics in a clean interface.

Below is a sample screenshot of the UI:
![Ui](https://github.com/user-attachments/assets/7ddcc765-d2a6-4a5d-a60b-a0ecfd77a8a8)



## Features

- **Real-time Image Analysis**: Upload and analyze organ images instantly
- **High-Precision Recognition**: Powered by a fine-tuned LeNet architecture
- **Confidence Scoring**: Get detailed confidence metrics for each prediction
- **User-Friendly Interface**: Clean, intuitive design for seamless operation
- **Multi-format Support**: Compatible with common image formats (JPG, JPEG, PNG)

## Getting Started

### Prerequisites

Make sure you have Python 3.8+ installed on your system. You'll need the following packages:

```bash
pip install -r requirements.txt
```

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/orgovision.git
cd orgovision
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Saving Model Weights Before Running the App

Before launching OrgoVision, ensure you have saved the model weights properly. Follow these steps to save the weights:

1. Open the `Classify.ipynb` notebook.
2. Run the cells that train or load the model.
3. run the following cell to save the weights:

   ```python
   lenet_model.save('OrgoVision/my_model.keras')
   ```

   Ensure the `models/` directory exists or create it using:

   ```bash
   mkdir models
   ```

4. Verify that the `orgovision_weights.h5` file is present in the `models/` directory.

Once the weights are saved, you can proceed to run the app.



1. Launch OrgoVision by running the imports cell and then run the last cell   # responsible for the UI
2. Click "Upload Image" to select an organ image
3. Wait for the analysis to complete
4. View the prediction results and confidence score

The application will display:

- Predicted organ type
- Confidence percentage
- Original image with automatic scaling

### Prediction Results

Below is a screenshot showing the prediction results:
![Prediction4](https://github.com/user-attachments/assets/e375dfe4-9837-48cc-acd8-e51da92da5b1)
![Prediction3](https://github.com/user-attachments/assets/84831f94-f95e-4aaa-8c5e-1c7fc3b3f3fa)

### Confusion Matrix

The confusion matrix provides a visual representation of the model's performance:
![confusion_matrix](https://github.com/user-attachments/assets/e40f7b55-af4c-48c6-a5fa-b3e3212dba3c)

### Application in Action (Video)

https://github.com/user-attachments/assets/73cb0d59-4245-4311-8e0b-b2dcc15d1909

## Development Setup

If you're looking to contribute or modify OrgoVision, here's what you'll need:

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt
```


## Model Information

OrgoVision uses a modified LeNet architecture trained on a comprehensive dataset of organ images. The model achieves:

- 95% accuracy on validation data
- Fast inference time (<2s per image)
- Support for 10+ organ classifications

## Project Structure

```
OrgoVision/
├── Classify.ipynb       # Model notebook
├── requirements.txt    # Dependencies
├── models_/            # Trained model files
├── finalTest_/           # Some dataset to test the model
├── LICENSE              # MIT License
├── requirements.txt     # Requirements.txt file
├── README.md            # README file
```

## Common Issues & Solutions

**Image Won't Load?**

- Check if the image format is supported (JPG, JPEG, PNG)
- Ensure the file isn't corrupted
- Verify you have read permissions for the file

**Slow Performance?**

- Close other resource-intensive applications
- Check if your GPU drivers are up to date
- Ensure you have sufficient RAM available

## Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Medical imaging dataset provided by [AOMIC, Seniors at NewGiza university]
- Special thanks to the TensorFlow and OpenCV communities
- Unforgettable help from our colleague ![MuhamedSalah](https://github.com/MuhamedSalah10)
- UI design inspired by modern medical software interfaces

## Support

Having issues? We're here to help:

- Open an issue on GitHub
- Email us at [support@orgovision.com](mailto\:bassel.abdelmonem@eng-st.cu.edu.eg)
- Check out our FAQ section

*Note: This README will be updated as the project evolves. Last updated: January 2025*

---
