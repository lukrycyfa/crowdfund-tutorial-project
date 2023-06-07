import pytest
from brownie import accounts, network
from brownie.network.gas.strategies import LinearScalingStrategy


gas_strategy =  LinearScalingStrategy("10 gwei", "50 gwei", 1.1)

@pytest.fixture(scope="module", autouse=True)
def Funds(FundRaiser):
    yield FundRaiser.deploy({'from': accounts[0], "gas_price":gas_strategy})

@pytest.fixture(autouse=True) 
def isolation(fn_isolation):
    pass

def test_nftfunds_Donate_functions(Funds):
    """
    Test Minting And Donation Functions.
    """
    print(network.show_active())
    assert Funds.owner() == accounts[0]
    Funds.Donate({'from':accounts[1], 'value':2000000000000000000, 'gas_price':gas_strategy})
    Funds.safeMint("new/nft/acc1", {'from': accounts[1], 'gas_price':gas_strategy})
    Funds.Donate({'from':accounts[2], 'value':4000000000000000000, 'gas_price':gas_strategy})
    Funds.safeMint("new/nft/acc2", {'from': accounts[2], 'gas_price':gas_strategy})
    assert Funds._donationtBalance() == 6000000000000000000
    assert Funds._TotalDonations() == 6000000000000000000
    Funds.TransferDonations(accounts[3],{'from':Funds.owner(), 'value':2400000000000000000, 'gas_price':gas_strategy})
    assert Funds._donationtBalance() == 3600000000000000000
    assert Funds._TotalDonations() == 6000000000000000000
    assert Funds.ownerOf(1) == accounts[1]
    assert Funds.ownerOf(2) == accounts[2]


def test_nftfunds_Blog_functions(Funds, accounts):
    """
    Test Blogs Post And Like Functions.
    """
    print(network.show_active())
    Funds.NewPost("You have a new Post", "You have...", {'from': accounts[1], 'gas_price':gas_strategy})
    Funds.NewPost("Another post from another accouunt", "Another post...", {'from': accounts[2], 'gas_price':gas_strategy})
    Funds.LikeandUnlikePost(0, {'from': accounts[2], 'gas_price':gas_strategy})
    Funds.LikeandUnlikePost(1, {'from': accounts[1], 'gas_price':gas_strategy})
    Posts = Funds.ReturnPosts()
    assert Posts[0][2] == "You have a new Post"
    assert Posts[0][1] == accounts[1]
    assert Posts[0][4] == 1
    assert Posts[1][2] == "Another post from another accouunt"
    assert Posts[1][1] == accounts[2]
    assert Posts[1][4] == 1
    P1 = Funds.ReturnLiked(0, {'from': accounts[2]})
    P2 = Funds.ReturnLiked(1, {'from': accounts[1]})
    assert P1 == True
    assert P2 == True
    Funds.LikeandUnlikePost(0, {'from': accounts[2], 'gas_price':gas_strategy})
    Funds.LikeandUnlikePost(1, {'from': accounts[1], 'gas_price':gas_strategy})
    P1 = Funds.ReturnLiked(0, {'from': accounts[2]})
    P2 = Funds.ReturnLiked(1, {'from': accounts[1]})
    assert P1 == False
    assert P2 == False
    Funds.DeletePost(0,  {'from': accounts[1], 'gas_price':gas_strategy})
    Posts = Funds.ReturnPosts()
    assert len(Posts) == 1