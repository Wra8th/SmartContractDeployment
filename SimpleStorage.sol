// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage{
    uint256 favoriteNumber = 5;
    // bool favbool = true;
    // string facstring = "abcsd";
    // int256 favint = -5;
    // bytes32 favbyte = "cat";
    //default visibility is internal

    struct People{
        uint256 favoriteNumber;
        string name;
    }
    People[] public people;
    // People public person = People({favoriteNumber: 2, name: "patric"});

    mapping(string => uint256) public nameToFavoriteNumber;

    //storing favorite number 
    function store (uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }


    //view: read state off the block chain, pure: purely do some type of math
    function retrieve() public view returns(uint256){
        return favoriteNumber;
    }
    //memory: store it during execution
    //storage: keep it forever
    function addPerson(string memory _name, uint256 _favoriteNumber) public{
        people.push(People(_favoriteNumber, _name)); //pushing in to the array
        nameToFavoriteNumber[_name] = _favoriteNumber; //mapping
    }
    
}
