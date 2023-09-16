import requests
import typing as t
from tabulate import tabulate

url_nbu_rates_json = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
nbu_response = requests.get(url_nbu_rates_json)

nbu_json: list[dict[str, str | int | float]]  = nbu_response.json()

COUNTRY_CODES = ["USD", "EUR", "PLN", "GBP", "CZK"]

class NbuExchangeRates:
    def __init__(self, 
                 full_data_nbu: t.Iterable[dict[str, str | int | float]], 
                 codes: list[str]) -> None:
        
        self.date_str: str = full_data_nbu[0]["exchangedate"]
        self.codes: list[str] = codes
        self.short_data_nbu: dict[str, dict[str, str | float]] = self._short_data_nbu(full_data_nbu)

    def _short_data_nbu(
            self, 
            full_data_nbu: t.Iterable[dict[str, str | int | float]], 
            ) -> dict[str, dict[str, str | float]]:
        
        filter_data_nbu = filter(lambda x: x["cc"] in self.codes, full_data_nbu)
        short_data_nbu = {full_dict["cc"]:
                        {k: v for k, v in full_dict.items() if k in ["txt", "rate", "cc"]} 
                        | {"unrate": 1.0 / full_dict["rate"] }
                        for full_dict in filter_data_nbu
                        }
        return short_data_nbu
    
    def __str__(self) -> str:
        return tabulate(self.short_data_nbu.values(), 
                        headers={"txt":"Country", "cc":"code", "rate":"rate", "unrate": "unrate"} ,
                        tablefmt='fancy_grid')
    
    def _validation_code(self, code: str) -> str.upper:
        if (code:=code.upper()) not in self.codes:
            raise KeyError(f"this code {code} not recognized")
        return code
    
    def convert(self, money: int, code:str, to_grn: bool=True) -> float:
        rate = "rate" if to_grn else "unrate"
        if money <= 0 :
            return 0
        code = self._validation_code(code)
        return money / self.short_data_nbu[code][rate] 
    

grn_nbu = NbuExchangeRates(nbu_json, COUNTRY_CODES)

print(grn_nbu)
usd = grn_nbu.convert(1_000, "usd")
print(f'1_000 grn = {usd} usd at {grn_nbu.date_str}')

grn = grn_nbu.convert(1_000, "usd", to_grn=False)
print(f'1_000 usd = {grn} grn at {grn_nbu.date_str}')