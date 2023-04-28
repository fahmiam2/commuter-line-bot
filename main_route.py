import requests
import json
import logging
import os
# from uuid import uuid4

logger = logging.getLogger(__name__)

class Route():
    def __init__(self, area: str = None) -> None:
        self.cfg: dict = None
        self.area: str = area
        self.area_num: int = None
        self.image_urls: dict = None
        self.image_url: str = None

    def get_config(self) -> dict:
        try:
            with open("config.json", 'r') as f:
                self.cfg: dict = json.load(f)
            return self.cfg
        except FileNotFoundError:
            logger.error("Config file not found.")
        except json.JSONDecodeError as e:
            logger.error(f"Error while decoding config file: {e}")

    def get_route_map(self):
        try:
            response: requests.Response = requests.get(self.get_config()["ROUTE_BASE_URL"])
            if response.status_code == 200:
                logger.info(f"data successfully retrieved with status code {response.status_code}")
                data_api: dict = response.json()["data"]
                self.image_urls: dict = {route["area"]:route["permalink"] for route in data_api}
                return self.image_urls
            else:
                logger.error(f"Can't retrieve data with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error while retrieving station IDs: {e}")

    def find_route_map(self):
        self.get_route_map()
        
        area_mapping = {
            "JABODETABEK": 0,
            "BANDUNG RAYA": 2,
            "YOGYAKARTA": 6,
            "SURABAYA": 8
        }
        
        self.area_num = area_mapping.get(self.area)
        
        if self.area_num is not None and self.image_urls and self.area_num in self.image_urls:
            self.image_url = self.image_urls[self.area_num]
            return self.image_url
        else:
            logger.error(f"Area '{self.area}' not found.")
            return None

        
    def download_route_map(self, url: str) -> str:
        # local_filename = f"{uuid4()}.png"
        local_filename = f"{self.area}_commuterline_routemap.png"
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(local_filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        return local_filename
    
if __name__ == "__main__":
    area = "JABODETABEK"
    route = Route(area=area)
    image_url = route.find_route_map()
    if image_url:
        local_image_path = route.download_route_map(image_url)
        print(f"Downloaded {area} route map to {local_image_path}")
        # os.remove(local_image_path)
    else:
        print(f"Failed to download {area} route map.")


        

            
            
    