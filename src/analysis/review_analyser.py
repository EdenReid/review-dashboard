import re 
from collections import Counter 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class ReviewAnalyser:

    def __init__(self):

        self.analyser = SentimentIntensityAnalyzer()

    def get_most_common_words(self, df, n=10):

        if df is None:
            return []
        all_text = " ".join(df["Review"].astype(str)).lower()
        all_text = re.sub(r"[^\w\s]", "", all_text)
        words = all_text.split()
        stopwords = {
            "a","about","above","after","again","against","all","am","an","and","any","are","aren","as","at",
            "be","because","been","before","being","below","between","both","but","by",
            "can","could",
            "did","do","does","doing","down","during",
            "each",
            "few","for","from","further",
            "had","has","have","having","he","her","here","hers","herself","him","himself","his","how",
            "i","if","in","into","is","it","its","itself",
            "just",
            "me","more","most","my","myself","made",
            "no","nor","not","now",
            "of","off","on","once","only","or","other","our","ours","ourselves","out","over","own",
            "same","she","should","so","some","such",
            "than","that","the","their","theirs","them","themselves","then","there","these","they","this","those","through","to","too",
            "under","until","up",
            "very",
            "was","we","were","what","when","where","which","while","who","whom","why","with","would",
            "you","your","yours","yourself","yourselves"
        }

        filtered_words = [
            word for word in words 
            if word not in stopwords and len(word) > 2
        ]

        counts = Counter(filtered_words)

        return counts.most_common(n)

    def get_sentiment_scores(self, df):

        if df is None:
            return []

        df = df.copy()

        sentiment_scores = [] 

        for review in df["Review"]:
            score = self.analyser.polarity_scores(str(review))
            score = score["compound"]
            score = ((score + 1) / 2) * 5 # converts from -1 to 1 scale into 0 to 5
            score = round(score, 1)

            sentiment_scores.append(score)

        df["Sentiment"] = sentiment_scores

        return df 

if __name__ == "__main__":

    import pandas as pd
    from src.data.review_data_handler import ReviewDataHandler

    handler = ReviewDataHandler()
    analyser = ReviewAnalyser()

    file_path = "src/data/review_test_data_25_rows.csv"

    valid, message, df = handler.validate_file(file_path)

    if not valid:
        print("error")
    else:

        min_date, max_date = handler.find_min_max_dates(df) 
        df = handler.get_sorted_reviews(min_date, max_date)
        df = analyser.get_sentiment_scores(df)

        for index, row in df.iterrows():
            print(f"Review: {row['Review']}")
            print(f"Sentiment Score: {row['Sentiment']}")
            print() 