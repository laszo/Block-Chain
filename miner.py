from block import Block, BlockChain
from net import broadcast_block


hash_cash = None


def dowork():
    blk = Block(0, '', {})
    return blk


def main():
    for i in range(9):
        blk = dowork()
        BlockChain.add_block(blk)
        broadcast_block(blk)
    for b in BlockChain.query_all():
        print(str(b))


if __name__ == '__main__':
    main()
