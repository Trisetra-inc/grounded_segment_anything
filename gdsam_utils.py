import base64
import boto3
import cv2
import requests
import numpy as np


def encode(img: np.ndarray, ext: str = ".jpg") -> str:
    _, buffer = cv2.imencode(ext, img)
    return base64.b64encode(buffer).decode("utf-8")


def decode(img: str) -> np.ndarray:
    buffer = base64.b64decode(img)
    return cv2.imdecode(np.frombuffer(buffer, dtype=np.uint8), -1)


def load_image_from_url(url: str) -> cv2.Mat:
    """
    Loads an image from a URL.

    Args:
    url (str): URL of the image

    Returns:
    numpy.ndarray: Image
    """
    # Download the image
    resp = requests.get(url)
    # Convert the image to a NumPy array
    image = np.asarray(bytearray(resp.content), dtype=np.uint8)
    # Decode the NumPy array to an image
    image: cv2.Mat = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


def upload_image_to_s3(image: cv2.Mat, key: str, bucket: str = "androidcamera2rawdd46db682a5b475d83dbfbe980017a4e", ext: str = ".jpg"):
    """
    Uploads an image to S3.

    Args:
    image (numpy.ndarray): Image
    bucket (str): S3 bucket name
    key (str): S3 key
    """
    _, buffer = cv2.imencode(ext, image)
    key = key.replace(f"https://{bucket}.s3.amazonaws.com/", "").split("?").pop(0)

    s3_client = boto3.client("s3")
    s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=buffer.tobytes(),
    )
    
    return f"https://{bucket}.s3.amazonaws.com/{key}"


def save_image(image: cv2.Mat, path: str):
    """
    Saves an image to the given path.

    Args:
    image (numpy.ndarray): Image
    path (str): Path to save the image
    """
    cv2.imwrite(path, image)
