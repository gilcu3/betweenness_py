#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dill


def work():
    data = 'wiki_Vote'
    with open('%s.bin' % data, 'rb') as fin:
        edges = dill.load(fin)
    with open('%s.in' % data, 'w') as fin:
        for edge in edges:
            print('%d %d' % (edge[0], edge[1]), file = fin)



def main(args):
    work()

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
