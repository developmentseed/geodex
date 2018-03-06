"""
search.py

@author: DevelopmentSeed

Backend algorithms for finding tiles within a geospatial boundary
"""
from queue import LifoQueue

from shapely.geometry import shape
from pygeotile.tile import Tile

from geodex.utils import get_overlap_child_tiles, format_tile


def tile_search(boundary, max_zoom, tile_format='google',
                output_format='{x} {y} {z}', print_to=None):
    """Print (or save) tiles belonging to a shape object.

    Parameters:
    ----------
    boundary: str
        JSON corresponding to a single polygon/multipolygon
    max_zoom: int
        Zoom at which to terminate file search
    tile_format: str
        Desired tile format. `google` (default), `tms`, or `quad_tree`
    output_format: str
        Format string for printing the tile indices. Only used for tile_format
        `google` and `tms`. Must contain `{x}`, `{y}`, and `{z}`.
    print_to: object with `write` functionality
        `None` (default) prints to sys.stdout. Pass a (non-binary) file object
        to print directly to an open file.

    Returns:
    -------
    total_tiles: int
        Number of tiles found

    Note: this function is useful if you want to directly incorporate tile
    searching into a script (i.e., not on the command line).
    """
    #########################################
    # Initialize boundary and queue
    #########################################
    bound_shape = shape(boundary)  # Convert JSON to shape object
    stack = LifoQueue()
    total_tiles = 0

    # Put whole-world tile on stack
    start_tile = Tile.from_google(0, 0, 0)
    stack.put([start_tile, False])

    #########################################
    # Depth-first search on tile indices
    #########################################
    while not stack.empty():

        # Pop the top tile in the stack
        top_tile, comp_contained = stack.get()

        # Check if desired zoom has been reached
        if top_tile.zoom >= max_zoom:
            # If at max zoom, print tile inds or save to file (if specified)
            print(format_tile(top_tile, tile_format, output_format),
                  file=print_to)
            total_tiles += 1

        # Otherwise, zoom in one increment, find children tiles, add to stack
        else:
            ret_tiles = get_overlap_child_tiles(top_tile, bound_shape,
                                                comp_contained)
            for rt in ret_tiles:
                stack.put(rt)

    return total_tiles


def process_geojson(boundaries, max_zoom, tile_format, output_format):
    """Process entire list of boundaries."""
    total_tiles = 0

    # Loop through all boundaries and compute tiles for each
    for bound in boundaries:
        bound_tiles = tile_search(bound, max_zoom, tile_format, output_format)
        total_tiles += bound_tiles

    return total_tiles
