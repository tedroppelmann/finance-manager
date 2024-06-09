from typing import List

class Category:

    def __init__(self, name : str, keywords : List[str] = None):
        self.name = name
        if keywords is not None:
            self.keywords = keywords
        else:
            self.keywords = []
    
    def add_keyword(self, keyword : str):
        self.keywords.append(keyword)
    
    def check_keywords_in_text(self, text : str):
        return any(keyword.upper() in text.upper() for keyword in self.keywords)
    
    def add_keyword_manually(self):
        keyword = input("Enter a keyword: ")
        self.keywords.append(keyword)