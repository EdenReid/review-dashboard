import re, pandas as pd
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
            "can","could","get", "gets", "got", "getting",
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
    
    def get_average_sentiment(self, df):

        if df is None or "Sentiment" not in df.columns:
            return None

        average_score = df["Sentiment"].mean()

        classification = "Neutral"

        if average_score > 3:
            classification = "Positive"
        elif average_score < 2:
            classification = "Negative"

        return (round(average_score, 1), classification)
    
    def get_daily_average_sentiments(self, df, min_date, max_date):

        if df is None or "Sentiment" not in df.columns:
            return None

        daily_avg = df.groupby(df["Date"])["Sentiment"].mean()
        all_dates = pd.date_range(start=min_date, end=max_date)
        
        daily_avg = daily_avg.reindex(all_dates)
        daily_avg = daily_avg.ffill() 

        return daily_avg

