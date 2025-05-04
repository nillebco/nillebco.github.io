import cv2
import numpy as np
import os

# Define file paths
image_path = "logo.jpg"
mask_path = "_mask-bg.png"
output_path = "logo_transparent.png"

# Check if input files exist
if not os.path.exists(image_path):
    print(f"Error: Image file not found at {image_path}")
    exit()
if not os.path.exists(mask_path):
    print(f"Error: Mask file not found at {mask_path}")
    exit()

# Load the original image (ensure it's read in color)
img = cv2.imread(image_path, cv2.IMREAD_COLOR)
if img is None:
    print(f"Error: Could not load image from {image_path}")
    exit()

# Load the mask as grayscale
mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
if mask is None:
    print(f"Error: Could not load mask from {mask_path}")
    exit()

# Check if dimensions match
if img.shape[:2] != mask.shape[:2]:
    print(f"Error: Image dimensions {img.shape[:2]} and mask dimensions {mask.shape[:2]} do not match.")
    exit()

# Convert the image to BGRA (adding an alpha channel)
bgra = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

# Assign the mask to the alpha channel
# Assumes mask uses 255 for opaque and 0 for transparent
bgra[:, :, 3] = mask

# Save the result as PNG
cv2.imwrite(output_path, bgra)

print(f"Successfully created transparent image: {output_path}")

# Optional: Display the result (requires matplotlib)
# try:
#     from matplotlib import pyplot as plt
#     plt.imshow(cv2.cvtColor(bgra, cv2.COLOR_BGRA2RGBA)) # Convert BGRA to RGBA for display
#     plt.title('Result with Transparency')
#     plt.axis('off')
#     plt.show()
# except ImportError:
#     print("Matplotlib not installed, skipping display.") 