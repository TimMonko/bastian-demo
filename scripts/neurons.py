# /// script
# dependencies = [
#   "napari[pyqt6,optional]",
#   "ndevio",
#   "bioio-czi",
#   "napari-ndev"
# ]
# ///

from tifffile import imread
import pathlib
import napari
import numpy as np
import re
from ndevio import nImage
from napari.settings import get_settings

settings = get_settings()
settings.application.playback_fps = 1

# read all images in the labels folder and stack them
data_dir = pathlib.Path(__file__).parent / 'labels'
label_files = sorted(data_dir.glob('*.tiff'))
image_file = pathlib.Path(r"C:\Users\timmo\Documents\GitHub\BastianLab\Ferritin_NCOA4-Phalloidin\Raw_Images\2024-08-07 25x 48HIC NCOA4 647 FT 568 PHALL 488 DAPI OBL.czi")

labels = [nImage(f) for f in label_files[:]]

scale = (labels[0].scale.Y, labels[0].scale.X)

image = nImage(image_file)
print(image.channel_names)

# labels[0].get_image_data(C=0)
DAPI_list = []
FTN_list = []
NCOA4_list = []
PHALL_list = []

DAPI_img_list = []
FTN_img_list = []
NCOA4_img_list = []
PHALL_img_list = []

for lbl in labels:
    # Extract scene name from label filename (pattern before .ome.tiff)
    match = re.search(r'(P\d+-[A-H]\d+)\.ome\.tiff$', lbl.path.name)

    scene = match.group(1)

    # Get label data
    DAPI = lbl.get_image_data('YX', C=0)
    FTN = lbl.get_image_data('YX', C=1)
    NCOA4 = lbl.get_image_data('YX', C=2)
    PHALL = lbl.get_image_data('YX', C=3)

    DAPI_list.append(DAPI)
    FTN_list.append(FTN)
    NCOA4_list.append(NCOA4)
    PHALL_list.append(PHALL)

    image.set_scene(scene)
    DAPI_img_list.append(image.get_image_data('YX', C=3))
    FTN_img_list.append(image.get_image_data('YX', C=1))
    NCOA4_img_list.append(image.get_image_data('YX', C=0))
    PHALL_img_list.append(image.get_image_data('YX', C=2))

DAPI_stack = np.stack(DAPI_list, axis=0)
FTN_stack = np.stack(FTN_list, axis=0)
NCOA4_stack = np.stack(NCOA4_list, axis=0)
PHALL_stack = np.stack(PHALL_list, axis=0)

DAPI_img_stack = np.stack(DAPI_img_list, axis=0)
FTN_img_stack = np.stack(FTN_img_list, axis=0)
NCOA4_img_stack = np.stack(NCOA4_img_list, axis=0)
PHALL_img_stack = np.stack(PHALL_img_list, axis=0)

viewer = napari.Viewer()
viewer.add_image(
    DAPI_img_stack,
    name='DAPI Image',
    scale=scale,
    colormap='cyan',
)
viewer.add_image(
    FTN_img_stack,
    name='FTN Image',
    scale=scale,
    colormap='magenta',
    blending='additive',
    contrast_limits=(230, 13000)
)
viewer.add_image(
    NCOA4_img_stack,
    name='NCOA4 Image',
    scale=scale,
    colormap='yellow',
    blending='additive',
    contrast_limits=(1300, 3400),
)
viewer.add_image(
    PHALL_img_stack,
    name='PHALL Image',
    scale=scale,
    colormap='grey',
    blending='additive',
    contrast_limits=(700, 4300)
)
viewer.add_image(
    DAPI_stack,
    name='DAPI Label',
    scale=scale,
    colormap='cyan',
    blending='additive',
    contrast_limits=(0, 1)
)
viewer.add_image(
    FTN_stack,
    name='FTN Label',
    scale=scale,
    colormap='magenta',
    blending='additive',
    contrast_limits=(0, 1)
)
viewer.add_image(
    NCOA4_stack,
    name='NCOA4 Label',
    scale=scale,
    colormap='yellow',
    blending='additive',
    contrast_limits=(0, 1)
)
viewer.add_image(
    PHALL_stack,
    name='PHALL Label',
    scale=scale,
    colormap='purple',
    blending='additive',
    contrast_limits=(0, 1)
)

viewer.grid.enabled = True
viewer.grid.stride = 4
viewer.scale_bar.visible = True
viewer.scale_bar.unit = "µm"
# viewer.window.add_plugin_dock_widget('napari-ndev', 'nDev App')

if __name__ == "__main__":
    napari.run()