import sys
import json
import random
import tls_client
import csv

from fake_useragent import UserAgent

with open('config.json') as f:
    config = json.load(f)

shorten = lambda s: f"{s[:4]}...{s[-5:]}" if len(s) >= 9 else s

botAccounts = {
    "LUNARCc6FmA3hzPrwmXW3z6RNX1MYXhKS4opYoqCm9P": "Lunar",
    "vs1ongEMwP15z6RKykbUbWwAf8WXFKNTLkfEr5JN6K7": "VisionAIO",
    "BSfD6SHZigAfDWSjzD5Q41jw8LmKwtmjskPH9XW1mrRW": "Photon",
    "7HeD6sLLqAnKVRuSfc1Ko3BSPMNKWgGTiWLKXJF31vKM": "Bloom",
    "b1oomGGqPKGD6errbyfbVMBuzSC8WtAAYo8MwNafWW1": "Bloom",
    "GengarGzVQiNwzmXFC6sz3oT4HY91MnV26nDX6z2U97V": "SharpAIO",
    "minTcHYRLVPubRK8nt6sqe2ZpWrGDLQoNLipDJCGocY": "Mintech",
    "6m2CDdhRgxpH4WjvdzxAYbGxwdGUz5MziiL5jek2kBma": "OKX",
    "BANANAjs7FJiPQqJTGFzkZJndT9o7UmKiYYGaJz6frGu": "Banana Gun",
    "9QT9pBnnvrRXdEdkYhp5KrB9SqgTopmmVNunUm726DbJ": "StarkDex Bot",
    "97VmzkjX9w8gMFS2RnHTSjtMEDbifGXBq9pgosFdFnM": "TradeWiz",
    "CABAL69DYBisjkdHxwVktMy2TPHYVYc2D3UDQQ2DLwKM": "Cabal Bot",
    "b1oodtXw4tigt8MoRcRrWUGCW31WeFUtFMsFgwQpSQ9": "Blood",
    "Axiom3a2w1UbMt2SMgqSvRiuJFTPusDhwKamNgPTeNQ9": "Axiom",
    "PEPPER3dYQpY2TTqHp3XinzRu519X7GswmVNb5tqK8L": "Peppermints"    
}

