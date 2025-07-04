from flask import Flask, request, jsonify
from rembg import remove
from PIL import Image
import io
import base64
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Background Remover API is live"

@app.route('/remove-background', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    try:
        image_file = request.files['image']
        input_image = Image.open(image_file)
        output_image = remove(input_image)

        buffer = io.BytesIO()
        output_image.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()

        return jsonify({'processed_image': img_str})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # ✅ use Render's port
    app.run(host='0.0.0.0', port=port)
