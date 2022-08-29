from django.shortcuts import render
from .models import video_data

# Create your views here.
import requests
import json

# https://github.com/Anandjeechoubey/async-yt-api


# USING API STARTS HERE
# HERE I HAVE USED API RESULT LIMIT OF 100 ONLY (maxResults=100)


class YTData:
    def __init__(
        self, api_key, query
    ):  # taking arguments for API key and query that is to be searched
        self.api_key = api_key
        self.query = query
        self.next_page_token = None  # token for next page as YouTube API key only provides maximum 0f 50 data in single page and provide key for next page for further data
        self.data = (
            dict()
        )  # dictionary for storing relevent fields from API key (here video title, description, publishtime, image url, channel is extracted)
        self.data["Video List"] = []
        self.count = 1




# function for calling class YTdata which will call API to get data
def display_string(request):
    # List of API keys that can be used
    API_Key = [
        "AIzaSyB9QNacHSAQ4deQp4RjVf3gXZOKXtMCwJk",
        "AIzaSyDK-WNR6d2LayUqiemCKOcMYPlDV6jvTh0",
        "AIzaSyCmLgeX3GtUgfn7ZjkkWHfOWCMb1MkDEpU",
        "AIzaSyAip91VlvxNxaw7Fd1mF1s0lUtegg5WtPU",
        "AIzaSyDAYksLzTBkPf9TQC6th2c9iBSXZ6-Dl8I",
        "AIzaSyDa1vWMOyRYGq4Qv4Lg_AelhTAiHw4E7OQ",
    ]
    # specific query (here used is "smartphone")
    query = "smartphone"
    # Code to check whether a key is exhausted or not
    current_api = ""
    for i in range(len(API_Key)):
        if i == len(API_Key):
            # checking and printing in console if all API keys are used
            print("All API Keys are Exhausted!\nTry Again Tomorrow!")
            break
        # if API key is not giving data then it will give a error message if we try to call the API checking if API key is giving data or not
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&maxResults=100&type=video&eventType=completed&order=date&key={API_Key[i]}"
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        if "error" in data:
            pass
        else:
            print("API Key", i + 1, "is used!")
            api = API_Key[i]
            current_api = api
    yt = YTData(current_api, query)
    yt.get_channel_stats_page1()
    yt.get_channel_stats_pagen()
    # Getting data here in form of dictionary
    dictionary_data = yt.return_data()
    dictionary_data = dictionary_data["Video List"]
    # passing data to HTML file for displaying in web page
    context = {"data": dictionary_data}
    return render(request, "yt/home.html", context)
