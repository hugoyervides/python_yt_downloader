from Dao.QueueDao import QueueDao
from Dao.VideoDao import VideoDao
import pymongo
import time

class VideoManager:

    config: object = {
        'DOWNLOAD_PATH': './downloads',
        'MAX_CACHE_SIZE': 8000, #This is in MB
        'PURGE_SIZE': 100, #Amount of data to delete if we reach the MAX_CACHE_SIZE limit
        'MONGO_CONNECTION_STRING': 'mongodb://localhost:27017',
        'VIDEOS_COLLECTION_NAME': 'videos',
        'QUEUE_COLLECTION_NAME': 'queue',
        'DB_NAME': 'pythonyt'
    }

    queue_dao: QueueDao = None
    video_dao: VideoDao = None

    def __init__(self) -> None:
        # override configs with environment variables if available
        self.override_configs()

        # start daos
        mongo_client: MongoClient = pymongo.MongoClient(self.config['MONGO_CONNECTION_STRING'],connect=False)
        db = mongo_client[self.config['DB_NAME']]
        videos_collection = mydb[self.config['VIDEOS_COLLECTION_NAME']]
        queue_collection = mydb[self.config['QUEUE_COLLECTION_NAME']]

        self.queue_dao = QueueDao(queue_collection)
        self.video_dao = VideoDao(video_collection)


    def override_configs(self) -> None:
        for key in self.config.keys():
            if os.getenv(key) is not None:
                config[key] = os.getenv(key)

    def get_video(self, video_id: str) -> None:
        if not self.video_dao.exist(video_id):
            self.download_video(vide_id)

        return self.video_dao.get_video(video_id)

    def download_video(self, video_id: str) -> bool:
        # check if video is already in queue 
        for i in range(5):
            if self.queue_dao.exists(video_id):
                time.sleep(2) 
            break
        
        #Check if video is already on disk
        if self.video_dao.exist(video_id):
            return

        # check if we have free space on disk 
        # TODO

        # add video to queue and start downloading
        self.queue_dao.add(video_id)
        try:
            video_info: object = self.video_service.download_audio(vide_id)
        except:
            # TODO: Logger

            return False
