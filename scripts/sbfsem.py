# /// script
# dependencies = [
#   "napari[pyqt6,optional]",
#   "tifffile",
# ]
# ///

import napari
import pathlib
from tifffile import imread

# Data cache directory
data_dir = pathlib.Path(__file__).parent / 'data'
data_dir.mkdir(exist_ok=True)

image_002 = data_dir / "002_ROI2_Cropped.tif"
label_002 = data_dir / "002_ROI2_Cropped_Mito_Labels.tif"

image_004 = data_dir / "004_ROI2_Cropped.tif"
label_004 = data_dir / "004_ROI2_Cropped_Mito_Labels.tif"

# Downsample factor (1 = no downsampling, 2 = half resolution, etc.)
downsample = 2

# Load data once - all layers will share these array references
img_002_data = imread(image_002)[::downsample, ::downsample, ::downsample]
lbl_002_data = imread(label_002)[::downsample, ::downsample, ::downsample]
img_004_data = imread(image_004)[::downsample, ::downsample, ::downsample]
lbl_004_data = imread(label_004)[::downsample, ::downsample, ::downsample]

# Adjust scale to account for downsampling
scale = (50*downsample, 5*downsample, 5*downsample)

viewer = napari.Viewer()

# Add layers sharing the same data reference with plane settings
viewer.add_image(
    img_002_data,
    name="Image 002 Z",
    blending='translucent',
    scale=scale, 
    depiction='plane',
    plane={'normal': (1, 0, 0)},
)
viewer.add_image(
    img_002_data,
    name="Image 002 Y",
    blending='translucent',
    scale=scale,
    depiction='plane',
    plane={'normal': (0, 1, 0)}
)
viewer.add_image(
    img_002_data,
    name="Image 002 X",
    blending='translucent',
    scale=scale,
    depiction='plane',
    plane={'normal': (0, 0, 1)}
)
lbl002 = viewer.add_labels(
    lbl_002_data,
    name="Labels 002",
    scale=scale,
    iso_gradient_mode='smooth',
)

viewer.add_image(
    img_004_data,
    name="Image 004 Z",
    blending='translucent',
    scale=scale,
    depiction='plane',
    plane={'normal': (1, 0, 0)}
)
viewer.add_image(
    img_004_data,
    name="Image 004 Y",
    blending='translucent',
    scale=scale,
    depiction='plane',
    plane={'normal': (0, 1, 0)}
)
viewer.add_image(
    img_004_data,
    name="Image 004 X",
    blending='translucent',
    scale=scale,
    depiction='plane',
    plane={'normal': (0, 0, 1)}
)
lbl004 = viewer.add_labels(
    lbl_004_data,
    name="Labels 004",
    scale=scale,
    iso_gradient_mode='smooth',
)

lbl002.bounding_box.visible = True
lbl004.bounding_box.visible = True

viewer.scale_bar.visible = True
viewer.scale_bar.unit = "nm"

viewer.grid.stride = 4
viewer.grid.enabled = True

viewer.dims.ndisplay = 3
viewer.camera.angles = (-12, 57, 152)

if __name__ == "__main__":
    napari.run()