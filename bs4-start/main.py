from bs4 import BeautifulSoup
import requests

response = requests.get(url="https://news.ycombinator.com/")
yc_webpage = response.text

soup = BeautifulSoup(yc_webpage, "html.parser")
article_tags = soup.find_all(class_="titleline")
article_texts = []
article_links = []
for article_tag in article_tags:
    tag = article_tag.find("a")
    text = tag.getText()
    article_texts.append(text)
    link = tag.get("href")
    article_links.append(link)

article_upvotes = [int(score.getText().split()[0]) for score in soup.find_all(name="span", class_="score")]

largest_number = max(article_upvotes)
largest_index = article_upvotes.index(largest_number)

print(article_texts[largest_index])
print(article_links[largest_index])

print(article_texts)
print(article_links)
print(article_upvotes)

# all_anchor_tags = soup.find_all(name="a")
# print(all_anchor_tags)
#
# all_paragraph_tags = soup.find_all(name="p")
# print(all_paragraph_tags)
#
# heading = soup.find(name="h1", id="name")
# section_heading = soup.find(name="h3", class_="heading")
# print(section_heading.get("class"))

# company_url = soup.select_one(selector="p a")
# print(company_url)
