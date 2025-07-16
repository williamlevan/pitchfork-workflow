from utils.logger import log
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def fetch_pitchfork():
    """Fetch Pitchfork Selects Playlist articles"""
    log("Fetching Pitchfork articles...")
    newsUrl = "https://pitchfork.com/news/"
    response = requests.get(newsUrl)
    if response.status_code != 200:
        log(f"Failed to fetch Pitchfork articles: {response.status_code}")
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    playlistArticles = []
    
    # Here, I want to get every h3 element whose inner html includes the text "This Week's Pitchfork Selects Playlist"
    playlist_elements = soup.find_all("h3")
    filtered_elements = [element for element in playlist_elements if "Pitchfork Selects Playlist" in element.get_text()]
    for element in filtered_elements:
        # Get the parent div
        parent_div = element.find_parent("div")
        children_list = list(parent_div.children)
        article_title = ""
        article_url = ""
        article_date = ""
        for child in children_list:
            if child.name == "a":
                article_url = child.get("href")
                a_child = child.find("h3")
                article_title = a_child.get_text()
            if child.name == "div":
                time_child = child.find("time")
                if time_child:
                    article_date = time_child.get_text()
        # if article_date ("Month DD, YYYY") is within the last two weeks, add it to the playlistArticles array
        if article_date:
            # convert article_date to a date object
            formatted_date = datetime.strptime(article_date, "%B %d, %Y")
            if formatted_date > datetime.now() - timedelta(weeks=2):
                playlistArticles.append({"title": article_title, "url": article_url, "date": article_date})    
    
    return playlistArticles
