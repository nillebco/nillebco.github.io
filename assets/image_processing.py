import cv2
import numpy as np
from matplotlib import pyplot as plt


def reduce_background_contrast(image_path, output_path, custom_mask_path=None, save_mask_to_file=False):
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB
    
    if custom_mask_path is None:
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Apply threshold to detect the bird (assumption: bird is high contrast)
        _, mask = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Invert mask so the bird remains unchanged
        mask = cv2.bitwise_not(mask)

        if save_mask_to_file:
            cv2.imwrite(output_path.replace(".jpg", "_mask.png"), mask)
    else:
        # Use the provided mask
        mask = cv2.imread(custom_mask_path, cv2.IMREAD_UNCHANGED)
        
        # Ensure mask has the same dimensions as the image
        if mask.shape[:2] != image.shape[:2]:
            raise ValueError("Custom mask dimensions must match image dimensions")
        
        # Ensure mask is binary (0 or 255)
        if mask.dtype != np.uint8:
            mask = mask.astype(np.uint8) * 255
    
    # Create a blurred version of the image to reduce contrast
    blurred = cv2.GaussianBlur(image, (1005, 1005), 10000)
    
    # Blend the original image and the blurred image based on the mask
    result = np.where(mask[:, :, None] == 255, image, blurred)
    
    # Save the result
    result_image = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_path, result_image)
    
    # Display the original image, mask, and result
    plt.figure(figsize=(15, 5))
    
    plt.subplot(131)
    plt.imshow(image)
    plt.title('Original Image')
    plt.axis('off')
    
    plt.subplot(132)
    plt.imshow(mask, cmap='gray')
    plt.title('Mask (White = Unchanged)')
    plt.axis('off')
    
    plt.subplot(133)
    plt.imshow(result)
    plt.title('Result')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()

# Example usage
input_image_path = "logo.jpg"
output_image_path = "logo_reduced.jpg"
custom_mask_path = "inversed_mask.png"

reduce_background_contrast(input_image_path, output_image_path, custom_mask_path, save_mask_to_file=True)