feeWallets = {
    "97VmzkjX9w8gMFS2RnHTSjtMEDbifGXBq9pgosFdFnM": "TradeWiz",
    "BB5dnY55FXS1e1NXqZDwCzgdYJdMCj3B92PU6Q5Fb6DT": "GMGN",
    "28KqHiudrpzfVkVWQ1jztQ2Aarf4W3CvTitjWEqTCkpA": "BullX",
    "HWEoBxYs7ssKuudEjzjmpfJVX7Dvi7wescFsVx2L5yoY": "Bloxroute",
    "7ks326H4LbMVaUC8nW5FpC5EoAf5eK5pf4Dsx4HDQLpq": "Bloxroute",
    "TEMPaMeCRFAS9EKF53Jd6KpHxgL47uWLcpFArU1Fanq": "Temporal",
    "noz3jAjPiHuBPqiSPkkugaJDkJscPuRhYnSpbi8UvC4": "Temporal",
    "noz3str9KXfpKknefHji8L1mPgimezaiUyCHYMDv1GE": "Temporal",
    "noz6uoYCDijhu1V7cutCpwxNiSovEwLdRHPwmgCGDNo": "Temporal",
    "noz9EPNcT7WH6Sou3sr3GGjHQYVkN3DNirpbvDkv9YJ": "Temporal",
    "nozc5yT15LazbLTFVZzoNZCwjh3yUtW86LoUyqsBu4L": "Temporal",
    "nozFrhfnNGoyqwVuwPAW4aaGqempx4PU6g6D9CJMv7Z": "Temporal",
    "nozievPk7HyK1Rqy1MPJwVQ7qQg2QoJGyP71oeDwbsu": "Temporal",
    "noznbgwYnBLDHu8wcQVCEw6kDrXkPdKkydGJGNXGvL7": "Temporal",
    "nozNVWs5N8mgzuD3qigrCG2UoKxZttxzZ85pvAQVrbP": "Temporal",
    "nozpEGbwx4BcGp6pvEdAh1JoC2CQGZdU6HbNP1v2p6P": "Temporal",
    "nozrhjhkCr3zXT3BiT4WCodYCUFeQvcdUkM7MqhKqge": "Temporal",
    "nozrwQtWhEdrA6W8dkbt9gnUaMs52PdAv5byipnadq3": "Temporal",
    "nozUacTVWub3cL4mJmGCYjKZTnE9RbdY5AP46iQgbPJ": "Temporal",
    "nozWCyTPppJjRuw2fpzDhhWbW355fzosWSzrrMYB1Qk": "Temporal",
    "nozWNju6dY353eMkMqURqwQEoM3SFgEKC6psLCSfUne": "Temporal",
    "nozxNBgWohjR75vdspfxR5H9ceC7XXH99xpxhVGt3Bb": "Temporal",
    "NexTbLoCkWykbLuB1NkjXgFWkX9oAtcoagQegygXXA2": "Next Block 1",
    "nextBLoCkPMgmG8ZgJtABeScP35qLa2AMCNKntAP7Xc": "Next Block 2",
    "NextbLoCkVtMGcV47JzewQdvBpLqT9TxQFozQkN98pE": "Next Block 3",
    "NEXTbLoCkB51HpLBLojQfpyVAMorm3zzKg7w9NFdqid": "Next Block 4",
    "NeXTBLoCKs9F1y5PJS9CKrFNNLU1keHW71rfh7KgA1X": "Next Block 5",
    "neXtBLock1LeC67jYd1QdAa32kbVeubsfPNTJC1V5At": "Next Block 6",
    "nEXTBLockYgngeRmRrjDV31mGSekVPqZoMGhQEZtPVG": "Next Block 7",
    "96gYZGLnJYVFmbjzopPSU6QiEV5fGqZNyN9nmNhvrZU5": "Jito1",
    "HFqU5x63VTqvQss8hp11i4wVV8bD44PvwucfZ2bU7gRe": "Jito2",
    "Cw8CFyM9FkoMi7K7Crf6HNQqf4uEMzpKw6QNghXLvLkY": "Jito3",
    "ADaUMid9yfUytqMBgopwjb2DTLSokTSzL1zt6iGPaS49": "Jito4",
    "DfXygSm4jCyNCybVYYK6DwvWqjKee8pbDmJGcLWNDXjh": "Jito5",
    "ADuUkR4vqLUMWXxW9gh6D6L8pMSawimctcNZ5pGwDcEt": "Jito6",
    "DttWaMuVvTiduZRnguLF7jNxTgiMBZ1hyAumKUiL2KRL": "Jito7",
    "3AVi9Tg9Uo68tJfuvoKvqKNWKkC5wPdSSdeBnizKZ6jT": "Jito8",
    "6fQaVhYZA4w3MBSXjJ81Vf6W1EDYeUPXpgVQ6UQyU1Av": "0slot",
    "4HiwLEP2Bzqj3hM2ENxJuzhcPCdsafwiet3oGkMkuQY4": "0slot",
    "7toBU3inhmrARGngC7z6SjyP85HgGMmCTEwGNRAcYnEK": "0slot",
    "8mR3wB1nh4D6J9RUCugxUpc6ya8w38LPxZ3ZjcBhgzws": "0slot",
    "6SiVU5WEwqfFapRuYCndomztEwDjvS5xgtEof3PLEGm9": "0slot",
    "TpdxgNJBWZRL8UXF5mrEsyWxDWx9HQexA9P1eTWQ42p": "0slot",
    "D8f3WkQu6dCF33cZxuAsrKHrGsqGP2yvAHf8mX6RXnwf": "0slot",
    "GQPFicsy3P3NXxB5piJohoxACqTvWE9fKpLgdsMduoHE": "0slot",
    "Ey2JEr8hDkgN8qKJGrLf2yFjRhW7rab99HVxwi5rcvJE": "0slot",
    "4iUgjMT8q2hNZnLuhpqZ1QtiV8deFPy2ajvvjEpKKgsS": "0slot",
    "3Rz8uD83QsU8wKvZbgWAPvCNDU6Fy8TSZTMcPm3RB6zt": "0slot",
    "FCjUJZ1qozm1e8romw216qyfQMaaWKxWsuySnumVCCNe": "0slot",
}


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
                activities = self.sendRequest.get(url, headers=self.headers).json()['data']['activities']
                for activity in activities:
                    if activity.get("event_type") == "buy":
                        transaction = activity['tx_hash']
                        contractAddress = activity['token']['address']
                        return transaction, contractAddress
                print(f"failed to get last buy from {walletAddress}, last buy may be a transferred token")
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
                    "maxSupportedTransactionVersion": 0,
                    "commitment": "confirmed"
                }
            ]
        }
        response = self.sendRequest.post(self.rpc_url, json=payload)
        txData = response.json()

        if txData["result"]['meta']["err"] is not None:
            return None, txData
        block = int(txData['result']['slot'])
        return block, txData
    
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
                        "rewards": False,
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
                txWindow = transactions
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

