// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;

import "OpenZeppelin/openzeppelin-contracts@4.8.2/contracts/token/ERC721/ERC721.sol";
import "OpenZeppelin/openzeppelin-contracts@4.8.2/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "OpenZeppelin/openzeppelin-contracts@4.8.2/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "OpenZeppelin/openzeppelin-contracts@4.8.2/contracts/access/Ownable.sol";
import "OpenZeppelin/openzeppelin-contracts@4.8.2/contracts/utils/Counters.sol";


contract FundRaiser is ERC721, ERC721Enumerable, ERC721URIStorage, Ownable {

  
    /**
     * @dev Id's Counter's
     */  
    using Counters for Counters.Counter;
    using Counters for Counters.Counter;
    using Counters for Counters.Counter;
    using Counters for Counters.Counter; 
    Counters.Counter private _DonorsCount;
    Counters.Counter private _PostsCount;
    Counters.Counter private _ActPstCount; 
    Counters.Counter private _tokenIdCounter;

    /**
     * @dev Balances
     */  
    uint public _TotalDonations;
    uint private _DonationBalance;

    /**
     * @dev Donors Construct
     */  
    struct Donor{ 
        uint donorsIdx;  
        address adr;  
        uint amount; 
        uint donCount;    
    }

    /**
     * @dev Post Construct
     */  
    struct Post{ 
        uint postIdx;  
        address author;  
        string post;
        string slug;
        uint likecount;     
    }

    /**
     * @dev likeAdrs Construct
     */ 
    struct likeAdrs{
      address user;
      bool liked;
    }

    /**
     * @dev Construct Mappings
     */ 
    mapping(uint => mapping(address => likeAdrs)) public PostLikes;

    mapping(uint => Post) public AllPosts;

    mapping(address  => Donor) public AllDonors;

    address[] public DonorsAdrLst;

    
    //Initiated At first Contract Deployment.
    constructor() ERC721("FundRaiserNFTs", "FRN") { 
          // Initialize the tokenIdCounter to start 1
         _tokenIdCounter.increment();
    }


    /**
     * @dev Event Emmiters
     */ 
    event TokenMinted( address sender, uint tokenId );
    event DonationMade( address sender, uint amount );
    event DonationTransfered( address sender, uint amount ); 
    event NewPostAdded( address sender, string slug );
    event LikedPost( address sender, uint postId, bool liked );
    event DeletedPost( address sender, uint postId );


    // CROWDFUND SECTION
    /**
     * @dev Safe Mints a Token to a donor and assigns a uri to the token  
     */
    function safeMint(string memory uri) public {
        require(AllDonors[msg.sender].donCount > balanceOf(msg.sender), "The Connected account is Not eligible to Mint token"); 
        uint256 tokenId = _tokenIdCounter.current(); 
        _tokenIdCounter.increment();    
        _safeMint(msg.sender, tokenId);
        _setTokenURI(tokenId, uri);
        emit TokenMinted(msg.sender, tokenId); 
    }


    /**
     * @dev Recives donations and transfers to the contract owner  
     */
    function Donate() public payable {
        require(msg.sender != owner(), "Donations Can Not Be Made By The Contract Owner");
        require(msg.value >= (10**18)*2, "Sent Value Below Minimum Donation");
        payable(owner()).transfer(msg.value);
        _TotalDonations += msg.value;
        _DonationBalance += msg.value;
        if(AllDonors[msg.sender].adr == msg.sender ){
            AllDonors[msg.sender].amount += msg.value;
            AllDonors[msg.sender].donCount +=1;
            emit DonationMade(msg.sender, msg.value);  
            return;
        }        
        Donor storage D = AllDonors[msg.sender];
        D.donorsIdx = _DonorsCount.current();
        _DonorsCount.increment();
        D.adr = msg.sender;
        D.amount = msg.value;
        D.donCount +=1;
        DonorsAdrLst.push(msg.sender);
        emit DonationMade(msg.sender, msg.value); 
        return;
    }

    /**
     * @dev Transfers donations to other acounts 
     */
    function TransferDonations(address payable adr) public payable onlyOwner {
        require(msg.sender != adr, "Transfer To Own Account Is Not Valid");
        require(msg.value < _DonationBalance, "Withdrawal Limits Excceded");
        adr.transfer(msg.value);
        _DonationBalance -= msg.value;
        emit DonationTransfered(msg.sender, msg.value);
    }


    /**
     * @dev Returns an array of donors addresses
     */
    function DonorAdr() public view onlyOwner returns (address[] memory)
    {
        address[] memory Adrs = new address[](DonorsAdrLst.length);
        for (uint256 i = 0; i < DonorsAdrLst.length; i++) {   
            Adrs[i] = DonorsAdrLst[i]; 
        }
        return Adrs;
    }    


    /**
     * @dev Returns donation balance
     */
    function _donationtBalance() public onlyOwner view returns( uint ){
        return _DonationBalance;
    }  

    function OwnWallet()public view returns (uint256[] memory)
    {
        uint256 ownerTokenCount = balanceOf(msg.sender);
        uint256[] memory tokenIds = new uint256[](ownerTokenCount);
        for (uint256 i = 0; i < ownerTokenCount; i++) {
            tokenIds[i] = tokenOfOwnerByIndex(msg.sender, i); 
        }
        return tokenIds;
    }


    // BLOG SECTION 
    /**
     * @dev Called To Adds New Posts To The Blog 
     */
    function NewPost(string memory post, string memory slug) public {
        require(bytes(post).length > 0, "Invalid Post");
        Post storage P = AllPosts[_PostsCount.current()];
        P.postIdx = _PostsCount.current();
        P.author = msg.sender;
        P.post = post;
        P.slug = slug; 
        _PostsCount.increment();
        _ActPstCount.increment();
        emit NewPostAdded(msg.sender, slug);      
    }


    /**
     * @dev Called To Like And Unlike Posts
     */
    function LikeandUnlikePost(uint postId) public {
        require(AllPosts[postId].postIdx == postId, "Invalid... Post Does Not Exist");
        if(PostLikes[postId][msg.sender].user == msg.sender){
            if(PostLikes[postId][msg.sender].liked ==  true){
                  PostLikes[postId][msg.sender].liked = false;
                  AllPosts[postId].likecount -= 1;
                  emit LikedPost(msg.sender, postId, false);
                  return;
            }
            PostLikes[postId][msg.sender].liked = true;
            AllPosts[postId].likecount += 1;
            emit LikedPost(msg.sender, postId, true);
            return;
        }
        AllPosts[postId].likecount += 1;
        likeAdrs storage l = PostLikes[postId][msg.sender];
        l.user = msg.sender;
        l.liked = true;
        emit LikedPost(msg.sender, postId, true);
        return;
    }


    /**
     * @dev Called To Return The LIKe Status Of An Account On A Post (a Bool) 
     */
    function ReturnLiked(uint postId) public view returns (bool)
    {
        require(AllPosts[postId].postIdx == postId, "invalid... Post Does Not Exist");
        if (PostLikes[postId][msg.sender].user != msg.sender){
            return false;
        }  
        bool Liked = PostLikes[postId][msg.sender].liked;
        return Liked;
    }


    /**
     * @dev Called To Delete A Post 
     */
    function DeletePost(uint postId) public{
        require(AllPosts[postId].postIdx == postId, "Invalid.. Post Does Not Exist");
        require(AllPosts[postId].author == msg.sender, "Account Unathorized To Delete Post");
        delete AllPosts[postId];
        _ActPstCount.decrement();
        emit DeletedPost(msg.sender, postId);
    }


    /**
     * @dev Called to Return An Array Of Active Post
     */   
    function ReturnPosts() public view returns (Post[] memory)
    { 
        uint idx = 0;
        Post[] memory Posts = new Post[](_ActPstCount.current());
        for (uint i = 0; i < _PostsCount.current(); i++) { 
              if(bytes(AllPosts[i].post).length > 0){
                  Posts[idx] = AllPosts[i];
                  idx++;
              }  
        }
        return Posts;
    }

    // The following functions are overrides required by Solidity.
    function _beforeTokenTransfer(address from, address to, uint256 tokenId, uint256 batchSize)
      internal
      override(ERC721, ERC721Enumerable)
    {
      super._beforeTokenTransfer(from, to, tokenId, batchSize);
    }

    function supportsInterface(bytes4 interfaceId)
      public
      view
      override(ERC721, ERC721Enumerable)
      returns (bool)
    {
      return super.supportsInterface(interfaceId);
    }

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
      super._burn(tokenId);
        
    }
    // Returns The Token URI Of The Requested Token.
    function tokenURI(uint256 tokenId)
      public
      view
      virtual
      override(ERC721, ERC721URIStorage)
      returns (string memory)
    {
      require(
        _exists(tokenId),
        "ERC721Metadata: URI query for nonexistent token"
      );
    
        return super.tokenURI(tokenId);

    }  

}
