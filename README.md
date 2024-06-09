# Virtual Keyboard with Eye Detection

Welcome to the Virtual Keyboard with Eye Detection project! This repository contains the implementation of a virtual keyboard system that utilizes eye detection for hands-free typing. The system leverages computer vision techniques to track eye blinks and hand gestures to simulate keyboard interactions, making it an innovative assistive technology.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This project is designed to help individuals with limited mobility interact with a computer through eye blinks and hand gestures. By using a camera to detect eye blinks and track hand movements, the system allows users to select keys on a virtual keyboard displayed on the screen.

The main components of this project are:
- Eye detection to identify blinks.
- Hand tracking to detect and track hand movements.
- Virtual keyboard interface for typing.

## Features

- **Eye Blink Detection**: Detects eye blinks using a webcam, enabling users to make selections on the virtual keyboard.
- **Hand Tracking**: Tracks hand movements to control the cursor and select keys.
- **Audio Feedback**: Provides audio feedback for key presses to enhance user experience.
- **Customizable Keyboard Layout**: Allows customization of the virtual keyboard layout to suit different user needs.

## Installation

To run this project, you need to have Python installed on your system. Follow the steps below to set up the environment and install the necessary dependencies.

1. **Clone the repository**:
    ```bash
    git clone https://github.com/AnuruddhSin/Virtual-keyboard-eye-detection.git
    cd Virtual-keyboard-eye-detection
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To use the virtual keyboard with eye detection, follow these steps:

1. **Run the main script**:
    ```bash
    python vir_keyboard_eye_det.py
    ```

2. **Position the camera**: Ensure that your face and hands are clearly visible to the camera.

3. **Interacting with the Keyboard**:
    - Use eye blinks to simulate key presses.
    - Move your hand to control the cursor on the screen.

## File Structure

The project directory contains the following files and folders:

- `.idea/`: Directory for IDE-specific settings (e.g., PyCharm).
- `__pycache__/`: Directory containing cached bytecode files.
- `click.mp3`: Audio file for click sound.
- `detecting_eye_blink_module.py`: Module for detecting eye blinks.
- `sclick.mp3`: Audio file for special click sound.
- `tracking_hand_module.py`: Module for tracking hand movements.
- `vir_keyboard_eye_det.py`: Main script to run the virtual keyboard application.

## Dependencies

The project relies on the following libraries and tools:

- OpenCV: For computer vision tasks.
- Mediapipe: For hand and face tracking.
- Numpy: For numerical operations.
- Pygame: For handling audio feedback.

Ensure that these dependencies are listed in the `requirements.txt` file, which can be installed using `pip`.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

Please ensure your code adheres to the existing coding conventions and includes appropriate tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

---

Feel free to use this README as a starting point and modify it according to your project's specific needs. If you have any questions or need further assistance, don't hesitate to reach out!
