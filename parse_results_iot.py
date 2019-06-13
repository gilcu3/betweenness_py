#!/usr/bin/env python3

import os
from statistics import mean, pstdev


import datasets.Cagr.load as Cagr
import datasets.Epa.load as Epa
import datasets.Eva.load as Eva
import datasets.CollegeMsg.load as CollegeMsg
import datasets.wiki_Vote.load as wiki_Vote
import datasets.p2p_Gnutella08.load as p2p_Gnutella08
import datasets.ca_HepPh.load as ca_HepPh
import datasets.ca_HepTh.load as ca_HepTh
import datasets.ego_Facebook.load as ego_Facebook
import datasets.email_Eu_core.load as email_Eu_core
import datasets.p2p_Gnutella04.load as p2p_Gnutella04
import datasets.p2p_Gnutella05.load as p2p_Gnutella05
import datasets.p2p_Gnutella09.load as p2p_Gnutella09
import datasets.wiki_RfA.load as wiki_RfA
from datasets.rmat_generator.loader import *


def parse():
    path_in = 'out/'
    path_out = 'out_latex/'

    d2d = {'CollegeMsg': 'CollegeMsg', 'p2p_Gnutella08': 'p2p-Gnutella08', 'wiki_Vote': 'Wiki-Vote', 'Cagr': 'ca-GrQc',
           'Epa': 'Epa', 'Eva': 'Eva', 'p2p_Gnutella05': 'p2p-Gnutella05', 'p2p_Gnutella04': 'p2p-Gnutella04',
           'p2p_Gnutella09': 'p2p-Gnutella09', 'ca_HepPh': 'ca-HepPh', 'ca_HepTh': 'ca-HepTh',
           'ego_Facebook': 'ego-Facebook', 'email_Eu_core': 'email-Eu-core', 'wiki_RfA': 'wiki-RfA'}

    real_u = ['ego_Facebook', 'Cagr', 'Epa', 'Eva', 'ca_HepTh', 'ca_HepPh']
    real_d = ['email_Eu_core', 'CollegeMsg', 'p2p_Gnutella08', 'wiki_Vote', 'p2p_Gnutella09', 'p2p_Gnutella05', 'p2p_Gnutella04', 'wiki_RfA']
    sin_d = []
    for n in range(1024, 16385, 1024):
        d2d['rmat_%d' % n] = 'RMAT-%d' % n
        sin_d.append('rmat_%d' % n)

    algos = ['brandes', 'icentral', 'ibet', 'toy_dynamic']

    res = {}
    global_speedup = 0
    global_total = 0
    for data in real_u + real_d + sin_d:
        for algo in algos:

            allt, allm = [], []
            f_str = '%s.%s_iot.out' % (algo, data)
            if os.path.exists(path_in + f_str):
                with open(path_in + f_str, 'r') as f:
                    for line in f.readlines():
                        ct, cm = map(float, line.split())
                        allt.append(ct)
                        allm.append(cm)

                if data not in res:
                    res[data] = {}
                res[data][algo] = (mean(allt), pstdev(allt), max(allm))
            else:
                if data not in res:
                    res[data] = {}
                res[data][algo] = ()

    def process_tab(datas, filename):
        nonlocal global_speedup,global_total
        with open(path_out + filename + '.tab', 'w') as fresults:
            for data in datas:
                # print(data)
                line = [d2d[data]]
                # print(sorted(res[data]))
                best_time = 1e9

                for algo in sorted(res[data]):

                    if len(res[data][algo]) != 0 and best_time > res[data][algo][0]:
                        best_time = res[data][algo][0]

                for algo in sorted(res[data]):
                    if len(res[data][algo]) != 0:
                        if(res[data][algo][0] == best_time):
                            line.append('\\textbf{%.2f}' % res[data][algo][0])
                        else:
                            line.append('%.2f' % res[data][algo][0])
                        line.append('%.2f' % res[data][algo][1])
                        line.append('%.0f' % res[data][algo][2])
                print(' & '.join(line), '\\\\', file=fresults)
            speedup = mean([res[data]['brandes'][0] / res[data]['toy_dynamic'][0] for data in datas])
            global_speedup += sum([res[data]['brandes'][0] / res[data]['toy_dynamic'][0] for data in datas])
            global_total += len(datas)
            print("%s - Bidcentral Speedup vs Brandes: %.2f" % (filename, speedup))

    def process_plot(datas, filename):
        with open(path_out + filename + '.plot', 'w') as fresults:
            line = ['D']
            line += ['Brandes_time', 'Brandes_mem', 'Bidcentral_time', 'Bidcentral_mem']
            print(' '.join(line), file=fresults)
            dd = [(eval(data).load().number_of_nodes(),data) for data in datas]
            for n, data in sorted(dd):
                # print(data)
                line = ['%d' % n]
                # print(sorted(res[data]))

                for algo in sorted(res[data]):
                    if len(res[data][algo]) != 0:
                        line.append('%.2f' % res[data][algo][0])
                        line.append('%.0f' % res[data][algo][2])
                print(' '.join(line), file=fresults)

    process_tab(real_u, 'results_remove_real_u')
    process_tab(real_d, 'results_remove_real_d')
    process_tab(sin_d, 'results_remove_sin_d')
    process_plot(sin_d, 'results_remove_sin_d')
    print('Global - Bidcentral Speedup vs Brandes: %.2f' % (global_speedup / global_total))

if __name__ == '__main__':
    parse()

