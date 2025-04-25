import openface
import facenet
import os
import pickle as pkl

# encoding the faces function:
def encode_faces(image_folder = 'faces'):
    known_encodings = []
    known_names = []
    for filename in os.listdir(image_folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(image_folder, filename)
            image = openface.__path__(image_path)
            encoding = openface.