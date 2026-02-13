from flask import Flask, request, render_template
import os
from src.predict import predict_multiple

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "..", "frontend", "templates"),
    static_folder=os.path.join(BASE_DIR, "..", "frontend", "static")
)

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/results', methods=['POST'])
def results():
    try:
        # Get reviews from textarea
        raw_text = request.form.get("review", "")
        reviews = [r.strip() for r in raw_text.splitlines() if r.strip()]

        if not reviews:
            return render_template("index.html", error="Please enter at least one review.")

        # Call predict_multiple() which returns dict with keys: results, summary, suggestion
        prediction_data = predict_multiple(reviews)

        # Extract components
        results = prediction_data["results"]       # list of dicts
        summary = prediction_data["summary"]       # dict with counts
        suggestion = prediction_data["suggestion"] # string with suggestions

        # Render results page
        return render_template(
            "results.html",
            results=results,
            summary=summary,
            suggestion=suggestion
        )

    except Exception as e:
        print("🔥 Error:", e)
        return render_template("index.html", error=str(e))


if __name__ == "__main__":
    app.run(debug=True)
