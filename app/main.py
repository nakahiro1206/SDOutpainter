from flask import Flask,request, send_file
from flask_cors import CORS
from scripts.Outpainter import Outpainter

app = Flask(__name__)
cors = CORS(app)

outpainter = Outpainter()

@app.route('/human-drawing',methods=['POST'])
def human_drawing():
    print("Requested received", request.method)
    print("model loaded", outpainter)

    files = request.files
    print(files)
    print(files.keys())
    """type of image is FileStorage"""
    left = files['left'] if 'left' in files else None
    right = files['right'] if 'right' in files else None
    up = files['top'] if 'top' in files else None
    down = files['bottom'] if 'bottom' in files else None

    """
    0: up_left   | 1: up   | 2: up_right  
    -------------+---------+--------------
    3: left      | 4: None | 5: right     
    -------------+---------+--------------
    6: down_left | 7: down | 8: down_right 
    """
    image_map = [None, up, None, 
                 left, None, right, 
                 None, down, None]

    result_image_io = outpainter.call(image_map) # ByteIO or StringIO
    return send_file(result_image_io, mimetype='image/png'), 200

if __name__ == "__main__":
    # print (app.url_map)
    # curl -X POST http://127.0.0.1:2000/human-drawing -F left=@Left.png -F up=@Top.png
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=2000)
