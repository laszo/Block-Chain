import hashlib
import time

from block import Block, BlockChain
from net import broadcast_block
from trans import make_trans

hash_cash = None


def mine_a_block(pre_blk):
    start = time.time()
    assert isinstance(pre_blk, Block)
    data = make_trans('myaddress', 'from miner', 50)
    blk = Block(pre_blk.index + 1, pre_blk.hash, data)
    data = blk.get_pow_header().encode().hex()
    nonce = scan_hash(blk.nonce, data, 20)
    blk.nonce = nonce
    blk.refresh_hash()
    end = time.time()
    print('mine_a_block, spend time: %d ' % int(end - start))
    return blk


def scan_hash(thenumber, thedata, k):
    while True:
        newdata = thedata + hex(thenumber).replace('0x', '')
        s = hashlib.sha256(newdata.encode()).hexdigest()
        i = int(s, 16)
        b = bin(i)
        b = b[2:]
        # print(k, s, i, b)
        if b[:k] == ''.join(['1' for i in range(k)]):
            return thenumber
        thenumber += 1


def main():
    for i in range(9):
        blk = mine_a_block(BlockChain.get_last_block())
        print(str(blk))
        BlockChain.add_block(blk)
        broadcast_block(blk)
    # for b in BlockChain.query_all():
    #     print(str(b))


if __name__ == '__main__':
    main()
    # real_scan(10, 'hello, world', 1)
    # real_scan(10, 'hello, world', 2)
    # real_scan(10, 'hello, world', 3)
    # real_scan(10, 'hello, world', 4)
    # print(scan_hash(10, 'hello, world', 10))
