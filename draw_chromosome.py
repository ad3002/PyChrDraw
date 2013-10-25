#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 09.10.2013
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com
import Image, ImageDraw, ImageFont
from collections import defaultdict

def load_bands_from_bed(file_name, color="#000000", border_color="#000000", last_column_color=False):
    ''' Load bands data from BED file.
    @param file_name: path to BED file
    @param color: band color
    @param border_color: border color
    @return: dictionary chr name to list of bands
    '''
    chr2bands = defaultdict(list)
    max_value = 0
    with open(file_name) as fh:
        for line in fh:
            line = line.strip()
            if line.startswith("#") or line is None:
                continue
            data = line.split()
            chromosome = data[0]
            start = int(data[1])
            end = int(data[2])
            if last_column_color:
                color = float(data[-1])
                if color > max_value:
                    max_value = color
            band = (start, end-start, color, border_color)
            chr2bands[chromosome].append(band)
    if last_column_color:
        return chr2bands, max_value
    return chr2bands

def load_snips_from_bed(file_name, color="#000000", border_color="#000000"):
    ''' Load bands data from BED file.
    @param file_name: path to BED file
    @param color: band color
    @param border_color: border color
    @return: dictionary chr name to list of bands
    '''
    chr2bands = defaultdict(list)
    with open(file_name) as fh:
        for line in fh:
            line = line.strip()
            if line.startswith("#") or line is None:
                continue
            data = line.split()
            chromosome = data[0]
            start = int(data[1])
            band = (start, start+1, color, border_color)
            chr2bands[chromosome].append(band)
    return chr2bands

def normalize_chromosome_sizes(chromosomes, real_size, bands=None):
    ''' Normalize chrs sizes by maximal chromosome length.
    @param chromosomes: dictionary with chromosome sizes
    @param real_size: maximum size in px
    @param bands: dict of chr name to list of (start, length, color, border) tuples for bands
    @return: (chromosomes, bands)
    '''
    max_chr = float(max(chromosomes.values()))
    for key in chromosomes:
        chromosomes[key] = int(round(real_size * chromosomes[key] / max_chr, 0))
    if bands:
        for key in bands:
            for i, (start, length, color, border) in enumerate(bands[key]):
                bands[key][i] = (   
                                    int(round(real_size*start/max_chr, 0)), 
                                    int(round(real_size*length/max_chr, 0)), 
                                    color, 
                                    border,
                                )
    return chromosomes, bands

