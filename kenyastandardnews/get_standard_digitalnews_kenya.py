# MwendaKE Programs
# https://github.com/MwendaKE
# Email: erickmwenda256@gmail.com
# Phone: +254 702 623 729
# Phone: +254 799 678 038

import re
import requests
from bs4 import BeautifulSoup as BS4
from datetime import datetime

time_now = datetime.now().strftime("%d_%m_%y_%H_%M_%S")

STANDARD_NEWS_URL = "https://www.standardmedia.co.ke"

HEADERS = {"User-Agent": "Chrome/51.0.2704.103"}

SAVE_NEWS_FILE = f"standard_digital_news_{time_now}.txt"

soup = BS4(requests.get(STANDARD_NEWS_URL, headers=HEADERS).text, "html5lib")

standard_news_title = soup.title.get_text().strip()
news_containers = soup.find_all("div", class_="boda-bottom")
		
print(f"\n # {standard_news_title.upper()} # \n")

save_news = open(SAVE_NEWS_FILE, "w")
save_news.write(f"\n # {standard_news_title.upper()} # \n\n")
		
for article in news_containers:
	try:
		news_link = article.find("a").get("href", "No link")
		news_title = article.find("div", class_="sub-title").get_text().strip()
		news_time = article.find("small", class_="text-muted").find_next().get_text().strip()
				
		long_title = re.match("\w+\n", news_title)
	
		if long_title:
			new_news_title = re.split(long_title.group(), news_title)[1].strip()
			print(f" (-) {new_news_title} \n")
			save_news.write(f" (-) {new_news_title} \n")
				
		else:
			print(f" (>) {news_title} \n")
			print(f" (>) {news_link} \n")
			
			save_news.write(f" (>) {news_title} \n\n")
			save_news.write(f" (>) {news_link} \n")
				
			if len(news_time) < 12 and "ago" in news_time:
				print(f" (>) {news_time} \n") 
				
				save_news.write("\n")
				save_news.write(f" (>) {news_time} \n")
				
		print("="*20)
		
		save_news.write("\n")
		save_news.write("="*20)
		save_news.write("\n")
	
#	except Exception as error:
#	    print(f"\n{error}\n")
#	  
  			
	except:
		continue
		
save_news.close()

# MwendaKE Programs
# https://github.com/MwendaKE
# Email: erickmwenda256@gmail.com
# Phone: +254 702 623 729
# Phone: +254 799 678 038
		