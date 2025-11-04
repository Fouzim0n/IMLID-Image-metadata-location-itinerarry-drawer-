from PIL import Image, ExifTags
from datetime import datetime
from metadata_model import ImageMetadata
from file_utils import get_image_files


def extract_image_metadata(image_path: str) -> ImageMetadata:
    """Extract metadata from a single image file."""
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        exif = {}
        if exif_data:
            exif = {
                ExifTags.TAGS.get(tag, tag): value
                for tag, value in exif_data.items()
                if tag in ExifTags.TAGS
            }

        # --- Date ---
        created_at = exif.get("DateTimeOriginal")
        if created_at:
            try:
                created_at = datetime.strptime(created_at, "%Y:%m:%d %H:%M:%S").isoformat()
            except Exception:
                pass

        # --- GPS ---
        gps_info = exif.get("GPSInfo")
        location_name = None
        if gps_info:
            gps_data = {}
            for key in gps_info.keys():
                decoded = ExifTags.GPSTAGS.get(key, key)
                gps_data[decoded] = gps_info[key]

            lat = gps_data.get("GPSLatitude")
            lon = gps_data.get("GPSLongitude")
            lat_ref = gps_data.get("GPSLatitudeRef")
            lon_ref = gps_data.get("GPSLongitudeRef")

            if lat and lon and lat_ref and lon_ref:
                lat = sum([v / (60 ** i) for i, v in enumerate(lat)])
                lon = sum([v / (60 ** i) for i, v in enumerate(lon)])
                if lat_ref != "N":
                    lat = -lat
                if lon_ref != "E":
                    lon = -lon
                location_name = f"{lat:.6f}, {lon:.6f}"

        return ImageMetadata(
            name=image_path.split("/")[-1],
            format=image.format,
            size=image.size,
            created_at=created_at,
            location=location_name
        )
    except Exception as e:
        print(f"Error reading {image_path}: {e}")
        return ImageMetadata("unknown", "unknown", (0, 0), None, None)


#def process_all_images(folder_path: str):
def process_all_images(fileList):
    image_paths = fileList
    #image_paths = get_image_files(folder_path)
    
    metadata_list = []

    for path in image_paths:
        metadata = extract_image_metadata(path)
        metadata_list.append(metadata.to_dict())

    return metadata_list
