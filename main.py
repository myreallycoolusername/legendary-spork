import os
import time
from flask import Flask, request, send_file, redirect, url_for
from flask_executor import Executor
import freeGPT
from PIL import Image
from io import BytesIO
import uuid

app = Flask(__name__)
executor = Executor(app)

@app.route('/generate', methods=['GET'])
async def generate():
    id = request.args.get('id')
    prompt = request.args.get('prompt')
    resp = await getattr(freeGPT, "prodia").Generation().create(prompt)
    img = Image.open(BytesIO(resp))
    
    # Generate a random string for the filename
    filename = f"{uuid.uuid4()}.png"
    
    # Save the image to the static folder
    filepath = os.path.join('static', filename)
    img.save(filepath)

    # Schedule the deletion of the image file after 5 minutes
    executor.submit(delete_image, filepath, delay=300)

    # Redirect the user to the URL of the saved image
    return redirect(url_for('static', filename=filename))

def delete_image(filepath, delay):
    time.sleep(delay)
    if os.path.exists(filepath):
        os.remove(filepath)

if __name__ == '__main__':
    app.run()
    
