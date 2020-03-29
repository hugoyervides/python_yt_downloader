from flask import Flask, jsonify, Response, send_file
from video_manager import download_video, exists, get_file_path, update_timestamp
from bson import json_util
app = Flask(__name__)

def get_file(video, attachment):
    #Check if the file exists
    data = exists(video)
    if 'error' in data:
        return Response(
                json_util.dumps(data),
                mimetype='application/json')
    #Return the song and update timestamp
    update_timestamp(video)
    return send_file(get_file_path(video),as_attachment=attachment ,mimetype='audio/mpeg')

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
    return get_file(video, False)

@app.route('/download/<video>')
def download(video):
    return get_file(video, True)

@app.route('/exists/<video>')
def check_video(video):
    return Response(
            json_util.dumps(exists(video)),
            mimetype='application/json')

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)