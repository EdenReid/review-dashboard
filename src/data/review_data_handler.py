import os, csv, re
import pandas as pd
from collections import Counter

class ReviewDataHandler:
    def __init__(self):
        self.data = None

    def validate_file(self, file_path : str):

        _, file_extension = os.path.splitext(file_path) # validates file ending 
        if file_extension != ".csv":
            return False, "File ending must be .csv", None
        
        try:

            with open(file_path, newline="", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                headers = next(reader)
                headers = [h.strip() for h in headers]

                required_headers = ("Date","Review") # checking that file contains correct headers
                for header in required_headers:
                    if header not in headers:
                        return False, f"File missing {header} header", None 
                    
                date_index = headers.index("Date") 
                review_index = headers.index("Review")
                
                for row in reader: #checking for missing fields
                    if not row[date_index].strip() or not row[review_index].strip():
                        return False, "CSV file contains missing Date or Review values", None
                
                df = pd.read_csv(file_path, encoding="utf-8-sig")
                self.data = df

                return True, "", df
            
        except (FileNotFoundError, UnicodeDecodeError, csv.Error):

            return False, "File could not be read as a valid CSV", None
    
    def find_min_max_dates(self, df):
        df["Date"] = pd.to_datetime(df["Date"], dayfirst = True)

        min_date = df["Date"].min().date()
        max_date = df["Date"].max().date()
        
        return min_date, max_date
    
    def filter_reviews(self, start_date, end_date):
        
        if self.data is None:
            return None

        df = self.data.copy()

        df["Date"] = pd.to_datetime(df["Date"], dayfirst= True)
        
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)

        df = df[
            (df["Date"] >= start_date) &
            (df["Date"] <= end_date)
        ]
        
        return df
    
    def get_sorted_reviews(self, start_date, end_date):

        df = self.filter_reviews(start_date, end_date)

        if df is None:
            return

        df = df.sort_values(by="Date", ascending=False)

        return df 
    
    def get_most_common_words(self, start_date, end_date, n=10):

        df = self.filter_reviews(start_date, end_date)
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
    
if __name__ == "__main__":

    handler = ReviewDataHandler()
    file_path = "src/data/review_test_data_25_rows.csv"
    valid, msg, df = handler.validate_file(file_path)
    
    if valid:
        min_date, max_date = handler.find_min_max_dates(df)
        keywords = handler.get_most_common_words(min_date, max_date)
        for word, count in keywords:
            print(f"{word}: {count}")
    else:
        print("error")