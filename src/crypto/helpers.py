import bitcoinlib
from web3 import Account


class AddressGenerator:
    def __init__(self):
        self.crypto_address_generators = {
            'BTC': self.generate_btc_address,
            'ETH': self.generate_eth_address,
        }

    def generate_address(self, cryptocurrency):
        if cryptocurrency in self.crypto_address_generators:
            return self.crypto_address_generators[cryptocurrency]()
        else:
            raise ValueError(f"Unsupported cryptocurrency: {cryptocurrency}")

    def generate_btc_address(self):
        key = bitcoinlib.keys.Key()
        private_key = key.wif()
        address = key.address()
        return private_key, address

    def generate_eth_address(self, private_key=None):
        account = Account.create()
        private_key = account.key.hex()
        address = account.address
        return private_key, address
