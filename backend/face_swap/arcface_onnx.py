from __future__ import division
import numpy as np
import cv2
import onnx
import onnxruntime
import os
from face_swap.face_align import norm_crop
from config import SESSION_OPTIONS
class ArcFaceONNX:
    def __init__(self, model_file=None, session=None, providers=None):
        assert model_file is not None, "Model file path is None."
        self.model_file = model_file
        self.session = session
        self.taskname = 'recognition'

        if providers is None:
            providers = [("CUDAExecutionProvider")]

        model = onnx.load(self.model_file)
        graph = model.graph
        find_sub = any(node.name.startswith('Sub') for node in graph.node[:8])
        find_mul = any(node.name.startswith('Mul') for node in graph.node[:8])
        self.input_mean = 0.0 if find_sub and find_mul else 127.5
        self.input_std = 1.0 if find_sub and find_mul else 127.5

        if self.session is None:
            assert os.path.exists(self.model_file), "ArcFace weights not found."
            self.session = onnxruntime.InferenceSession(self.model_file, sess_options=SESSION_OPTIONS, providers=providers)

        input_cfg = self.session.get_inputs()[0]
        self.input_size = tuple(input_cfg.shape[2:4][::-1])
        self.input_name = input_cfg.name
        self.output_names = [out.name for out in self.session.get_outputs()]

    def get(self, img, face):
        aimg = norm_crop(img, landmark=face.kps, image_size=self.input_size[0])
        face.embedding = self.get_feat(aimg).flatten()
        return face.embedding

    def get_feat(self, imgs):
        if not isinstance(imgs, list):
            imgs = [imgs]
        blob = cv2.dnn.blobFromImages(imgs, 1.0 / self.input_std, self.input_size,
                                      (self.input_mean, self.input_mean, self.input_mean), swapRB=True)
        return self.session.run(self.output_names, {self.input_name: blob})[0]

    def batch_get(self, img, faces, batch_size=32):
        all_embeddings = []
        for i in range(0, len(faces), batch_size):
            batch_faces = faces[i:i + batch_size]
            all_aimg = [
                norm_crop(img, landmark=face.kps, image_size=self.input_size[0]) 
                for face in batch_faces
            ]
            blob = cv2.dnn.blobFromImages(
                all_aimg, 1.0 / self.input_std, self.input_size,
                (self.input_mean, self.input_mean, self.input_mean), swapRB=True
            )
            net_out = self.session.run(self.output_names, {self.input_name: blob})
            all_embeddings.extend(net_out)
        return np.array(all_embeddings)
