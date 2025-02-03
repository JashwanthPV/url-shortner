from flask import Flask, render_template, request, redirect, url_for, flash
import string
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Dictionary to store short and long URLs
url_mapping = {}

# Function to generate random short codes
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        original_url = request.form.get("url")
        
        if original_url:
            # Generate a unique short code
            short_code = generate_short_code()
            url_mapping[short_code] = original_url
            flash(f"Shortened URL: {request.url_root}{short_code}")
        else:
            flash("Please enter a valid URL.")
    return render_template("index.html")

@app.route("/<short_code>")
def redirect_url(short_code):
    long_url = url_mapping.get(short_code)
    if long_url:
        return redirect(long_url)
    else:
        flash("Invalid URL!")
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
