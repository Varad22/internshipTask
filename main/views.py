from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
from youtube_transcript_api import YouTubeTranscriptApi
import urllib.request
import json
import urllib

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
     
    return "%d:%02d:%02d" % (hour, minutes, seconds)

# Create your views here.
def home(response):
    info={}
    title=''
    link=''
    if response.method=="POST":
        link = response.POST['link']
        if "?" in link:
            VideoID = link.split('=')[-1]
        else:
            VideoID = link.split('/')[-1]

        params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % VideoID}
        url = "https://www.youtube.com/oembed"
        query_string = urllib.parse.urlencode(params)
        url = url + "?" + query_string

        with urllib.request.urlopen(url) as res:
            response_text = res.read()
            data = json.loads(response_text.decode())
            title = data['title']
        transcript_list = YouTubeTranscriptApi.list_transcripts(VideoID)

        for transcript in transcript_list:
            info = transcript.fetch()
        for i in info:
            i['timestamp'] = link+"&t="+str(i['start']).split('.')[0]
            i['start']=convert(i['start'])
    return render(response, 'main/index.html',{'data':info, 'title':title, 'link':link})