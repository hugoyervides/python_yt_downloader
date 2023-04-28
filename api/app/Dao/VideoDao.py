from pymongo import Collection

class VideoDao():

    video_collection: Collection = None

    def __init__(self, video_collection: Collection) -> None:
        if video_collection is None:
            raise ValueError("Colletion cant be null")

        self.video_collection = video_collection

    def exists(self, video_id: str) -> bool:
        if not video_id:
            return False

        query: object = { 'videoId': video_id }
        return self.video_collection.count_documents(query) > 0

    def refresh_video_timestmap(self, video_id: str) -> None:
        if not video_id:
            raise ValueError("Video id cant be null")

        query:object = { 'videoId' : video_id}
        updateQuery:object = { '$set' : {'LastUsedTimestamp' : int(time.time())}}
        self.video_collection.update_one(query,updateQuery)

    def get_video(self, video_id: str):
        if not video_id:
            raise ValueError("Video id cant be null")

        query: object = { 'videoId' : video_id }
        self.video_collection.find_one(query)

    def get_all(self):
        self.video_collection.find()

    def delete_video(self, video_id: str):
        if not vide_id:
            raise ValueError("Video id cant be null")
        
        query: object = { 'videoId': video_id }
        self.video_collection.delete_one(query)

    def insert_video(self, 
        videoId: str,
        title: str,
        length: int,
        author: str,
        description: str,
        location_on_disk: str):

        new_video: object = {
            'videoId': videoId,
            'title': title,
            'length': length,
            'author': author,
            'description': description,
            'location_on_disk': location_on_disk
        }
        self.video_collection.insert_one(new_vide)
    