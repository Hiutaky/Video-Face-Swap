import os
import onnxruntime


UPLOAD_FOLDER = "./uploaded_videos"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


BASE_DIR = os.path.abspath(UPLOAD_FOLDER)


RETINAFACE_MODEL_PATH = "./face_swap/weights/det_10g.onnx"
ARCFACE_MODEL_PATH = "./face_swap/weights/w600k_r50.onnx"
FACE_SWAPPER_MODEL_PATH = "./face_swap/weights/inswapper_128.onnx"
FACE_ENHANCER_MODEL_PATH = './face_swap/weights/gfpgan_1.4.onnx'


PROVIDERS = [("CUDAExecutionProvider"), "CPUExecutionProvider"]


SESSION_OPTIONS = onnxruntime.SessionOptions()
SESSION_OPTIONS.enable_mem_pattern = True
SESSION_OPTIONS.enable_profiling = False
SESSION_OPTIONS.enable_cpu_mem_arena = False
SESSION_OPTIONS.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_EXTENDED