from flask import Flask, jsonify, Response, send_file
from video_manager import download_video, exists, get_file_path
from bson import json_util
app = Flask(__name__)

@app.route('/convert/<video>')
def get_data(video):
    #Check if we have the video
    data = exists(video)
    if 'error' in data:
        return Response(
                json_util.dumps(download_video(video)),
                mimetype='application/json')
    return Response(
            json_util.dumps(data),
            mimetype='application/json')

@app.route('/stream/<video>')
def get_stream(video):
    #Check if the file exists
    data = exists(video)
    if 'error' in data:
        return Response(
                json_util.dumps(data),
                mimetype='application/json')
    #Stream the song
    return send_file(get_file_path(video), mimetype='audio/mpeg')

@app.route('/download/<video>')
def download(video):
    #Check if the file exists
    data = exists(video)
    if 'error' in data:
        return Response(
                json_util.dumps(data),
                mimetype='application/json')
    #Stream the song
    return send_file(get_file_path(video),as_attachment=True ,mimetype='audio/mpeg')

@app.route('/exists/<video>')
def check_video(video):
    return Response(
            json_util.dumps(exists(video)),
            mimetype='application/json')

#DEV APP RUN 
if __name__ == "__main__":
    app.run()