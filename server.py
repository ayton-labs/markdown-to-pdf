#!/usr/bin/env python3
"""Markdown to PDF — local web server."""

import json
import os
import subprocess
import tempfile

from flask import Flask, jsonify, request, send_file, send_from_directory, Response

APP_DIR = os.path.dirname(os.path.abspath(__file__))
STATS_FILE = os.path.join(APP_DIR, "stats.json")

app = Flask(__name__, static_folder=APP_DIR, static_url_path="/static")


def _bump_downloads():
    stats = {}
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE) as f:
            stats = json.load(f)
    stats["downloads"] = stats.get("downloads", 0) + 1
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)
    return stats["downloads"]


@app.route("/")
def index():
    return send_file(os.path.join(APP_DIR, "index.html"))


@app.route("/robots.txt")
def robots():
    return Response(
        "User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n",
        mimetype="text/plain",
    )


@app.route("/sitemap.xml")
def sitemap():
    # Update the URL once the domain is live
    url = request.url_root.rstrip("/")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{url}/</loc>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>"""
    return Response(xml, mimetype="application/xml")


@app.route("/pdf", methods=["POST"])
def pdf():
    md_text = request.data.decode("utf-8")
    style = request.args.get("style", "proposal")
    doc_name = request.args.get("name", "document")
    css_path = os.path.join(APP_DIR, f"{style}.css")

    if not os.path.exists(css_path):
        css_path = os.path.join(APP_DIR, "proposal.css")

    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False) as md_file:
        md_file.write(md_text)
        md_path = md_file.name

    html_path = md_path.replace(".md", ".html")
    pdf_path = md_path.replace(".md", ".pdf")

    try:
        # Pandoc: markdown → standalone HTML with embedded CSS
        subprocess.run(
            [
                "pandoc", md_path,
                "-f", "markdown+lists_without_preceding_blankline",
                "-t", "html5",
                "--standalone",
                "--embed-resources",
                f"--css={css_path}",
                "--metadata", "title=",
                "-o", html_path,
            ],
            check=True,
            capture_output=True,
        )

        # Inject doc name into <title> for PDF metadata
        with open(html_path, "r") as f:
            html_content = f.read()
        html_content = html_content.replace("<title></title>", f"<title>{doc_name}</title>")
        with open(html_path, "w") as f:
            f.write(html_content)

        # WeasyPrint: HTML → PDF
        import weasyprint
        weasyprint.HTML(filename=html_path).write_pdf(pdf_path)

        _bump_downloads()

        return send_file(
            pdf_path,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"{doc_name}.pdf",
        )
    finally:
        for f in [md_path, html_path, pdf_path]:
            if os.path.exists(f):
                os.unlink(f)


@app.route("/stats")
def stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE) as f:
            return jsonify(json.load(f))
    return jsonify({"downloads": 0})


if __name__ == "__main__":
    print(f"MD2PDF running at http://localhost:8787")
    app.run(port=8787, debug=False)
