import os
import joblib
from src.preprocess import clean_text

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "model", "linear_svc_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "model", "Tfidfvectorizer.pkl")

model = None
vectorizer = None

def load_model():
    """Load model and vectorizer if not already loaded."""
    global model, vectorizer
    if model is None or vectorizer is None:
        if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
            raise FileNotFoundError("Model or vectorizer file not found. Check paths!")
        print("🔹 Loading model...")
        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)
        print("✅ Model & Vectorizer loaded")

def predict_sentiment(text):
    """
    Predict sentiment for a single review.
    Returns:
        sentiment (str), score (float)
    """
    cleaned = clean_text(text)
    if not cleaned.strip():
        return "Neutral", 0.0
    vec = vectorizer.transform([cleaned])
    score = float(model.decision_function(vec)[0])
    
    if score > 0.3:
        sentiment = "Positive"
    elif score < -0.3:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    return sentiment, score

def predict_multiple(reviews):
    """
    Predict sentiment for multiple reviews.
    Returns:
        dict with keys:
        - results: list of dicts {"text", "sentiment", "score"}
        - summary: counts of Positive/Negative/Neutral
        - suggestion: management suggestions string
    """
    load_model()
    results = []
    summary = {"Positive": 0, "Negative": 0, "Neutral": 0}

    for text in reviews:
        sentiment, score = predict_sentiment(text)
        results.append({"text": text, "sentiment": sentiment, "score": score})
        summary[sentiment] += 1

    suggestion = generate_suggestions(results)

    return {
        "results": results,
        "summary": summary,
        "suggestion": suggestion
    }

def generate_suggestions(results):
    """
    Analyze negative and neutral reviews to generate management suggestions.
    """
    suggestions = []
    # Only focus on Negative or Neutral reviews
    negative_reviews = [r["text"].lower() for r in results if r["sentiment"] in ["Negative", "Neutral"]]

    # Map keywords to actionable suggestions
    keyword_suggestions = {
        "slow": "Improve service speed.",
        "wait": "Reduce waiting time for orders.",
        "rude": "Train staff for friendliness.",
        "cold": "Ensure food is served hot.",
        "bland": "Improve seasoning and flavor of dishes.",
        "overcooked": "Cook dishes properly.",
        "small": "Increase portion sizes.",
        "greasy": "Reduce oil in food.",
        "spicy": "Adjust spice levels to customer preference.",
        "noisy": "Improve restaurant ambiance."
    }

    for keyword, suggestion in keyword_suggestions.items():
        if any(keyword in review for review in negative_reviews):
            suggestions.append(suggestion)

    # Fallback if negative reviews exist but no keywords match
    if negative_reviews and not suggestions:
        suggestions.append("Review negative feedback and improve customer experience.")

    return " ".join(suggestions) if suggestions else "No major improvements needed."
