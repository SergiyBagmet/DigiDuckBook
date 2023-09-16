import requests
import typing as t
from tabulate import tabulate

url_nbu_rates_json = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
nbu_response = requests.get(url_nbu_rates_json)

nbu_json: list[dict[str, str | int | float]]  = nbu_response.json()


class NbuExchangeRates:
    def __init__(self, full_data_nbu: t.Iterable[dict[str, str | int | float]]) -> None:
        self.date_str = full_data_nbu[0]["exchangedate"]
        self.grn_rate = self._short_data_nbu(full_data_nbu, ["USD", "EUR",])

    def _short_data_nbu(
            self, 
            full_data_nbu: t.Iterable[dict[str, str | int | float]], 
            country_keys: list[str]
            ) -> list[dict[str, str | float]]:
        
        filter_data_nbu = filter(lambda x: x["cc"] in country_keys, full_data_nbu)
        short_data_nbu = [
                        {k: v for k, v in full_dict.items() if k in ["txt", "rate", "cc"]} | {"unrate": 1  /  full_dict["rate"] }
                        for full_dict in filter_data_nbu
                        ]
        return short_data_nbu
    
    def __str__(el: dict[str, str | float]) -> str:
        return tabulate(grn_nbu.grn_rate, 
                        headers={"txt":"Country", "cc":"code", "rate":"rate", "unrate": "unrate"} ,
                        tablefmt='fancy_grid')
    
grn_nbu = NbuExchangeRates(nbu_json)

print(grn_nbu)