from flask import Flask, request, jsonify
from PIL import Image
import pyocr
import io


app = Flask(__name__)

def get_image(url):
    import urllib.request
    with urllib.request.urlopen(url) as url:
        byte = url.read()
    return Image.open(io.BytesIO(byte))

def get_text_by_image(image, langage):
    pyocr.tesseract.TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    tools = pyocr.get_available_tools()
    tool = tools[0]
    builder = pyocr.builders.TextBuilder(tesseract_layout=6)
    text = tool.image_to_string(image, lang=langage, builder=builder)
    return text

@app.route('/ocr', methods=['GET'])
def ocr():
    url = request.headers.get("url")
    langage = request.headers.get("lang")
    print(url)
    print(langage)
    if(url is None or langage is None):
        return jsonify({'error': 'url or langage is not found.'})
    image = get_image(url)
    text = get_text_by_image(image, langage)
    json_list = {'text': text}
    return jsonify(json_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)