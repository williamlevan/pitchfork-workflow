from utils.logger import log
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def process_pitchfork(playlistArticles):
    """Process Pitchfork playlist articles"""
    log("Processing Pitchfork Playlist articles...")
    songs = []
    for article in playlistArticles:
        url = "https://pitchfork.com" + article['url']
        response = requests.get(url)
        if response.status_code != 200:
            log(f"Failed to fetch Pitchfork articles: {response.status_code}")
            continue
        soup = BeautifulSoup(response.text, "html.parser")
        body_inner_container = soup.find("div", class_="body__inner-container")
        title_div = body_inner_container.find("div", string="Pitchfork Selects: " + article['date'])
        next_sibling = title_div.find_next_sibling()
        text = str(next_sibling)
        text = text.split('<p>')[1].split('</p>')[0]
        text_array = text.split('<br/>')
        for text in text_array:
            split_text = text.split(':')
            artist = split_text[0]
            song = split_text[1]
            song = song[2:-1]
            songs.append({"artist": artist, "song": song})
            
    """Fetch and Process Pitchfork Best New Tracks""" 
    log("Processing Pitchfork Best New Tracks...")
    bestNewTracksUrl = "https://pitchfork.com/reviews/best/tracks/"
    response = requests.get(bestNewTracksUrl)
    if response.status_code != 200:
        log(f"Failed to fetch Best New Music articles: {response.status_code}")
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    summary_item_content = soup.find_all("div", class_="summary-item__content")
    for item in summary_item_content:
        a_elements = item.find_all("a")
        for a_element in a_elements:
            href = a_element.get("href")
            if href.startswith("/reviews/tracks/"):
                next_sibling = a_element.find_next_sibling()
                artist = next_sibling.get_text()
                song = a_element.get_text()
                song = song[1:-1]
                next_next_sibling = next_sibling.find_next_sibling()
                time_element = next_next_sibling.find("time")
                song_date = time_element.get_text()
                
                if song_date:
                    formatted_date = datetime.strptime(song_date, "%B %d, %Y")
                    if formatted_date > datetime.now() - timedelta(weeks=2):
                        songs.append({"artist": artist, "song": song})
    
    """Process Pitchfork New Tracks"""
    log("Processing Pitchfork New Tracks...")
    newTracksUrl = "https://pitchfork.com/reviews/tracks/"
    response = requests.get(newTracksUrl)
    if response.status_code != 200:
        log(f"Failed to fetch New Tracks articles: {response.status_code}")
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    summary_item_content = soup.find_all("div", class_="summary-item__content")
    for item in summary_item_content:
        a_elements = item.find_all("a")
        for a_element in a_elements:
            href = a_element.get("href")
            if href.startswith("/reviews/tracks/"):
                song = a_element.get_text()
                next_sibling = a_element.find_next_sibling()
                if "Best New" in next_sibling.get_text():
                    next_sibling = next_sibling.find_next_sibling()
                if not next_sibling.find("time"):
                    artist = next_sibling.get_text()
                    next_sibling = next_sibling.find_next_sibling()
                    if "Best New" in next_sibling.get_text():
                        next_sibling = next_sibling.find_next_sibling()
                    song_date = next_sibling.find("time").get_text()
                else:
                    artist = ""
                    song_date = next_sibling.find("time").get_text()
                
                if song_date:
                    formatted_date = datetime.strptime(song_date, "%B %d, %Y")
                    if formatted_date > datetime.now() - timedelta(weeks=2):
                        songs.append({"artist": artist, "song": song})

    albums = []
    """Process Pitchfork Best New Albums"""
    log("Processing Pitchfork Best New Albums...")
    bestNewAlbumsUrl = "https://pitchfork.com/reviews/best/albums/"
    response = requests.get(bestNewAlbumsUrl)
    if response.status_code != 200:
        log(f"Failed to fetch Best New Album articles: {response.status_code}")
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    summary_item_content = soup.find_all("div", class_="summary-item__content")
    for item in summary_item_content:
        a_elements = item.find_all("a")
        for a_element in a_elements:
            href = a_element.get("href")
            if href.startswith("/reviews/albums/"):
                next_sibling = a_element.find_next_sibling()
                time_element = next_sibling.find("time")
                if time_element:
                    artist = ""
                    album_date = time_element.get_text()
                else:
                    artist = next_sibling.get_text()
                    next_sibling = next_sibling.find_next_sibling()
                    time_element = next_sibling.find("time")
                    album_date = time_element.get_text()
                album = a_element.get_text()
                
                if album_date:
                    formatted_date = datetime.strptime(album_date, "%B %d, %Y")
                    if formatted_date > datetime.now() - timedelta(weeks=2):
                        albums.append({"artist": artist, "album": album})
    
    """Process Pitchfork Best New Reissues"""
    log("Processing Pitchfork Best New Reissues...")
    bestNewReissuesUrl = "https://pitchfork.com/reviews/best/reissues/"
    response = requests.get(bestNewReissuesUrl)
    if response.status_code != 200:
        log(f"Failed to fetch Best New Reissue articles: {response.status_code}")
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    summary_item_content = soup.find_all("div", class_="summary-item__content")
    for item in summary_item_content:
        a_elements = item.find_all("a")
        for a_element in a_elements:
            href = a_element.get("href")
            if href.startswith("/reviews/albums/"):
                next_sibling = a_element.find_next_sibling()
                time_element = next_sibling.find("time")
                if time_element:
                    artist = ""
                    album_date = time_element.get_text()
                else: 
                    artist = next_sibling.get_text()
                    next_sibling = next_sibling.find_next_sibling()
                    time_element = next_sibling.find("time")
                    album_date = time_element.get_text()
                album = a_element.get_text()
                
                if album_date:
                    formatted_date = datetime.strptime(album_date, "%B %d, %Y")
                    if formatted_date > datetime.now() - timedelta(weeks=2):
                        albums.append({"artist": artist, "album": album})
                
    """Process Pitchfork 8.0+ Reviews"""
    log("Processing Pitchfork 8.0+ Reviews...")
    best8PlusUrl = "https://pitchfork.com/reviews/best/high-scoring-albums/"
    response = requests.get(best8PlusUrl)
    if response.status_code != 200:
        log(f"Failed to fetch 8.0+ reviews articles: {response.status_code}")
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    summary_item_content = soup.find_all("div", class_="summary-item__content")
    for item in summary_item_content:
        a_elements = item.find_all("a")
        for a_element in a_elements:
            href = a_element.get("href")
            if href.startswith("/reviews/albums/"):
                album = a_element.get_text()
                next_sibling = a_element.find_next_sibling()
                if "Best New" in next_sibling.get_text():
                    next_sibling = next_sibling.find_next_sibling()
                if not next_sibling.find("time"):
                    artist = next_sibling.get_text()
                    next_sibling = next_sibling.find_next_sibling()
                    if "Best New" in next_sibling.get_text():
                        next_sibling = next_sibling.find_next_sibling()
                    album_date = next_sibling.find("time").get_text()
                else:
                    artist = ""
                    album_date = next_sibling.find("time").get_text()

                if album_date:
                    formatted_date = datetime.strptime(album_date, "%B %d, %Y")
                    if formatted_date > datetime.now() - timedelta(weeks=2):
                        albums.append({"artist": artist, "album": album})
                
    """Process Pitchfork Sunday Reviews"""            
    log("Processing Pitchfork Sunday Reviews...")
    sundayReviewsUrl = "https://pitchfork.com/reviews/sunday/"
    response = requests.get(sundayReviewsUrl)
    if response.status_code != 200:
        log(f"Failed to fetch Sunday reviews articles: {response.status_code}")
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    summary_item_content = soup.find_all("div", class_="summary-item__content")
    for item in summary_item_content:
        a_elements = item.find_all("a")
        for a_element in a_elements:
            href = a_element.get("href")
            if href.startswith("/reviews/albums/"):
                album = a_element.get_text()
                next_sibling = a_element.find_next_sibling()
                if "Best New" in next_sibling.get_text():
                    next_sibling = next_sibling.find_next_sibling()
                if not next_sibling.find("time"):
                    artist = next_sibling.get_text()
                    next_sibling = next_sibling.find_next_sibling()
                    if "Best New" in next_sibling.get_text():
                        next_sibling = next_sibling.find_next_sibling()
                    album_date = next_sibling.find("time").get_text()
                else:
                    artist = ""
                    album_date = next_sibling.find("time").get_text()
                
                if album_date:
                    formatted_date = datetime.strptime(album_date, "%B %d, %Y")
                    if formatted_date > datetime.now() - timedelta(weeks=2):
                        albums.append({"artist": artist, "album": album})

    return [songs, albums]