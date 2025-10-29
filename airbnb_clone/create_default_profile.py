from PIL import Image
import os

# Create the media directory if it doesn't exist
media_dir = os.path.join(os.path.dirname(__file__), 'media')
if not os.path.exists(media_dir):
    os.makedirs(media_dir)

# Create a new 300x300 gray image
img = Image.new('RGB', (300, 300), color='#808080')

# Save it as default.jpg in the media directory
default_path = os.path.join(media_dir, 'default.jpg')
img.save(default_path)

print(f"Created default profile picture at {default_path}")