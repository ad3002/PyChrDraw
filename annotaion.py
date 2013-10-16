#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 09.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from trseeker.tools.draw_tools import draw_distribution_plot

def read_snp_position_data(file_name):
    ''' Read SNP positions from file.
    @param file_name: file name with data (chr\tposition\n)
    @return: chr -> positions
    '''
    print "Read SNPs data"
    bands = defaultdict(list)
    with open(file_name) as fh:
    	lines = fh.readlines()
    	data = [x.strip().split() for x in lines if not x.startswith("#")]
    for chrom, pos in data:
    	bands[chrom].append(int(pos))
    return bands

def compute_interval_freq(bands, chrs_lengths, bp_per_pixel=100000):
    ''' Compute SNPs intervals for drawing.
    @param bands: dictionary chr_name -> positions
    @param chrs_lengths: dictionary chr_name -> chr length
    @param bp_per_pixel: number nucleotides per pixel on image
    @return: (chr2pos2freq, distribution)
    '''
    chr2pos2freq = {}
    distribution = defaultdict(int)
    for name, length in chrs_lengths.items():
    	snps = bands[name]
    	snps.sort()
    	bins = defaultdict(int)
    	for snip in snps:
    		b = snip / bp_per_pixel
    		bins[b*bp_per_pixel] += 1
    	for value in bins.values():
    		distribution[value] += 1
    	chr2pos2freq[name] = bins
    return chr2pos2freq, distribution

def normalize_interval_freq(chr2pos2freq, distribution, max_cutoff=70):
    ''' Compute normalized SNPs intervals for drawing.
    @param bands: dictionary chr_name -> positions
    @param chrs_lengths: dictionary chr_name -> chr length
    @param bp_per_pixel: number nucleotides per pixel on image
    @param max_cutoff: maximal value of enrichment in interval
    '''
    M = [max(chr2pos2freq[x].values()) for x in chr2pos2freq.keys()]
    m = float(max(M))
    for name in chr2pos2freq:
    	for k in chr2pos2freq[name]:
    		if chr2pos2freq[name][k] > max_cutoff:
    			chr2pos2freq[name][k] = max_cutoff
    		chr2pos2freq[name][k] /= max_cutoff
    return chr2pos2freq

if __name__ == '__main__':
	chrs_lengths = {
    'chrA1': 247373621,
    'chrA2': 168782860,
    'chrA3': 146459317,
    'chrB1': 211444635,
    'chrB2': 158019773,
    'chrB3': 154608951,
    'chrB4': 149370783,
    'chrC1': 225678925,
    'chrC2': 161383699,
    'chrD1': 123211129,
    'chrD2': 90492622,
    'chrD3': 98640036,
    'chrD4': 98204123,
    'chrE1': 63723751,
    'chrE2': 65984037,
    'chrE3': 44542608,
    'chrF1': 72274105,
    'chrF2': 84331791,
	}

	chrs_lengths = {
        'A1': 239302903,
        'A2': 169043629,
        'A3': 142459683,
        'B1': 205241052,
        'B2': 154261789,
        'B3': 148491654,
        'B4': 144259557,
        'C1': 221441202,
        'C2': 157659299,
        'D1': 116869131,
        'D2': 89822065,
        'D3': 95741729,
        'D4': 96020406,
        'E1': 63002102,
        'E2': 64039838,
        'E3': 43024555,
        'F1': 68669167,
        'F2': 82763536,
        'X': 126427096,
    }

	file_name = "/Users/akomissarov/Downloads/cat_snp.txt"
	# file_name = "/Users/akomissarov/Downloads/cheetah.sSNP.tab/cheetah.sSNP.tab"
	image_file = "cat.png"
	bands = read_snp_position_data(file_name)
	chr2pos2freq, distribution = compute_interval_freq(bands, chrs_lengths, bp_per_pixel=10000)
	draw_distribution_plot(distribution, image_file)
	