import os
import cv2
import numpy as np
import pandas as pd

# Directory containing images
image_dir = './data/rgb'
output_csv = 'snr_data.csv'

# Define the window coordinates (top-left corner and size)
window_x, window_y = 512, 512  # Starting point of the window
window_size = 128

# Initialize lists to store data
image_names = []
average_values = []
std_devs = []

# Read all image filenames in the directory
image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpeg')]

# List to store the pixel values from the window for each image
pixel_data = []

for image_file in image_files:
    # Full path to the image
    image_path = os.path.join(image_dir, image_file)

    # Read the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Convert to grayscale
    if image is None:
        print(f"Failed to read image: {image_file}")
        continue

    # Extract the window
    window = image[window_y:window_y + window_size, window_x:window_x + window_size]

    # Compute statistics for the window
    avg_value = np.mean(window)
    std_dev = np.std(window)

    # Append data to lists
    image_names.append(image_file)
    average_values.append(avg_value)
    std_devs.append(std_dev)

    # Store pixel values for SNR computation
    pixel_data.append(window.flatten())

# Compute the aggregated SNR for the device
aggregate_signal = np.mean(average_values)  # Average of all mean values
aggregate_noise = np.sqrt(np.mean(np.array(std_devs) ** 2))  # RMS of standard deviations

# Compute SNR and SNR in dB
snr = aggregate_signal / (aggregate_noise + 1e-10)  # Avoid division by zero
snr_db = 20 * np.log10(snr)

# Save results to CSV
data = {
    'Image Name': image_names,
    'Average Value': average_values,
    'Standard Deviation': std_devs,
}

# Save individual image data
df = pd.DataFrame(data)
df.to_csv(output_csv, index=False)

# Save the aggregated SNR results
aggregated_results = {
    'Aggregate Signal': [aggregate_signal],
    'Aggregate Noise': [aggregate_noise],
    'SNR': [snr],
    'SNR (dB)': [snr_db]
}
aggr_df = pd.DataFrame(aggregated_results)
aggr_df.to_csv('aggregated_snr.csv', index=False)

print(f"Results saved to {output_csv} and aggregated SNR to aggregated_snr.csv.")
