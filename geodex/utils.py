"""
utils.py

@author: developmentseed

Functions used to generate a list of tiles via recursion
"""
from os import path as op

import json
from shapely.geometry import Polygon
from pygeotile.tile import Tile


def _get_quadrant_tiles(tile):
    """Return indicies of tiles at one higher zoom (in google tiling scheme)"""
    ul = (tile.google[0] * 2, tile.google[1] * 2)

    return [Tile.from_google(ul[0], ul[1], tile.zoom + 1),           # UL
            Tile.from_google(ul[0], ul[1] + 1, tile.zoom + 1),       # LL
            Tile.from_google(ul[0] + 1, ul[1], tile.zoom + 1),       # UR
            Tile.from_google(ul[0] + 1, ul[1] + 1, tile.zoom + 1)]   # LR


def _calc_overlap(geom1, geom2):
    """Return area overlap"""

    return geom1.intersection(geom2).area


def load_geojson(geojson_fpath):
    """Load geojson and return all contained polygons.

    Parameters:
    ----------
    geojson_fpath: str
        Filepath of to geojson containing boundaries.

    Returns:
    -------
    bounds: list
        List of geometries read from geojson file."""

    if not op.exists(geojson_fpath):
        raise FileNotFoundError('{} does not exist'.format(geojson_fpath))
    if not op.splitext(geojson_fpath) not in ['.geojson', '.json']:
        raise ValueError('{} should be a .geojson or .json file'.format(geojson_fpath))

    bounds = None
    with open(geojson_fpath, 'r') as geojson_f:
        raw_json = json.loads(geojson_f.read())
        features = raw_json['features']

        bounds = [feat['geometry'] for feat in features
                  if feat['geometry']['type'] in ['Polygon', 'MultiPolygon']]
    return bounds


def format_tile(tile, tile_format, format_str='{x} {y} {z}'):
    """Convert tile to necessary format.

    Parameters
    ----------
    tile: pygeotile.tile.Tile
        Tile object to be formatted.
    tile_format: str
        Desired tile format. `google`, `tms`, or `quad_tree`
    format_str: str
        String to guide formatting. Only used for `google` or `tms`
        (as quad_tree is one value).
        Default: "{x} {y} {z}". Example: "{z}-{x}-{y}"
    """

    if tile_format == 'google':
        td = {key: val for key, val
              in zip(['x', 'y', 'z'], list(tile.google) + [tile.zoom])}
        return format_str.format(**td)

    elif tile_format == 'tms':
        td = {key: val for key, val
              in zip(['x', 'y', 'z'], list(tile.tms) + [tile.zoom])}
        return format_str.format(**td)

    elif tile_format == 'quad_tree':
        return tile.quad_tree

    else:
        raise ValueError('`tile_format`: {} not recognized'.format(tile_format))


def get_overlap_child_tiles(tile, roi_geom, completely_contained=False):
    """Find all children tiles that overlap a boundary

    Parameters
    ----------
    tile: pygeotile.tile.Tile
        Tile that is checked for overlap with `roi_geom`.
    roi_geom: shapely.geometry.shape
        Boundary of region-of-interest.
    completely_contained: bool
        Whether or not a tile is completely contained in the boundary.
        If a tile is found to have 100% overlap with boundary, set to `True`
        and algorithm can avoid calculating overlap for all future child tiles.
        Default False.

    Returns:
    -------
    return_tiles: list of pygeotile.tile.Tile, bool
        Tiles that are children of `tile` and overlap the boundary

    """

    return_tiles = []
    quad_tiles = _get_quadrant_tiles(tile)  # Compute four contained tiles

    # If sub-tiles are completely contained within boundary, no need to compute overlap
    if completely_contained:
        return [[qt, True] for qt in quad_tiles]

    # For each tile, compute overlap with ROI boundary
    for qt in quad_tiles:
        ll, ur = qt.bounds  # Get lower-left and upper-right points
        tile_pts = ((ll[1], ll[0]), (ur[1], ll[0]),
                    (ur[1], ur[0]), (ll[1], ur[0]))
        tile_polygon = Polygon(tile_pts)

        # Calculate overlap of tile with ROI
        overlap_area = _calc_overlap(roi_geom, tile_polygon)

        # If 100% overlap, indicate this to avoid checking overlap in future
        if overlap_area == tile_polygon.area:
            return_tiles.append([qt, True])
        elif overlap_area > 0:
            return_tiles.append([qt, False])

    return return_tiles
