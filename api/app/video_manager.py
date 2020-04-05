import pymongo
from pytube import YouTube
from pydub import AudioSegment
import time
import os

#CONFIG 
DOWNLOAD_PATH = './downloads'
APP_URL = 'http://api.insane-hosting.net/converter/'
MAX_CACHE_SIZE = 8000 #This is in MB
PURGE_SIZE = 100 #Amount of data to delete if we reach the MAX_CACHE_SIZE limit

#Connect to the Database
myclient = pymongo.MongoClient("mongodb://db:27017",connect=False)

#Select database and collection
mydb = myclient["pythonyt"]
mycol = mydb["videos"]
myqueue = mydb["queue"]

#Function to check if a video is in processing queue
def check_queue(videoId):
    query = { 'videoId' : videoId}
    if myqueue.find(query).count() > 0:
        print('[VIDEO MANAGER] Video already in processing queue, skiping')
        return True
    else:
        return False

#Function to remove video from queue
def remove_queue(videoId):
    print('[VIDEO MANAGER] Removing video ' +  videoId + ' from processing queue')
    query = { 'videoId' : videoId}
    myqueue.delete_one(query)

#Function to add video to queue
def add_queue(videoId):
    print('[VIDEO MANAGER] Adding video to processing queue')
    query = { 'videoId' : videoId}
    myqueue.insert_one(query)

#Function to update video timestamp
def update_timestamp(videoId):
    query = { 'videoId' : videoId}
    updateQuery = { '$set' : {'downloadTimestamp' : int(time.time())}}
    mycol.update_one(query,updateQuery)

def get_file_path(videoId):
    return DOWNLOAD_PATH + '/' + videoId + '.mp3'

#Function to check if a video exists in the database
def exists(videoId):
    query = { 'videoId' : videoId }
    result = mycol.find(query)
    if result.count() > 0:
        return result[0]
    else:
        return {'error' : 'File does not exist on the server'}

#function to purge unused videos
def purge_cache():
    print('[VIDEO MANAGER] Storage is full! deleting unused songs')
    #get most unused songs
    songs = mycol.find().sort('downloadTimestamp')
    dataDeleted = 0
    numberOfFilesDeleted = 0
    for s in songs:
        if dataDeleted < PURGE_SIZE:
            filePath = DOWNLOAD_PATH + '/' + s['videoId'] + '.mp3'
            dataDeleted += (1 * pow(10,-6)) * os.path.getsize(filePath)
            numberOfFilesDeleted += 1
            #Delete from db and system
            query = {'videoId':s['videoId']}
            mycol.delete_one(query)
            os.remove(filePath)
    print('[VIDEO MANAGER] Purge completed ' + str(numberOfFilesDeleted) + ' files deleted, ' + str(dataDeleted) + 'MB of data deleted')

def space_used():
    totalSize = 0
    for filename in os.listdir(DOWNLOAD_PATH):
        path = DOWNLOAD_PATH + '/' + filename
        totalSize += (1 * pow(10,-6)) * os.path.getsize(path)
    return totalSize

#Function to download a new video
def download_video(videoId):
    #check if we have not reached the 
    if space_used() > MAX_CACHE_SIZE:
        purge_cache()
    #Check if the video already exists in the db
    if 'error' in exists(videoId):
        print('[VIDEO MANAGER] Starting download of video ' + videoId)
        videoURL = 'https://youtube.com/watch?v=' + videoId
        try:
            yt = YouTube(videoURL)
        except:
            return { 'error' : 'Error finding video'}
        #check if video is not over 10 mintues
        if yt.length > 630:
            print('[VIDEO MANAGER] Error, video is too long!!')
            return { 'error': 'Video is to long!'}
        
        videoInfo = { "videoId": videoId, 
                    "title" : yt.title, 
                    "length" : yt.length, 
                    "author" : yt.author, 
                    "description": yt.description, 
                    "streamURL" : APP_URL + 'stream/' + videoId,
                    "downloadURL" : APP_URL + 'download/' + videoId,
                    "downloadTimestamp": int(time.time())}
        #get the stream and download
        stream = yt.streams.filter(only_audio=True).first()
        filePath = stream.download(DOWNLOAD_PATH,videoId)
        print('[VIDEO MANAGER] Video downloaded, converting file to MP3')
        mp4_audio = AudioSegment.from_file(filePath, "mp4")
        #Export it to mp3
        metadata = {'artist': videoInfo['author'], 'title': videoInfo['title']}
        mp4_audio.export(DOWNLOAD_PATH + '/' + videoId + '.mp3', format='mp3', tags=metadata)
        print('[VIDEO MANAGER] Convertion complete, inserting video on DB and deleting mp4 file')
        #Remove the old mp4 file
        os.remove(filePath)
        #Add the song to the database
        mycol.insert_one(videoInfo)
        print('[VIDEO MANAGER] Success!')
        return videoInfo
    else:
        print('[VIDEO MANAGER] Video ' + videoId + ' already exists on the server, skiping')
        query = { 'videoId' : videoId }
        return mycol.find_one(query)
    
