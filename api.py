import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def upload_img(access_token: str, instance_url: str, image_data: bytes, description: str):
    """
    you can grab bytes for images from a http request to a web server or from reading a file
    for example:
    
    image_data=requests.get("https://mysite.com/image.png")
    or
    image_data=open("image.png", "rb")
    """
    resp = requests.post(urljoin(instance_url, "api/v2/media"),
        data={
            "description": description,
        },
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        files={"file": image_data}
    )
    return resp.json()


def toot(access_token: str, instance_url: str, message: str, images: list = []):
    """
    in the images list, each is either a list or a touple which the first index
    contains the image data in bytes, and the next is the description
    for example:
    images=[[image_bytes, "a picture of a cat"], [image_bytes, "a picture of a dog"]]
    """
    image_ids = [
        upload_img(access_token, instance_url, image, description)["id"] for image, description in images
    ]
    requests.post(urljoin(instance_url, "api/v1/statuses/"),
        data={
            "status": message,
            "visibility": "public",
            "media_ids[]": image_ids
        },
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )


def get_comics():
    year = time.strftime("%Y")
    year_comic_page = requests.get(f"https://www.housepetscomic.com/archive/?archive_year={year}")
    soup = BeautifulSoup(year_comic_page.text, "html.parser")
    latest_comics = soup.find_all("a", {
        "rel": "bookmark",
        "href": re.compile("^https://")
    })
    # return a list of every comic made on the current year
    return latest_comics


def scrape_comic(url: str):
    page_soup = BeautifulSoup(requests.get(url).text, "html.parser")
    # this contains beautifulsoup html data
    comic_image_data = page_soup.find("img", {
        "title": True,
        "alt": True
    })
    comic_image_url = comic_image_data.get("src")
    return {
        "ricks_message":comic_image_data.get("title"),
        "image_data":requests.get(comic_image_url).content,
        "title":page_soup.title.text.split(" \u2013 ")[0]
    }