#pip install fuzzywuzzy
#pip install python-Levenshtein
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import psycopg2
from psycopg2 import connect, Error
def poisk(word, books: dict):
    lst = []
    for book_id in books:
        lst.append(books[book_id].title["ru"])
    a = process.extract(word, lst, limit=3)
    print(a)
    ans = []
    for i in a:
        for j in books.values():
            if i[0] == j.title["ru"]:
                ans.append(j)

    return ans


