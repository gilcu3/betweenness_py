#! /usr/bin/env python3

from memory_profiler import memory_usage

import data
import networkx as nx
from time import time
import resource
from multiprocessing import Process
import copy
import gc
import os
import sys
import pickle


import icentral
import toy_dynamic
import brandes


import datasets.Cagr.load as cagr
import datasets.Epa.load as epa
import datasets.Eva.load as eva
import datasets.CollegeMsg.load as collegemsg
import datasets.wiki_Vote.load as wikivote
import datasets.p2p_Gnutella08.load as nutella08
import datasets.ca_HepPh.load as cahepph
import datasets.ca_HepTh.load as cahepth
import datasets.ego_Facebook.load as egofacebook
import datasets.email_Eu_core.load as emaileu
import datasets.p2p_Gnutella04.load as nutella04
import datasets.p2p_Gnutella05.load as nutella05
import datasets.p2p_Gnutella09.load as nutella09
import datasets.wiki_RfA.load as wikirfa
from datasets.rmat_generator.loader import *


def measure(params):
    tnow = time()
    # memory is impossible to measure in very short lived program
    # (cycle 336 in) memory_profiler.py when parameters are modified inside function
    # posed a problem for bidcentral, as the others are undirected
    # had to lower interval default parameter
    mem = memory_usage(params, interval=0.02, max_usage=True)[0]
    return time() - tnow, mem


def pmeasure(A0, edge, undirected_directed, filestr):
    if undirected_directed:
        res0 = measure((A0.remove, (edge,)))
        res1 = measure((A0.remove, ((edge[1], edge[0]),)))
        res = (res0[0] + res1[0], max(res0[1], res1[1]))
    else:
        res = measure((A0.update, (edge,)))

    with open(filestr, 'a') as out:
        print(res[0], res[1], file=out)


def full(algo, dataset, edges):
    resource.setrlimit(resource.RLIMIT_DATA, (10 * 2**30, 10 * 2**30))

    g = dataset.load()
    try:
        dname = str(dataset.__name__).split('.')[1]
    except:
        dname = str(dataset.__name__)
    filestr = 'out/%s.%s_iot.out' % (algo.__module__, dname)

    if os.path.exists(filestr):
        return
        os.remove(filestr)

    try:
        if nx.is_directed(g):
            if algo.directed():
                A = algo(g)
                for edge in edges:
                    A0 = copy.deepcopy(A)
                    gc.collect()
                    p = Process(target=pmeasure, args=(A0, edge, False, filestr))
                    p.start()
                    p.join()

                    # results.append(res)
        else:
            if algo.directed() and algo.__module__ != 'brandes':
                ng = nx.to_directed(g.copy()).copy()
                A = algo(ng)

                for edge in edges:
                    A0 = copy.deepcopy(A)
                    gc.collect()
                    p = Process(target=pmeasure, args=(A0, edge, True, filestr))
                    p.start()
                    p.join()
                    # results.append(res)
            else:
                A = algo(g)
                for edge in edges:
                    A0 = copy.deepcopy(A)
                    gc.collect()
                    p = Process(target=pmeasure, args=(A0, edge, False, filestr))
                    p.start()
                    p.join()
                    # results.append(res)
    except Exception as e:
        print('ERROR', algo.__module__, e)


if __name__ == '__main__':
    d, algo = sys.argv[1], sys.argv[2]
    # d, algo = 'eva', 'toy_dynamic'
    d, algo = eval(d), eval(algo).algo
    now = time()
    g = d.load()
    try:
        name = str(d.__name__).split('.')[1]
    except:
        name = str(d.__name__)
    print(algo.__module__, name, g.number_of_nodes(), g.number_of_edges(), 'Directed' if nx.is_directed(g) else 'Undirected')

    filestr = 'edges/%s_iot.bin' % name

    if not os.path.exists(filestr):
        edges = [data.get_random_edge(g) for _ in range(100)]
        with open(filestr, 'wb') as edgefile:
            pickle.dump(edges, edgefile)
    else:
        with open(filestr, 'rb') as edgefile:
            edges = pickle.load(edgefile)

    full(algo, d, edges)
    print('time', time() - now)
