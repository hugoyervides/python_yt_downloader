from flask import Flask, jsonify, Response, send_file
from video_manager import download_video, exists, get_file_path, update_timestamp, remove_queue, add_queue, check_queue
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
    #check if we have the video on queue
    if check_queue(video):
        return Response(
                json_util.dumps({
                    'error' : 'Video already in processing queue'
                }),
                mimetype='application/json')
    #add video to queue
    add_queue(video)
    #Check if we have the video
    data = exists(video)
    if 'error' in data:
        #Video not in the server, downloadit
        songData = download_video(video)
        #Remove the video from the processing queue
        remove_queue(video)
        return Response(
                json_util.dumps(songData),
                mimetype='application/json')
    else:
        #Video already in the server, remove from the processing queue and return the video data
        remove_queue(video)
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
    app.run()