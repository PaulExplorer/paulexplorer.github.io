# MyPortfolio

Welcome to the **MyPortfolio** repository, a personal website designed to showcase my journey as a developer, my skills, and my projects. This project is built with **Flask** and uses JSON files to manage dynamic and multilingual content.

## About

This portfolio traces my evolution as a developer, from my beginnings with Python to my current projects in Rust and WebAssembly. It is designed to be simple, elegant, and easy to update.

## Features

- **Multilingual**: Native support for multiple languages (defaulting to English and French), managed via Flask routes (`/en`, `/fr`).
- **Dynamic Content**: All text content (journey, projects, "about") is stored in `data/content.json`, making updates easy without touching HTML code.
- **Flask Framework**: Lightweight and efficient backend using Flask and Jinja2.
- **Responsive Design**: Adapted for viewing on mobile and desktop.

## Installation

To run this project locally:

```bash
git clone https://github.com/PaulExplorer/paulexplorer.github.io.git
cd paulexplorer.github.io

# Create and activate virtual environment
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate

pip install -r requirements.txt
```

## Usage

Once dependencies are installed, you can start the development server:

```bash
python app.py
```

The site will be accessible at: `http://127.0.0.1:5000/`

The root route `/` will automatically redirect to the English version `/en` (or according to the logic defined in `app.py`).

## Project Structure

- `app.py`: Entry point of the Flask application. Handles routes and content loading logic.
- `data/content.json`: Contains all site text (timeline, projects, etc.) for each language.
- `templates/`: HTML files (Jinja2) for page structure (`home.html`, `projects.html`).
- `static/`: Static files (CSS, images, favicon).
- `build.py`: Utility script (if applicable, for static generation or other build tasks).

## Customization

To modify the portfolio content, simply edit the `data/content.json` file. No server restart is needed if debug mode is on, just a page refresh.

## Author

**PaulExplorer** (Passionate Developer)
