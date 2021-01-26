import nltk, re, pprint
from nltk.tokenize import word_tokenize
from urllib import request
from bs4 import BeautifulSoup
import pandas as pd
import random
import requests
import re    # to extract table with regex
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException  
import time
import json
import sys


def sele_papers(link, keyword, N):
    browser = webdriver.Chrome('/Users/na/Downloads/chromedriver')
    browser.get(link)
    browser.find_element_by_name('q').send_keys(keyword)
    browser.find_element_by_name("q").send_keys(Keys.RETURN)


    #full path /html/body/div/div[10]/div[2]/div[2]/div[2]
    papers = browser.find_elements_by_xpath("//*[@id='gs_res_ccl_mid']/div[@*]")
    # print (papers)
    links = {}
    for i, eachPaper in enumerate(papers):
      if (i <= N):
        # print (eachArticle.find_element_by_xpath('.//g-card/div/div/div[2]/a').get_attribute('href'))
        #full path /html/body/div/div[10]/div[2]/div[2]/div[2]/div[1]/div[2]/h3/a
        # print ("----")
        # print (eachPaper.find_element_by_xpath('.//div[@*]/h3/a').get_attribute('href'))
        # print (eachPaper.find_element_by_xpath('.//div[@*]/div[1]').text)
        # print (eachPaper.find_element_by_xpath('.//div[@*]/div[2]').text)
        # print (eachPaper.find_element_by_xpath('.//div[@*]/div[3]').text)
        try:
          links["link"] = eachPaper.find_element_by_xpath('.//div[@*]/h3/a').get_attribute('href') #link
          links["author"] = eachPaper.find_element_by_xpath('.//div[@*]/div[1]').text #author
          links["abstract"] = eachPaper.find_element_by_xpath('.//div[@*]/div[2]').text #abstract
          links["ref"] = eachPaper.find_element_by_xpath('.//div[@*]/div[3]').text #ref
          # print (links)
        except NoSuchElementException:
          continue
      
    # time.sleep(3)
    browser.quit()
    return links

def sele_articles(link, keyword, N):
    browser = webdriver.Chrome('/Users/na/Downloads/chromedriver')
    browser.get(link)
    browser.find_element_by_name('q').send_keys(keyword + " news")
    browser.find_element_by_name("q").send_keys(Keys.RETURN)
    # btn = browser.find_element_by_xpath("/html/body/div[1]/div[3]/form/div[2]/div[1]/div[3]/center/input[1]")
    # btn.click()
    tabs = browser.find_elements_by_xpath('//*[@id="hdtb-msb-vis"]/div[@*]')
    foundNewsTab = False
    for tab in tabs:
      title = tab.text
      # print (title)
      if (title == "뉴스"):
        tab.click()
        foundNewsTab = True
        break
    
    if foundNewsTab == False:
      print ("error")
    
    articles = browser.find_elements_by_xpath("//*[@id='rso']/*")
    # print (articles)
    links = []
    for i, eachArticle in enumerate(articles):
      if (i <= N):
        # print (eachArticle.find_element_by_xpath('.//g-card/div/div/div[2]/a').get_attribute('href'))
        links.append(eachArticle.find_element_by_xpath('.//g-card/div/div/div[2]/a').get_attribute('href'))
      
    # time.sleep(3)
    browser.quit()
    return links

link = "https://www.google.com/"


## load json data
# with open('./train_annotated.json') as json_file:
#     json_data = json.load(json_file)

# print (type(json_data))
# eachEntitySet = json_data[0]["vertexSet"][0]
# jsonn = {}
# # print (eachEntitySet) #entity one
# for i, eachEntitySet in enumerate(json_data[0]["vertexSet"]):
#   print (eachEntitySet)
#   jsonn[i] = {}
#   if (i <= 1):
#     for eachNode in eachEntitySet:
#       keyword = eachNode["name"]
#       print (keyword, " -----------------------------")
#       # print (sele_articles(link, keyword, 5))
#       if (keyword in jsonn[i]):
#         continue
#       # print (sele_papers("https://scholar.google.com", keyword, 5))
#       jsonn[i][keyword] = sele_papers("https://scholar.google.com", "search", 1)

# with open('./searchPapers.txt', 'w') as f:
#   f.write(json.dumps(jsonn))

sele_papers("https://scholar.google.com", "search", 1)
  