from src.predict import predict_multiple

reviews = ["The taste was amazing!", "Worst food ever."]

results = predict_multiple(reviews)
for r in results:
    print(r)
