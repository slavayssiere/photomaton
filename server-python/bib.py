import json
import time

def wait_display(server, camera, uncount, wait_time=3):
  for num in range(wait_time, -1, -1):
    uncount['nb']=num
    camera.annotate_text = str(num)
    server.send_message_to_all(json.dumps(uncount)) 
    print(json.dumps(uncount))
    time.sleep(1)
