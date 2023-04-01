import requests
from urllib.parse import urljoin

def upload_img(access_token: str, instance_url: str, image_data: bytes, description: str):
    resp = requests.post(urljoin(instance_url, "api/v2/media"),
        data={
            "description":description,
        },
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        files={"file":image_data}
    )
    return resp.json()


def toot(access_token: str, instance_url: str, message: str, images: list=[]):
    image_ids = [
        upload_img(access_token, instance_url, open(image, "rb"), description)["id"] for image, description in images
    ]
    print(image_ids)
    resp = requests.post(urljoin(instance_url, "api/v1/statuses/"),
        data={
            "status":message,
            "visibility":"public",
            "media_ids[]":image_ids
        },
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    print(resp.content)