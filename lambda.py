import json

import numpy as np
from gdsam_utils import load_image_from_url, upload_image_to_s3, encode, decode

def handler(event, context):
    try:
        print("event", str(event))
        base64_img: str = event.get("base64_img")
        print("base64_img", base64_img)
        img_url: str = event.get("img_url")
        print("img_url", img_url)
        only_classify: bool = event.get("only_classify", False)
        print("only_classify", only_classify)
        only_segment: bool = event.get("only_segment", False)
        print("only_segment", only_segment)
        upload_to_s3: str = event.get("upload_to_s3", False)
        print("upload_to_s3", upload_to_s3)
        s3_key: str = event.get("s3_key")
        print("s3_key", s3_key)

        if (base64_img is None) and (img_url is None):
            raise Exception("No image provided")
        if base64_img is not None:
            input_image = decode(base64_img)
        if img_url is not None:
            input_image = load_image_from_url(img_url)

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
