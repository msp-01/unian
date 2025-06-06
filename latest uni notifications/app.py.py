from flask import Flask, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def index():
    announcements = []

    def add_announcement(title, link, source):
        # Filter out unwanted titles
        if title.lower() in ["duyuru", "devamı"]:
            return
        announcements.append({
            "title": title.strip(),
            "link": link,
            "source": source
        })

    # MATSE Faculty
    try:
        res_matse = requests.get("https://matse.eskisehir.edu.tr/tr/Duyuru")
        soup = BeautifulSoup(res_matse.text, "html.parser")
        items = soup.select(".gdlr-core-blog-full-head-right h3 a")
        for tag in items:
            if tag.has_attr("href"):
                add_announcement(
                    tag.text,
                    "https://matse.eskisehir.edu.tr" + tag["href"],
                    "MATSE"
                )
    except Exception as e:
        print(f"MATSE error: {e}")

    # MF Faculty
    try:
        res_mf = requests.get("https://mf.eskisehir.edu.tr/tr/Duyuru")
        soup = BeautifulSoup(res_mf.text, "html.parser")
        items = soup.select("a[href^='/tr/Duyuru/Detay']")
        added_titles = set()
        for tag in items:
            title = tag.text.strip()
            if tag.has_attr("href") and title and title not in added_titles:
                add_announcement(
                    title,
                    "https://mf.eskisehir.edu.tr" + tag["href"],
                    "MF"
                )
                added_titles.add(title)
    except Exception as e:
        print(f"MF error: {e}")

    # Main University
    try:
        res_main = requests.get("https://www.eskisehir.edu.tr/tr/Duyuru")
        soup = BeautifulSoup(res_main.text, "html.parser")
        items = soup.select("a[href^='/tr/Duyuru/Detay']")
        added_titles = set()
        for tag in items:
            title = tag.text.strip()
            if tag.has_attr("href") and title and title not in added_titles:
                add_announcement(
                    title,
                    "https://www.eskisehir.edu.tr" + tag["href"],
                    "ESTÜ"
                )
                added_titles.add(title)
    except Exception as e:
        print(f"Main site error: {e}")

    return render_template_string("""
        <html>
        <head>
            <title>Duyurular</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; }
                ul { list-style: none; padding: 0; }
                li { margin-bottom: 10px; }
                a { text-decoration: none; color: #0645ad; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <h1>Tüm Duyurular</h1>
            <ul>
                {% for a in announcements %}
                    <li><strong>[{{ a.source }}]</strong> <a href="{{ a.link }}" target="_blank">{{ a.title }}</a></li>
                {% endfor %}
            </ul>
        </body>
        </html>
    """, announcements=announcements)

if __name__ == "__main__":
    app.run(debug=True)
