import requests
import json
import logging
import os
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class Route:
    AREA_MAPPING = {
        "JABODETABEK": 0,
        "BANDUNG RAYA": 2,
        "YOGYAKARTA": 6,
        "SURABAYA": 8
    }

    def __init__(self, area: str = None) -> None:
        self.cfg: Dict[str, str] = None
        self.area: str = area
        self.area_num: int = None
        self.image_urls: Dict[int, str] = None
        self.image_url: str = None

    def get_config(self) -> Optional[Dict[str, str]]:
        """Load configuration from config.json."""
        try:
            with open("config.json", 'r') as f:
                self.cfg: Dict[str, str] = json.load(f)
            return self.cfg
        except FileNotFoundError:
            logger.error("Config file not found.")
        except json.JSONDecodeError as e:
            logger.error(f"Error while decoding config file: {e}")

    def get_route_map(self) -> Optional[Dict[int, str]]:
        """Retrieve route map URLs from the API."""
        try:
            response: requests.Response = requests.get(self.get_config()["ROUTE_BASE_URL"])
            if response.status_code == 200:
                logger.info(f"data successfully retrieved with status code {response.status_code}")
                data_api: Dict[str, str] = response.json().get("data", None)
                if data_api is not None:
                    self.image_urls: Dict[int, str] = {route["area"]:route["permalink"] for route in data_api}
                    return self.image_urls
                else:
                    logger.error("Data key not found in API response")
            else:
                logger.error(f"Can't retrieve data with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error while retrieving station IDs: {e}")

    def find_route_map(self) -> Optional[str]:
        """Find and return the route map URL for the specified area."""
        logger.info("Entering find_route_map method")
        self.get_route_map()

        self.area_num = self.AREA_MAPPING.get(self.area)

        if self.area_num is not None and self.image_urls and self.area_num in self.image_urls:
            self.image_url = self.image_urls[self.area_num]
            return self.image_url
        else:
            logger.error(f"Area '{self.area}' not found.")
            return None

    def download_route_map(self, url: str) -> str:
        """Download the route map image from the provided URL."""
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
        local_image_path = route
        local_image_path = route.download_route_map(image_url)
        print(f"Downloaded {area} route map to {local_image_path}")
        # os.remove(local_image_path)
    else:
        print(f"Failed to download {area} route map.")
