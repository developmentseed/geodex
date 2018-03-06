"""
main.py

@author: DevelopmentSeed

Core command line functionality for geodex
"""

import sys
import argparse
import logging
from datetime import datetime as dt

from geodex.version import __version__
from geodex.search import process_geojson
from geodex.utils import load_geojson


logger = logging.getLogger(__name__)
max_zoom = 22  # Highest zoom level allowed
tile_format_options = ['google', 'quad_tree', 'tms']


def parse_args(args):
    """Parse command line arguments."""

    desc = 'geodex (v%s)' % __version__
    #dhf = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(description=desc)

    #pparser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--version', help='Print version and exit',
                        action='version', version=__version__)
    parser.add_argument('--log', default=2, type=int, choices=range(0, 6),
                        help='0:all, 1:debug, 2:info, 3:warning, 4:error, 5:critical')

    parser.add_argument('geojson', type=str,
                        help='File path to geojson file containing at least one geospatial boundary.')
    parser.add_argument('zoom', type=int, choices=range(0, max_zoom + 1),
                        help='Zoom level specifying spatial resolution of returned tiles. Must be integer 0-22.',
                        metavar='zoom')
    parser.add_argument('tile-format', type=str, default='google', nargs='?',
                        choices=tile_format_options,
                        help="Specify the tile index format. Default: 'google'")
    parser.add_argument('--output-format', '-o', default='{x} {y} {z}',
                        type=str, help=("Output tile format string."
                                        "Only valid for tile-formats `google` or `tms`."
                                        "Default: '{x} {y} {z}'. Example: '{z}-{x}-{y}'"))

    # turn Namespace into dictionary
    parsed_args = vars(parser.parse_args(args))

    return parsed_args


def cli():
    """Validate input and execute command"""
    args = parse_args(sys.argv[1:])
    logger.setLevel(args.pop('log') * 10)
    #cmd = args.pop('command')

    geojson_fpath = args.get('geojson')
    zoom = args.get('zoom')
    tile_format = args.get('tile-format')
    output_format = args.get('output_format')

    st_dt = dt.now()  # Start time
    logger.info('Elapsed time: %s', st_dt)

    ###################################
    # Run tile search
    ###################################
    # Get all polygon bounds from geojson file
    geojson_bounds = load_geojson(geojson_fpath)

    # Process all polygons
    process_geojson(geojson_bounds, zoom, tile_format, output_format)

    #########################################
    # Print some final details
    #########################################
    delta = dt.now() - st_dt
    logger.info('Elapsed time: %s', delta)


if __name__ == "__main__":
    cli()
