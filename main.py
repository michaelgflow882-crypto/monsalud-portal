from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)

# ---- TEST MODE toggle (no Omada calls yet) ----
TEST_MODE = True


def greeting_now():
    h = datetime.now().hour
    if h < 11: return "Good morning"
    if h < 13: return "Good noon"
    if h < 17: return "Good afternoon"
    if h < 21: return "Good evening"
    return "Good night"


def theme_now():
    hour = datetime.now().hour
    mode = "day" if 6 <= hour < 18 else "night"
    # monthly theme id (extend later: halloween/december/etc.)
    theme = "default"
    return theme, mode


@app.route("/")
def index():
    theme, mode = theme_now()
    return render_template(
        "portal.html",
        greet=greeting_now(),
        date_now=datetime.now().strftime("%B %d, %Y"),
        theme=theme,
        mode=mode,
        fb_page_url="https://m.me/61582345860795",
        remaining_seconds=3600  # demo 1hr countdown
    )


# Fake voucher redeem for testing
@app.route("/redeem", methods=["POST"])
def redeem():
    code = request.form.get("voucher", "").strip().upper()
    # Accept only test codes while TEST_MODE is True
    valid_test_codes = {"TEST123", "FREE30"}
    if TEST_MODE:
        if code in valid_test_codes:
            return """
            <script>
            window.location.href='https://m.me/61582345860795';
            </script>
            """
        return redirect(url_for("index") + "?err=1")
    # (Live mode will go here later)
    return redirect(url_for("index") + "?err=1")


# Healthcheck (for uptime monitors later)
@app.route("/health")
def health():
    return "ok", 200

# Branch location configuration
BRANCH_LOCATIONS = {
    "default": {"name": "MG Wellness Main", "address": "Main Branch"},
    "branch_a": {"name": "MG Wellness - Branch A", "address": "Branch A Location"},
    "branch_b": {"name": "MG Wellness - Branch B", "address": "Branch B Location"},
    "branch_c": {"name": "MG Wellness - Branch C", "address": "Branch C Location"},
}

@app.route("/speed")
def speed_test():
    branch_id = request.args.get("branch", "default")
    branch = BRANCH_LOCATIONS.get(branch_id, BRANCH_LOCATIONS["default"])
    theme, mode = theme_now()
    return render_template(
        "speed.html",
        branch_name=branch["name"],
        branch_address=branch["address"],
        branch_id=branch_id,
        theme=theme,
        mode=mode
    )


if __name__ == "__main__":
    # Replit uses its own host/port; this works locally too.
    app.run(host="0.0.0.0", port=5000, debug=True)