def getFeeInfo(tx_data):
    feePaidTo = {}
    feePaid = 0
    instructions = tx_data["result"]["transaction"]["message"]["instructions"]
    for instr in instructions:
        if "parsed" in instr and instr["parsed"].get("type") == "transfer":
            info = instr["parsed"].get("info", {})
            dest = info.get("destination")
            lamports = int(info.get("lamports", 0))
            if dest in feeWallets:
                solAmount = lamports / 1_000_000_000
                feePaidTo[feeWallets[dest]] = solAmount
                feePaid += solAmount
    return feePaidTo, feePaid

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

# comment out line 232 and uncomment out the line above and replace it with their tx and CA if it's an older buy

if transaction is None or contractAddress is None:
    print("could not retrieve main wallet transaction details")
    sys.exit(1)

mainBlock, main_tx_data = finder.getBlockHash(transaction)
if mainBlock is None:
    print("Main transaction failed; cannot proceed.")
    sys.exit(1)

output_data = {
    walletAddress: {
        "contractAddress": contractAddress,
        "mainTranscation": transaction,
        "mainBlock": mainBlock,
        "potentialCopyTraders": {}
    }
}

mainTx, mainBlock, potentialCopyTraders = finder.getPotentialCopyTraders(mainBlock, walletAddress, contractAddress, blockLimit=blockLimit, txLimit=txLimit)
for copyWallet, tx_signature, contestantBlock in potentialCopyTraders:
    blockDelay = contestantBlock - mainBlock
    
    botUsed = botAccounts.get(copyWallet, "")
    feePaidTo = {}
    feePaid = 0
    try:
        result = finder.getBlockHash(tx_signature)
        if result[0] is None:
            continue
        tx_data = result[1]
        instructions = tx_data["result"]["transaction"]["message"]["instructions"]
        for instr in instructions:
            if "programId" in instr and instr["programId"] in botAccounts:
                botUsed = botAccounts[instr["programId"]]
                break
        feePaidTo, feePaid = getFeeInfo(tx_data)
    except Exception as e:
        print(f"Error retrieving details for transaction {tx_signature}: {e}")
    
    output_data[walletAddress]["potentialCopyTraders"][copyWallet] = {
        "hash": tx_signature,
        "blockDelay": blockDelay,
        "botUsed": botUsed,
        "feePaidTo": feePaidTo,
        "feePaid": feePaid
    }

filename = f"results/copytraders_{shorten(walletAddress)}_{shorten(contractAddress)}.json"
with open(filename, "w") as outfile:
    json.dump(output_data, outfile, indent=4)

csv_filename = f"results/copytraders_{shorten(walletAddress)}_{shorten(contractAddress)}.csv"
with open(csv_filename, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["WalletAddress", "Trader", "TxSignature", "BlockDelay", "BotUsed", "FeePaidTo", "FeePaid"])
    for trader, data in output_data[walletAddress]["potentialCopyTraders"].items():
        writer.writerow([
            walletAddress,
            trader,
            data["hash"],
            data["blockDelay"],
            data["botUsed"],
            json.dumps(data["feePaidTo"]),
            data["feePaid"]
        ])

print(f"Target Wallet: {walletAddress} - {shorten(transaction)} - Block: {mainBlock}")
print("\nPotential copy traders:")

potential_copy_list = finder.getPotentialCopyTraders(mainBlock, walletAddress, contractAddress, blockLimit=blockLimit, txLimit=txLimit)[2]
for idx, (copyWallet, txSignature, contestantBlock) in enumerate(potential_copy_list, start=1):

    blockDelay = contestantBlock - mainBlock
    botUsed = botAccounts.get(copyWallet, "")
    feePaidTo = {}
    feePaid = 0

    try:
        result = finder.getBlockHash(txSignature)
        if result[0] is None:
            continue
        txData = result[1]
        instructions = txData["result"]["transaction"]["message"]["instructions"]
        for instr in instructions:
            if "programId" in instr and instr["programId"] in botAccounts:
                botUsed = botAccounts[instr["programId"]]
                break
        feePaidTo, feePaid = getFeeInfo(txData)
    except Exception as e:
        print(f"Error retrieving details for transaction {txSignature}: {e}")
    botInfo = f" (Bot: {botUsed})" if botUsed else ""
    print(f"{idx}. {copyWallet} - {shorten(txSignature)} - Block: {contestantBlock} (Delay: {blockDelay} blocks){botInfo} | FeePaidTo: {feePaidTo}, FeePaid: {feePaid}")

print(f"\n\nCheck {filename} and {csv_filename} for more info")
