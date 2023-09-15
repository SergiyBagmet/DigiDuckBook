import requests


nbu_response = requests.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json")

nbu_json = nbu_response.json()
