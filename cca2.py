from skimage import measure
from skimage.measure import regionprops
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import localization

# this gets all the connected regions and groups them together
label_image = measure.label(localization.binary_car_image)

# getting the maximum width, height and minimum width and height that a license plate can be
plate_dimensions = (0.03*label_image.shape[0], 0.1*label_image.shape[0], 0.2*label_image.shape[1], 0.5*label_image.shape[1])
min_height, max_height, min_width, max_width = plate_dimensions
# print (plate_dimensions)
plate_objects_cordinates = []
plate_like_objects = []
fig, (ax1) = plt.subplots(1)
ax1.imshow(localization.gray_car_image, cmap="gray")

# regionprops creates a list of properties of all the labelled regions
for region in regionprops(label_image):
    min_row, min_col, max_row, max_col = region.bbox
    if region.area < 50:
        #if the region is so small then it's likely not a license plate
        continue
    # the bounding box coordinates
    region_height = max_row - min_row
    region_width = max_col - min_col
    # print (region_width, region_height)
    # ensuring that the region identified satisfies the condition of a typical license plate
    if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
        # print (region_height, region_width)
        plate_like_objects.append(localization.binary_car_image[min_row:max_row,
                                                                min_col:max_col])
        plate_objects_cordinates.append((min_row, min_col,
                                        max_row, max_col))
        rectBorder = patches.Rectangle((min_col, min_row), max_col-min_col, max_row-min_row, edgecolor="red", linewidth=2, fill=False)
        ax1.add_patch(rectBorder)
    # let's draw a red rectangle over those regions

plt.show()