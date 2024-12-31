from flask import Flask, request, jsonify, send_from_directory, render_template
from tensorflow.keras.models import load_model  # type: ignore
from tensorflow.keras.preprocessing.image import load_img, img_to_array  # type: ignore
import numpy as np
import os

app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')

MODEL_PATH = 'backend/model/cataract_model.h5'
UPLOAD_FOLDER = 'backend/static/uploads'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = load_model(MODEL_PATH)

@app.route('/')
def serve_home():
    return render_template('index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided.'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected.'}), 400

    image_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(image_path)

    img = load_img(image_path, target_size=(150, 150))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    label = 'Cataract' if prediction[0] > 0.5 else 'Normal'
    confidence = float(prediction[0])

    os.remove(image_path)

    return jsonify({'label': label, 'confidence': confidence})

if __name__ == '__main__':
    app.run(debug=True)
