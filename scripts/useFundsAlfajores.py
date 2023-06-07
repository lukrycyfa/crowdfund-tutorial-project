import os
from .utility import *
from brownie import config, accounts, network, FundRaiser
from brownie.network.gas.strategies import LinearScalingStrategy
import json


Funds = {}
gas_strategy = LinearScalingStrategy("10 gwei", "50 gwei", 1.1)
metamaskAccounts = [accounts.add(config["wallets"]["from_key0"]), accounts.add(config["wallets"]["from_key1"]), accounts.add(config["wallets"]["from_key2"])] 
try:
    with open('./build/deployments/deployAlfajores.json', 'r') as alfajores:
        adr = json.load(alfajores)     
        Funds = FundRaiser.at(adr["address"])
    
except Exception as e:
    print(e.args)
    print("pls Deploy A Contract On ALfajores First")
    quit()    

# Called To Make Donations And Mint Tokens
def donate_mint():
    while True:
        print("You Get To Mint One Image For Each Donation"), print("Type q to quit"), print(network.show_active())
        print("pick An account to interact with your contract")
        for acc in range(len(metamaskAccounts)):
            if acc == 0:
                continue
            print(f"{acc}.", metamaskAccounts[acc])
        accIdx = enterIdx((len(metamaskAccounts)))   
        img_lst = os.listdir("./nfts/images")
        donation = enterValDonation()
        for i, r in enumerate(img_lst):
            print(f"{i}.", r)
        print("Pick One Nft To Mint")
        get_nft = enterIdx(len(img_lst))
        with open(f"./nfts/images/{img_lst[get_nft]}", 'rb') as img_file: # this block of code downwards require network
            try:
                curtoken = Funds.totalSupply()
                tokenId = curtoken + 1  
                upd = upload_img_to_ipfs(img_file, f'{img_lst[get_nft]}')
                if upd[1].status_code == 200:
                    print(upd[0])            
                    with open(f"./nfts/metadata/{img_lst[get_nft][0:-4]}.json", 'r') as meta_file:    
                        file = json.load(meta_file)
                        new_meta = {}
                        new_meta['image'], new_meta['owner'], new_meta['tokenId'] = upd[0], str(metamaskAccounts[accIdx]), tokenId
                        for l, v in enumerate(file):
                            new_meta[v] = file[v]        
                        meta_upd = upload_nft_meta(new_meta)
                        if meta_upd[1].status_code == 200:
                            Funds.Donate({'from':metamaskAccounts[accIdx], 'value':donation, 'gas_price':gas_strategy})
                            Funds.safeMint(meta_upd[0], {'from':metamaskAccounts[accIdx], 'gas_price':gas_strategy})
                            new_meta['metaUrl'] = meta_upd[0]  
                            with open(f"./nfts/awardalfajores/awd_{tokenId}.json", 'w') as awd_meta:
                                json.dump(new_meta, awd_meta, indent=4)
                            print("Token Metadata Succefully uploaded to Ipfs, and a copy created in nft/awardalfajores/ dir"), print(" "), print(" ")     
                        else:
                            print("Unable To Upload Metadata To Ipfs")     
                else:
                    print("Unable To Upload Image To Ipfs")            
            except Exception as e:
                print(e.args)                   


# Called To Post Content
def returnPosts_Pst():
    while True:
        print("Post To Add Content To The Blog"), print("pick An account to interact with your contract"), print(network.show_active())
        for acc in range(len(metamaskAccounts)):
            print(f"{acc}.", metamaskAccounts[acc])
        post_lst = Funds.ReturnPosts()
        print(" "), print("pick An account to interact with your contract")        
        accIdx = enterIdx((len(metamaskAccounts)))
        print(" "), print("~POSTS~")
        for pst in post_lst:
            print(f"Id.{pst[0]}", f"Author:{pst[1][0:9]+'...'+pst[1][-9:-1]}", f"Slug:{pst[3]}", f"Post:{pst[2]}", f"Likes:{pst[4]}")
        print(" "), print("Post Some content to the blog") 
        post = enterPost()
        Funds.NewPost(post, f"{post[0:15]}...", {'from': metamaskAccounts[accIdx], 'gas_price':gas_strategy})
        print(f" Added a New post ~ {post[0:15]}..."), print(" "), print(" ")


# Called To Like And Unlike Post's
def like_unlikePst():
    while True:
        print("LIke and unlike Post"), print("pick An account to interact with your contract"), print(network.show_active())
        for acc in range(len(metamaskAccounts)):
            print(f"{acc}.", metamaskAccounts[acc])
        post_lst = Funds.ReturnPosts()
        print(" "), print("pick An account to interact with your contract")
        accIdx = enterIdx((len(metamaskAccounts)))
        print(" "), print("~POSTS~")
        for pst in post_lst:
            print(f"Id.{pst[0]}", f"Author:{pst[1][0:9]+'...'+pst[1][-9:-1]}", f"Slug:{pst[3]}", f"Post:{pst[2]}", f"Likes:{pst[4]}")    
        print(" "), print("pick a post ID to like and unlike")  
        idx = enterIdx(len(post_lst))
        Funds.LikeandUnlikePost(post_lst[idx][0] , {'from':metamaskAccounts[accIdx], 'gas_price':gas_strategy})
        print(f"Like status updated for post with Id ~ {idx}"), print(" "), print(" ")
 