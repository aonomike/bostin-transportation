import requests
from requests.auth import HTTPBasicAuth
import json


class SubwayRoutes:
    def __init__(self):
        self.routes = self._get_routes()

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
        key = {"api-key": "8c149f3600a849a390e3fb41ba67083a"}
        url = f"https://api-v3.mbta.com/stops?filter[route]={route_id}&include=route"
        response = requests.get(url, headers=key).json()
        return response["data"]

    def _get_routes(self):
        url = "https://api-v3.mbta.com/routes?filter[type]=0,1"
        key = {"api-key": "8c149f3600a849a390e3fb41ba67083a"}
        response = requests.get(url, headers=key)
        response_data = response.json()
        return response_data["data"]

    def get_stops_in_multiple_routes(self):
        stops_with_routes = self._get_route_with_stops()

        for stop in stops_with_routes:
            if len(stops_with_routes[stop]) > 1:
                print(f"Stop {stop[1]} connects the routes {stops_with_routes[stop]}")

    def _get_route_with_stops(self):
        from collections import defaultdict

        routes_with_stops = defaultdict(list)
        for route in self.routes:
            stops = self._get_stops_for_route(route["id"])
            for stop in stops:
                key = (stop["id"], stop["attributes"]["name"])
                routes_with_stops[key].append(route["attributes"]["long_name"])
        return routes_with_stops

    def get_route_given_stops(stop1, stop1):
        pass


subway_routes = SubwayRoutes()
# subway_routes.print_subway_routes()
# print(subway_routes.get_routes_with_max_stops())
subway_routes.get_stops_in_multiple_routes()
