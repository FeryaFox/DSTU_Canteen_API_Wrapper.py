import requests
from .Models import DishInfo, Canteen, ResponseModel


class DSTUBackendAPIWrapper:
    def __init__(self, url: str = "http://127.0.0.1:8000/api/"):
        self.url = url

    def get_all_canteen(self) -> list[Canteen] | list:
        endpoint = "canteen"
        return_l = []
        r = self.__make_request(self.url + endpoint)
        for i in r.data["data"]:
            return_l.append(Canteen(**i))
        return return_l

    def get_canteen_by_id(self, canteen_id: int) -> Canteen | None:
        endpoint = "canteen/{}"
        r = self.__make_request(self.url + endpoint.format(canteen_id))
        match r.status_code:
            case 200:
                return Canteen(*r.data["data"])
            case 404:
                return None
            case 422 | 500:
                print(f"ERROR! {r.status_code}")

    def get_all_dish(self, canteen_id: int | None = None) -> list[DishInfo] | None:
        endpoint = "dish"
        return_l = []

        if canteen_id is None:
            r = self.__make_request(self.url + endpoint).data["data"]
        else:
            r = self.__make_request(self.url + endpoint + f"?canteen_id={canteen_id}").data["data"]
        match r.status_code:
            case 200:
                for i in r:
                    return_l.append(DishInfo(**i))
                return return_l
            case 404:
                return None
            case 422 | 500:
                print(f"ERROR! {r.status_code}")

    def get_dish_info_by_id(self, dish_id: int, canteen_id: int | None = None) -> DishInfo | None:
        endpoint = "dish/{}"
        if canteen_id is None:
            r = self.__make_request(self.url + endpoint.format(dish_id))
        else:
            r = self.__make_request(self.url + endpoint.format(dish_id) + f"?canteen_id={canteen_id}")
        match r.status_code:
            case 200:
                return DishInfo(**r.data["data"])
            case 404:
                return None
            case 422 | 500:
                print(f"ERROR! {r.status_code}")

    @staticmethod
    def __make_request(url: str) -> ResponseModel:
        r = requests.get(url)
        match r.status_code:
            case 200:
                data_json = r.json()
                print({"data": data_json})
                return ResponseModel(r.status_code, {"data": data_json})
            case 404:
                return ResponseModel(r.status_code, {})
            case 402:
                return ResponseModel(r.status_code, {})
            case 500:
                return ResponseModel(r.status_code, {})
