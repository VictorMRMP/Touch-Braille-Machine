# Braille Touch Display

This repository contains the code and documentation for the "Braille Touch Display" project, developed as part of my **Trabalho de Conclusão de Curso (TCC)**. The project aims to create an input device that allows text entry through tactile cells using TTP223B touch sensors.

## Objective

The Braille Touch Display project is designed to provide a way to write text using Braille cells, which are sensitive to touch. The system translates Braille input into characters or commands, allowing the user to compose and edit text, with audio feedback for each input. This project also includes a Bluetooth interface, enabling the system to function as a wireless keyboard.

## Features

- **Braille Input**: The device uses 6 TTP223B touch sensors to represent a Braille character input system.
- **Bluetooth Integration**: The system can send Braille input via Bluetooth as a wireless keyboard to a connected device.
- **Audio Feedback**: Each character and action (e.g., space, punctuation, backspace) is accompanied by an audio cue to help users verify input.
- **Text Editing**: Users can add, delete, and navigate through text via touch interactions.

## Hardware Used

- **TTP223B Touch Sensors**: These sensors are used for detecting touch, representing the Braille cells.
- **ESP32**: A microcontroller with Bluetooth capabilities used for sending the input wirelessly to the computer or other devices.

## Software

- **Languages**: Arduino C++ for the ESP32 microcontroller.
- **Libraries**:
  - `BleKeyboard` for Bluetooth keyboard functionality.
  - `gTTS` (Google Text-to-Speech) for generating audio feedback.
  - `pygame` for playing audio on the PC.

## Components

- **Touch Cells**: 6 TTP223B touch sensors for Braille input.
- **Auxiliary Buttons**: Used for commands like "Backspace", "Up Arrow", and "Down Arrow".
- **Audio Feedback**: Custom MP3 and WAV files are used for audio feedback based on the input.

## Code Overview

The project consists of two main parts:
1. **Braille Machine ESP32**: This part handles the conversion of touch input into Braille characters and sends the output to the computer via Bluetooth. It also manages auxiliary buttons for additional commands (e.g., backspace, cursor movement).
2. **Keyboard Text Reader**: This part manages the graphical interface for displaying text on the computer, reading input from the serial port, and providing audio feedback.


## Future Improvements
1. **Additional Commands**: Implement more complex commands like text formatting.
2. **Improved User Interface**: Enhance the graphical interface for better user experience.
3. **Mobile App Integration**: Extend functionality to work with mobile devices via Bluetooth.

## Acknowledgments
**TTP223B Touch Sensors**: For touch-based input.
**ESP32**: For Bluetooth communication.
**gTTS**: For generating text-to-speech audio.
**Pygame**: For playing audio feedback on the computer.
