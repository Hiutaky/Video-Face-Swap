from face_swap.refiner import generate_preview_and_gif
from config import UPLOAD_FOLDER
import os 
path = os.path.join(UPLOAD_FOLDER, '8290b1dd-23f1-40a5-9fba-7a47b5c1c3bd')
file = os.path.join(path,  'result.mp4')
generate_preview_and_gif(
    file,
    path
)