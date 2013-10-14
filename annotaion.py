#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 09.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

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
