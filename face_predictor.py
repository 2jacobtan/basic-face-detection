#Using Python 3.6.9 64-bit, on Windows 10

import sys
import requests
import numpy as np
import cv2
import json
#import re

# Display a cv2 image
def show_image(image, name="image"):
  cv2.imshow(name,image)
def close_images():
  cv2.waitKey(0)
  cv2.destroyAllWindows()

# Get the image url
if len(sys.argv) == 2:
  access_token = sys.argv[1]
else:
  access_token = "a39a2418dfeec087"
  print(f"No token given. Using default token: {access_token}")
url_request = requests.get('https://hackattic.com/challenges/basic_face_detection/problem?access_token='+access_token)
data = url_request.text

# # Used regex for fun… could just use json package
# url_match = re.match(r".+: \"(.+)\"",data) 
# url = url_match.group(1)

# Replaced above regex version with this json version
url = json.loads(data)["image_url"]

# Load image to cv2
image_request = requests.get(url,stream=True)
image_raw = image_request.raw
image = np.asarray(bytearray(image_raw.read()), dtype="uint8")
image = cv2.imdecode(image, cv2.IMREAD_COLOR)

#show_image(image)

# Convert image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

images = tuple(
  tuple(gray[i*100:i*100+100,j*100:j*100+100] for j in range(8))
    for i in range(8)
)

# #To test that images are correctly loaded and indexed
# for i in range(8):
#   for j in range(8):
#     show_image(images[i][j],f"{i}{j}")


# Set up face detection function
cascPath = "haarcascade_frontalface_default.xml"
## Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)
## Face detection function. Returns True if face is detected
def detect_face(img, index: str = "99") -> bool:
  faces = faceCascade.detectMultiScale(
      img,
      scaleFactor=1.1,
      minNeighbors=5,
      minSize=(30, 30),
      #flags = cv2.CV_HAAR_SCALE_IMAGE
  )
  num_faces_found = len(faces)
  #print(f"{i}{j} found {num_faces_found} faces!")

  # Draw a rectangle around the faces
  x_offset = int(index[1])*100
  y_offset = int(index[0])*100
  for (x, y, w, h) in faces:
    x+=x_offset
    y+=y_offset
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

  return True if num_faces_found >= 1 else False

detected_faces = []

for i in range(8):
  for j in range(8):
    if detect_face(images[i][j],str(i)+str(j)):
      detected_faces.append([i,j])

# for index in detected_faces:
#   print(index)

system_output = f'{{"face_tiles": {detected_faces}}}'
sys.stdout.write(system_output)

# # check that output is valid JSON
# print("\n")
# print(json.loads(system_output)["face_tiles"])

show_image(image, "after detection")

close_images()