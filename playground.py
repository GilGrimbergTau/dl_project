import json

def process_pixel_stats(file_path):

    with open(file_path, 'r') as f:
        dataset_cloud_stats = json.load(f)

# Initialize counters and sums
    zero_pixel_sections_count = 0
    ones_pixel_sections_count = 0
    total_pixels_not_zero_sum = 0
    total_pixels_zero_sum = 0
    ground_images_count = 0
    cloudy_images_count = 0

    # Iterate through each section in the JSON
    for section_name, stats in dataset_cloud_stats.items():
        not_zero = stats.get("total_pixels_not_zero", 0)
        is_zero = stats.get("total_pixels_zero", 0)
        ground_images = stats.get("ground_images_count", 0)
        cloudy_images = stats.get("cloudy_images_count", 0)

        # 1. Count sections where total_pixels_not_zero is 0
        if not_zero == 0 and is_zero > 0:
            zero_pixel_sections_count += 1
        elif not_zero > 0:
            ones_pixel_sections_count += 1


        ground_images_count += ground_images
        cloudy_images_count += cloudy_images

        # 2. Accumulate total sum of non-zero pixels
        total_pixels_not_zero_sum += not_zero

        # 3. Accumulate total sum of zero pixels
        total_pixels_zero_sum += is_zero

    # Output the results
    print(f"Number of sections where without clouds: {zero_pixel_sections_count}")
    print(f"Number of sections where with clouds: {ones_pixel_sections_count}")
    print(f"Total ground images count: {ground_images_count}")
    print(f"Total cloudy images count: {cloudy_images_count}")
    print(f"Total sum of clouds: {total_pixels_not_zero_sum}")
    print(f"Total sum of background: {total_pixels_zero_sum}")
    print(f"Cloud percentage: {total_pixels_not_zero_sum / (total_pixels_not_zero_sum + total_pixels_zero_sum) * 100:.2f}%")

# Run the function
if __name__ == "__main__":
    process_pixel_stats("/opt/DL_project/raw_dataset/dataset_cloud_stats.json")