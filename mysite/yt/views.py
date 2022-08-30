from django.shortcuts import render
from .models import video_data
from .serializers import VideosSerializer

# Create your views here.
import requests
import json

# https://github.com/youtube/api-samples
# collectin repo YT API


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

    # function for loading page to get the required fields
    def get_loading_stats(self):
        # using URL to get data from API
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={self.query}&maxResults=100&type=video&eventType=completed&order=date&key={self.api_key}"
        # getting data in json form and converting it into string for extraction of relevent fields
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            self.next_page_token = data["nextPageToken"]
            # getting max number of data given in that page
            n = data["pageInfo"]["resultsPerPage"]
            # looping through each data for fields
            for i in range(n):
                video_title = data["items"][i]["snippet"]["title"]
                image = data["items"][i]["snippet"]["thumbnails"]["high"]["url"]
                publishTime = data["items"][i]["snippet"]["publishedAt"]
                channel = data["items"][i]["snippet"]["channelTitle"]
                descrip = data["items"][i]["snippet"]["description"]
                # storing data into dictionary
                self.data["Video List"].append(
                    {
                        "index": self.count,
                        "title": video_title,
                        "description": descrip,
                        "publishtime": publishTime,
                        "channel": channel,
                        "image": image,
                    }
                )
                self.count += 1

        except:
            data = None

    def get_channel_stats(self):
        # using URL to get data from API and applying token received from previous page
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&pageToken={self.next_page_token}&maxResults=100&q={self.query}&type=video&eventType=completed&order=date&key={self.api_key}"
        # getting data in json form and converting it into string for extraction of relevent fields
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            self.next_page_token = data["nextPageToken"]
            # getting max number of data given in that page
            n = data["pageInfo"]["resultsPerPage"]
            # looping through each data for fields
            for i in range(n):
                video_title = data["items"][i]["snippet"]["title"]
                descrip = data["items"][i]["snippet"]["description"]
                publishTime = data["items"][i]["snippet"]["publishedAt"]
                image = data["items"][i]["snippet"]["thumbnails"]["high"]["url"]
                channel = data["items"][i]["snippet"]["channelTitle"]
                # storing data into dictionary
                self.data["Video List"].append(
                    {
                        "index": self.count,
                        "title": video_title,
                        "description": descrip,
                        "publishtime": publishTime,
                        "image": image,
                        "channel": channel,
                    }
                )
                self.count += 1

        except:
            data = None

        # returning dictionary that has relevent fields for displaying
    def return_data(self):
        return self.data


def searchQuery(self, request, format=None):
    serializer_class = VideosSerializer
    data = self.request.data
    print(data)
    query = data["title"]
    print(query)
    queryset = video_data.objects.filter(
        title = query
    )  
    print(queryset)
    serializer = video_data(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)  


# function for calling class YTdata which will call API to get data
def display_string(request):
    # List of API keys that can be used
    API_Key = [
        "AIzaSyDK3D7jgGxwEeGsWzWgMtgu3eLZPM5OeFA",
        "AIzaSyAip91VlvxNxaw7Fd1mF1s0lUtegg5WtPU",
        "AIzaSyDa1vWMOyRYGq4Qv4Lg_AelhTAiHw4E7OQ",
        "AIzaSyCmLgeX3GtUgfn7ZjkkWHfOWCMb1MkDEpU",
        "AIzaSyDK-WNR6d2LayUqiemCKOcMYPlDV6jvTh0",
        "AIzaSyD1N1nQECXYAxmdwcRFV0tqkAa2zLkBFCQ",
        "AIzaSyDAYksLzTBkPf9TQC6th2c9iBSXZ6-Dl8I",
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
            break
    yt = YTData(current_api, query)
    yt.get_loading_stats()
    yt.get_channel_stats()
    # Getting data here in form of dictionary
    dictionary_data = yt.return_data()
    dictionary_data = dictionary_data["Video List"]
    # passing data to HTML file for displaying in web page
    context = {"data": dictionary_data}
    return render(request, "yt/home.html", context)
