import pymongo
from pytube import YouTube
from pydub import AudioSegment
import os

DOWNLOAD_PATH = './downloads'

#Connect to the Database
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

#Select database and collection
mydb = myclient["pythonyt"]
mycol = mydb["videos"]

#Function to check if a video exists in the database
def exists(videoId):
    query = { 'videoId' : videoId }
    if mycol.find(query).count() > 0:
        return True
    else:
        return False

#Function to download a new video
def download_video(videoId):
    videoURL = 'https://youtube.com/watch?v=' + videoId
    yt = YouTube(videoURL)
    #get the stream and download
    stream = yt.streams.filter(only_audio=True).first()
    filePath = stream.download(DOWNLOAD_PATH,videoId)
    mp4_audio = AudioSegment.from_file(filePath, "mp4")
    #Export it to mp3
    mp4_audio.export(DOWNLOAD_PATH + '/' + videoId + '.mp3', format='mp3')
    #Remove the old mp4 file
    os.remove(filePath)

    

download_video('e-IWRmpefzE')