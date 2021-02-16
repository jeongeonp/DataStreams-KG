import re  # to extract table with regex
import time
import string
import json
import sys
import random
import os
import argparse

from urllib import request
from urllib.parse import quote_plus
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import spacy
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import gensim
from gensim.models import Word2Vec


print("Loading models ...")
start = time.time()
# nlp = spacy.load("en_core_web_sm")
nlp = spacy.load("en_core_web_lg")
lm = WordNetLemmatizer()
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
word2vec_model = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin.gz', binary=True)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Set chromedriver path
# driver = webdriver.Chrome(executable_path="/Users/na/Documents/DataStreams-KG/chromedriver", chrome_options=chrome_options)
session = requests.Session()
session.cookies.clear()
ua = UserAgent()
proxies = {
  'http': 'http://10.10.1.10:3128',
  'https': 'https://121.168.101.205:8080',
}
headers = {
    "User-Agent": ua.random,
    "Accept": "text_html,application_xhtml+xml,application_xml;q=0.9,image_webp,**/**;q=0.8"
}

print("elapsed time : ", time.time() - start)


# def get_vector(word):
#     if word in word2vec_model:
#         return word2vec_model[word]
#     else:
#         return None

# def search_google(sentence: str):
#     word_set = []
#     # Search specific word or sentence.
#     baseUrl = "https://scholar.google.co.kr/scholar?hl=en&as_sdt=0%2C5&q="
#     # baseUrl = 'https://www.google.com/search?q='
#     plusUrl = sentence
#     url = baseUrl + quote_plus(plusUrl)

#     driver.get(url)
#     driver.find_element_by_name('q').send_keys(sentence)
#     driver.find_element_by_name("q").send_keys(Keys.RETURN)
#     #full path /html/body/div/div[10]/div[2]/div[2]/div[2]
#     papers = driver.find_elements_by_xpath("//*[@id='gs_res_ccl_mid']/div[@*]")
#     print (papers)

#     page = session.get(url)
#     c = page.content
#     soup = BeautifulSoup(c, 'html.parser')

#     # Get stuff
#     mydivs = soup.findAll("div", { "class" : "gs_r" })
#     print(mydivs)


#     html = driver.page_source
#     soup = BeautifulSoup(html, 'html.parser')
#     v = soup.select('.yuRUbf')
#     print(type(v))

#     # for i in v:
#     #     print(i.select_one('.LC20lb.DKV0Md').text)
#     #     print(i.a.attrs['href'])
#     #     print()

#     # 사이트에서 텍스트 검색
#     texts = []

#     # Split text to sentences
#     # doc = nlp(texts)

#     # Parse sentence structure with Spacy
#     for doc in nlp.pipe(texts, disable=["tagger", "parser"]):
#         print([(ent.text, ent.label_) for ent in doc.ents])

#     # Extract noun or noun phrase along sentence structure
#     noun = ""
#     word_set.append(noun)

#     # Validate similarity or clustering

#     return word_set



