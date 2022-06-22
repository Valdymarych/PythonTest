from requests import *
from bs4 import BeautifulSoup

site=get("https://war.ukrzen.in.ua/alerts/")
print(site.content)
bs=BeautifulSoup(site.content,"html.parser")
p=bs.find("ul")
print(p)