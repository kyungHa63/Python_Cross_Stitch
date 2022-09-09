#!/usr/bin/env python
# -*- coding: utf-8 -*-

class SVG:
    
    xml = ''
    
    def __init__(self, black_white = False, minor_lines = False, symbols = True):
        self.black_white = black_white
        self.minor_lines = minor_lines
        self.symbols = symbols
        
    def get_rgb_from_dmc_item(self, item):
        return 'rgb('+str(item[0])+','+str(item[1])+','+str(item[2])+');'

    def gen_glyph(self, num, x, y, color, s = 1, pattern = 'all'):
        x = str(int(x+s*0.5))
        y = str(int(y+s*0.9))
        if sum(color[0:2])>255 or self.black_white:
            font_color = '" fill="black" '
        else:
            font_color = '" fill="white" '
        # Capital letters
        if num<26:
            text = str(chr(65+num))
        # Small letters
        elif num<51:
            text = str(chr(97+num-26))
        # Capital letters
        else: # Numbers
            text = str(num-51)
        if pattern != 'all':
            if text in pattern:
                return '<text text-anchor="middle" x = "' + x + '" y = "' + y + font_color+' font-weight="bold" font-size="' + str(int(s*0.9)) + '">' + text + '</text>'
            else:
                return  ''
        else:
            return '<text text-anchor="middle" x = "' + x + '" y = "' + y + font_color + ' font-weight="bold" font-size="' + str(
                int(s * 0.9)) + '">' + text + '</text>'

    def add_rect(self, palette, index, x, y, size, pattern = 'all'):
        glyph_scale = size
        fill = 'fill:rgb(255,255,255);' if self.black_white else 'fill:'+self.get_rgb_from_dmc_item(palette[index])
        stroke = 'stroke:rgb(20,20,20);stroke-width:1;' if self.minor_lines else 'stroke:none;'
        sym = self.gen_glyph(index, x, y, palette[index], glyph_scale, pattern) if self.symbols else ''
        self.xml += '<rect x="'+str(x)+'" y="'+str(y)+'" width="'+str(size)+'" height="'+str(size)+'" style="'+fill+stroke+'"/>' + sym
        
    def prep_for_drawing(self, width, height):
        self.xml += '<svg xmlns="http://www.w3.org/2000/svg" width="'+str(width)+'" height="'+str(height)+'" style ="fill:none;">'
        self.xml += '<style>.svg_txt{font-size:20px;}.glyph{stroke:#000000;stroke-width:1;stroke:1;}</style>'
    
    def mid_arrows(self, size, width, height):
        h = str(size/2)
        f = str(size)
        self.xml += "<path d=\"M0 "+h+"L"+f+" "+h+"M"+h+" 0L"+f+" "+h+" "+h+" "+f+"\" stroke=\"black\" stroke-width=\"2\" fill=\"none\" transform='translate(0 " + str(height/2) + ")'/>"
        self.xml += "<path d=\"M"+h+" 0L"+h+" "+f+" M"+f+" "+h+"L"+h+" "+f+" 0 "+h+"\" stroke=\"black\" stroke-width=\"2\" fill=\"none\" transform='translate(" + str(width/2) + " 0)'/>"
    
    def major_gridlines(self, size, width, height):
        for x in range(size + size * 10, width, size * 10):
            self.xml += "<line x1=\"" + str(x) + "\" y1=\"" + str(size) + "\" x2=\"" + str(x) + "\" y2=\"" + str(height) + "\" style=\"stroke:black;stroke-width:2\" />"
        for y in range(size + size * 10, height, size * 10):
            self.xml += "<line x1=\"" + str(size) + "\" y1=\"" + str(y) + "\" x2=\"" + str(width) + "\" y2=\"" + str(y) + "\" style=\"stroke:black;stroke-width:2\" />"
            
    def add_key_colour(self, x, y, size, index, colour, num_stitch):
        # key
        glyph_scale = size
        fill = 'fill:rgb(255,255,255);' if self.black_white else 'fill:rgb('+str(colour[0])+', '+str(colour[1])+', '+str(colour[2])+');'
        stroke = 'stroke:rgb(20,20,20);stroke-width:1;' if self.minor_lines else 'stroke:none;'
        sym = self.gen_glyph(index, x, y, colour, glyph_scale) if self.symbols else ''
        self.xml += '<rect x="0" y="'+str(y)+'" width="'+str(size)+'" height="'+str(size)+'" style="'+fill+stroke+'"/>' + sym
        # colour name
        self.xml += '<rect x="' + str(size) + '" y="' + str(y) + '" width="' + str(size * 10) + '" height="' + str(
            size) + '" style="fill:rgb(255,255,255);stroke:black;stroke-width:1;"/>'
        self.xml += '<text x = "' + str(x + size * 1.5) + '" y = "' + str(y + size / 2.0) + '" fill="black">' + colour[
            3] + '</text>'
        # number of stitches
        self.xml += '<rect x="' + str(size*11) + '" y="' + str(y) + '" width="' + str(size * 2) + '" height="' + str(
            size) + '" style="fill:rgb(255,255,255);stroke:black;stroke-width:1;"/>'
        self.xml += '<text x = "' + str(x + size * 11.5) + '" y = "' + str(y + size / 2.0) + '" fill="black">' + str(num_stitch) + '</text>'

        # colour code
        self.xml += '<rect x="'+str(size*13)+'" y="'+str(y)+'" width="'+str(size* 2)+'" height="'+str(size)+'" style="fill:rgb(255,255,255);stroke:black;stroke-width:1;"/>'
        self.xml += '<text x = "' + str(x + size* 13 + (size/2.0)) + '" y = "' + str(y + size / 2.0) + '" fill="black">' + colour[4] + '</text>'
        
    def save(self, filename):
        self.xml += '</svg>'
        f = open(filename,'w')
        f.write(self.xml)
        f.close()
        