import os, csv
import pandas as pd
class ReviewDataHandler:
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

                return True, "", df
            
        except FileNotFoundError, UnicodeDecodeError, csv.Error:

            return False, "File could not be read as a valid CSV", None
        
    def find_min_max_dates(self, df):
        df["Date"] = pd.to_datetime(df["Date"])

        min_date = df["Date"].min().date()
        max_date = df["Date"].max().date()
        
        return min_date, max_date