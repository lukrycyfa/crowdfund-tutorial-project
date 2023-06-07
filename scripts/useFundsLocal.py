import os
from .utility import *
from brownie import accounts, network, FundRaiser
from brownie.network.gas.strategies import LinearScalingStrategy


Funds = {}
gas_strategy = LinearScalingStrategy("10 gwei", "50 gwei", 1.1)
try:
    with open('./build/deployments/deployLocal.json', 'r') as local:
        adr = json.load(local)     
        Funds = FundRaiser.at(adr["address"])    
except Exception as e:
    print(e.args)
    print("pls Deploy A Contract On The Local Network First")
    quit()    

# Called To Make Donations And Mint Tokens
def donate_mint():
    while True:
        print("You Get To Mint One Image For Each Donation"), print("Type q to quit"), print(network.show_active())
        print("pick An account to interact with your contract")
        for acc in range(8):
            print(f'{acc}.', accounts[acc])
        accIdx = enterIdx(8)    
        img_lst = os.listdir("./nfts/images")
        donation = enterValDonation()
        for i, r in enumerate(img_lst):
            print(f"{i}.", r)
        print("Pick One Nft To Mint")
        get_nft = enterIdx(len(img_lst))
        curtoken = Funds.totalSupply()
        tokenId = curtoken + 1  
        with open(f"./nfts/metadata/{img_lst[get_nft][0:-4]}.json", 'r') as meta_file:    
            file = json.load(meta_file)
            new_meta = {}
            new_meta['image'], new_meta['owner'], new_meta['tokenId'] = f"./nfts/images/{img_lst[get_nft]}", str(accounts[accIdx]), tokenId
            for l, v in enumerate(file):
                new_meta[v] = file[v]
        # since we don't have a local ipfs we would just use the meta directory path as the url.
        try:        
            Funds.Donate({'from':accounts[accIdx], 'value':donation, 'gas_price':gas_strategy})
            Funds.safeMint(f"./nfts/metadata/{img_lst[get_nft][0:-4]}.json", {'from':accounts[accIdx], 'gas_price':gas_strategy})
            new_meta['metaUrl'] = f"./nfts/metadata/{img_lst[get_nft][0:-4]}.json"  
            with open(f"./nfts/awardlocal/awd_{tokenId}.json", 'w') as awd_meta:
                json.dump(new_meta, awd_meta, indent=4)
            print("Token Minted Succefully, and a copy created in nft/awardlocal/ dir"), print(" "), print(" ")
        except Exception as e:
                print(e.args)                           


# Called To Post Content
def returnPosts_Pst():
    while True:
        print("Post To Add Content To The Blog"), print("pick An account to interact with your contract"), print(network.show_active())
        for acc in range(8):
            print(f"{acc}.", accounts[acc])
        post_lst = Funds.ReturnPosts()
        print(" "), print("pick An account to interact with your contract")        
        accIdx = enterIdx(8)
        print(" "), print("~POSTS~")
        for pst in post_lst:
            print(f"Id.{pst[0]}", f"Author:{pst[1][0:9]+'...'+pst[1][-9:-1]}", f"Slug:{pst[3]}", f"Post:{pst[2]}", f"Likes:{pst[4]}")
        print(" "), print("Post Some content to the blog") 
        post = enterPost()
        Funds.NewPost(post, f"{post[0:15]}...", {'from': accounts[accIdx], 'gas_price':gas_strategy})
        print(f" Added a New post ~ {post[0:15]}..."), print(" "), print(" ")


# Called To Like And Unlike Post's
def like_unlikePst():
        while True:
            print("LIke and unlike Post"), print("pick An account to interact with your contract"), print(network.show_active())
            for acc in range(8):
                print(f"{acc}.", accounts[acc])
            post_lst = Funds.ReturnPosts()
            print(" "), print("pick An account to interact with your contract")    
            accIdx = enterIdx(8)
            print(" "), print("~POSTS~")
            for pst in post_lst:
                print(f"Id.{pst[0]}", f"Author:{pst[1][0:9]+'...'+pst[1][-9:-1]}", f"Slug:{pst[3]}", f"Post:{pst[2]}", f"Likes:{pst[4]}")
            print(" "), print("pick a post Id to like and unlike")  
            idx = enterIdx(len(post_lst))
            Funds.LikeandUnlikePost(post_lst[idx][0] , {'from':accounts[accIdx], 'gas_price':gas_strategy})
            print(f"Like status updated for post with Id ~ {idx}"), print(" "), print(" ")


#add a litile more test to the test script    