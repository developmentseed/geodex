"""
test_utils.py

@author: DevelopmentSeed

Test all utilities.
"""
import os
import unittest
from unittest.mock import patch
from io import StringIO

from pygeotile.tile import Tile

from geodex.search import tile_search, process_geojson
from geodex.utils import load_geojson

testpath = os.path.dirname(__file__)

class TestCore(unittest.TestCase):
    """Test core functionality."""

    @patch('sys.stdout', new_callable=StringIO)
    def test_single_boundary_tile_search(self, mock_stdout):

        """Test that tiles are correctly found for a single boundary."""
        tile_inds = ('2494 2126 12\n'
                     '2494 2125 12\n'
                     '2493 2126 12\n'
                     '2493 2125 12\n')

        # Load geojson, get 0th object
        shape_json = load_geojson('./roi_single.geojson')[0]

        num_tiles = tile_search(shape_json, max_zoom=12)
        self.assertEqual(num_tiles, 4)
        self.assertEqual(mock_stdout.getvalue(), tile_inds)


    @patch('sys.stdout', new_callable=StringIO)
    def test_multiboundary_tile_search(self, mock_stdout):
        """Test that tiles are correctly found for multiple boundaries."""
        tile_inds = ('2494 2126 12\n'
                     '2494 2125 12\n'
                     '2493 2126 12\n'
                     '2493 2125 12\n'
                     '1944 1569 12\n'
                     '1943 1569 12\n'
                     '2086 1974 12\n'
                     '2086 1973 12\n'
                     '2085 1974 12\n'
                     '2085 1973 12\n')

        shape_json = load_geojson('./roi_triple.geojson')
        num_tiles = process_geojson(shape_json, max_zoom=12,
                                    tile_format='google')
        self.assertEqual(num_tiles, 10)
        self.assertEqual(mock_stdout.getvalue(), tile_inds)
