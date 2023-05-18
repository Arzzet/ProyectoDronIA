import cv2
import os
import numpy as np
import time
from mtcnn import MTCNN
import dlib

detector = MTCNN()

face_recognition_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

def load_users():
    users = {}
    for user_name in os.listdir("faces"):
        user_faces = []
        for face_image in os.listdir(f"faces/{user_name}"):
            image = cv2.imread(f"faces/{user_name}/{face_image}")
            face_locations = detector.detect_faces(image)

            if face_locations:
                x, y, w, h = face_locations[0]['box']
                face = image[y:y+h, x:x+w]
                face_rect = dlib.rectangle(x, y, x+w, y+h)
                face_shape = dlib.shape_predictor("shape_predictor_5_face_landmarks.dat")
                shape = face_shape(image, face_rect)
                face_encoding = face_recognition_model.compute_face_descriptor(image, shape)
                user_faces.append(face_encoding)

        users[user_name] = user_faces
    return users

def login(users):
    user_encodings = [encoding for encodings in users.values() for encoding in encodings]
    cap = cv2.VideoCapture(0)
    face_shape = dlib.shape_predictor("shape_predictor_5_face_landmarks.dat")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = detector.detect_faces(rgb_frame)
        face_encodings = []
        for face in face_locations:
            x, y, w, h = face['box']
            face_rect = dlib.rectangle(x, y, x+w, y+h)
            shape = face_shape(frame, face_rect)
            face_encoding = face_recognition_model.compute_face_descriptor(frame, shape)
            face_encodings.append(face_encoding)

        if face_encodings:
            for face_encoding in face_encodings:
                distances = np.array([np.linalg.norm(np.array(user_encoding) - np.array(face_encoding)) for user_encoding in user_encodings])
                min_distance_index = np.argmin(distances)
                if distances[min_distance_index] < 0.5:
                    matched_user_name = list(users.keys())[min_distance_index]
                    print(f"Bienvenido, {matched_user_name}")
                    return

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def register_user(user_name):
    detector = MTCNN()
    face_recognition_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")
    face_shape = dlib.shape_predictor("shape_predictor_5_face_landmarks.dat")

    cap = cv2.VideoCapture(0)

    os.makedirs(f"faces/{user_name}", exist_ok=True)

    print("Presiona 'c' para capturar la imagen y 'q' para salir.")
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = detector.detect_faces(rgb_frame)

        for face in face_locations:
            x, y, w, h = face['box']
            face_rect = dlib.rectangle(x, y, x+w, y+h)
            shape = face_shape(frame, face_rect)
            face_encoding = face_recognition_model.compute_face_descriptor(frame, shape)

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('c'):
            if face_locations:
                x, y, w, h = face_locations[0]['box']
                face_image = frame[y:y+h, x:x+w]
                face_image = cv2.resize(face_image, (128, 128))
                cv2.imwrite(f"faces/{user_name}/{int(time.time())}.jpg", face_image)
                print("Imagen capturada")

        elif cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    if not os.path.exists("faces"):
        os.makedirs("faces")

    while True:
        choice = input("¿Quieres registrarte (R) o iniciar sesión (L)? (Q para salir): ").lower()
        if choice == 'r':
            register_user()
        elif choice == 'q':
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    main()