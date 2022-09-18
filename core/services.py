import pandas as pd
import requests

url = f'https://statusinvest.com.br/fundos-imobiliarios/MXRF11'
response = requests.get(url)

if response.status_code == 200:
    df = pd.read_html(response.content, encoding='utf-8')[0]
    print(df)