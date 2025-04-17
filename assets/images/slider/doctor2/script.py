import os
from PIL import Image
import argparse

def generate_responsive_images(input_image_path, output_folder, sizes):
    """
    Generate responsive images and return the srcset HTML code.
    
    :param input_image_path: Path to the original image file.
    :param output_folder: Folder to save the resized images.
    :param sizes: List of tuples containing (width, suffix) for each size.
    :return: HTML srcset code.
    """
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Extract the base name of the input file (without extension)
    base_name = os.path.splitext(os.path.basename(input_image_path))[0]
    
    # Open the original image
    img = Image.open(input_image_path)
    
    # Initialize the srcset strings
    webp_srcset = []
    jpeg_srcset = []
    
    # Generate resized images
    for width, suffix in sizes:
        # Resize the image while maintaining aspect ratio
        resized_img = img.resize((width, int(width * img.height / img.width)), Image.Resampling.LANCZOS)
        
        # Save as WebP
        webp_filename = f"{base_name}-{suffix}.webp"
        webp_path = os.path.join(output_folder, webp_filename)
        resized_img.save(webp_path, "WEBP", quality=85)
        webp_srcset.append(f"{webp_path} {width}w")
        
        # Save as JPEG
        jpeg_filename = f"{base_name}-{suffix}.jpeg"
        jpeg_path = os.path.join(output_folder, jpeg_filename)
        resized_img.convert("RGB").save(jpeg_path, "JPEG", quality=85)
        jpeg_srcset.append(f"{jpeg_path} {width}w")
    
    # Generate HTML code for srcset
    html_code = f"""
<picture>
    <source 
        srcset="{', '.join(webp_srcset)}" 
        type="image/webp"
        sizes="(max-width: 600px) 480px, (max-width: 900px) 800px, 1200px"
    >
    <source 
        srcset="{', '.join(jpeg_srcset)}" 
        type="image/jpeg"
        sizes="(max-width: 600px) 480px, (max-width: 900px) 800px, 1200px"
    >
    <img 
        src="{os.path.join(output_folder, f'{base_name}-large.jpeg')}" 
        alt="Responsive Image"
        class="w-48 h-48 rounded-full object-cover shadow-lg"
        loading="lazy"
    >
</picture>
"""
    return html_code


def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Generate responsive images and srcset HTML code.")
    parser.add_argument("input_link", help="Path to the original image file.")
    parser.add_argument("output_link", help="Folder to save the resized images.")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Define the sizes for srcset
    sizes = [
        (480, "small"),
        (800, "medium"),
        (1200, "large")
    ]
    
    # Generate responsive images and get the HTML code
    try:
        html_output = generate_responsive_images(args.input_link, args.output_link, sizes)
        print("\nGenerated HTML Code:")
        print(html_output)
        print("\nImages have been successfully saved to the output folder.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()