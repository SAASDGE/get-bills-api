import os
from decouple import config
from datetime import datetime
import subprocess
import requests
from http import HTTPStatus
import sys
import re
today = datetime.now()
API_TOKEN = config('API_TOKEN', default=None)
ISSUED_AT_MONTH = config('ISSUED_AT_MONTH', default=today.month)
ISSUED_AT_YEAR = config('ISSUED_AT_YEAR', default=today.year)
PATH_TO_DOWNLOAD = config('PATH_TO_DOWNLOAD', default=f'{os.getcwd()}/faturas')
API_BASE_URL = config('API_BASE_URL', default='')

if not ISSUED_AT_MONTH:
    ISSUED_AT_MONTH = today.month
if not ISSUED_AT_YEAR:
    ISSUED_AT_YEAR = today.year
if not PATH_TO_DOWNLOAD:
    PATH_TO_DOWNLOAD = f'{os.getcwd()}/faturas'
if not API_BASE_URL:
    print("[ERRO] Preencha a variável de ambiente API_BASE_URL com a URL da API.")
    sys.exit()

REGARDING_MAP = {
    1: f"JAN/",
    2: f"FEV/",
    3: f"MAR/",
    4: f"ABR/",
    5: f"MAI/",
    6: f"JUN/",
    7: f"JUL/",
    8: f"AGO/",
    9: f"SET/",
    10: f"OUT/",
    11: f"NOV/",
    12: f"DEZ/",
}


def runcmd(link, path_to_download):
    file_name = re.search(r".+/(?P<file_name>.+\.pdf).", link).group('file_name')
    print(link, file_name)
    subprocess.run(['wget', '-q', '-c', link,'-O', f'{path_to_download}/{file_name}'], check=True)


def download_bills(bills, path_to_download):
    for index, bill in enumerate(bills):
        print(f"Downloading {index + 1}/{len(bills)}")
        runcmd(bill, path_to_download)


def get_bills_by_emission_date(api_session, agents):
    for agent_name, agent_id in agents.items():
        bills_list = []
        url = f'{API_BASE_URL}/bills/?installation_data__agent={agent_id}&issued_at__month={ISSUED_AT_MONTH}&issued_at__year={ISSUED_AT_YEAR}'
        print(f"\nBaixando faturas do Agente {agent_name}:")
        path_to_download = os.path.join(PATH_TO_DOWNLOAD, agent_name, f'{ISSUED_AT_YEAR}/{REGARDING_MAP[ISSUED_AT_MONTH]}')
        os.makedirs(path_to_download, exist_ok=True)
        while True:
            if url is None:
                break

            response = api_session.get(url)
            data = response.json()
            if response.status_code == HTTPStatus.OK:
                for bill in data['results']:
                    bills_list.append(bill["bill_generated"])

            url = data['next']
        download_bills(bills_list[:30], path_to_download)


def get_agents(api_session):
    url = f'{API_BASE_URL}/agents'

    agents = {}
    while True:
        if url is None:
            break

        response = api_session.get(url)
        data = response.json()
        if response.status_code == HTTPStatus.OK:
            for agent in data['results']:
                if "BOW-E" in agent['name'].upper():
                    if agent['description']:
                        agent['name'] = ' '.join([agent['name'], agent["description"]])
                    agents[agent['name']] = agent['id']
        else:
            raise Exception(data['detail'])
        url = data['next']

    return agents


def start_api_session():
    session = requests.Session()
    session.headers.update({'Authorization': f'Token {API_TOKEN}'})
    return session


def main():
    try:
        if not os.path.isdir(PATH_TO_DOWNLOAD):
            os.mkdir(PATH_TO_DOWNLOAD)
        api_session = start_api_session()
        agents = get_agents(api_session)
        get_bills_by_emission_date(api_session, agents=agents)
    except Exception as exc:
        print(f"[ERRO] {exc}")


if __name__ == "__main__":
    main()
