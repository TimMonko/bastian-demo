# /// script
# dependencies = [
#   "napari[pyqt5,optional]",
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
downsample = 1

# Define datasets to load
datasets = [
    {
        'image_path': image_002,
        'label_path': label_002,
        'name': '002',
    },
    {
        'image_path': image_004,
        'label_path': label_004,
        'name': '004',
    },
]

# Plane orientations for orthogonal views
planes = [
    ('Z', (1, 0, 0)),
    ('Y', (0, 1, 0)),
    ('X', (0, 0, 1)),
]

# Adjust scale to account for downsampling
scale = (50*downsample, 5*downsample, 5*downsample)

viewer = napari.Viewer()

# Load and display each dataset
for dataset in datasets:
    # Load data once - all layers will share these array references
    img_data = imread(dataset['image_path'])[::downsample, ::downsample, ::downsample]
    lbl_data = imread(dataset['label_path'])[::downsample, ::downsample, ::downsample]
    
    # Add image layers with different plane orientations
    for plane_name, plane_normal in planes:
        viewer.add_image(
            img_data,
            name=f"{dataset['name']} {plane_name}",
            blending='translucent',
            scale=scale,
            depiction='plane',
            plane={'normal': plane_normal},
        )
    
    # Add labels layer
    lbl_layer = viewer.add_labels(
        lbl_data,
        name=f"{dataset['name']}",
        scale=scale,
        iso_gradient_mode='smooth',
    )
    lbl_layer.bounding_box.visible = True

viewer.scale_bar.visible = True
viewer.scale_bar.unit = "nm"

viewer.grid.stride = 4
viewer.grid.enabled = True

viewer.dims.ndisplay = 3

viewer.camera.angles = (-15, 63, 155)
viewer.camera.perspective = 60

if __name__ == "__main__":
    napari.run()