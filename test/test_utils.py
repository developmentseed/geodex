"""
test_utils.py

@author: DevelopmentSeed

Test all utilities.
"""
import os
import unittest
from pygeotile.tile import Tile

from geodex.utils import _get_quadrant_tiles, format_tile
testpath = os.path.dirname(__file__)


class TestUtils(unittest.TestCase):
    """Test utility functions."""

    def test_get_quadrant_tiles(self):
        """Test ability to get tile children on level of increased zoom."""
        tile = Tile.from_google(0, 0, 0)
        child_tiles = _get_quadrant_tiles(tile)
        self.assertEqual(child_tiles, [Tile.from_google(0, 0, 1),
                                       Tile.from_google(0, 1, 1),
                                       Tile.from_google(1, 0, 1),
                                       Tile.from_google(1, 1, 1)])


    def test_string_output(self):
        """Test that tile details are correctly printed."""

        tile = Tile.from_google(3, 1, 2)

        self.assertEqual(format_tile(tile, 'google'), '3 1 2')
        self.assertEqual(format_tile(tile, 'tms'), '3 2 2')
        self.assertEqual(format_tile(tile, 'quad_tree'), '13')

        self.assertEqual(format_tile(tile, 'google', '{z}-{x}-{y}'), '2-3-1')
        self.assertEqual(format_tile(tile, 'tms', '{z}-{x}-{y}'), '2-3-2')


    def test_overlap(self):
        """Test that overlap between two shapes is correct."""
        pass
