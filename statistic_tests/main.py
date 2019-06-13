#! /usr/bin/env python3

import matplotlib.pyplot as plt
import os
from statistics import mean, pstdev

import stac
import orange
from scipy.stats import wilcoxon
# CD scores and plot


def process(mtype, gtype):
	
	if mtype == 'add':
		algos = ['brandes', 'ibet', 'toy_dynamic']
		names = ['Brandes', 'Ibet', 'Bidcentral']
		extra = ''
	else:
		algos = ['brandes', 'toy_dynamic']
		names = ['Brandes', 'Bidcentral']
		extra = '_iot'
	path_in = '../out/'
	
	d2d = {}
	if gtype == 'sin':
		datas = []
		for n in range(1024, 16385, 1024):
			d2d['rmat_%d' % n] = 'RMAT-%d' % n
			datas.append('rmat_%d' % n)
	else:
		datas = ['email_Eu_core', 'CollegeMsg', 'p2p_Gnutella08', 'wiki_Vote', 'p2p_Gnutella09', 'p2p_Gnutella05', 'p2p_Gnutella04', 'wiki_RfA']

	res = {}
	for data in datas:
		for algo in algos:
			allt = []
			f_str = '%s.%s%s.out' % (algo, data, extra)
			if os.path.exists(path_in + f_str):
				with open(path_in + f_str, 'r') as f:
					for line in f.readlines():
						ct, _ = map(float, line.split())
						allt.append(ct)

				if data not in res:
					res[data] = {}
				res[data][algo] = mean(allt)
			else:
				if data not in res:
					res[data] = {}
				res[data][algo] = ()
	series = [[] for algo in algos]
	for i, algo in enumerate(algos):
		for data in datas:
			series[i].append(res[data][algo])
	return series, names


def friedman_test(series, names, filename):
	_, p, avranks, pivots = stac.friedman_test(*series)  # iman_davenport modification
	print('p-value: %.2e' % p)

	path_out = '../out_latex/'

	cd_1 = orange.compute_CD(avranks, 30, alpha='0.05', test='nemenyi')
	print(cd_1)
	orange.graph_ranks(avranks, names, cd=cd_1, width=6, textspace=1.5)
	plt.savefig(path_out + filename + '_nemenyi' + '.png')

	cd_2 = orange.compute_CD(avranks, 30, alpha='0.05', test='bonferroni-dunn')
	print(cd_2)
	orange.graph_ranks(avranks, names, cd=cd_2, width=6, textspace=1.5)
	plt.savefig(path_out + filename + '_bonferroni-dunn' + '.png')


def wilcoxon_test(series, names, filename):
	_, p = wilcoxon(series[0], series[1])
	print('p-value: %.2e' % p)

if __name__ == '__main__':
	mtype, gtype = 'add', 'sin'
	series, names = process(mtype, gtype)
	filename = 'cd_%s_%s_d' % (mtype, gtype)
	friedman_test(series, names, filename)
	
	mtype, gtype = 'remove', 'sin'
	series, names = process(mtype, gtype)
	filename = 'cd_%s_%s_d' % (mtype, gtype)
	wilcoxon_test(series, names, filename)
	# process('add', 'real')
	# process('remove', 'real')

