import os
import openai
from PIL import Image, ImageFilter
from io import BytesIO
import requests
import os

# Set API key
openai.api_key = os.getenv('OPENAI_KEY')

# Function to generate an image using DALL-E
def generate_image(prompt1):
    print(f"Generating an image for the prompt: {prompt1}")
    
    # Call DALL-E API to generate an image
    response = openai.Image.create(
        prompt=prompt1,
        n=1,
        size="256x256"
    )

    # Extract the image URL from the response
    image_url = response['data'][0]['url']

    # Download and save the generated image
    img_data = requests.get(image_url).content
    with open('image_created.png', 'wb') as handler:
        handler.write(img_data)

    print("Your image was generated and saved as `image_created.png`.")

# Function to create variations of an existing image using DALL-E
def create_variations(img_path):
    print("Creating variations of the image...")
    
    # Call DALL-E API to create variations of the input image
    with open(img_path, 'rb') as img_file:
        response = openai.Image.create_variation(
            image=img_file,
            n=1,
            size="256x256"
        )

    # Extract the URL of the created variation image
    image_url = response['data'][0]['url']

    # Download and save the created variation image
    img_data = requests.get(image_url).content
    with open('image_var.png', 'wb') as handler:
        handler.write(img_data)

    print("Your image variation was generated and saved as `image_var.png`.")

# Function to resize an image to user-specified dimensions
def resize_image(image_path):
    with Image.open(image_path) as img:
        print("Choose a dimension for resizing the image:")
        print("1. 256x256")
        print("2. 512x512")
        print("3. 1024x1024")
        option = input("Enter your option: ")
        if option == "1":
            target_size = (256, 256)
        elif option == "2":
            target_size = (512, 512)
        elif option == "3":
            target_size = (1024, 1024)
        else:
            print("Invalid option. Using default size 256x256.")
            target_size = (256, 256)

        # Resize the image
        resized_img = img.resize(target_size)

        # Save the resized image
        resized_img.save('resized_image.png')

    print("Your given image was resized and saved under `resized_image.png`")

# Function to apply filters to an image using PIL
def apply_filters(image_path):
    with Image.open(image_path) as img:
        print("Choose a filter to apply on the image:")
        print("1. Contour")
        print("2. Edge Enhance")
        print("3. Find Edges")
        print("4. Gaussian Blur")
        option = input("Enter your option: ")

        if option == "1":
            filtered_img = img.filter(ImageFilter.CONTOUR)
        elif option == "2":
            filtered_img = img.filter(ImageFilter.EDGE_ENHANCE)
        elif option == "3":
            filtered_img = img.filter(ImageFilter.FIND_EDGES)
        elif option == "4":
            filtered_img = img.filter(ImageFilter.GaussianBlur(radius=5))
        else:
            print("Invalid option. Applying Contour filter by default.")
            filtered_img = img.filter(ImageFilter.CONTOUR)
        
        # Save the filtered image
        filtered_img.save('filtered_image.png')
        print("Filter applied successfully, 'filtered_image.png' created.")

def list_directory_files():
    files = os.listdir()
    print("Files in the current directory:")
    for file in files:
        print(file)

def main():
    while True:
        print("\n1. Generate an image with DALL-E")
        print("2. Create variations of an image")
        print("3. Resize an image")
        print("4. Add a filter to your image")
        print("5. List files in the current directory")
        print("0. Exit")
        
        option = input("Choose an option: ")

        if option == "1":
            prompt = input("Enter the prompt for DALL-E: ")
            generate_image(prompt)
        elif option == "2":
            image_path = input("Enter the path of the image: ")
            create_variations(image_path)
        elif option == "3":
            image_path = input("Enter the path of the image you want resized: ")
            resize_image(image_path)
        elif option == "4":
            image_path = input("Enter the path of the image you want to add a filter to: ")
            apply_filters(image_path)
        elif option == "5":
            list_directory_files()
        elif option == "0":
            print("Exiting the program...")
            break
        else:
            print("Invalid option. Please enter a valid number.")

if __name__ == "__main__":
    main()
