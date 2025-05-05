import cv2
import numpy as np
import os

# Define file paths
image_path = "logo.jpg"
mask_path = "_mask-bg.png"
output_path = "logo_transparent_expanded.png"

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
mask_gray = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
if mask_gray is None:
    print(f"Error: Could not load mask from {mask_path}")
    exit()

# Check if dimensions match
if img.shape[:2] != mask_gray.shape[:2]:
    print(f"Error: Image dimensions {img.shape[:2]} and mask dimensions {mask_gray.shape[:2]} do not match.")
    exit()

# Threshold the mask to make it purely black and white
# Assuming the logo area in the mask is lighter (closer to 255)
_, mask_binary = cv2.threshold(mask_gray, 128, 255, cv2.THRESH_BINARY)

# Define a kernel for dilation (e.g., a 7x7 circle for ~3 pixel radius)
kernel_size = 7
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))

# Dilate the white areas (logo) of the binary mask
dilated_mask = cv2.dilate(mask_binary, kernel, iterations=1)

# Convert the image to BGRA (adding an alpha channel)
bgra = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

# Assign the *dilated* mask to the alpha channel
# Assumes mask uses 255 for opaque and 0 for transparent
bgra[:, :, 3] = dilated_mask

# Save the result as PNG
cv2.imwrite(output_path, bgra)

print(f"Successfully created transparent image with expanded white border: {output_path}")

# Optional: Display the result (requires matplotlib)
# try:
#     from matplotlib import pyplot as plt
#     # Display the original mask, thresholded mask, dilated mask, and final result for comparison
#     fig, axs = plt.subplots(1, 4, figsize=(20, 5))
#     axs[0].imshow(mask_gray, cmap='gray')
#     axs[0].set_title('Original Mask')
#     axs[0].axis('off')
#     axs[1].imshow(mask_binary, cmap='gray')
#     axs[1].set_title('Thresholded Mask')
#     axs[1].axis('off')
#     axs[2].imshow(dilated_mask, cmap='gray')
#     axs[2].set_title('Dilated Mask')
#     axs[2].axis('off')
#     axs[3].imshow(cv2.cvtColor(bgra, cv2.COLOR_BGRA2RGBA)) # Convert BGRA to RGBA for display
#     axs[3].set_title('Result with Transparency')
#     axs[3].axis('off')
#     plt.tight_layout()
#     plt.show()
# except ImportError:
#     print("Matplotlib not installed, skipping display.")
# except Exception as e:
#      print(f"An error occurred during display: {e}") 