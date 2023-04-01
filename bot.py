from api import toot
import requests

with open("keys.secret", "r") as f:
    access_token = f.read()

def main():
    toot(
        access_token=access_token,
        message="test 123, testing image",
        instance_url="https://botsin.space/",
        images=[["test_comic.png", "test comic"]]
    )

if __name__ == "__main__":
    main()