# Gestural Command Bridge (GCB) - AI-Hardware Interface

## Project Overview
This project establishes a real-time bridge between computer vision-based AI and physical hardware. It uses a Python-based AI module to detect human gestures and translates them into precise control commands for an Arduino-driven system.

## The Engineering Challenge: Latency & Stability
The primary challenge was managing the data synchronization between the high-level Python environment and the low-level Arduino firmware. I implemented **Temporal Filtering** to eliminate false positives in gesture detection and optimized the **Serial Communication Protocol** to ensure sub-millisecond latency.

## Tech Stack
* **Software:** Python (OpenCV, MediaPipe, PySerial).
* **Hardware:** Arduino (C/C++), Sensors, and Actuators.
* **Architecture:** Distributed processing (Local PC for AI, MCU for physical execution).

## Key Features
* High-speed landmark detection.
* Robust error handling for Serial communication.
* Real-time gesture-to-action mapping.
