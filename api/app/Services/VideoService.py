from pytube import YouTube

class VideoService:

    YOUTUBE_URL_TEMPLATE: str = "https://youtube.com/watch?v="
    MAX_VIDEO_LENGT: int = 630 # Seconds

    def __init__(self) -> None:
        # TODO

    def save_audio(self, video_id: str, location: str) -> object:
        # TODO

    def save_video(self, video_id: str, location: str) -> object:
        video_url: str = self.YOUTUBE_URL_TEMPLATE + video_id

        yt = YouTube(video_url)

        #check if video is not over 10 mintues
        if yt.length > self.MAX_VIDEO_LENGT:
            raise Exception(f'Video length cant be more than {MAX_VIDEO_LENGT/60} minutes')

    def video_to_audio(self, video_location:str, output_location: str) -> object:
        # TODO