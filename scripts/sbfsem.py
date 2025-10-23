# /// script
# dependencies = [
#   "napari[pyqt6,optional]",
# ]
# ///

import napari
import pathlib

# Data cache directory
data_dir = pathlib.Path(__file__).parent / 'data'
data_dir.mkdir(exist_ok=True)

image_002 = data_dir / "002_ROI2_Cropped.tif"
label_002 = data_dir / "002_ROI2_Cropped_Mito_Labels.tif"

image_004 = data_dir / "004_ROI2_Cropped.tif"
label_004 = data_dir / "004_ROI2_Cropped_Mito_Labels.tif"

viewer = napari.Viewer()

viewer.open(image_002, name="Image 002 Z", scale=(50,5,5))
viewer.open(image_002, name="Image 002 Y", scale=(50,5,5))
viewer.open(image_002, name="Image 002 X", scale=(50,5,5))
viewer.open(label_002, name="Labels 002", scale=(50,5,5), dtype="uint16")

viewer.open(image_004, name="Image 004 Z", scale=(50,5,5))
viewer.open(image_004, name="Image 004 Y", scale=(50,5,5))
viewer.open(image_004, name="Image 004 X", scale=(50,5,5))
viewer.open(label_004, name="Labels 004", scale=(50,5,5), dtype="uint16")

l0 = viewer.layers[0]
l0.depiction = 'plane'
l0.plane.normal = (1,0,0)
l1 = viewer.layers[1]
l1.depiction = 'plane'
l1.plane.normal = (0,1,0)
l2 = viewer.layers[2]
l2.depiction = 'plane'
l2.plane.normal = (0,0,1)

l4 = viewer.layers[4]
l4.depiction = 'plane'
l4.plane.normal = (1,0,0)
l5 = viewer.layers[5]
l5.depiction = 'plane'
l5.plane.normal = (0,1,0)
l6 = viewer.layers[6]
l6.depiction = 'plane'
l6.plane.normal = (0,0,1)

viewer.scale_bar.visible = True
viewer.scale_bar.unit = "nm"

viewer.grid.stride = 4
viewer.grid.enabled = True

viewer.dims.ndisplay = 3
viewer.camera.angles = (-20, 60, 145)


if __name__ == "__main__":
    napari.run()