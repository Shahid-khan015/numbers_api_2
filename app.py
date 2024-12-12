from flask import Flask, Response , jsonify
import os
from flask_cors import CORS 

app = Flask(__name__)

CORS(app)

application = app

out_dir = r"dataset/numbers/"
video_extensions = ('.mp4', '.avi', '.mov', '.mkv')
video_links = {}
num = [ f for f in os.listdir(out_dir) ]
links = [os.path.join(out_dir, f) for f in num]

mp4 = {}
for link in links:
    mp4_link = [os.path.join(link, f) for f in os.listdir(link) if f.endswith(video_extensions)]
    for mp4_l in mp4_link:
        mp4[link.replace(out_dir  , '')] = mp4_l


@app.route('/')
def home():
    return jsonify(mp4)



@app.route('/<number>')
def render(number):
    def generate(video_path):
        with open(video_path, 'rb') as f:
            while True:
                chunk = f.read(1024 * 1024)
                if not chunk:
                    break
                yield chunk

    return Response(generate(mp4[f"{number}"]), mimetype='video/mp4')

if __name__ == '__main__':
    app.run()
