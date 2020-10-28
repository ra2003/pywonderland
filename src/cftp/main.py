# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Draw a random lozenge tiling generated by CFTP with Cairo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Usage:  python main.py

By default this will sample a random lozenge tiling of a
20x20x20 hexagon from uniform distribution.

"""
try:
    import cairocffi as cairo
except ImportError:
    import cairo

from cftp import LozengeTiling, run_cftp


# mathematica color style
TOP_COLOR = (0.678, 0.847, 1)
LEFT_COLOR = (0.314, 0.188, 0.475)
RIGHT_COLOR = (1, 0.569, 0.459)
EDGE_COLOR = (0, 0, 0)
LINE_WIDTH = 0.12
HALFSQRT3 = 0.5 * 3**0.5


def square_to_hex(verts):
    """
    Transform vertices in `ac`-plane to the usual xy-plane.
    :verts:  a list of 2d points in ac-plane.
    """
    return [(HALFSQRT3 * x, y - 0.5 * x) for x, y in verts]


def main(hexagon_size, imgsize):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, imgsize, imgsize)
    ctx = cairo.Context(surface)

    # we will put the center of the hexagon at the origin
    a, b, c = hexagon_size
    ctx.translate(imgsize / 2.0, imgsize / 2.0)
    extent = max(c, a * HALFSQRT3, b * HALFSQRT3) + 1
    ctx.scale(imgsize / (extent * 2.0), -imgsize / (extent * 2.0))
    ctx.translate(-b * HALFSQRT3, -c / 2.0)

    # paint background
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)

    T = LozengeTiling(hexagon_size)
    sample = run_cftp(T)
    for key, val in T.get_tiles(sample).items():
        for verts in val:
            A, B, C, D = square_to_hex(verts)
            ctx.move_to(A[0], A[1])
            ctx.line_to(B[0], B[1])
            ctx.line_to(C[0], C[1])
            ctx.line_to(D[0], D[1])
            ctx.close_path()
            if key == "T":
                ctx.set_source_rgb(*TOP_COLOR)
            elif key == "L":
                ctx.set_source_rgb(*LEFT_COLOR)
            else:
                ctx.set_source_rgb(*RIGHT_COLOR)
            ctx.fill_preserve()
            ctx.set_line_width(LINE_WIDTH)
            ctx.set_source_rgb(*EDGE_COLOR)
            ctx.stroke()

    surface.write_to_png("random_lozenge_tiling.png")


if __name__ == "__main__":
    main((20, 20, 20), 600)
