import requests
import json
import logging
from datetime import datetime, timedelta
import pytz

# get station name from user && get jam awal dan jam akhir >> cek jadwal kereta dan posisi kereta misalkan
# get station id based on station name >> def get_station_id && def find_station_id_by_name
# get schedule based on station_id && jam awal && jam akhir
# https://api-partner.krl.co.id/krlweb/v1/schedule?stationid={sta_id}&timefrom={start_time}&timeto={end_time}

class Krl():
    def __init__(self, station_name: str = None, start_time: str = None, end_time: str = None) -> None:
        self.station_name: str = station_name
        self.cfg: dict = None
        self.station_ids: dict = None
        self.station_id: str = None
        self.start_time: str = start_time or self.get_current_time()
        self.end_time: str = end_time or (datetime.strptime(self.start_time, '%H:%M') + timedelta(hours=1)).strftime('%H:%M')

    def get_current_time(self) -> str:
        tz: pytz.tzinfo = pytz.timezone('Asia/Jakarta')
        now: datetime = datetime.now(tz)
        return now.strftime("%H:00")

    def get_config(self) -> dict:
        with open("config.json", 'r') as f:
            self.cfg: dict = json.load(f)
        return self.cfg
    
    def get_station_id(self) -> dict:
        try:
            response: requests.Response = requests.get(self.get_config()["KRL_STATION_API"])
            if response.status_code == 200:
                print(f"data successfully retrieved with status code {response.status_code}")
                data_api: dict = response.json()["data"]
                self.station_ids: dict = {station["sta_name"]:station["sta_id"] for station in data_api}
                return self.station_ids
            else:
                return print(f"Can't retrieve data with status code {response.status_code}")
        except:
            pass

    def find_station_id_by_name(self) -> str:
        self.get_station_id()
        if self.station_ids and self.station_name.upper() in self.station_ids:
            self.station_id: str = self.station_ids[self.station_name.upper()]
            return self.station_id
        else:
            print(f"Station '{self.station_name.upper()}' not found.")
            return None
        
    def get_schedule(self) -> dict:
        self.find_station_id_by_name()
        schedule_api_url: str = f"https://api-partner.krl.co.id/krlweb/v1/schedule?stationid={self.station_id}&timefrom={self.start_time}&timeto={self.end_time}"
        print(schedule_api_url)
        response: requests.Response = requests.get(schedule_api_url)
        if response.status_code == 200:
            data_api_krl: dict = response.json()["data"]
            return data_api_krl

# krl: Krl = Krl(station_name="Tangerang")
# print(krl.get_schedule())

class Fare(Krl):
    def __init__(self, station_name: str = None, dest_station_name: str = None, start_time: str = None, end_time: str = None) -> None:
        super().__init__(station_name, start_time, end_time)
        self.dest_station_name = dest_station_name
        self.dest_station_id = None

    def find_dest_station_id_by_name(self) -> str:
        self.get_station_id()
        if self.station_ids and self.dest_station_name.upper() in self.station_ids:
            self.dest_station_id: str = self.station_ids[self.dest_station_name.upper()]
            return self.dest_station_id
        else:
            print(f"Station '{self.dest_station_name.upper()}' not found.")
            return None
        
    def get_fare(self) -> dict:
        self.find_station_id_by_name()
        self.find_dest_station_id_by_name()
        fare_api_url: str = f"https://api-partner.krl.co.id/krlweb/v1/fare?stationfrom={self.station_id}&stationto={self.dest_station_id}"
        response: requests.Response = requests.get(fare_api_url)
        if response.status_code == 200:
            print("data fare berhasil")
            data_fare_krl: dict = response.json()["data"]
            return data_fare_krl
        
fare: Fare = Fare(station_name="Tangerang", dest_station_name="Tanahtinggi")
# fare_info = fare.get_fare()
# print(fare_info)
# print(fare.find_dest_station_id_by_name())
print(fare.get_fare())

