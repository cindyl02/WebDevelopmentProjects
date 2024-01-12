import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

response = requests.get(url=URL)
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")

all_movies = [movie.getText() for movie in soup.find_all(name="h3", class_="title")]
movies = "\n".join(all_movies[::-1])

with open("data.txt", "w") as data_file:
    data_file.write(movies)
