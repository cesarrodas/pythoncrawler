import time
import json
import urllib
import requests
from bs4 import BeautifulSoup

start_url = "https://en.wikipedia.org/wiki/React_(JavaScript_library)"
start = input("Enter a topic to learn: ")
saving = input("Did you want to save your search? (y|n) : ")
if(saving == "y" or saving == "yes"):
    file_name = input("Enter a file name for this search: ") + ".txt"
    saving = True
else:
    saving = False


target_url = "https://en.wikipedia.org/wiki/Philosophy"

def related_articles():
    search_url = "http://en.wikipedia.org/w/api.php?format=json&action=query&generator=search&gsrnamespace=0|1&gsrlimit=20&prop=pageimages|extracts&pilimit=max&exintro&explaintext&exsentences=3&exlimit=max&pithumbsize=400&gsrsearch=" + str(start)
    print(search_url)
    response = requests.get(search_url).json()
    articles = response['query']['pages'].keys()
    if(saving):
        try:
            search_file = open(file_name, "w")
        except:
            print("could not open the file")

    for article in articles:
        if(saving):
            try:
                search_file.write("==========================================" + "\n\n")
                search_file.write(response['query']['pages'][article]['title'] + "\n\n")
                search_file.write("http://en.wikipedia.org/?curid=" + article + "\n\n")
                search_file.write("Description: " + response['query']['pages'][article]['extract'] + "\n\n")
            except Exception as e:
                print(e)
        print("\n")
        print(response['query']['pages'][article]['title'])
        print("http://en.wikipedia.org/?curid=" + article)
    if(saving):
        try:
            search_file.close()
        except:
            print("could not close the file")

def find_first_link(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    content_div = soup.find(id="mw-content-text").find(class_="mw-parser-output")
    for element in content_div.find_all("p", recursive=False):
        if element.find("a", recursive=False):
            article_link = element.find("a", recursive=False).get('href')
            break

    if not article_link:
        return

    first_link = urllib.parse.urljoin('https://en.wikipedia.org/', article_link)

    return first_link

def continue_crawl(search_history, target_url, max_steps=25):
    if search_history[-1] == target_url:
        print("We've found the target article!")
        return False
    elif len(search_history) > max_steps:
        print("The search has gone on suspiciously long, aborting search!")
        return False
    elif search_history[-1] in search_history[:-1]:
        print("We've arrived at an article we've already seen, aborting search!")
        return False
    else:
        return True

article_chain = [start_url]

related_articles()

# while continue_crawl(article_chain, target_url):
#     print(article_chain[-1])
#     # download html of last article in article_chain
#     # find the first link in that html
#     first_link = find_first_link(article_chain[-1])
#
#     if not first_link:
#         print("We've arrived at an article with no links, aborting search!")
#         break
#     # add the first link to article_chain
#     article_chain.append(first_link)
#     # delay for about two seconds
#     time.sleep(2)
