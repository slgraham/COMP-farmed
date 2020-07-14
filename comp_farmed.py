import json
from web3 import Web3, HTTPProvider
from pycoingecko import CoinGeckoAPI

import os
from dotenv import load_dotenv

# compound contracts
comp = Web3.toChecksumAddress('0xc00e94cb662c3520282e6f5717214004a7f26888')
comptroller = Web3.toChecksumAddress(
    '0x3d9819210a31b4961b30ef54be2aed79b9c9cd3b')
lens = Web3.toChecksumAddress('0xd513d22422a3062Bd342Ae374b4b9c20E0a9a074')

# set up connection to infura
load_dotenv()
infura_project_id = os.getenv("INFURA_PROJECT_ID")
infura_url = 'https://mainnet.infura.io/v3/' + infura_project_id
w3 = Web3(Web3.HTTPProvider(infura_url))

# load the lens contract ABI
with open('lens.json') as file:
    abi_json = json.load(file)
lens_abi = abi_json

# create the lens contract object
lens_contract = w3.eth.contract(address=lens, abi=lens_abi)

# gets total COMP earned by a address: the sum of current balance and current accrued


def comp_usd_price():
    cg = CoinGeckoAPI()
    comp_id = 'compound-governance-token'
    result = cg.get_price(ids=comp_id, vs_currencies='usd')
    price = result[comp_id]['usd']
    return price


def get_comp(address):
    metadata = lens_contract.functions.getCompBalanceMetadataExt(
        comp, comptroller, address).call()
    held = metadata[0]
    accrued = metadata[3]
    return (held + accrued)/10**18
