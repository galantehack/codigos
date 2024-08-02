from flask import Flask, request, render_template, send_file
import pyshorteners
import qrcode
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from PIL import Image

app = Flask(__name__)
s = pyshorteners.Shortener()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['long-url']
    short_url = s.tinyurl.short(long_url)
    return render_template('index.html', short_url=short_url)

@app.route('/qrcode', methods=['POST'])
def generate_qr():
    if 'qr-data' in request.form:
        data = request.form['qr-data']
        img = qrcode.make(data)
    else:
        return "No data provided", 400

    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png', as_attachment=True, download_name='qrcode.png')

@app.route('/barcode', methods=['POST'])
def generate_barcode():
    data = request.form['barcode-data']
    if not data or len(data) != 12:
        return "Invalid data provided", 400

    EAN = barcode.get_barcode_class('ean13')
    ean = EAN(data, writer=ImageWriter())
    buf = BytesIO()
    ean.write(buf)
    buf.seek(0)
    return send_file(buf, mimetype='image/png', as_attachment=True, download_name='barcode.png')

if __name__ == '__main__':
    app.run(debug=True)
