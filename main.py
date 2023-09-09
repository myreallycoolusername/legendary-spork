from flask import Flask, request, send_file
from flask_executor import Executor
import freeGPT
from PIL import Image
from io import BytesIO
import os
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
    img.save(filename)

    # Schedule the deletion of the image file after 5 minutes
    executor.submit(delete_image, filename, delay=300)

    # Send the image file to the user
    response = send_file(filename, mimetype='image/png')
    return response

def delete_image(filename, delay):
    time.sleep(delay)
    os.remove(filename)

if __name__ == '__main__':
    app.run()
