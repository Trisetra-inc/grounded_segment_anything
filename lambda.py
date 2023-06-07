import base64
import json

import cv2
import numpy as np
from gdsam_utils import load_image_from_url, upload_image_to_s3


def encode(img: np.ndarray, ext: str = ".jpg") -> str:
    _, buffer = cv2.imencode(ext, img)
    return base64.b64encode(buffer).decode("utf-8")

def decode(img: str) -> np.ndarray:
    buffer = base64.b64decode(img)
    return cv2.imdecode(np.frombuffer(buffer, dtype=np.uint8), -1)


def handler(event, context):
    try:
        print("event", str(event))
        base64_img: str = event.get("base64_img")
        print("base64_img", base64_img)
        img_url: str = event.get("img_url")
        print("img_url", img_url)
        auto_enhance: bool = event.get("auto_enhance")
        print("auto_enhance", auto_enhance)
        upload_to_s3: bool = event.get("upload_to_s3")
        print("upload_to_s3", upload_to_s3)
        s3_key: str = event.get("s3_key")
        print("s3_key", s3_key)

        if (base64_img is None) and (img_url is None):
            raise Exception("No image provided")
        if base64_img is not None:
            input_image = decode(base64_img)
        if img_url is not None:
            input_image = load_image_from_url(img_url)

        model = load_model()
        rotation_label, probablity = predict_rotation_label(input_image, model)
        if rotation_label == 0 or probablity < 0.9:
            output_img = input_image
        else:
            output_img, _ = rotate_image(input_image, rotation_label)

        if auto_enhance:
            output_img = enhance_image(output_img)

        if upload_to_s3:
            s3_key = upload_image_to_s3(output_img, key=img_url if s3_key is None else s3_key)
            return { "statusCode": 200, "body": json.dumps({ "s3_key": s3_key }) }

        return {
            "statusCode": 200,
            "body": json.dumps({
                "rotated_img": encode(output_img),
            })
        }
    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