def draw_enrichmnet(settings):
    
    chrs = settings["cheetah_chrs"]
    ref_chrs = settings["chromosome_sizes"]
    bands = settings["cat_snips_file"]

    real_chr_size = settings["canvas"]["real_chr_size"]

    im = Image.new("RGBA", (settings["canvas"]["width"],settings["canvas"]["height"]), settings["canvas"]["bg_color"])
    draw = ImageDraw.Draw(im)
   
    max_chr_length = float(max([x for x in chrs.values()]))
    max_chr_length_ref = float(max([x for x in ref_chrs.values()]))
    max_chr_length = max(max_chr_length, max_chr_length_ref)
    print "-->", max_chr_length/real_chr_size

    chrs = [(k, real_chr_size*(v/max_chr_length)) for k, v in chrs.items()]
    ref_chrs = [(k, real_chr_size*(v/max_chr_length)) for (k, v) in ref_chrs]
    chrs.sort()
    x = settings["canvas"]["left_corner"]
    y = settings["canvas"]["top_corner"]

    font = ImageFont.truetype("/home/akomissarov/Dropbox/PyBioDraw/fonts/arialbd.ttf", 64)
    
    for i, (name, length) in enumerate(chrs):
        rectbbox = [x, y, x+length, y + 100]
        print rectbbox
        draw.rectangle(rectbbox, fill="#ffffff", outline="#000000")

        # for p in bands[name]:

        #     p = 4000 * int(p) / max_chr_length 

        #     rect = (x+p,y+2, x+p, y+96)

        #     draw.line(rect, fill="#4096EE")
        for k,v in settings["chr2pos2freq"][name].items():
            
            p = 2473 * int(k) / max_chr_length
            rect = (x+p,y+2, x+p, y+96)
            # color = int(v * 255)
            # if color > 254:
            #     color = 254
            # color = 254 - color
            # color = (color, color, color)
            m = 10
            for c in colors_map:
                if abs(c[0] - v) < m:
                    color = c[1:]
                    m = abs(c[0] - v)
            draw.line( rect, fill=color )

        txt = str(len(settings["chr2pos2freq"][name]))
        w, h = font.getsize(txt)
        draw.text((settings["width"]-250, y+(100-h)/2), txt, font=font, fill="#000000")

        y += 150

        w, h = font.getsize(name)
        draw.text((x-20-w, y-h), name, font=font, fill="#000000")
        
        (name, length) = ref_chrs.pop(0)
        rectbbox = [x, y, x+length, y + 100]

        draw.rectangle(rectbbox, fill="#ffffff", outline="#000000")
        
        # for p in settings["ref_bands"][name]:

        #     p = 2473 * int(p) / max_chr_length 

        #     rect = (x+p,y+2, x+p, y+98)

        #     draw.line(rect, fill="#C79810")
        # name = settings["cheetah2cat"][name]
        for k,v in settings["REF_chr2pos2freq"][name].items():
            
            p = 2473 * int(k) / max_chr_length
            rect = (x+p,y+2, x+p, y+98)
            # color = int(v * 255)
            # if color > 254:
            #     color = 254
            # color = 254 - color
            # color = (color, color, color)
            m = 10
            for c in colors_map:
                if abs(c[0] - v) < m:
                    color = c[1:]
                    m = abs(c[0] - v)
            draw.line( rect, fill=color )

        txt = str(len(settings["REF_chr2pos2freq"][name]))
        w, h = font.getsize(txt)
        draw.text((settings["width"]-250, y+(100-h)/2), txt, font=font, fill="#000000")

        y += 250


    print "Save file to", settings["output_file"]
    im.save(settings["output_file"])

def draw_vertical_chromosome(draw, x, y, length, bands=None, chr_width=100, name=None, scale=1, stars=None):
    ''' Draw chromosome
    @param draw: ImageDraw object
    @param x: x coordinate of left top corner
    @param y: y coordinate of left top corner
    @param length: chromosome length
    @param bands: bands list of (start, lenght, inner_color, border_color)
    @param chr_width: chromosome width in px
    @param name: chromosome name
    @param scale: scaling, default value - 1
    @param stars: list of star positions
    '''
    if not bands:
        bands = []
    arcbbox = (x, y, x + chr_width, y + chr_width)
    draw.arc(arcbbox, 180, 0, fill='#000000')
    y += chr_width/2
    arcbbox = (x, y + length-chr_width/2, x+chr_width, y + length+chr_width/2)
    draw.arc(arcbbox, 0, 180, fill='#000000')
    rectbbox = [x, y, x + chr_width, y + length]
    draw.rectangle(rectbbox, fill="#ffffff", outline="#000000")
    draw.line((x,y, x+chr_width, y), fill="#ffffff")
    draw.line((x,y + length, x+chr_width, y + length), fill="#ffffff")
    
    if name:
        draw_legend(draw, name, x, y+length+chr_width/2+25, chr_width)
    for band in bands:
        y, length, color, outline = band
        y += chr_width/2
        rectbbox = [x+1, y, x + chr_width-1, y + length]
        draw.rectangle(rectbbox, fill=color, outline=outline)
    if stars:
        for y in stars:
            y += chr_width/2
            draw_legend(draw, "*", x+chr_width+10, y, None, font_size=35)

