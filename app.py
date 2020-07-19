from flask import Flask, send_from_directory
from PIL import Image
import os

app = Flask(__name__)


@app.route('/')
def home():
    return "backend home"


@app.route('/image/<string:filename>')
def image(filename):
    if not os.path.exists(os.path.join("images", filename)):
        return 404, "Not Ok dude"
    return send_from_directory('images', filename)


# flask params defaults https://stackoverflow.com/a/14032302/8608146

@app.route('/thumb/<int:width>,<int:height>/<string:filename>')
# flutter cannot handle 308 so we need to send a request with
# a different default value from the client flutter app for eg. height: 1000
# Height is set as a huge value because lower dims are preferred
@app.route('/thumb/<string:filename>', defaults={'width': 460, 'height': 100000})
def thumbnail(filename, width, height):
    if not os.path.exists(os.path.join("images", filename)):
        return 404, "Not Ok dude"

    print(filename, width, height)
    # TODO err check
    img = Image.open(os.path.join("images", filename))
    w, h = img.width, img.height

    aspect = w/h

    tw = width
    th = tw/aspect

    th1 = height
    tw1 = th1 * aspect

    if tw1 < tw:
        # lower dims is preferable
        tw = tw1
        th = th1

    target_file_name = f"{tw}_{th}_{filename}"
    target_file = os.path.join("thumbnails", target_file_name)

    # cached thumbnail
    if os.path.exists(target_file):
        return send_from_directory("thumbnails", target_file_name)

    img.thumbnail((tw, th))
    img.save(target_file)

    return send_from_directory("thumbnails", target_file_name)


# http://192.168.43.159:3000/
app.run('0.0.0.0', 3000, debug=True, threaded=True)
