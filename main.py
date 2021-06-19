import ebooklib
from ebooklib import epub
import re
import pandas as pd

#read epub
def BookReader(name):
    content = []
    book = epub.read_epub(name)
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            #text processing
            raw_data = str(item.get_body_content(), encoding='utf-8')
            pattern = re.compile(r'<.*?>')
            text = pattern.sub('', raw_data).replace('&#13;', '')
            if len(text.strip()) > 0:
                content.append(text)
    return content

#search text
def ContentDetector(book, words, index):
    banned = False
    banned_type = words.loc[index][0]
    banned_words = words.loc[index][1:].tolist()
    separator = '|'
    pattern = '(' + separator.join(banned_words) + ')'
    for chapter in book:
        result = re.search(pattern, chapter, re.IGNORECASE)
        if result is not None:
            print("This book has inappropriate content")
            banned = True
            break
    if banned == False:
        print("This book is appropriate for you")

if __name__ == "__main__":
    Workbank = pd.read_csv("Workbank.csv", header = None)
    #types = Workbank.loc[:, 0].tolist()
    book = BookReader("PJTLT - Chapter15 A God Buys Us Cheeseburgers.epub")
    ContentDetector(book, Workbank, 0) #last parameter is the index of the forbidden type in Workbank
