import re
from bs4 import BeautifulSoup as bs
from nltk.corpus import stopwords
import os
from collections import defaultdict
import Levenshtein as ls
import json

# nltk.download('stopwords')  # Download stopwords in English
stopwords = set(stopwords.words("english"))

indexDatas = []

# Processing the HTML files
for filepath in os.listdir("./websites"):
    html_file = open("./websites/{}".format(filepath), "r", encoding="utf-8")
    content = html_file.read()
    page = bs(content, "lxml")

    html_file_name = html_file.__str__().split("/")
    html_file_name = html_file_name[2].split("\'")
    html_file_name = html_file_name[0]

    words = []
    cleaned_words = []

    pFinder = page.find_all("p")
    for i in pFinder:
        words.extend(i.get_text().lower().split())

    for item in words:
        if item.__contains__("["):
            index_value = words.index(item)
            item = item.split("[")
            item = item[0]
            item = re.sub("[^A-Za-z0-9]", "", item)
            words[index_value] = item

        if item.__contains__(",") or item.__contains__(".") or item.__contains__("\"") \
                or item.__contains__("(") or item.__contains__(")") or item.__contains__("/"):
            index_value = words.index(item)
            item = item.replace(",", "")
            item = item.replace(".", "")
            item = item.replace("\"", "")
            item = item.replace("(", "")
            item = item.replace(")", "")
            item = item.replace("/", "")
            words[index_value] = item
        if item not in stopwords and not item.isnumeric():
            cleaned_words.append(item)

    inverted_index = defaultdict(lambda: {"count": 0, "index": []})
    for idx, word in enumerate(cleaned_words):
        inverted_index[word]['count'] += 1
        inverted_index[word]['index'].append(idx)
    # print(inverted_index)
    indexDatas.append({"filename": html_file_name, "data": inverted_index})
    # all_inverted_indexes.append(inverted_index)
    # print(html_file_name)
    # print(len(all_inverted_indexes))


# Implementing country search function ---------------------------------------------------------------------------------
def country_search(keyword):
    for indexData in indexDatas:
        if keyword in indexData["data"]:
            print("The word {} appears in {} with the count of {} at the index of {}"
                  .format(keyword, indexData["filename"], indexData["data"][keyword].get('count'),
                          indexData["data"][keyword].get('index')))


def edit_distance_and_fuzzy_search(keyword):
    for indexData in indexDatas:
        for referred_word in indexData['data']:
            edit_distance_ratio = ls.ratio(keyword, referred_word)
            if edit_distance_ratio > 0.75:
                edit_distance = ls.distance(keyword, referred_word)
                print("The edit distance between {} and {} is: {} with the ratio of {} and it's in the {}"
                      .format(keyword, referred_word, edit_distance, edit_distance_ratio.__round__(2),
                              indexData['filename']))


# Search and find similar values -------------------------------------------------------------------------------------
search = ""
while search != "exit":
    search = input("what is the keyword? ")
    country_search(search)
    print()
    edit_distance_and_fuzzy_search(search)
