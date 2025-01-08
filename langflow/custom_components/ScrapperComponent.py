# from langflow.field_typing import Data
from langflow.custom import Component
from langflow.io import MessageTextInput, Output
from langflow.schema import Data


class CustomComponent(Component):
    display_name = "Custom Components"
    description = "Used to fetch post data for particular profile."
    documentation: str = "http://docs.langflow.org/components/custom"
    icon = "code"
    name = "CustomComponent"

    inputs = [
        MessageTextInput(
            name="input_value",
            display_name="Input Value",
            info="This is a custom component Input",
            value="Hello, World!",
            tool_mode=True,
        ),
    ]

    outputs = [
        Output(display_name="Output", name="output", method="build_output"),
    ]

    def build_output(self) -> Data:
        data = Data(value=self.input_value)
        post_data = self.getPostDataFromRapid(data.value)
        self.status = post_data
        return post_data

    def get_proxy(self,protocol: str = "http", country: str = "us", anonymity: str = "all") -> str:
        try:
            # Fetch proxy list from ProxyScrape
            resp = requests.get(
                f"https://api.proxyscrape.com/v2/?request=displayproxies&protocol={protocol}&timeout=10000&country={country}&ssl=all&anonymity={anonymity}"
            )
            resp.raise_for_status()
            proxy_list = resp.text.strip().split("\r\n")

            # Fallback to another source if ProxyScrape is empty
            if not proxy_list or proxy_list == [""]:
                resp = requests.get(f"https://www.proxy-list.download/api/v1/get?type={protocol}")
                resp.raise_for_status()
                proxy_list = resp.text.strip().split("\r\n")

            if not proxy_list:
                raise ValueError("No proxies available from the sources.")

            # Randomly select a proxy
            return random.choice(proxy_list)
        except Exception as e:
            print(f"Error getting proxy: {e}")
            return None

    def getPostDataFromRapid(self,username):
        URL = "https://instagram-scraper-api2.p.rapidapi.com/v1.2/posts"
        MAX_POSTS = 30
        POST_TYPE = {
            "reel": "reel",
            "post": "static_image",
            "album": "carousel",
        }
        pagination_token = None
        page_count = 1
        post_count = 0
        processed_posts = []

        while post_count <= MAX_POSTS:
            print("Page:", page_count)
            querystring = {"username_or_id_or_url": username}
            if pagination_token:
                querystring["pagination_token"] = pagination_token

            headers = {
                "x-rapidapi-key": "<YOUR RAPID API KEY>",
                "x-rapidapi-host": "instagram-scraper-api2.p.rapidapi.com"
            }
            proxy = self.get_proxy()
            proxies = {
                "http": f"http://{proxy}"
            }
            response = requests.get(URL, headers=headers, params=querystring, proxies=proxies)
            json_response = response.json()
            response.raise_for_status()

            post_count += json_response["data"]["count"]
            pagination_token = json_response["pagination_token"]
            post_items = json_response["data"]["items"]

            for data in post_items:
                processed_posts.append({
                    "post_id": data["id"],
                    "user_id": json_response["data"]["user"]["id"],
                    "user_profile_name": username,
                    "post_type": POST_TYPE[data["media_name"]],
                    "likes": data["like_count"] if data["like_and_view_counts_disabled"] is False else 0,
                    "views": data["play_count"] if POST_TYPE[data["media_name"]] == "reel" else 0,
                    "shares": data["share_count"] if POST_TYPE[data["media_name"]] == "reel" else 0,
                    "comments": data["comment_count"]
                })
            if not pagination_token:
                break
            page_count += 1

        return processed_posts

'[{"user_profile_name": "'+self.user_profile_name+'", "user_id": "'+self.user_id+'"}]'
