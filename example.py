from math import floor, ceil
from typing import AnyStr


ASCII_TO_INT: dict = {i.to_bytes(1, 'big'): i for i in range(256)}
INT_TO_ASCII: dict = {i: b for b, i in ASCII_TO_INT.items()}


def compress(data: AnyStr) -> bytes:
    if isinstance(data, str):
        data = data.encode()
    keys: dict = ASCII_TO_INT.copy()
    n_keys: int = 256
    compressed: list = []
    start: int = 0
    n_data: int = len(data)+1
    while True:
        if n_keys >= 512:
            keys = ASCII_TO_INT.copy()
            n_keys = 256
        for i in range(1, n_data-start):
            w: bytes = data[start:start+i]
            if w not in keys:
                compressed.append(keys[w[:-1]])
                keys[w] = n_keys
                start += i-1
                n_keys += 1
                break
        else:
            compressed.append(keys[w])
            break
    bits: str = ''.join([bin(i)[2:].zfill(9) for i in compressed])
    return int(bits, 2).to_bytes(ceil(len(bits) / 8), 'big')


def decompress(data: AnyStr) -> bytes:
    if isinstance(data, str):
        data = data.encode()
    keys: dict = INT_TO_ASCII.copy()
    bits: str = bin(int.from_bytes(data, 'big'))[2:].zfill(len(data) * 8)
    n_extended_bytes: int = floor(len(bits) / 9)
    bits: str = bits[-n_extended_bytes * 9:]
    data_list: list = [int(bits[i*9:(i+1)*9], 2)
                       for i in range(n_extended_bytes)]
    previous: bytes = keys[data_list[0]]
    uncompressed: list = [previous]
    n_keys: int = 256
    for i in data_list[1:]:
        if n_keys >= 512:
            keys = INT_TO_ASCII.copy()
            n_keys = 256
        try:
            current: bytes = keys[i]
        except KeyError:
            current = previous + previous[:1]
        uncompressed.append(current)
        keys[n_keys] = previous + current[:1]
        previous = current
        n_keys += 1
    return b''.join(uncompressed)


comp = compress('Notice of RightsAll rights reserved. No part of this book may be reproduced, stored in a retrievalsystem or transmitted in any form or by any means, without the prior writtenpermission of the publisher, except in the case of brief quotations embodied incritical articles or reviews.Notice of LiabilityThe author and publisher have made every effort to ensure the accuracy of theinformation herein. However, the information contained in this book is soldwithout warranty, either express or implied. Neither the authors and SitePointPty. Ltd., nor its dealers or distributors will be held liable for any damages to becaused either directly or indirectly by the instructions contained in this book, orby the software or hardware products described herein.Trademark NoticeRather than indicating every occurrence of a trademarked name as such, thisbook uses the names only in an editorial fashion and to the benefit of thetrademark owner with no intention of infringement of the trademark.')
print (comp)
print ('\n')
descomp = decompress(comp)
print (descomp)