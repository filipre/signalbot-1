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

#  class SignalHandler:
#     def __init__(self) -> None:
      
#       pass

nummer_robot ="+41797307123"
signal_api = SignalCliRestApi("http://localhost:8000",nummer_robot)
internal_group_id = "4eBiE2qluMSFcadk6DLl6gLUUY2JweWlSxf7RXM2Q4M="


def send_signal_text_message():
    id = internal_group_id
    signal_api.send_message("Test", [id])

send_signal_text_message()