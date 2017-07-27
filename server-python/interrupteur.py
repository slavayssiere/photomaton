import  RPi.GPIO as GPIO
import time
from picamera import PiCamera, Color
import uuid
import asyncio
import websockets
import threading
import logging
from websocket_server import WebsocketServer
import json
from PIL import Image
import bib

############ Server for websocker
print('wait for connextion on 8000')
server = WebsocketServer(8000, host='0.0.0.0', loglevel=logging.INFO)
t1 = threading.Thread(target=server.run_forever)
t1.start()
print('start thread')

############ GPIO setup
GPIO.setmode(GPIO.BCM)

GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)


############ Camera setup

global_width = 1461
global_height = 1944

camera = PiCamera()
camera.resolution = (global_width, global_height)
camera.annotate_text_size = 120
# camera.annotate_background = Color('blue')
# camera.annotate_foreground = Color('yellow')
camera.preview_fullscreen = True
# first: x, y, width, height
# camera.preview_window=(0, 0, 900, 1600)

############# Init
data = {}
data['bouton1']=False
data['bouton2']=False
data['bouton3']=False
data['bouton4']=False

first_button4 = False
button3_case = True
finalText = ""
count_notuse=0

############# Loop control
while True:

  time.sleep(0.2)

  etat_bouton_1 = GPIO.input(14)
  if etat_bouton_1 == False:
    print('bouton 1 appuye')
    finalText=""

  etat_bouton_2 = GPIO.input(23)
  if etat_bouton_2 == False:
    print('bouton 2 appuye')
    if first_button4 == False:
      camera.color_effects = (128,128)
    finalText=""

  etat_bouton_3 = GPIO.input(25)
  if etat_bouton_3 == False:
    print('bouton 3 appuye')
    finalText=""

  etat_bouton_4 = GPIO.input(16)
  if etat_bouton_4 == False:
    print('bouton 4 appuye')
     
    if first_button4 == False:
      first_button4 = True
      time.sleep(0.5)
    else:
      finalText= "Vive les maries !"
      first_button4 = False 

  else:
    if first_button4 == True:
      if etat_bouton_1 == False:
        finalText = "Une journee inoubliable !"
        first_button4 = False
      elif etat_bouton_2 == False:
        finalText = "Un souvenir du mariage"
        first_button4 = False
      elif etat_bouton_3 == False:
        finalText = "Merci la vie !"
        first_button4 = False
        button3_case = False



  if not etat_bouton_1 or not etat_bouton_2 or not etat_bouton_3 or not etat_bouton_4:
    count_notuse = 0
    data['bouton1']=etat_bouton_1
    data['bouton2']=etat_bouton_2
    data['bouton3']=etat_bouton_3
    data['bouton4']=etat_bouton_4
    data['diplay_texte']=first_button4
    data['type']='button_state'
    server.send_message_to_all(json.dumps(data))
    print(json.dumps(data))
  
    uncount = {}
    uncount['type']='countdown' 
  
    if first_button4 == False:
      camera.start_preview()

      bib.wait_display(server,camera,uncount, wait_time=3)
      camera.annotate_text = finalText

      print('cheese')

      name_alea = str(uuid.uuid4())
      raw_image = "/home/pi/Code/ui-photo/public/photos/test-" + name_alea + ".jpg"
      blank_image_path = "/home/pi/Code/ui-photo/public/mariages-background.jpg"
      camera.capture(raw_image)


      if not etat_bouton_3 and button3_case:

         img_width = 584
         img_height = 777

         # blank_image = Image.open(blank_image_path)
         blank_image = Image.new("RGB", (global_width, global_height), "white")
         source_image = Image.open(raw_image)
         source_image.thumbnail((img_width,img_height), Image.ANTIALIAS)

         bib.wait_display(server,camera,uncount, wait_time=2)
         camera.annotate_text = finalText

         raw_image_2 = "/home/pi/Code/ui-photo/public/photos/test-" + name_alea + "-2.jpg"
         camera.capture(raw_image_2)
         source_image_2 = Image.open(raw_image_2)
         source_image_2.thumbnail((img_width,img_height), Image.ANTIALIAS)

         bib.wait_display(server,camera,uncount, wait_time=2)
         camera.annotate_text = finalText
 
         raw_image_3 = "/home/pi/Code/ui-photo/public/photos/test-" + name_alea + "-3.jpg"
         camera.capture(raw_image_3)
         source_image_3 = Image.open(raw_image_3)
         source_image_3.thumbnail((img_width,img_height), Image.ANTIALIAS)

         bib.wait_display(server,camera,uncount, wait_time=2)
         camera.annotate_text = finalText

         raw_image_4 = "/home/pi/Code/ui-photo/public/photos/test-" + name_alea + "-4.jpg"
         camera.capture(raw_image_4)
         source_image_4 = Image.open(raw_image_4)
         source_image_4.thumbnail((img_width,img_height), Image.ANTIALIAS)

         size_h_1 = 100
         size_h_2 = 977
         size_w_1 = 100
         size_w_2 = 784
		 
         blank_image.paste(source_image,   (size_w_1, size_h_1))
         blank_image.paste(source_image_2, (size_w_2, size_h_1))
         blank_image.paste(source_image_3, (size_w_1, size_h_2))
         blank_image.paste(source_image_4, (size_w_2, size_h_2))
         blank_image.save(raw_image)
      else:			
          button3_case = True
        
      camera.stop_preview()
      camera.color_effects = None

      message = {} 
      message['photo_raw']="photos/test-"+name_alea + ".jpg"
      message['type']='image'
      server.send_message_to_all(json.dumps(message))
      print(json.dumps(message))
  else:
    count_notuse=count_notuse+1
    if count_notuse == 100:
      message = {} 
      message['photo_raw']="mariages-background.jpg"
      message['type']='image'
      server.send_message_to_all(json.dumps(message))
      
	  
