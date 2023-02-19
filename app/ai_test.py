import openai
import requests
import os
from PIL import Image
import base64

image_dir_name = "images"
image_dir = os.path.join(os.curdir, image_dir_name)

promt = "Fotorealistisches Bild von zwei Galaxien welche verschmelzen"


openai.api_key = "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"

generation_response = openai.Image.create(
    prompt=promt,
    n=1,
    size="1024x1024",
    response_format="url"
)

generated_image_name = "generated_image.png"  # any name you like; the filetype should be .png
generated_image_filepath = os.path.join(image_dir, generated_image_name)
generated_image_url = generation_response["data"][0]["url"]  # extract image URL from response
generated_image = requests.get(generated_image_url).content  # download the image

with open(generated_image_filepath, "wb") as image_file:
    image_file.write(generated_image)

base64_encoded_data = base64.b64encode(generated_image)



print(generated_image_filepath)
im = Image.open(generated_image_filepath)
im.show()