from flask import Flask
app = Flask(__name__)

@app.route('/data/<video>')
def get_data(video):
    #TODO - Check if the video exists and if not download it and send the data of it

@app.route('/stream/<video>')
def get_stream(video):
    #TODO - Check if the video exists and if not download it and return the stream of the MP3

@app.route('/download/<video>')
def download_video(video):
    #TODO- Check if we have the video and if not download it and return a download of the MP3

@app.route('/exists/<video>')
def check_video(video):
    #TODO- Check if the video exists on the database and if it exists

#DEV APP RUN 
if __name__ == "__main__":
    app.run()