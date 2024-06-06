from flask import Flask,request, jsonify, send_file
from flask_cors import CORS, cross_origin
# from google.oauth2.service_account import Credentials
# import gspread
from scripts.load_model import Outpainter

app = Flask(__name__, static_folder="static", template_folder="templates")
# cors = CORS(app, resources={r"/*": {"origins": "*"}})
cors = CORS(app)

outpainter = Outpainter()

"""
app.secret_key = "secret"

def open_gs():
    # Google Sheet setting.
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    credentials = Credentials.from_service_account_file(
        "./static/awesome-advice-328201-fd45bb3e869e.json",
        scopes=scopes
    )
    gc = gspread.authorize(credentials)
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/17gEfTOPkqb916jOX2YwETBWtvgX_0XU7MtV3xuZutP0/edit?usp=sharing"
    spreadsheet = gc.open_by_url(spreadsheet_url)
    return spreadsheet

# CORS permission
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
"""

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
    up = files['up'] if 'up' in files else None
    down = files['down'] if 'down' in files else None
    up_left = files['up_left'] if 'up_left' in files else None
    up_right = files['up_right'] if 'up_right' in files else None
    down_left = files['down_left'] if 'down_left' in files else None
    down_right = files['down_right'] if 'down_right' in files else None

    """
    0: up_left   | 1: up   | 2: up_right  
    -------------+---------+--------------
    3: left      | 4: None | 5: right     
    -------------+---------+--------------
    6: down_left | 7: down | 8: down_right 
    """
    image_map = [up_left, up, up_right, 
                 left, None, right, 
                 down_left, down, down_right]

    result_image_io = outpainter.call(image_map) # ByteIO or StringIO
    return send_file(result_image_io, mimetype='image/png'), 200

if __name__ == "__main__":
    # print (app.url_map)
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=2000)
