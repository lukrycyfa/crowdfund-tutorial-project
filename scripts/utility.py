import requests
import json
from brownie import config

# Upload Images to Ipfs
def upload_img_to_ipfs(img, img_name):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

    payload={'pinataOptions': '{"cidVersion": 1}',
    'pinataMetadata': '{"name": "MyFile", "keyvalues": {"company": "Pinata"}}'}
    files=[
    ('file',(img_name,img,'application/octet-stream'))
    ]
    headers = {'pinata_api_key':config["pinata_keys"]["api_key"], 
    'pinata_secret_api_key':config["pinata_keys"]["secret_api_key"]}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print("Uploading Image To Ipfs.....")
    res = response.json()
    print(res['IpfsHash'], "image")

    return [f'https://gateway.pinata.cloud/ipfs/{res["IpfsHash"]}', response]

# Upload Metadata To Ipfs
def upload_nft_meta(nft_meta):
    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

    payload = json.dumps({
    "pinataContent": nft_meta 
    })
    headers = {
    'Content-Type': 'application/json',
    'pinata_api_key':config["pinata_keys"]["api_key"], 
    'pinata_secret_api_key':config["pinata_keys"]["secret_api_key"]
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print("Uploading metadata To Ipfs.....")
    res = response.json()
    print(res['IpfsHash'], "metadata")

    return [f'https://ipfs.io/ipfs/{res["IpfsHash"]}', response]

# Takes Input For Donation Value
def enterValDonation():
    state = True
    val = 0
    while state:
        num = input("enter amount to donate or q to quit:") 
        if num  == 'q':
            quit()
        else:        
            try:
                assert type(float(num) or int(num))
                if type(float(num)):
                    val = float(num) * 10 ** 18
                    state = False
                if type(int(num)):
                    val = int(num) * 10 ** 18
                    state = False
            except Exception as e:
                print(e.args)
                print("pls use an integer or a float value")
    return val 

# Takes Inputs For Indexes
def enterIdx(count):
    state = True
    val = 0
    while state:
        num = input("input an index or type q to quit:") 
        if num  == 'q':
            quit()
        else:     
            try:
                assert type(int(num))
                assert count > int(num) >=0
                val = int(num)
                state = False
            except Exception as e:
                print(e.args)
                print("Input Value Out Of Range")
    return val
  
# Takes Inputs for Posts
def enterPost():
    state = True
    stg = ""
    while state:
        stg = input("enter a post or type q to quit:")
        if stg  == 'q':
            quit()
        else:        
            try:
                assert len(stg) > 0
                state = False
            except Exception as e:
                print(e.args)
                print("Please input a string")
    return stg
