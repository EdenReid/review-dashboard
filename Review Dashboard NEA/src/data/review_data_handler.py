import os, csv

class ReviewDataHandler:
    def validate_file(self, file_path : str):

        _, file_extension = os.path.splitext(file_path) # validates file ending 
        if file_extension != ".csv":
            return False, "File ending must be .csv"
        
        try:

            with open(file_path, newline = "") as f: 
                reader = csv.reader(f)
                headers = next(reader)

                required_headers = ("Date","Review") # checking that file contains correct headers
                for header in required_headers:
                    if header not in headers:
                        return False, f"File missing {header} header"
                    
                date_index = headers.index("Date") 
                review_index = headers.index("Review")
                
                for row in reader: #checking for missing fields
                    if not row[date_index].strip() or not row[review_index].strip():
                        return False, "CSV file contains missing Date or Review values"

                return True, ""
            
        except FileNotFoundError, UnicodeDecodeError, csv.Error:

            return False, "File could not be read as a valid CSV"
        
print(ReviewDataHandler().validate_file("c:/users/19edenr/OneDrive - Holland Park School/Desktop/Review Dashboard NEA/data/missing_data_csv"))
