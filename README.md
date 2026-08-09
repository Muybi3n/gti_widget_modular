# GTI Widget Modular

**NOTE: This project is for Proof of Concept (POC) purposes only. It is not intended for production use.**

## Description

The `gti_widget_modular` project provides a modular, web-based UI demonstration for integrating Google Threat Intelligence (GTI). Built with HTML, Tailwind CSS, and Vanilla JavaScript, it allows users to dynamically analyze Indicators of Compromise (IOCs), vulnerabilities, and other threat intelligence data by interacting with the GTI API. 

Users can supply their GTI API key through the UI to visualize threat detections in a sliding widget. No API keys or sensitive credentials are hardcoded into this repository.

## Files
- `build_project.py`: A Python script that regenerates the project structure.
- `index.html`: The main web interface for the demo.
- `js/`, `css/`: Modular JavaScript and CSS assets for styling and GTI logic.

## Usage
Simply open `index.html` in a modern web browser to view the interface. Input your GTI API key in the configuration section to pull live data.
