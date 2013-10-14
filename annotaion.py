#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 09.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

from collections import defaultdict

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

# if __name__ == '__main__':
# 	file_name = "/Users/akomissarov/Downloads/cheetah.sSNP.tab/cheetah.sSNP.tab"
# 	bands = read_snp_position_data(file_name)
# 	