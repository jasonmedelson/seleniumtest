from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# Create your views here.

def index(request):
    return render(
        request,
        './index.html'
    )
def yt(request):
    return render(
        request,
        './yt.html'
    )
def twinge(request):
    return render(
        request,
        './twinge.html'
    )
def twingedata(request):
    if 'q' in request.GET:
        parse = request.GET['q']
        sort = parse.split(",")
        num = len(sort)
        names = []
        games = []
        zipped = []
        times = []
        data= []
        timeout = 10
        chrome_options = Options()#heroku setting
        chrome_options.binary_location = GOOGLE_CHROME_BIN#heroku setting
        chrome_options.add_argument('--disable-gpu')#heroku setting
        chrome_options.add_argument('--no-sandbox')#heroku setting
        driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)#heroku setting
        # options = webdriver.ChromeOptions() #local setting
        # options.add_argument('headless') #local setting
        # driver = webdriver.Chrome(chrome_options=options) #local setting
        for link in range(num):
            url = "http://twinge.tv/channels/"+sort[link]+"/games/#/7" #http://twinge.tv/channels/lirik/games/#/5
            names.append(link)
            x = 5
            while x > 0:
                driver.get("http://twinge.tv/channels/lirik/")
                try:
                    driver.get(url)
                    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'gameMenu'))
                    WebDriverWait(driver, timeout).until(element_present)
                    x = 0

                except TimeoutException:
                    print("Timed out waiting for page to load")
                    x = x - 1
            driver.implicitly_wait(3)
            game_elements = driver.find_elements_by_css_selector('.channelAllGames__game.ng-binding')
            count = 0
            pointer = 0
            for elements in game_elements:
                text = elements.text
                game_name = text.split("\n")[0]
                if game_name == "H1Z1":
                    pointer = count
                count += 1
            game = game_elements[pointer].text.split("\n")[0]
            games.append(game)
            time_elements = driver.find_elements_by_css_selector('.u-tac.channelAllGames__hover')
            time = time_elements[pointer].text
            times.append(time)
    zipped = zip(games,names,times)
    driver.quit()
    return render(
        request,
        'twingedata.html',
        context={'zipped':zipped },
    )
def youtube(request):
    if 'q' in request.GET:
        parse = request.GET['q']
        sort = parse.split("https")
        num = len(sort)
        links = []
        names = []
        profiles = []
        date = []
        views = []
        for link in range(1,num):
            url = "https"
            try:
                url+=sort[link]
                links.append(url)
                # req = urlreq.urlopen(url)
                url = url[:len(url)-2]
                req = requests.get(url, verify=False)
                soup = BeautifulSoup(req.content)
                name = soup.find_all("div", {"class": "yt-user-info"})
                name = name[0].text.strip()
                names.append(name)
                view = soup.find_all("div", {"class": "watch-view-count"})
                view = view[0].text.strip()
                view = view.split(" ")
                view = view[0]
                view = view.replace(",", "")
                view = int(view)
                views.append(view)
                timestamp = soup.find_all("div", {"id": "watch-uploader-info"})
                timestamp = timestamp[0].text.strip()
                try:
                    timestamp = timestamp.split("on ")
                    timestamp = timestamp[1]
                except:
                    timestamp = timestamp
                date.append(timestamp)
                account = soup.find_all("div", {"class": "yt-user-info"})
                account = account[0].find_all("a")
                account = account[0]['href'].strip()
                account = "youtube.com" + account
                profiles.append(account)
            except:
                names.append(" ")
                views.append(0)
                profiles.append(" ")
                date.append(" ")
    else:
        message = 'You submitted an empty form.'
        return HttpResponse(message)
    zipped = zip(date, names, links,  profiles, views)
    return render(
        request,
        'ytdata.html',
        context={'names': names, "zipped": zipped,
                 'dates': date, "items": num, "links": links,},
    )


def search(request):
    if 'q' in request.GET:
        parse = request.GET['q']
        sort = parse.split("https")
        num = len(sort)
        links = []
        names = []
        like = []
        retweet = []
        tweets=[]
        date=[]
        allinfo=[]
        for link in range(1,num):
            url = "https"
            try:
                url+=sort[link]
                links.append(url)
                # req = urlreq.urlopen(url)
                url = url[:len(url)-2]
                req = requests.get(url, verify=False)
                soup = BeautifulSoup(req.content)
                name = soup.find_all("span", {"class": "username"})
                name= name[4].text.strip()
                name = name[1:]
                names.append(name)

                tweet = soup.find_all("p", {"class": "TweetTextSize--jumbo"})
                tweet = tweet[0].text.strip()
                tweets.append(tweet)

                try:
                    retweets = soup.find_all("a", {"class": "request-retweeted-popup"})
                    retweets = retweets[0].text.strip()
                    retweets = retweets.split(" ")
                    retweets = retweets[0]
                    retweets = int(retweets.replace(",", ""))
                    retweet.append(retweets)
                except:
                    retweets = 0
                    retweet.append(retweets)

                try:
                    likes = soup.find_all("a", {"class": "request-favorited-popup"})
                    likes = likes[0].text.strip()
                    likes = likes.split(" ")
                    likes = likes[0]
                    likes = int(likes.replace(",", ""))
                    like.append(likes)
                except:
                    likes = 0
                    like.append(likes)

                timestamp = soup.find_all("span", {"class": "metadata"})
                timestamp = timestamp[0].text.strip()
                timestamp = timestamp.split("- ")
                timestamp = timestamp[1]
                try:
                    timestamp = timestamp.split("from")
                    timestamp = timestamp[0].strip()
                    date.append(timestamp)
                except:
                    timestamp = timestamp
                    date.append(timestamp)
            except:
                names.append(" ")
                like.append(0)
                retweet.append(0)
                tweets.append(" ")
                date.append(" ")

    else:
        message = 'You submitted an empty form.'
        return HttpResponse(message)
    for i in range(num-1):
        allinfo.append(date[i])
        allinfo.append(names[i])
        allinfo.append(links[i])
        allinfo.append(retweet[i])
        allinfo.append(like[i])
        allinfo.append(tweets[i])
    zipped = zip(date,names,links,retweet,like,tweets)
    return render(
        request,
        'data.html',
        context={'names': names, 'likes': like,
                 'retweets': retweet, 'tweets': tweets, "zipped":zipped,
                 'dates': date, "items":num,"links":links, "fulldata": allinfo},
    )

# def search(request):
#     if 'q' in request.GET:
#         message = 'You searched for: %r' % request.GET['q']
#     else:
#         message = 'You submitted an empty form.'
#     return HttpResponse(message)
