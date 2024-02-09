import json
import validators
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def add(link, channel):

    # finding weekdays and adding to dictionary weekdays_link = { weekday: [links] }
    if not validators.url(link):
        return "Invalid url!"
    chrome_options = Options()
    chrome_options.add_argument("start-maximized");
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(link)
    except Exception as e:
        print(e)
        return "Failed loading url!"
    wait = WebDriverWait(driver, 2)
    try:
        weekdays_link = dict()
        with open("weekdays_link.txt", "r") as data:
            weekdays_link = json.load(data)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ContentMetaInfo__info_item--utGrf")))
        raw_weekdays = driver.find_element(By.CLASS_NAME, "ContentMetaInfo__info_item--utGrf").text
        weekdays = []
        weekday_translate = { "월": "Monday", "화": "Tuesday", "수": "Wednesday", "목": "Thursday", "금": "Friday", "토": "Saturday", "일": "Sunday" }
        for i in raw_weekdays:
            if i in weekday_translate.keys():
                weekdays.append(weekday_translate[i])
                weekdays_link[weekdays[-1]].append(link)
        for i in weekdays:
            weekdays_link[i] = list(set(weekdays_link[i]))
        with open("weekdays_link.txt", "w") as data:
            json.dump(weekdays_link, data)
    except Exception as e:
        return "Failed identifying release weekdays of title!"
        print(e)
    # end

    # finding title, episode and adding to dictionary link_title_episode = { link: [title, episode] }
    preview_found = True
    title = ""
    try:
        title = driver.find_element(By.CLASS_NAME, "EpisodeListInfo__title--mYLjC").text
    except Exception as e:
        print(e)
    try:
        driver.find_element(By.CLASS_NAME, "EpisodeListPreview__button_preview--IBGaa")
        driver.find_element(By.CLASS_NAME, "EpisodeListPreview__button_preview--IBGaa").click()
    except Exception as e:
        print(e)
        preview_found = False
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "EpisodeListList__title--lfIzU")))
        episode = driver.find_element(By.CLASS_NAME, "EpisodeListList__title--lfIzU").text
        link_title_episode = dict()
        with open("link_title_episode.txt", "r") as data:
            link_title_episode = json.load(data)
        link_title_episode[link] = [title, episode]
        with open("link_title_episode.txt", "w") as data:
            json.dump(link_title_episode, data)
    except Exception as e:
        print(e)
        if not preview_found:
            return "Failed adding to notifications, maybe title needs age verification!"
        else:
            return "Failed adding to notifications, maybe there is no episodes yet!"
    # end
    # adding dictionary link_channel = { link: [channel] }
    try:
        channel_title_link = dict()
        with open("channel_title_link.txt", "r") as data:
            channel_title_link = json.load(data)
        if str(channel) not in channel_title_link.keys():
            channel_title_link[str(channel)] = list()
        channel_title_link[str(channel)].append([title, link])
        channel_title_link[str(channel)] = [list(item) for item in set(tuple(row) for row in channel_title_link[str(channel)])]
        with open("channel_title_link.txt", "w") as data:
            json.dump(channel_title_link, data)
    except Exception as e:
        print(e)
        return "Failed adding to notifications. Please contact the administrator!"
    # end

    # adding link: [channel]
    try:
        link_channel = dict()
        with open("link_channel.txt", "r") as data:
            link_channel = json.load(data)
        if link not in link_channel.keys():
            link_channel[link] = list()
        link_channel[link].append(channel)
        link_channel[link] = list(set(link_channel[link]))
        with open("link_channel.txt", "w") as data:
            json.dump(link_channel, data)
    except Exception as e:
        print(e)
        return "Failed adding to notifications. Please contact the administrator!"
    # end
    driver.quit()
    return "Added " + title + " to your notifications!"


def list_of_titles(channel):

    channel = str(channel)
    try:
        channel_title_link = dict()
        with open("channel_title_link.txt", "r") as data:
            channel_title_link = json.load(data)
        if channel not in channel_title_link.keys():
            return "No titles yet"
        answer = ""
        for i in range(len(channel_title_link[channel])):
            answer += str(i + 1) + ". " + channel_title_link[channel][i][0] + "\n"
        return answer
    except:
        return "Error trying to get titles of the channel"


def remove(x, channel):
    channel = str(channel)
    # deleting element from dictionary channel: [title, link]
    channel_title_link = dict()
    with open("channel_title_link.txt", "r") as data:
        channel_title_link = json.load(data)
    if channel not in channel_title_link or x < 1 or x > len(channel_title_link[channel]):
        return "Not a valid number!"
    x -= 1
    title, link = channel_title_link[channel][x]
    channel_title_link[channel].pop(x)
    if not channel_title_link[channel]:
        del channel_title_link[channel]
    with open("channel_title_link.txt", "w") as data:
        json.dump(channel_title_link, data)
    # end

    # deleting element from link: [title, episode]
    link_title_episode = dict()
    with open("link_title_episode.txt", "r") as data:
        link_title_episode = json.load(data)
    del link_title_episode[link]
    with open("link_title_episode.txt", "w") as data:
        json.dump(link_title_episode, data)
    # end

    # deleting element from weekdays: [link]
    weekdays_link = dict()
    with open("weekdays_link.txt", "r") as data:
        weekdays_link = json.load(data)
    for i in weekdays_link:
        if link in weekdays_link[i]:
            weekdays_link[i].remove(link)
    with open("weekdays_link.txt", "w") as data:
        json.dump(weekdays_link, data)
    # end
    
    # deleting element from link_channel
    channel = int(channel)
    link_channel = dict()
    with open("link_channel.txt", "r") as data:
        link_channel = json.load(data)
    link_channel[link].remove(channel)
    if not link_channel[link]:
        del link_channel[link]
    with open("link_channel.txt", "w") as data:
        json.dump(link_channel, data)
    # end
    return f"Successfully deleted {title} from notifications!"


def find_last(link):
    chrome_options = Options()
    chrome_options.add_argument("start-maximized");
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(link)
    wait = WebDriverWait(driver, 2)
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "EpisodeListPreview__button_preview--IBGaa")))
        driver.find_element(By.CLASS_NAME, "EpisodeListPreview__button_preview--IBGaa").click()
    except Exception as e:
        print(e)
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "EpisodeListList__title--lfIzU")))
        return driver.find_element(By.CLASS_NAME, "EpisodeListList__title--lfIzU").text
    except:
        return ""