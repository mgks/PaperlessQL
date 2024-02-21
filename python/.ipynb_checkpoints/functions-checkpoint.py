import base64
from PIL import Image

def image_to_blob(image_path):
    """Converts an image file to a Base64-encoded blob.

    Args:
        image_path (str): The path to the image file.

    Returns:
        str: The Base64-encoded blob representation of the image.

    Raises:
        ValueError: If the image file format is not supported.
    """

    try:
        with open(image_path, "rb") as f:
            image_data = f.read()

        # Check for supported formats
        image = Image.open(image_path)
        if image.format not in ("JPEG", "PNG", "WEBP"):
            raise ValueError(f"Unsupported image format: {image.format}")

        # Compress image data (optional)
        # You can use libraries like Pillow or imageio for compression
        # Example using Pillow:
        # resized_image = image.resize((256, 256))  # Resize to reduce size
        # image_data = resized_image.convert("RGB").tobytes()  # Convert to RGB for compression

        return base64.b64encode(image_data).decode("utf-8")

    except FileNotFoundError:
        raise ValueError(f"Image file not found: {image_path}")