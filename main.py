from flask import Flask, render_template, request
import torch
import torchvision.transforms as transforms
import numpy as np
import matplotlib.pyplot as plt
import base64
import io
from PIL import Image
from PIL import ImageEnhance

app = Flask(__name__)

# Load the trained U-Net model
model = torch.load('UNetEfficientnetB0-best.pth', map_location=torch.device('cpu'), weights_only=False).eval()

# Define the transformation to match your model's input shape
transform = transforms.Compose([
    transforms.Resize((384, 768)),  # Adjust to match your model's input size
    transforms.ToTensor()
])

def encode_image(image):
    """Convert a Matplotlib figure or PIL image to base64 string"""
    img_io = io.BytesIO()
    image.save(img_io, format='PNG')
    img_io.seek(0)
    return base64.b64encode(img_io.getvalue()).decode('utf-8')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "No file uploaded"
    file = request.files['file']
    if file.filename == '':
        return "No file selected"
    
    # Read and preprocess image
    image = Image.open(io.BytesIO(file.read())).convert("L")  # Convert to grayscale
    image_tensor = transform(image).unsqueeze(0)  # Add batch dimension

    # Run model prediction
    with torch.no_grad():
        output = model(image_tensor)
    output_mask = output.squeeze().cpu().numpy()

    # Convert original image to base64
    original_image_base64 = encode_image(image)

    # Convert mask to base64
    plt.figure(figsize=(5, 5))
    plt.imshow(output_mask, cmap='gray')
    plt.axis('off')
    img_mask_io = io.BytesIO()
    plt.savefig(img_mask_io, format='PNG', bbox_inches='tight', pad_inches=0)
    img_mask_io.seek(0)
    mask_image_base64 = base64.b64encode(img_mask_io.getvalue()).decode('utf-8')

    # Create overlay image (Original + Mask)
#   Convert mask to an RGBA image with transparency
    mask_overlay = Image.fromarray((output_mask * 255).astype(np.uint8)).convert("L")  
    mask_overlay = mask_overlay.resize(image.size, Image.BILINEAR)

# Convert grayscale mask to a colored RGBA mask (Red color)
    colored_mask = Image.new("RGBA", mask_overlay.size, (255, 0, 0, 0))  # Red mask with 0 transparency
    colored_mask.paste((255, 0, 0, 150), (0, 0) + mask_overlay.size, mask_overlay)  # Add transparency

# Convert original image to RGBA
    image_rgba = image.convert("RGBA")

# Overlay the mask onto the original image
    overlay = Image.alpha_composite(image_rgba, colored_mask)

# Convert back to RGB before saving
    overlay = overlay.convert("RGB")

# Encode the overlay image
    overlay_image_base64 = encode_image(overlay)

    return render_template(
        'result.html',
        original_image=original_image_base64,
        mask_image=mask_image_base64,
        overlay_image=overlay_image_base64
    )

if __name__ == '__main__':
    app.run(debug=True)
