from pysignalclirestapi import SignalCliRestApi
import openai
import time
import traceback
import json
import pprint
import requests
import os
from PIL import Image
import base64
import logging

logging.basicConfig(level=logging.DEBUG)

group_id_1 = 'group.N09BR1BUL3l5dEo3SXlQdmNJczZMeVlwa0hhSDNwS1h5NUUvdG55SlVrTT0='
group_id_2 = 'group.N09BR1BUL3l5dEo3SXlQdmNJczZMeVlwa0hhSDNwS1h5NUUvdG55SlVrTT0='
internal_group_id = "4eBiE2qluMSFcadk6DLl6gLUUY2JweWlSxf7RXM2Q4M="
nummer_marlon = "+41762193971"
nummer_stephanie = "+41792710638"
nummer_david = "+41799342408"
nummer_martina = "+41786011674"
nummer_robot ="+41797307123"


image_dir_name = "images"
image_dir = os.path.join(os.curdir, image_dir_name)


openai.api_key = "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"
signal_api = SignalCliRestApi("http://localhost:8000",nummer_robot)
group_ids = []

def create_group_list():
    group_list = signal_api.list_groups()

    for entry in group_list:
        id = entry["id"]
        internal_id = entry["internal_id"]
        new_entry = {
            "id": id,
            "internal_id": internal_id
        }
        group_ids.append(new_entry)

def search_group_id(internal_id):
    for entry in group_ids:
        if internal_id == entry["internal_id"]:
            id = entry["id"]
            logging.debug(f"fund group id: {id}")
            return id

def get_ai_text_response(text):
    new_text = "" + text
    ai_response = openai.Completion.create(engine="text-davinci-003", prompt=new_text, max_tokens=250)
    ai_response_text = ai_response["choices"][0]["text"]
    return ai_response_text.strip()

def get_ai_image_response(text):
    generation_response = openai.Image.create(
    prompt=text,
    n=1,
    size="1024x1024",
    response_format="url"
    )
    generated_image_name = "generated_image.png"  # any name you like; the filetype should be .png
    generated_image_filepath = os.path.join(image_dir, generated_image_name)
    generated_image_url = generation_response["data"][0]["url"]  # extract image URL from response
    generated_image = requests.get(generated_image_url).content  # download the image

    with open(generated_image_filepath, "wb") as image_file: # Speichere File -> kann ev. entfernt werden
        image_file.write(generated_image)

    return generated_image_filepath

    # base64_encoded_data = base64.b64encode(generated_image) # Wandle in base64 um



def send_signal_text_message(ai_response):
    id = internal_group_id
    signal_api.send_message(ai_response, [id])
    

def send_signal_image_message(image_path, id): # TODO API ansprechen um ein Bild zu senden
    try:
        signal_api.send_message(message="bitte", recipients=[id], filenames=image_path)
    except Exception as exception:
        logging.debug(exception)

def filter(nachricht):
    is_found = False
    filter_list = [nummer_robot]
    source_number = nachricht["envelope"]["sourceNumber"]
    for filter in filter_list:
        if filter == source_number:
            is_found = True
        else:
            pass
    
    return is_found


def send_to_ai(nachricht_text, id=internal_group_id):
    logging.debug("Start send_to_ai")
    picture = nachricht_text.startswith("Bild:")
    if picture == True:
        logging.debug("send_to_ai Start get_ai_image_response")
        image_path = get_ai_image_response(nachricht_text)
        send_signal_image_message(image_path)
    else:
        logging.debug(f"send_to_ai starts get_ai_text_response Text: {nachricht_text}")
        ai_response = get_ai_text_response(nachricht_text)
        logging.debug(f"send_to_ai starts send_signal_text_message Response: {ai_response}")
        send_signal_text_message(ai_response)

    
def recieve_signal():

    nachrichten = signal_api.receive()

    for nachricht in nachrichten:
        pp_nachricht = pprint.pprint(nachricht)
        logging.debug(pp_nachricht)
        try:
        
            envelope = nachricht["envelope"]
            dataMessage = envelope["dataMessage"]
            groupInfo = dataMessage["groupInfo"]
            message_group_id = groupInfo["groupId"]
            
        except:
            logging.debug("Internal ID not fund \n")
            continue

        id = search_group_id(message_group_id)

        if message_group_id == internal_group_id:
            if filter(nachricht) == False:
                nachricht_text = nachricht["envelope"]["dataMessage"]["message"]
                logging.debug(nachricht_text)                            
                send_to_ai(nachricht_text=nachricht_text)
            else:
                logging.debug("Filter hat True zurückgegeben\n")
        else:
            logging.debug("Die GruppenID stimmt nicht mit der ID KI-Test überein\n")
   
app_state = True

while app_state == True:
    if group_ids == []:
        logging.debug("Create Group-List\n")
        create_group_list()
    logging.debug("Start Recieving\n")
    recieve_signal()
    logging.debug("Start Sleep \n")
    time.sleep(1)


