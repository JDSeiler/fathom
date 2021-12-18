from decouple import config
from typing import Any, Dict, Optional, TypedDict
import requests
import time


class RequestDetails(TypedDict):
    req_url: str
    headers: Any


class ApiResponse(TypedDict):
    payload: Optional[Any]
    status: int
    text: Optional[str]
    details: RequestDetails


class Client:
    def __init__(self):
        self.api_key = config('API_KEY', cast=str)
        self.na1_route = 'https://na1.api.riotgames.com'
        self.americas_route = 'https://americas.api.riotgames.com'
        self.PAUSE_TIME = 0.05  # 50 ms to avoid going over the 20 req / sec limit

    def get_summoner_matches(self, summoner_name: str):
        summoner_info_res = self.get(self.na1_route, f"/lol/summoner/v4/summoners/by-name/{summoner_name}")
        time.sleep(self.PAUSE_TIME)
        puuid = summoner_info_res['payload']['puuid']

        match_ids = []
        more_matches = True
        curr_idx = 0
        batch_size = 50

        while more_matches:
            match_ids_res = self.get(
                self.americas_route,
                f"/lol/match/v5/matches/by-puuid/{puuid}/ids",
                {'start': curr_idx, 'count': batch_size}
            )

            if match_ids_res['status'] != 200:
                print(match_ids_res['status'])
                print(match_ids_res['text'])
                raise Exception('Got a non-ok response while fetching match IDs')

            ids = match_ids_res['payload']
            if len(ids) == 0:
                more_matches = False
            else:
                match_ids.extend(match_ids_res['payload'])
                curr_idx += batch_size
            time.sleep(self.PAUSE_TIME)

        matches = []
        for idx, m_id in enumerate(match_ids):
            print(f"Fetching match {idx+1} of {len(match_ids)}")
            match_info_res = self.get(
                self.americas_route,
                f"/lol/match/v5/matches/{m_id}"
            )

            if match_info_res['status'] != 200:
                print(match_info_res['status'])
                print(match_info_res['text'])
                raise Exception('Got a non-ok response while fetching match info')

            matches.append(match_info_res['payload'])
            time.sleep(self.PAUSE_TIME)

        return matches

    def get(self, route: str, request_path: str, query_params: Dict[str, str] = None) -> ApiResponse:
        full_request_path = route + request_path
        headers = {'X-Riot-Token': self.api_key}

        # requests can techincally handle arrays as QP values, but lets ignore that.
        r = requests.get(full_request_path, headers=headers, params=query_params)
        return {
            'payload': r.json() if r.ok else None,
            'status': r.status_code,
            'text': r.text if not r.ok else None,
            'details': {
                'req_url': r.url,
                'headers': r.headers
            }
        }
