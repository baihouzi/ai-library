import os
import pickle

import face_recognition
import cv2
import numpy as np

from const import *


def snapshot(face_db):
    snap_path = os.path.join(STATIC_PATH, 'snap.png')

    if os.path.exists(snap_path):
        os.remove(snap_path)

    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()

    if ret:
        cv2.imwrite(snap_path, frame)
        video_capture.release()

        encs = face_db._calc_encoding(frame)

        if len(encs) > 0:
            return snap_path
        else:
            return None


def clear_snapshot():
    snap_path = os.path.join(STATIC_PATH, 'snap.png')

    if os.path.exists(snap_path):
        os.remove(snap_path)


class FaceDB:
    def __init__(self, encoding_path, sync_keys=None):
        self.encoding_path = encoding_path
        self.db = {}

        self.load_db()

        if sync_keys is not None:
            db_dict = {}

            for k in sync_keys:
                db_dict[k] = self.db[k]

            self.db = db_dict
            self.save_db()

    def save_db(self):
        save_dict = {}

        for k, v in self.db.items():
            arr = v.tolist()
            save_dict[k] = arr

        with open(self.encoding_path, 'wb') as file:
            pickle.dump(save_dict, file)

    def load_db(self):
        if os.path.exists(self.encoding_path):
            with open(self.encoding_path, 'rb') as file:
                load_dict = pickle.load(file)

                for k, v in load_dict.items():
                    ndarr = np.array(v)
                    self.db[k] = ndarr

    def add_encoding(self, key, encoding):
        self.db[key] = encoding
        self.save_db()

    def del_encoding(self, key):
        self.db.pop(key)
        self.save_db()

    def update_encoding(self, key, encoding):
        self.db[key] = encoding
        self.save_db()

    def query_encoding(self, key):
        return self.db[key]

    def compare_face(self, img):
        known_ids = list(self.db.keys())
        known_encodings = list(self.db.values())
        match_id = -1

        my_enc = self._calc_encoding(img)[0]
        matches = face_recognition.compare_faces(known_encodings, my_enc)

        if True in matches:
            match_index = matches.index(True)
            match_id = known_ids[match_index]

        return match_id

    def register_face(self, key, img):
        # TODO : what if there's no face?
        my_enc = self._calc_encoding(img)[0]
        self.add_encoding(key, my_enc)

    def register_face_from_snapshot(self, key):
        img = cv2.imread(os.path.join(STATIC_PATH, 'snap.png'))
        my_enc = self._calc_encoding(img)[0]
        self.add_encoding(key, my_enc)

    def _calc_encoding(self, img):
        small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)

        return face_encodings


if __name__ == '__main__':
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()

    if ret:
        encodings = calc_encoding(frame)
        print(encodings)
