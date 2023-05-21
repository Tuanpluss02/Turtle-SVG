import io
import os
import sys
import argparse
import turtle as t
from math import ceil

from svgpathtools import svg2paths2
import numpy as np

def read_svg(path, seg_unit):
    paths, attrs, svg_attr = svg2paths2(path) # type: ignore
    svg_size = (int(svg_attr['width'].replace('px','')), 
                int(svg_attr['height'].replace('px','')) )
    viewbox = [float(f) for f in svg_attr['viewBox'].split(' ')]

    polys = []
    for path in paths:
        poly = []
        for subpaths in path.continuous_subpaths():
            points = []
            for seg in subpaths:
                interp_num = ceil(seg.length()/seg_unit)
                points.append(seg.point(np.arange(interp_num)/interp_num))
            points = np.concatenate(points)
            points = np.append(points, points[0])
            poly.append(points)
        polys.append([[(p.real, p.imag) for p in pl] for pl in poly])
    return (polys, attrs, svg_size, viewbox)

def change_shape(t, h):
    i = int(round((h+90)/45)%8)
    t.shape(sprite_path.format(i))

def head_to(t, x, y, draw=True, have_sprite=True):
    wasdown = t.isdown()
    heading = t.towards(x,y)
    t.pen(pendown=draw)
    t.seth(heading)
    if have_sprite:
        t.clearstamps()
        change_shape(t, heading)
        t.goto(x,y)
        t.stamp()
    else:
        t.goto(x,y)
    t.pen(pendown=wasdown)

def draw_polygon(t, poly, fill='black', stroke='black', have_sprite=True):
    if fill=='none':
        fill = 'black'
    t.color(stroke,fill)
    p = poly[0]
    head_to(t,p[0],-(p[1]), False, have_sprite)
    for p in poly[1:]: 
        head_to(t,p[0],-(p[1]), have_sprite=have_sprite)
    t.up()

def draw_multipolygon(t, mpoly, fill='black', stroke='black', have_sprite=True):
    p = mpoly[0][0]
    head_to(t,p[0],-(p[1]), False, have_sprite)
    if fill!='none':
        t.begin_fill()
    for i, poly in enumerate(mpoly):
        draw_polygon(t, poly, fill, stroke, have_sprite)
        if i!=0:
            head_to(t,p[0],-(p[1]), False, have_sprite)
    if fill!='none':
        t.end_fill()

def main_draw(svg_file, sprite_path, seg_unit=8):
    polys, attrs, svg_size, viewbox = read_svg(svg_file, seg_unit=seg_unit)
    svg_w, svg_h = (viewbox[2]-viewbox[0], viewbox[3]-viewbox[1])
    svg_m = min(svg_w, svg_h)
    ar = svg_w/svg_h

    window = t.Screen()
    win_m = min(window.window_width(),window.window_height())
    if ar>1:
        window.setup(win_m*ar, win_m)
    else:
        window.setup(win_m, win_m/ar)
    scale = win_m / svg_m

    t.reset()
    t.speed(50)
    t.setworldcoordinates(viewbox[0]*1.1, -viewbox[3]*1.1, viewbox[2]*1.1, -viewbox[1]*1.1)
    t.mode(mode='world')
    t.tracer(n=10, delay=0)
    have_sprite = sprite_path is not None
    if have_sprite:
        for i in range(8):
            for f in [2, 3]:
                t.register_shape(sprite_path.format(i,f))

    for poly, attr in zip(polys, attrs): # type: ignore
        if 'style' in attr.keys():
            attr.update({attrs.split(':')[0]:attrs.split(':')[1] for attrs in attr['style'].split(';')})
        if 'stroke' not in attr.keys():
            attr['stroke'] = attr['fill']

        t.pen(outline=0.5*scale) # type: ignore
        if 'stroke-width' in attr.keys():
            t.pen(outline=float(attr['stroke-width'])*scale) # type: ignore

        if 'fill' in attr.keys():
            draw_multipolygon(t, poly, fill=attr['fill'], stroke=attr['stroke'], have_sprite=have_sprite)
        

    t.tracer(n=1, delay=0)
    head_to(t,viewbox[2],-viewbox[3], False, have_sprite)
    if have_sprite:
        t.clearstamps()
        change_shape(t, 0)
    # t.penup() 
    # t.goto(0, -70)  
    # t.write("Made by StormX", align="center", font=("Arial", 12, "normal"))
    t.done()




def cml_parse_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('--svg', '-s' , type=str, help='svg path')
    # parser.add_argument('--sprite', '-t', type=str, help='sprite path')
    return parser

if __name__ == '__main__': 
    abspath = os.path.abspath(__file__)
    dirname = os.path.dirname(abspath)

    parser = cml_parse_arg()
    args = parser.parse_args()
    svg_file = args.svg
    #sprite_path = args.sprite

    if svg_file is None:
        svg_file = 'input/h1.svg'
    sprite_path = 'cursors/a{}_3.gif'

    svg_file = os.path.join(dirname, svg_file)
    if sprite_path is not None:
        sprite_path = os.path.join(dirname, sprite_path)
    main_draw(svg_file, sprite_path)
