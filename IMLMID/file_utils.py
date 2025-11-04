import os

def get_image_files(folder_path: str):
    """Return a list of image file paths inside a folder."""
    supported_ext = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff")
    return [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith(supported_ext)
    ]