def draw_horizontal_chromosome(draw, x, y, length, bands=None, chr_width=100, name=None, scale=1, stars=None):
    '''
    Draw chromosome
    @param draw: ImageDraw object
    @param x: x coordinate of left top corner
    @param y: y coordinate of left top corner
    @param length: chromosome length
    @param bands: bands list of (start, lenght, inner_color, border_color)
    @param chr_width: chromosome width in px
    @param name: chromosome name
    @param scale: scaling, default value - 1
    @param stars: list of star positions
    '''
    if name:
        (w, h) = draw_legend(draw, name, x, y, None, height=chr_width)
    x += 80
    if not bands:
        bands = []
    arcbbox = (x, y, x + chr_width, y + chr_width)
    draw.arc(arcbbox, 0, 360, fill='#000000')
    x += chr_width/2
    arcbbox = (x + length-chr_width/2, y, x + length+chr_width/2, y + chr_width)
    draw.arc(arcbbox, 0, 360, fill='#000000')
    rectbbox = [x, y, x + length, y + chr_width]
    chromosome_start = x
    draw.rectangle(rectbbox, fill="#ffffff", outline="#000000")
    draw.line((x, y, x, y+chr_width), fill="#ffffff")
    draw.line((x + length, y, x + length, y + chr_width), fill="#ffffff")
    
    for band in bands:
        (x, length, color, outline) = band
        rectbbox = [x+chromosome_start, y+1, x+length+chromosome_start, y+chr_width-1]
        draw.rectangle(rectbbox, fill=color, outline=outline)
    if stars:
        for x in stars:
            x += chr_width/2
            draw_legend(draw, "*", x, y+chr_width+10, None, font_size=35)


def draw_centromere():
    raise NotImplemented

def draw_telomere():
    raise NotImplemented

def draw_legend(draw, text, x, y, width, height=None, font_size=35, font_file="/home/akomissarov/Dropbox/PyChrDraw/fonts/arialbd.ttf", text_color="#000000"):
    ''' Draw legend on image.
    @param draw: ImageDraw object
    @param x: x coordinate of left top corner
    @param y: y coordinate of left top corner
    @param width: text width
    @param font_size: text font size, default value - 35
    @param font_file: path to ttf file, default value - ../fonts/arialbd.ttf
    @param text_color: text color, default value - #000000
    '''
    text = str(text)
    font = ImageFont.truetype(font_file, font_size)
    w, h = draw.textsize(text, font)
    if width:
        x += (width - w)/2
    if height:
        y += (height - h)/2    
    draw.text((x, y), text, font=font, fill=text_color)
    return (w, h)

def draw_full_legend(draw, x, y, names, colors_vals, width=350, height=1230):
    ''' Draw legend for color annotated images
    @param draw: ImageDraw object
    @param x: x coordinate of left top corner
    @param y: y coordinate of left top corner
    @param width: box width, default value is 350 px
    @param height: box height, default value is 1230 px
    @param names: list of names
    @param colors_vals: dictionary from name to color
    '''

    # draw borders
    rectbbox = [x, y, x + width, y +height]
    draw.rectangle(rectbbox, fill="#ffffff", outline="#dddddd")
    rectbbox = [x+1, y+1, x + width-1, y+height-1]
    draw.rectangle(rectbbox, fill="#ffffff", outline="#dddddd")

    # draw legend
    x += 50
    y += 35
    for i, title in enumerate(names):
        y +=  70
        color = colors_vals[title]
        rectbbox = [x, y, x + 50, y + 50]
        draw.rectangle(rectbbox, fill=color, outline="#000000")
        draw_legend(draw, title, x + 80, y, None, font_size = 42)

def draw_chromosome_scheme(draw, x, y):
    ''' Draw chromosome scheme with cen and tel positions.
    @param draw: ImageDraw object
    @param x: x coordinate of left top corner
    @param y: y coordinate of left top corner
    '''
    bands = [
        (y+130, 100, "#cccccc","#cccccc"),
        (y+240, 280, "#eeeeee","#eeeeee"),
        (y+530, 100, "#cccccc","#cccccc"),
    ]
    draw_vertical_chromosome(draw, x-10, y+130, 500, bands=bands, chr_width=70)
    draw_legend(draw, "PeriCen", x + 90, y+180, None, font_size = 42)
    draw_legend(draw, "Arm", x + 90, y+380, None, font_size = 42)
    draw_legend(draw, "PeriTel", x + 90, y+580, None, font_size = 42)
