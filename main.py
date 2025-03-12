import sys
import json
import random
import tls_client

from fake_useragent import UserAgent

with open('config.json') as f:
    config = json.load(f)

shorten = lambda s: f"{s[:4]}...{s[-5:]}" if len(s) >= 9 else s

class CopyWalletFinder:
    def __init__(self, rpc_url):
        self.rpc_url = rpc_url
        self.sendRequest = tls_client.Session(client_identifier="chrome_103")

    def randomiseRequest(self):
        self.identifier = random.choice(
            [browser for browser in tls_client.settings.ClientIdentifiers.__args__
             if browser.startswith(('chrome', 'safari', 'firefox', 'opera'))]
        )
        self.sendRequest = tls_client.Session(
            random_tls_extension_order=True, client_identifier=self.identifier
        )
        parts = self.identifier.split('_')
        identifier, version, *rest = parts
        other = rest[0] if rest else None
        if identifier == "opera":
            identifier = "chrome"
        os = "iOS" if version == "iOS" else "Windows"

        self.user_agent = UserAgent(browsers=[identifier.title()], os=[os]).random

        self.headers = {
            'Host': 'gmgn.ai',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'dnt': '1',
            'priority': 'u=1, i',
            'referer': 'https://gmgn.ai/?chain=sol',
            'user-agent': self.user_agent
        }

    def getLastBuy(self, walletAddress: str):
        retries = 3
        url = f"https://gmgn.ai/api/v1/wallet_activity/sol?type=buy&wallet={walletAddress}&limit=10&cost=10"
        for attempt in range(retries):
            self.randomiseRequest()
            try:
                response = self.sendRequest.get(url, headers=self.headers)
                data = response.json()['data']['activities'][0]
                transaction = data['tx_hash']
                contractAddress = data['token']['address']
                return transaction, contractAddress
            except Exception:
                print(f"failed to get last buy from {walletAddress}")
        return None, None

    def getBlockHash(self, transaction: str):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTransaction",
            "params": [
                transaction,
                {
                    "encoding": "jsonParsed",
                    "maxSupportedTransactionVersion": 0
                }
            ]
        }
        response = self.sendRequest.post(self.rpc_url, json=payload)
        block = int(response.json()['result']['slot'])
        return block

    def getPotentialCopyTraders(self, startBlock: int, walletAddress: str, contractAddress: str, blockLimit: int = 0, txLimit: int = 0):
        mainTranscation = None
        mainBlock = startBlock  
        potentialCopyTraders = {}

        for curentBlock in range(startBlock, startBlock + blockLimit + 1):
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getBlock",
                "params": [
                    curentBlock,
                    {
                        "encoding": "json",
                        "maxSupportedTransactionVersion": 0,
                        "transactionDetails": "full",
                        "rewards": False
                    }
                ]
            }
            response = self.sendRequest.post(self.rpc_url, json=payload)
            data = response.json()
            transactions = data['result']['transactions']

            if curentBlock == startBlock:
                targetIndex = None

                for i, tx in enumerate(transactions):
                    account_keys = tx['transaction']['message']['accountKeys']
                    if walletAddress in account_keys:
                        post_token_balances = tx['meta'].get('postTokenBalances', [])
                        if post_token_balances:
                            mint = post_token_balances[0].get('mint')
                            if mint == contractAddress:
                                targetIndex = i
                                mainTranscation = tx['transaction']['signatures'][0]
                                break

                if targetIndex is None:
                    print("target wallet transaction with the matching mint was not found in the starting block.")
                    targetIndex = 0  
                txWindow = transactions[targetIndex+1:targetIndex+txLimit]

            else:
                txWindow = transactions
            for i, tx in enumerate(txWindow):
                contestant = tx['transaction']['message']['accountKeys'][0]
                if contestant == walletAddress:
                    continue
                postTokenBalances = tx['meta'].get('postTokenBalances', [])
                if any(balance.get('mint') == contractAddress for balance in postTokenBalances):
                    contestantTx = tx['transaction']['signatures'][0]
                    if contestant not in potentialCopyTraders:
                        potentialCopyTraders[contestant] = (contestantTx, curentBlock)

        uniqueContestants = [(wallet, tx, blk) for wallet, (tx, blk) in potentialCopyTraders.items()]
        return mainTranscation, mainBlock, uniqueContestants

rpc_url = config['rpc_url']
walletAddress = config['walletAddress']
blockLimit = config['blockLimit']
txLimit = config['txLimit']

if walletAddress == "":
    print("no target wallet address found")
    sys.exit(1)

finder = CopyWalletFinder(rpc_url)

transaction, contractAddress = finder.getLastBuy(walletAddress) 

#transaction, contractAddress = "", "" 

# comment out line 143 and uncomment out the line above and replace it with their tx and CA if it's an older buy

if transaction is None or contractAddress is None:
    print("could not retrieve main wallet transaction details")
    sys.exit(1)

block = finder.getBlockHash(transaction)

mainTransaction, mainBlock, potentialCopyTraders = finder.getPotentialCopyTraders(block, walletAddress, contractAddress, blockLimit=blockLimit, txLimit=txLimit)

output_data = {
    walletAddress: {
        "mainTranscation": mainTransaction,
        "main_block": mainBlock,
        "potential_copy_traders": {}
    }
}

for copyWallet, transcation, contestantBlock in potentialCopyTraders:
    block_delay = contestantBlock - mainBlock
    output_data[walletAddress]["potential_copy_traders"][copyWallet] = {
        "hash": transcation,
        "block delay": block_delay
    }

filename = f"copytraders_{shorten(walletAddress)}_{shorten(contractAddress)}.json"
with open(filename, "w") as outfile:
    json.dump(output_data, outfile, indent=4)

print(f"Target Wallet: {walletAddress} - {shorten(mainTransaction)} - Block: {mainBlock}")
print("\nPotential copy traders:")

for idx, (copyWallet, transaction, contestantBlock) in enumerate(potentialCopyTraders, start=1):
    block_delay = contestantBlock - mainBlock
    print(f"{idx}. {copyWallet} - {shorten(transcation)} - Block: {contestantBlock} (Delay: {block_delay} blocks)")

print(f"\n\ncheck {filename} for more info")
