import time
import api

with open("keys.secret", "r") as f:
    access_token = f.readline().strip()

def main():
    print("getting latest comic")
    current_comics = api.get_comics()
    while True:
        time.sleep(5)
        print("getting latest comics")
        comics = api.get_comics()
        if len(comics) > len(current_comics):
            latest_comic = api.scrape_comic(comics[-1]["href"])
            status = api.toot(
                access_token=access_token,
                instance_url="https://botsin.space",
                message=f'{latest_comic["title"]}\n{comics[-1]["href"]}',
                images=[[
                    latest_comic["image_data"],
                    latest_comic["ricks_message"]
                ]]
            )
            if status == 1:
                current_comics = comics
                print("updated")
            else:
                print("something broke, retrying again in 5 secconds")
        else:
            print("no updates yet")


if __name__ == "__main__":
    main()