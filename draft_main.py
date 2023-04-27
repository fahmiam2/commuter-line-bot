import requests
import json
import logging

# get station name from user && get jam awal dan jam akhir >> cek jadwal kereta dan posisi kereta misalkan
# get station id based on station name >> def get_station_id && def find_station_id_by_name
# get schedule based on station_id && jam awal && jam akhir
# https://api-partner.krl.co.id/krlweb/v1/schedule?stationid={sta_id}&timefrom={start_time}&timeto={end_time}
# 

class Krl:
    def __init__(self, origin_station_name, dest_station_name) -> None:
        self.config = None
        self.origin_station_name = None
        self.dest_station_name = None

    def get_config(self):
        with open("config.json", 'r') as f:
            self.config = json.load(f)
        return self.config
    
    def get_station_id(self):
        response = requests.get(self.get_config()["KRL_STATION_API"])
        if response.status_code == 200:
            station_id_data = response.json()["data"]
            station_id = {station["sta_name"]: station["sta_id"] for station in station_id_data}
            return station_id
        else:
            print("Error while fetching station data.")
            return None

    def find_station_id_by_name(self):
        station_name = self.origin_station_name
        station_ids = self.get_station_id()
        if station_ids and station_name in station_ids:
            return station_ids[station_name]
        else:
            print(f"Station '{station_name}' not found.")
            return None
        
    # def get_schedule(self, origin_station_name, destination_station_name):
    #     origin_id = self.find_station_id_by_name(origin_station_name)
    #     destination_id = self.find_station_id_by_name(destination_station_name)

    #     if not origin_id or not destination_id:
    #         return None
        

    #     schedule_api_url = f"https://api-partner.krl.co.id/krlweb/v1/schedule?stationid={sta_id}&timefrom={start_time}&timeto={end_time}"
    #     payload = {
    #         "org": origin_id,
    #         "dest": destination_id
    #     }

    #     response = requests.get(schedule_api_url, params=payload)

    #     if response.status_code == 200:
    #         schedule_data = response.json()
    #         return schedule_data
    #     else:
    #         print("Error while fetching schedule data.")
    #         return None

krl = Krl()
origin_station_name = "JAKARTAKOTA"
destination_station_name = "BOGOR"
# schedule_data = krl.get_schedule(origin_station_name, destination_station_name)
# print(schedule_data)
print(krl.find_station_id_by_name(origin_station_name))