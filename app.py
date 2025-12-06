from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    abort,
    send_from_directory,
)
import json
import os

app = Flask(__name__)


# Load content
def load_content():
    with open(os.path.join("data", "content.json"), "r", encoding="utf-8") as f:
        return json.load(f)


content_data = load_content()


@app.route("/")
def index():
    # Detect best language match from browser
    # For simplicity, default to 'en' content-wise, but logic can be added.
    # Accept-Language header parsing could go here.
    return redirect(url_for("home", lang="en"))


@app.route("/<lang>")
def home(lang):
    if lang not in content_data:
        return abort(404)

    return render_template("home.html", lang=lang, content=content_data[lang])


@app.route("/<lang>/projects")
def projects(lang):
    if lang not in content_data:
        return abort(404)

    return render_template("projects.html", lang=lang, content=content_data[lang])


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


# Context processor to make 'lang' available to all templates (optional,
# but we are passing it explicitly for now, which is also fine).
# But we need a helper for the toggle link.


@app.context_processor
def utility_processor():
    def toggle_lang(current_lang):
        return "fr" if current_lang == "en" else "en"

    return dict(toggle_lang=toggle_lang)


if __name__ == "__main__":
    app.run(debug=True)
