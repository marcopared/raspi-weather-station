import cv2
import numpy as np

# Create a camera object
cap = cv2.VideoCapture(1)
# Create a window
cv2.namedWindow("Live Stream", cv2.WINDOW_NORMAL)

# Live stream, and capture an image if spacebar is pressed
while True:
    ret, frame = cap.read()
    cv2.imshow('Live Stream', frame)
    if cv2.waitKey(1) == ord(' '):
        cv2.imwrite("frame.jpg", frame)
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()

# Now, read the image
img = cv2.imread('frame.jpg') # Read an image

# Display the image
cv2.imshow('Image', img) # Display
cv2.waitKey(0) # wait until a key is pressed

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Display the grayscale image
cv2.imshow('Grayscale', gray)
cv2.waitKey(0)

# Perform Canny edge detection on the grayscale image
edges = cv2.Canny(gray, 100, 200)

# Display the edges
cv2.imshow('Edges', edges)
cv2.waitKey(0)

# Apply other kinds of filters
blur = cv2.GaussianBlur(img, (11, 11), 0)
cv2.imshow('Blur', blur)
cv2.waitKey(0)

sharpen = cv2.filter2D(img, -1, np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]))
cv2.imshow('Sharpen', sharpen)
cv2.waitKey(0)

###################################################################################

# Face detection using Haar cascades
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Detect faces
faces = face_cascade.detectMultiScale(gray, 1.1, 4)
img_faces = img.copy()

# Draw the faces on the original imIage
for (x, y, w, h) in faces:
    cv2.rectangle(img_faces, (x, y), (x+w, y+h), (255, 0, 0), 2)

# Display the image with faces
cv2.imshow('Faces', img_faces)
cv2.waitKey(0)

# Now, read the image
img = cv2.imread('frame.jpg') # Read an image

# Display the image
cv2.imshow('Image', img) # Display
cv2.waitKey(0) # wait until a key is pressed

# Using masks to find objects of a certain color:

# Convert image to HSV color space
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Define blue color range
lower_blue = np.array([100, 50, 50])
upper_blue = np.array([130, 255, 255])

# Create a mask of blue pixels in the image
mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Apply the mask to the original image to extract only blue objects
img_blue_objects = cv2.bitwise_and(img, img, mask=mask)

# Display the image with blue objects
cv2.imshow('Blue Objects', img_blue_objects)
cv2.waitKey(0)
