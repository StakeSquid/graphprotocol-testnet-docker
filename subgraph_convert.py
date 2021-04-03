#!/usr/bin/python3

import base58
import argparse

def to_id(hash):
    bytes_value = base58.b58decode(hash)
    hex_value = bytes_value.hex()
    return "0x"+hex_value[4:]

def to_ipfs_hash(id):
    #https://ethereum.stackexchange.com/questions/17094/how-to-store-ipfs-hash-using-bytes32
    hex_value = bytes.fromhex("1220"+id[2:])
    ipfs_hash = base58.b58encode(hex_value)
    return ipfs_hash.decode("utf-8")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Convert subgraph id to subgraph ipfs hash and vice versa.'
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--to_ipfs_hash", type=str,
        metavar="0x31edcacc9a53bc8ab4be2eeb0d873409da4c4228cb2d60e4243bd3b4e8af7500",
        help="convert from subgraph id to subgraph ipfs hash")
    group.add_argument("--to_id", type=str,
        metavar="QmRhYzT8HEZ9LziQhP6JfNfd4co9A7muUYQhPMJsMUojSF",
        help="convert from subgraph ipfs hash to subgraph id")
    args = parser.parse_args()

    if args.to_id:
      print(to_id(args.to_id))

    if args.to_ipfs_hash:
      print(to_ipfs_hash(args.to_ipfs_hash))
