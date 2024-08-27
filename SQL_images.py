import cv2
import numpy as np

# Load the image (convert to grayscale for edge detection)
image = cv2.imread('path to image', cv2.IMREAD_GRAYSCALE)

# Detect edges using Canny edge detection
edges = cv2.Canny(image, 100, 200)

# Find contours (edges) in the image
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Get image height for flipping y-coordinates
image_height = image.shape[0]

# Prepare MULTIPOLYGON SQL command
multipolygon_parts = []

# Iterate over each contour to form polygons
for contour in contours:
    points = []
    for point in contour:
        x, y = point[0]
        # Flip the y-coordinate
        flipped_y = image_height - y
        points.append(f"{x} {flipped_y}")
    
    # Ensure the polygon is closed by adding the first point at the end
    if len(points) >= 3:
        points.append(points[0])
        points_text = ", ".join(points)
        multipolygon_parts.append(f"(({points_text}))")

# Only generate SQL if we have valid polygons
if multipolygon_parts:
    multipolygon_text = ", ".join(multipolygon_parts)
    sql_command = f"DECLARE @multiPolygon GEOMETRY;\nSET @multiPolygon = GEOMETRY::STMPolyFromText('MULTIPOLYGON({multipolygon_text})', 0);\nSELECT @multiPolygon;"
    print(sql_command)
else:
    print("No valid polygons were detected to form a MULTIPOLYGON.")
