from pymongo import Collection

class QueueDao:

    queue_collection: Collection = None

    def __init__(self, queue_collection: Collection) -> None:
        if queue_collection is None:
            raise ValueError("Collection cant be null")
        
        self.queue_collection = queue_collection

    def exists(self, video_id: str) -> bool:
        if not video_id:
            return False
        
        query: object = { 'videoId' : video_id }
        return self.queue_collection.count_documents(query) > 0

    def add_video(self, video_id: str) -> None:
        if not video_id:
            raise ValueError("vide_id cant be null")

        query: object = { 'videoId': video_id }
        self.queue_collection.insert_one(query)
    
    def remove_video(self, video_id: str) -> None:
        if not video_id :
            raise ValueError("video id cant be null")

        query: object = { 'videoId' : video_id}
        self.queue_collection.delete_one(query)