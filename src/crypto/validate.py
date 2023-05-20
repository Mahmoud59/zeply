import requests
import web3


def check_eth(address):
    try:
        web3.Web3.is_checksum_address(address)
        return True
    except Exception:
        return False


def check_btc(address):
    try:
        url = f"https://blockchain.info/rawaddr/{address}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
        if 'address' in data and data['address'] == address:
            return True
    except Exception:
        return False
