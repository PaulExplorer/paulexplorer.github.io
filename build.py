import os
import json
import shutil
from jinja2 import Environment, FileSystemLoader

# Configuration
DATA_FILE = os.path.join("data", "content.json")
TEMPLATES_DIR = "templates"
STATIC_DIR = "static"
BUILD_DIR = "build"


def load_content():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def toggle_lang(current_lang):
    return "fr" if current_lang == "en" else "en"


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def build():
    # Load content
    content_data = load_content()

    # Setup Jinja2 env
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

    # Clean and create build directory
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
    ensure_dir(BUILD_DIR)

    # Copy static files
    # We want build/static/...
    shutil.copytree(STATIC_DIR, os.path.join(BUILD_DIR, "static"))

    # Copy favicon to root if exists
    favicon_path = os.path.join(STATIC_DIR, "favicon.ico")
    if os.path.exists(favicon_path):
        shutil.copy(favicon_path, os.path.join(BUILD_DIR, "favicon.ico"))

    # Helper for url_for
    # Since we structure as build/<lang>/<page>.html
    # Links will be relative.
    # From <lang>/page.html to static: ../static/...
    # From <lang>/page.html to <other_lang>/page.html: ../<other_lang>/page.html

    endpoint_map = {"home": "index.html", "projects": "projects.html"}

    def url_for(endpoint, **values):
        if endpoint == "static":
            filename = values.get("filename")
            return f"../static/{filename}"

        lang = values.get("lang")
        if not lang:
            # Fallback or error, though templates seem to always pass lang
            return "#"

        page = endpoint_map.get(endpoint)
        if page:
            return f"../{lang}/{page}"
        return "#"

    # Add globals
    env.globals["url_for"] = url_for
    env.globals["toggle_lang"] = toggle_lang

    # Mock request object class
    class MockRequest:
        def __init__(self, endpoint):
            self.endpoint = endpoint

    # Generate pages for each language
    for lang in ["en", "fr"]:
        lang_dir = os.path.join(BUILD_DIR, lang)
        ensure_dir(lang_dir)

        data = content_data.get(lang)
        if not data:
            print(f"Warning: No data for language {lang}")
            continue

        # Render Home
        # Endpoint 'home'
        # content=data because templates usage is content.timeline etc.
        # In app.py: render_template('home.html', lang=lang, content=content_data[lang])

        template_home = env.get_template("home.html")
        output_home = template_home.render(
            lang=lang, content=data, request=MockRequest("home")
        )
        with open(os.path.join(lang_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(output_home)

        # Render Projects
        # Endpoint 'projects'
        # Need to check if projects.html exists, user mentioned it might be created or referenced
        # "et peut être une page pour afficher les projects ?" -> "projects.html" was mentioned in app.py
        if os.path.exists(os.path.join(TEMPLATES_DIR, "projects.html")):
            template_projects = env.get_template("projects.html")
            output_projects = template_projects.render(
                lang=lang, content=data, request=MockRequest("projects")
            )
            with open(
                os.path.join(lang_dir, "projects.html"), "w", encoding="utf-8"
            ) as f:
                f.write(output_projects)
        else:
            print("Notice: projects.html template not found, skipping.")

    # Create root index.html with redirect
    # Simple HTML redirect to English
    root_index = """<!DOCTYPE html>
            <html>
            <head>
                <meta http-equiv="refresh" content="0; url=en/index.html" />
            </head>
            <body>
                <p>Redirecting to <a href="en/index.html">en/index.html</a></p>
            </body>
            </html>
        """
    with open(os.path.join(BUILD_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(root_index)

    print("Build completed successfully in 'build/' directory.")


if __name__ == "__main__":
    build()
