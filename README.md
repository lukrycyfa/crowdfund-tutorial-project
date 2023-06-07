# Getting Started With CrowdFund-Dapp

- This project was created To this [Crowdfund-Tutorial](http://place-link-here) 

## Requirements

- [Node.js](https://nodejs.org/en/download)

- [Python](https://www.python.org/downloads/)

## Installations

### Install Ganche-cli

```bash
npm install ganache --global
```
### Clone The project From This Repo

```bash
git clone https://github.com/lukrycyfa/Crowdfund-Dapp.git
```
### Cd Into The Root Directory

```bash
pip install -r requirements.txt
```
### Install Contract Dependencies

```bash
brownie pm install OpenZeppelin/openzeppelin-contracts@4.8.2
```
## Testing Contract On Ganache Local Network

### Start Ganache-cli On A Separate Terminal

```bash
ganache-cli
```
### Compile, Deploy And Test The Contract On Ganache.

```bash
brownie compile
```
```bash
brownie run deploy.py
```
```bash
brownie test tests/test_OnGanache.py
```


## Testing The Contract On Celo Alfajores Network

### Add The Alfajores Network To Brownie

```bash
brownie networks add Alfajores alfajores host=https://alfajores-forno.celo-testnet.org chainid=44787 explorer=https://alfajores-blockscout.celo-testnet.org
```

### Add Your Metamask Private Key To The .env file in the root

- create a .env file in the root directory
- create three metamask accounts, export the private keys and update this keys

```yaml
export PRIVATE_KEY_OWNER="Your Metamask Private Key One"
export PRIVATE_KEY_ACC1="Your Metamask Private Key Two"
export PRIVATE_KEY_ACC2="Your Metamask Private Key Three"
```

### Compile, Deploy And Test The Contract On Alfajores

```bash
brownie compile
```
```bash
brownie run deploy.py --network alfajores
```
```bash
brownie test tests/test_OnAlfajores.py --network alfajores
```

- This Project requires api keys from pinata ipfs for storing images and metadata so head over to [Pinata Ipfs](https://app.pinata.cloud/). Sign up with pinata, get a secret key and an api key instructions on that are found in the doc's [Authentication](https://docs.pinata.cloud/pinata-api/authentication).

- To make use of these script's `./scripts/useFundsAlfajores.py` and `./scripts/useFundsLocal.py` you will need to go through the generative art section in the [tutorial](https://app.pinata.cloud/). Then update these key's below in your .env file.

```yaml
export API_KEY=your api key
export SECRET_API_KEY=your api secret key
```

