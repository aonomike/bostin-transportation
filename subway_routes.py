import requests
from requests.auth import HTTPBasicAuth
import json
from collections import defaultdict


key = {"api-key": "8c149f3600a849a390e3fb41ba67083a"}
BASE_URL = "https://api-v3.mbta.com/"
# TODO: Refactor to have base url in a constant
class SubwayRoutes:
    def __init__(self):
        self.routes = self._get_routes()
        self.stops = self._get_all_stops()
    
    def _get_all_stops(self):
        # TODO : To paginate later
        # https://api-v3.mbta.com/stops?page[limit]=100&page[offset]=10
        url = f"{BASE_URL}/stops?filter[route_type]=0,1"
        response = requests.get(url, headers=key)
        response_data = response.json()
        return response_data["data"]


    def print_subway_routes(self):

        """
        I rely on the server API to filter the results for me since I am
        """
        routes = self._get_long_names_of_subway_routes()
        print(", ".join(routes))

    def _get_long_names_of_subway_routes(self):
        subway_routes_long_names = []
        for route in self.routes:
            subway_routes_long_names.append(route["attributes"]["long_name"])
        return subway_routes_long_names

    def get_routes_with_max_stops(self):
        stops_count = dict()
        route_with_max_stops = {"name": "", "number": 0}
        route_with_min_stops = {"name": "", "number": float("inf")}
        for route in self.routes:
            number_of_stops = len(self._get_stops_for_route(route["id"]))
            if number_of_stops and number_of_stops > route_with_max_stops["number"]:
                route_with_max_stops["name"] = route["attributes"]["long_name"]
                route_with_max_stops["number"] = number_of_stops
            if number_of_stops and number_of_stops < route_with_min_stops["number"]:
                route_with_min_stops["name"] = route["attributes"]["long_name"]
                route_with_min_stops["number"] = number_of_stops
        return [route_with_min_stops, route_with_max_stops]

    def _get_stops_for_route(self, route_id):
        url = f"https://api-v3.mbta.com/stops?filter[route]={route_id}&include=route"
        response = requests.get(url, headers=key).json()
        return response["data"]

    def _get_routes(self):
        url = "https://api-v3.mbta.com/routes?filter[type]=0,1"
        response = requests.get(url, headers=key)
        if response.status_code != 200:
            print("no success")
            return
        response_data = response.json()

        return response_data["data"] 
    def get_stops_in_multiple_routes(self):
        print('get all stops')
        stops_with_routes = self._get_route_with_stops()
        print('size of stops {stops_with_routes}')
        print('loop through stops to find routes')
        for stop in stops_with_routes:
            if len(stops_with_routes[stop]) > 1:
                print(f"Stop {stop[1]} connects the routes {self._get_route_names({stops_with_routes[stop])")


    def _get_route_names(self, routes):
        import ipdb; ipdb.set_trace()
        return [route["name"] for route in routes["data"] ]

    def _get_route_with_stops(self):
        # get all the stops
        # for each stop append to stop_routes the routes
        # return all the stops that have more than one route
        stop_routes = defaultdict(list)
        for stop in self.stops:
            routes = self.get_route_given_stop(stop["id"])
            key = (stop["id"], stop["attributes"]["name"])
            stop_routes[key].extend(routes)
        import ipdb; ipdb.set_trace()
        
        return stop_routes

            
        # for route in self.routes:
        #     stops = self._get_stops_for_route(route["id"])
        #     for stop in stops:
        #         stop_routes[key].append(route["attributes"]["long_name"])
        # return stop_routes
    def get_route_given_stop(self, stop):
        stop_routes = requests.get(f'{BASE_URL}routes?filter[type]=0,1&filter[stop]={stop}',headers=key)
        return stop_routes

    def get_route_given_stops(self, stop1, stop2):
        stop1_routes = requests.get(f'https://api-v3.mbta.com/routes?filter[type]=0,1&filter[stop]={stop1}',headers=key)
        stop2_routes = requests.get(f'https://api-v3.mbta.com/routes?filter[type]=0,1&filter[stop]={stop2}',headers=key)
        
        stop1_routes_data = stop1_routes.json()["data"]
        stop2_routes_data = stop2_routes.json()["data"]

        stop1_route_names = [route['attributes']['long_name'] for route in stop1_routes_data]
        stop2_route_names = [route['attributes']['long_name'] for route in stop2_routes_data]

        similar_routes = set.intersection(set(stop1_route_names), set(stop2_route_names))

        if len(similar_routes) > 0:
            print(f"The stops are connected via route {similar_routes}")

subway_routes = SubwayRoutes()
subway_routes.print_subway_routes()
print(subway_routes.get_routes_with_max_stops())
subway_routes.get_stops_in_multiple_routes()
subway_routes.get_route_given_stops('place-davis', 'place-pktrm')
