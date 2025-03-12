<h1 align="center">
	<img src="https://i.imgur.com/rA7czJZ.png" width="150px"><br>
    Solana Contested Wallet Checker
</h1>
<p align="center">
	Check if a wallet is contested with potential copy traders on Solana. 
</p>
<h1 align="left">
Setup
</h1>

Add your RPC URL to config.json. (Go to https://helius.dev if you don't have one)<br><br>
Add your target wallet address to config.json (use the test ones below if you don't have)<br><br>
Edit your block and transaction limit<br><br>

Block Limit - how many blocks after the target wallet you wanna check until<br><br>
Transaction Limit - amount of transcations you want to check in that block

<details open>
<summary>Test Wallets</summary>
<br>
Cupsey <code>suqh5sHtr8HyJ7q8scBimULPkPpA557prMG47xCHQfK</code><br>
Euris - <code>DfMxre4cKmvogbLrPigxmibVTTQDuzjdXojWzjCXXhzj</code><br>
Waddles - <code>73LnJ7G9ffBDjEBGgJDdgvLUhD5APLonKrNiHsKDCw5B</code><br>
Gake - <code>DNfuF1L62WWyW3pNakVkyGGFzVVhj4Yr52jSmdTyeBHm</code>
</details>

<h1 align="left">
Installation
</h1>

`
pip install -r requirements.txt
`
<br><br>
`
python main.py
`
