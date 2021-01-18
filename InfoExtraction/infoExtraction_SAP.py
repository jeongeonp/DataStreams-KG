import nltk, re, pprint
from nltk.tokenize import word_tokenize
from urllib import request
from bs4 import BeautifulSoup
import pandas as pd
import random


def findPapers(url,number):
    print("### Start searching with given url")
    paperList = []

    author = []
    journal_and_date = []
    
    title_and_link = []

    # Looks for the first 30 paper results 

    for i in range(number):
        soup = BeautifulSoup(request.urlopen(url).read(), 'html.parser')
        #print(soup.text)
        author = author + (soup.find_all('p', 'la-list-authors'))
        journal_and_date = journal_and_date + (soup.find_all('p', 'la-list-pub'))
        #pmid = pmid + (soup.find_all('span', 'docsum-pmid'))
        title_and_link = title_and_link + (soup.find_all('a', 'font-14-bold' , href = True, title = True))

        print(len(author))

    cnt = 0
    
    # Goes through the 30 papers and looks for the paper information: PMID, year, title, author, and journal
    for i in range(len(author)):

        crop = journal_and_date[2*i].text.strip().find(",")
        currYear = (journal_and_date[2*i].text.strip()[crop + 2 :crop + 6])
        currTitle = title_and_link[i].text.strip()
        currLink = title_and_link[i]["href"]
        currAuthor = (author[i].text.strip().split(","))
        currJournal = (journal_and_date[2*i].text.strip()[:crop])

        paperList.append([currLink, currYear, currTitle, currAuthor, currJournal])
        cnt += 1
                    
    print("Total number of papers with the keyword [ Traffic ] :" , cnt)
    print("")
    

    return paperList

def abstract_finder(content):
    for i in range(len(content)):
        if (content[i].text.strip() == "Abstract"):
            return content[i+1]

def keyword_finder(content):
    for i in range(len(content)):
        if("Keywords" in content[i].text.strip()):
            return content[i]

def sentParsing(paperList):
    # To store sentences with the five categories of verbs
    abstractList = []

    authorList = {}
    journalList = {}

    papercnt = 0

    print("Input number of papers: ", len(paperList))

    # Goes through all the papers found
    for paper in paperList:
        print("On paper #", papercnt)

        # Puts the author (organization) and journal name into each dictionary created
        for author in paper[3]:
            if author in authorList:
                authorList[author] = authorList[author] + 1
            else:
                authorList[author] = 1

        if paper[4] in journalList:
            journalList[paper[4]] = journalList[paper[4]] + 1
        else:
            journalList[paper[4]] = 1


        papercnt += 1
        url = paper[0]
        soup = BeautifulSoup(request.urlopen(url).read(), 'html.parser')
        content = (soup.find_all("p"))
        abstract = abstract_finder(content)
        keywords_raw = keyword_finder(content)

        keywords = keywords_raw.text.strip()[9:].strip().split(",")
        
        #print(keywords)

        #print(abstract[0].text.strip())
        print()
        abstractList.append({"title": paper[2], "keywords": keywords, "abstract": abstract.text.strip()})

    print("Output number of papers: ", papercnt)
    return abstractList


paperList = []
url = "http://www.sapub.org/journal/articles.aspx?journalid=1048"
paperList = paperList + findPapers(url,1)


print(paperList)
print(len(paperList))

print(sentParsing(paperList))