# main execution command
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='dropFile evaluation program')
    parser.add_argument('-d', help='knowledge search depth for recursion', default=1)
    parser.add_argument('-w', help='knowledge search width(<=30) for recursion', default=1)
    args = parser.parse_args()

    depth = int(args.d)
    width = int(args.w)

    subgraph = dict.fromkeys(['nodes', 'links'])
    subgraph['nodes'] = []
    subgraph['links'] = []

    # print("Running Evaluation DropFile...")
    # start = time.time()
    # recommend_word = []

    # print("elapsed time: {}sec".format(time.time()-start))
    # print("result words: ", recommend_word)

    # # Search specific word or sentence.
    # baseUrl = 'https://scholar.google.co.kr/scholar?hl=en&as_sdt=0%2C5&q='
    # plusUrl = input('What are you going to search? :')

    # recommend_word = search_google(plusUrl)

    # # exit Chrome
    # driver.close()

    # -*- coding: utf-8 -*-
    """
    This code creates a database with a list of publications data from Google
    Scholar.
    The data acquired from GS is Title, Citations, Links and Rank.
    It is useful for finding relevant papers by sorting by the number of citations
    This example will look for the top 100 papers related to the keyword
    'non intrusive load monitoring', so that you can rank them by the number of citations

    As output this program will plot the number of citations in the Y axis and the
    rank of the result in the X axis. It also, optionally, export the database to
    a .csv file.

    Before using it, please update the initial variables

    """




    def get_citations(content):
        out = 0
        for char in range(0, len(content)):
            if content[char:char + 9] == 'Cited by ':
                init = char + 9
                for end in range(init + 1, init + 6):
                    if content[end] == '<':
                        break
                out = content[init:end]
        return int(out)


    def get_year(content):
        for char in range(0, len(content)):
            if content[char] == '-':
                out = content[char - 5:char - 1]
        if not out.isdigit():
            out = 0
        return int(out)


    def get_author(content):
        for char in range(0, len(content)):
            if content[char] == '-':
                out = content[2:char - 1]
                break
        return out


    def get_abstract(content):
        return content[:-1]

    def LemTokens(tokens):
        return [lm.lemmatize(token) for token in tokens]

    def LemNomalize(text):
        return LemTokens(word_tokenize(text.lower().translate(remove_punct_dict)))

    def search(keyword, d):
        if (d == 0):
            return
        number_of_results = 100  # number of results to look for on Google Scholar
        save_database = False  # choose if you would like to save the database to .csv
        path = './nilm_100_exact_author_'+ keyword + '.csv'  # path to save the data

        # Variables
        links = list()
        title = list()
        citations = list()
        year = list()
        rank = list()
        author = list()
        abstract = list()
        recommend_list = list()

        rank.append(0)  # initialization necessary for incremental purposes

        for n in range(0, number_of_results, 10):
            url = 'https://scholar.google.com/scholar?start=' + str(n) + '&q=' + keyword.replace(' ', '+') + '&hl=en&as_sdt=0,5'
            # url = 'https://scholar.google.com/scholar?hl=ko&as_sdt=0%2C5&q=amnesia&btnG='
            headers = {
                "User-Agent": ua.random,
                "Accept": "text_html,application_xhtml+xml,application_xml;q=0.9,image_webp,**/**;q=0.8"
            }
            page = session.get(url, headers=headers)
            c = page.content

            # Create parser
            soup = BeautifulSoup(c, 'html.parser')

            # Get stuff
            mydivs = soup.findAll("div", {"class": "gs_ri"})
            # print(mydivs)

            for div in mydivs:
                try:
                    # print(div.find('h3').find('a').get('href'))
                    links.append(div.find('h3').find('a').get('href'))
                except:  # catch *all* exceptions
                    links.append('Look manually at: https://scholar.google.com/scholar?start=' + str(n) + '&q=non+intrusive+load+monitoring')

                try:
                    # print(div.find('h3').find('a').text)
                    title.append(div.find('h3').find('a').text)
                except:
                    title.append('Could not catch title')

                # print("======================== abstact :", div.find('div', {'class': 'gs_rs'}).text)
                # citations.append(get_citations(div.find('div',{'class' : 'gs_fl'}).text))
                # print(div.find('div',{'class' : 'gs_a'}).text)
                if div.find('div', {'class': 'gs_a'}) is not None and div.find('div', {'class': 'gs_rs'}) is not None:
                    citations.append(get_citations(str(div.format_string)))
                    year.append(get_year(div.find('div', {'class': 'gs_a'}).text))
                    author.append(get_author(div.find('div', {'class': 'gs_a'}).text))
                    abstract.append(get_abstract(div.find('div', {'class': 'gs_rs'}).text))
                    rank.append(rank[-1] + 1)
        # Create a dataset and sort by the number of citations
        data = pd.DataFrame(zip(author, title, citations, year, links, abstract), index=rank[1:],
                            columns=['Author', 'Title', 'Citations', 'Year', 'Source', 'Abstract'])
        data.index.name = 'Rank'

        data_ranked = data.sort_values(by='Citations', ascending=False)
        print(data_ranked.head(20))

        # # Plot by citation number
        # plt.plot(rank[1:],citations,'*')
        # plt.ylabel('Number of Citations')
        # plt.xlabel('Rank of the keyword on Google Scholar')
        # plt.title('Keyword: '+keyword)

        # # Save results
        data_ranked.to_csv(path, encoding='utf-8-sig') # Change the path

        recommend_words = []

        word_score = {}
        for text in data_ranked['Abstract']:
            # # Basic word bag
            # words = word_tokenize(text)  # tokenize words by nltk word_toknizer
            # stops = stopwords.words('english')
            # words = [word.lower() for word in words]  # convert uppercase to lowercase
            # words = [word for word in words if re.match('^[a-zA-Z]\w+$', word)]  # regex version of above line
            # words = [lm.lemmatize(word) for word in words]  # lemmatize words
            # words = [word for word in words if word not in stops]
            # print(words)

            # # Noun phrase
            # doc = nlp(text)
            # head_list = [chunk.root.lemma_ for chunk in doc.noun_chunks]
            # words = [word.lower() for word in head_list]
            # words = [word.lower() for word in words]  # convert uppercase to lowercase
            # words = [word for word in words if re.match('^[a-zA-Z]\w+$', word)]  # regex version of above line
            # print(words)

            # # Noun
            # words = word_tokenize(text)  # tokenize words by nltk word_toknizer
            # words_with_pos = pos_tag(words)
            # noun = ["NN", "NNS", "NNP", "NNPS"]
            # words_with_pos = [word[0] for word in words_with_pos if word[1] in noun]
            # words = [word.lower() for word in words_with_pos]  # convert uppercase to lowercase
            # words = [word for word in words if re.match('^[a-zA-Z]\w+$', word)]  # regex version of above line
            # words = [lm.lemmatize(word) for word in words]  # lemmatize words
            # # print(words)
            # recommend_words += words

            # tfidf_vect = TfidfVectorizer(tokenizer=LemNomalize, stop_words='english', ngram_range=(1, 2), min_df=0.05, max_df=0.85)
            # ftr_vect = tfidf_vect.fit_transform(data_ranked['Abstract'])
            #
            # kmeans = KMeans(n_clusters=3, max_iter=10000, random_state=42)
            # cluster_label = kmeans.fit_predict(ftr_vect)
            # data_ranked['Cluster_label'] = cluster_label
            # print(data_ranked.sort_values(by=['Cluster_label']))

            # Word2Vec
            stops = stopwords.words('english')
            words = word_tokenize(text)
            words = [word.lower() for word in words]
            words = [word for word in words if re.match('^[a-zA-Z]\w+$', word)]
            words = [lm.lemmatize(word) for word in words]
            words = [word for word in words if word not in stops]
            print(words)

            # embedding_model = Word2Vec(sentences=words, size=100, window=2, min_count=50, workers=4, iter=100, sg=1)
            # model_result = word2vec_model.wv.most_similar(keyword)
            # print(model_result)

            for word in words:
                if word not in word2vec_model.wv:
                    continue
                else:
                    if word not in word_score:
                        word_score[word] = word2vec_model.similarity(keyword, word)
                        print("similarity with " + word + " is :", word2vec_model.similarity(keyword, word))
        sorted_score_list = sorted(word_score.items(), key=lambda kv: kv[1], reverse=True)
        
        for idx in range(30):
            recommend_list.append(sorted_score_list[idx][0])
        if keyword in recommend_list:
            recommend_list.remove(keyword)
            recommend_list.append(sorted_score_list[30][0])
        print("Top 30 words after clustering : ", recommend_list)

        links = list(map(lambda u: dict({'source': keyword, 'target': u, 'label': str(word2vec_model.similarity(keyword, u))}), recommend_list[:10]))
        nodes = list(map(lambda u: dict({'id': u }), recommend_list[:10]))
        nodes.append(dict({'id': keyword}))
        
        subgraph['nodes'].extend(nodes)
        subgraph['links'].extend(links)
        print("subgraph of " + keyword + " : ", subgraph)
        
        for z in range(width):
          search(recommend_list[z], d-1)
        
        return


    # Update these variables according to your requirement
    keyword = str(input("Search keyword : "))  # the double quote will look for the exact keyword,
    # the simple quote will also look for similar keywords
    search(keyword, depth)

    with open('subgraph.json', 'w') as f:
        json.dump(subgraph, f)

    # print("Recommend wordset : ", recommend_words)
    # x = {}
    # return_list = []
    # for i in range(len(recommend_words)):
    #     if recommend_words[i] in x:
    #         x[recommend_words[i]] += 1
    #     else:
    #         x[recommend_words[i]] = 1

    # sorted_list = sorted(x.items(), key=lambda kv: kv[1], reverse=True)
    # # print(sorted_list)
    # for idx in range(30):
    #     return_list.append(sorted_list[idx][0])
    # if keyword in return_list:
    #     return_list.remove(keyword)
    #     return_list.append(sorted_list[30][0])

    # print("Top 30 words after clustering : ", return_list)



