import time
import api

with open("keys.secret", "r") as f:
    access_token = f.read()

def main():
    current_comics = api.get_comics()
    while True:
        time.sleep(5)
        comics = api.get_comics()
        if len(comics) > len(current_comics):
            current_comics = comics
            latest_comic = api.scrape_comic(comics[-1]["href"])
            api.toot(
                access_token=access_token,
                instance_url="https://botsin.space",
                message=f'{latest_comic["title"]}\n{comics[-1]["href"]}',
                images=[[
                    latest_comic["image_data"],
                    latest_comic["ricks_message"]
                ]]
            )
            print("updated")
        else:
            print("no updates yet")


if __name__ == "__main__":
    main()