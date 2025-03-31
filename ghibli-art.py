from diffusers import StableDiffusionImg2ImgPipeline
import torch
from PIL import Image
import io
from google.colab import files
import matplotlib.pyplot as plt
import time

# Load model function
def load_model():
    model_id = "nitrosocke/Ghibli-Diffusion"  # Correct model ID
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    print("Loading model...")
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id, torch_dtype=dtype)
    pipe.to("cuda" if torch.cuda.is_available() else "cpu")
    pipe.enable_attention_slicing()  # Optimize memory usage
    print("Model loaded!")
    return pipe

# Function to generate Ghibli-style image
def generate_ghibli_image(image, pipe, strength):
    image = image.convert("RGB")
    image = image.resize((512, 512))  # Ensure proper size
    
    prompt = "Ghibli-style anime painting, soft pastel colors, highly detailed, masterpiece"
    
    print("Generating image...")
    start_time = time.time()
    result = pipe(prompt=prompt, image=image, strength=strength).images[0]
    print(f"Image generated in {time.time() - start_time:.2f} seconds!")
    return result

# Check for GPU
gpu_info = "GPU is available!" if torch.cuda.is_available() else "Warning: GPU not available. Processing will be slow."
print(gpu_info)

# Load the model
pipe = load_model()

# Upload image section
print("Please upload your image file:")
uploaded = files.upload()

if uploaded:
    file_name = list(uploaded.keys())[0]
    image = Image.open(io.BytesIO(uploaded[file_name]))
    
    # Display original image
    plt.figure(figsize=(5, 5))
    plt.imshow(image)
    plt.title("Original Image")
    plt.axis('off')
    plt.show()
    
    # Ask for strength input with error handling
    while True:
        try:
            strength = float(input("Enter stylization strength (0.3-0.8, recommended 0.6): "))
            strength = max(0.3, min(0.8, strength))  # Clamp between 0.3 and 0.8
            break
        except ValueError:
            print("Invalid input. Please enter a number between 0.3 and 0.8.")
    
    # Generate and display the result
    result_img = generate_ghibli_image(image, pipe, strength)
    
    plt.figure(figsize=(5, 5))
    plt.imshow(result_img)
    plt.title("Ghibli Portrait")
    plt.axis('off')
    plt.show()
    
    # Save the output image and offer download
    output_filename = f"ghibli_portrait_{file_name}"
    result_img.save(output_filename)
    files.download(output_filename)
    print(f"Image saved as {output_filename} and download initiated!")
else:
    print("No file was uploaded. Please run the cell again and upload an image.")
