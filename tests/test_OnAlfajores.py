import pytest
from brownie import accounts, network, config
from brownie.network.gas.strategies import LinearScalingStrategy


gas_strategy =  LinearScalingStrategy("10 gwei", "50 gwei", 1.1)

metamaskAccounts = [accounts.add(config["wallets"]["from_key0"]), accounts.add(config["wallets"]["from_key1"]), accounts.add(config["wallets"]["from_key2"])] 

@pytest.fixture(scope="module", autouse=True)
def Funds(FundRaiser):
    yield FundRaiser.deploy({'from': metamaskAccounts[0], "gas_price":gas_strategy})


def test_nftfunds_Donate_functions(Funds):
    """
    Test Minting And Donation Functions.
    """
    print(network.show_active())
    assert Funds.owner() == metamaskAccounts[0]
    Funds.Donate({'from':metamaskAccounts[1], 'value':2000000000000000000, 'gas_price':gas_strategy})
    Funds.safeMint("new/nft/acc1", {'from': metamaskAccounts[1], 'gas_price':gas_strategy})
    Funds.Donate({'from':metamaskAccounts[2], 'value':2000000000000000000, 'gas_price':gas_strategy})
    Funds.safeMint("new/nft/acc2", {'from': metamaskAccounts[2], 'gas_price':gas_strategy})
    assert Funds._donationtBalance({'from': metamaskAccounts[0]}) == 4000000000000000000
    assert Funds._TotalDonations() == 4000000000000000000
    Funds.TransferDonations(metamaskAccounts[2],{'from':metamaskAccounts[0], 'value':2400000000000000000, 'gas_price':gas_strategy})
    assert Funds._donationtBalance({'from': metamaskAccounts[0]}) == 1600000000000000000
    assert Funds._TotalDonations() == 4000000000000000000
    assert Funds.ownerOf(1) == metamaskAccounts[1]
    assert Funds.ownerOf(2) == metamaskAccounts[2]


def test_nftfunds_Blog_functions(Funds):
    """
    Test Blogs Post And Like Functions.
    """
   
    print(network.show_active())
    Funds.NewPost("You have a new Post", "You have...", {'from': metamaskAccounts[1], 'gas_price':gas_strategy})
    Funds.NewPost("Another post from another accouunt", "Another post...", {'from': metamaskAccounts[2], 'gas_price':gas_strategy})
    Funds.LikeandUnlikePost(0, {'from': metamaskAccounts[2], 'gas_price':gas_strategy})
    Funds.LikeandUnlikePost(1, {'from': metamaskAccounts[1], 'gas_price':gas_strategy})
    Posts = Funds.ReturnPosts()
    assert Posts[0][2] == "You have a new Post"
    assert Posts[0][1] == metamaskAccounts[1]
    assert Posts[0][4] == 1
    assert Posts[1][2] == "Another post from another accouunt"
    assert Posts[1][1] == metamaskAccounts[2]
    assert Posts[1][4] == 1
    P1 = Funds.ReturnLiked(0, {'from': metamaskAccounts[2]})
    P2 = Funds.ReturnLiked(1, {'from': metamaskAccounts[1]})
    assert P1 == True
    assert P2 == True
    Funds.LikeandUnlikePost(0, {'from': metamaskAccounts[2], 'gas_price':gas_strategy})
    Funds.LikeandUnlikePost(1, {'from': metamaskAccounts[1], 'gas_price':gas_strategy})
    P1 = Funds.ReturnLiked(0, {'from': metamaskAccounts[2]})
    P2 = Funds.ReturnLiked(1, {'from': metamaskAccounts[1]})
    assert P1 == False
    assert P2 == False
    Funds.DeletePost(0,  {'from': metamaskAccounts[1], 'gas_price':gas_strategy})
    Posts = Funds.ReturnPosts()
    assert len(Posts) == 1
   