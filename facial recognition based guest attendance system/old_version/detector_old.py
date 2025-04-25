import numpy as np
import pandas as pd
import os
import cv2
import time
from datetime import datetime
from imutils.video import VideoStream
import retinaface
import retinaface.model
import retinaface.model.retinaface_model


# load the serialized face detection models
print(" Loading the model for facial recognition...")
net = cv2.dnn.readNetFromCaffe('-- # disk location address')

# load known faces from the known library:
def identified_faces(known_face_dir = "Identified_faces"):
    known_face_encodings = []
    known_face_names = []

    for image_name in os.listdir(known_face_dir):
        image_path = os.path.join(known_face_dir, image_name)
        img = retinaface.__path__(image_path)
        img_encoding = retinaface.model.retinaface_model(img)

        if len(img_encoding) > 0:
            img_encoding = img_encoding[0]
            known_face_encodings.append(img_encoding)
            known_face_names.append(os.path.splitext(image_name)[0])
        else:
            print(f"Warning: No face found in {image_name}. Skipping this image.")
    
    return known_face_encodings, known_face_names

# marking attendance:
def attendance_marking(name):
    now = datetime.now()
    dt_string = now.strftime('%Y-%m-%d %H:%M:%S')

    file_name = 'attendance.csv'
    if os.path.exists(file_name):
        attendance = pd.read_csv(file_name)
    else:
        attendance = pd.read_csv(columns = ["Name", "Time"])
    
    if name not in attendance["Name"].values:
        new_entry = pd.DataFrame([[name, dt_string]], columns=['Name', 'Time'])
        attendance = pd.concat([attendance, new_entry], ignore_index=True)
        attendance.to_csv(file_name, index=False)
        print(f"{name}'s attendance marked at {dt_string}.")

# initialize the viseo stream
print("Starting Video Strem...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

# load known faces for recognition:
known_face_encodings, known_face_names = identified_faces()

# loop over the frames from the video stream:
while True:
    # grab the frame from threaded video stream
    frame = vs.read()

    if frame is None:
        print("Failed to capture frame from camera. Exiting...")
        break

    # Grab the frame dimensions and convert it to a blob
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, 
                                 (300, 300), (104.0, 177.0, 123.0))

    # Pass the blob through the network and obtain detections
    net.setInput(blob)
    detections = net.forward()

     # Loop over the detections
    for i in range(0, detections.shape[2]):
        # Extract the confidence associated with the prediction
        confidence = detections[0, 0, i, 2]

        # Filter out weak detections by ensuring the confidence is above a threshold
        if confidence > 0.5:
            # Compute the (x, y)-coordinates of the bounding box for the object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # Check if the bounding box has valid dimensions
            if startX < 0 or startY < 0 or endX > w or endY > h:
                continue  # Skip if the bounding box is invalid

            # Extract the face ROI
            face = frame[startY:endY, startX:endX]

            # Ensure the face region is not empty
            if face.size == 0:
                continue

            # Convert the face to RGB for face recognition
            rgb_face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            
            # Resize and encode the face
            face_encoding = retinaface.model.retinaface_model(rgb_face)

            if len(face_encoding) > 0:
                face_encoding = face_encoding[0]
                
                # Compare face to known faces
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    attendance_marking(name)

                    # Draw a bounding box and label with the name
                    text = f"{name}: {confidence*100:.2f}%"
                    y = startY - 10 if startY - 10 > 10 else startY + 10
                    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                    cv2.putText(frame, text, (startX, y), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

    # Show the output frame
    cv2.imshow("Attendance System", frame)
    key = cv2.waitKey(1) & 0xFF

    # break from the loop if the 'q' key was pressed
    if key == ord("q"):
        break

# clean up
cv2.destroyAllWindows()
vs.stop()

