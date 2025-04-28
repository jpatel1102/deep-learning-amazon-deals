# 03_llm_recommendations.py

import pandas as pd
from transformers import pipeline
import os

# ---------------
# SETTINGS
# ---------------
INPUT_CSV = "data/collected_deals.csv"
OUTPUT_CSV = "data/deals_with_recommendations.csv"

# ---------------
# LOAD LLM PIPELINE
# ---------------
def load_llm():
    try:
        return pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
    except:
        print("⚠️ LLM model could not load, falling back to Mock recommender!")

        class MockLLM:
            def __call__(self, text):
                if "good" in text.lower() or "best" in text.lower():
                    return [{"label": "POSITIVE"}]
                else:
                    return [{"label": "NEGATIVE"}]

        return MockLLM()

# ---------------
# MAIN
# ---------------
if __name__ == "__main__":

    if not os.path.exists(INPUT_CSV):
        print("❗ Please run 01_data_collection.py first!")
        exit(1)

    df = pd.read_csv(INPUT_CSV)

    llm = load_llm()
    print("Running LLM Recommendations...")

    recommendations = []
    for title in df['title'].fillna(""):
        result = llm(title)
        recommendations.append(result[0]['label'])

    df['recommendation'] = recommendations

    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False)

    print(f"✅ Deals with recommendations saved to {OUTPUT_CSV}")
