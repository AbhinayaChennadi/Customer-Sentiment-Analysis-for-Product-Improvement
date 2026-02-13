from src.predict import predict_multiple

# Test reviews
reviews = [
    "The taste was amazing!",
    "Worst food ever.",
    "It was okay, nothing special."
]

results = predict_multiple(reviews)

for r in results:
    print(r)
