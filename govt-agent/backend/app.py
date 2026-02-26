from flask import Flask, render_template
import os
from urllib.parse import urlparse

app = Flask(__name__)

# --- Channel configuration (can be overridden by env vars) ---
CHANNEL_NAME = os.getenv("CHANNEL_NAME", "My Channel")
CHANNEL_URL = os.getenv("CHANNEL_URL", "https://www.youtube.com/shorts/0yGxtEFgO5g")

def extract_youtube_id(url: str) -> str:
    """
    Extracts the YouTube video ID from standard, share, or Shorts URLs.
    Examples:
      - https://www.youtube.com/watch?v=0yGxtEFgO5g
      - https://youtu.be/0yGxtEFgO5g
      - https://www.youtube.com/shorts/0yGxtEFgO5g
    """
    try:
        parsed = urlparse(url)
        path = parsed.path.strip("/")
        if "watch" in path and "v=" in parsed.query:
            # e.g., watch?v=ID
            from urllib.parse import parse_qs
            return parse_qs(parsed.query).get("v", [""])[0]
        if path.startswith("shorts/"):
            return path.split("shorts/")[-1].split("/")[0]
        # youtu.be/ID
        if parsed.netloc.endswith("youtu.be"):
            return path.split("/")[0]
        # fallback
        return ""
    except Exception:
        return ""

VIDEO_ID = extract_youtube_id(CHANNEL_URL)

@app.route("/")
def index():
    return render_template(
        "index.html",
        channel_name=CHANNEL_NAME,
        channel_url=CHANNEL_URL,
        video_id=VIDEO_ID
    )

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

# Local dev
if __name__ == "__main__":
    # Render uses Gunicorn; this block is for local runs only
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
