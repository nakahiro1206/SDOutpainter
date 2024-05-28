from flask import Flask,request, jsonify, send_file
from flask_cors import CORS, cross_origin
# from google.oauth2.service_account import Credentials
# import gspread
from static.generate import generate

app = Flask(__name__, static_folder="static", template_folder="templates")
# cors = CORS(app, resources={r"/*": {"origins": "*"}})
cors = CORS(app)
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
    print(request.method)
    # if(request.method!='POST'):
    #     return jsonify({"error": "method is invlid except POST"}), 400
    
    arguments = request.get_data()
    # print(arguments)
    files = request.files
    print(files)
    print(files.keys())
    image = request.files['image'] # image: FilStorage
    print(image); print(type(image));

    # filename = '000-000.png'
    # image_path = os.path.join('static', filename)
    # image.save(image_path)

    generated_image_io = generate(image) # ByteIO or StringIO
    return send_file(generated_image_io, mimetype='image/png'), 200

if __name__ == "__main__":
    # print (app.url_map)
    app.run(debug=True, host='0.0.0.0', port=2000)
