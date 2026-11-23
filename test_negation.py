
import csv
import json
import urllib.request
import urllib.parse

correct = 0
total = 0

with open("negation_test.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file,skipinitialspace=True)
    print("CSV Columns:", reader.fieldnames)

    for row in reader:
         row = {key.strip().replace('\ufeff', ''): value for key, value in row.items() if key}
        text = row["text"]
        expected = row["expected_sentiment"].strip().lower()

        encoded_text = urllib.parse.quote(text)
        url = f"http://127.0.0.1:5000/make_prediction?text={encoded_text}"

        try:
            with urllib.request.urlopen(url) as response:
                result = json.loads(response.read().decode("utf-8"))

            predicted = result["sentiment"].lower()
            confidence = result["confidence"]

            total += 1

            if predicted == expected:
                correct += 1
                status = "CORRECT"
            else:
                status = "WRONG"

            print(f"\nText: {text}")
            print(f"Expected: {expected}")
            print(f"Predicted: {predicted}")
            print(f"Confidence: {confidence}%")
            print(f"Status: {status}")

        except Exception as error:
            print(f"Error testing: {text}")
            print(error)

print("\n========== FINAL RESULT ==========")
print(f"Total tested: {total}")
print(f"Correct predictions: {correct}")

if total > 0:
    accuracy = (correct / total) * 100
    print(f"Accuracy: {accuracy:.2f}%")
