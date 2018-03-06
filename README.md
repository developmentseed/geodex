# GeoDex

GeoDex is tool to find tile indices for geospatial work. Given **(1)** a geojson file containing a boundary and **(2)** a zoom level, GeoDex will return all tile indices that at least partially overlap the boundary. Returned tile indices can be written to a text file for further processing.


## Basic usage
```
geodex test/roi_single.geojson 12
```
Returns:
```
2494 2126 12
2494 2125 12
2493 2126 12
2493 2125 12
```

Specify output format string:
```
geodex test/roi_single.geojson 12 'google' --output-format "{z}-{x}-{y}"
```
Returns:
```
12-2494-2126
12-2494-2125
12-2493-2126
12-2493-2125
```

## Typical usage
Write output of boundary to text file
Note that using `>` like below will **overwrite** `tile_indices.txt` if it exists.
```
geodex zone_1.geojson 15 'tms' > tile_indices.txt
```

Avoid overwrite by **appending** multiple outputs to text file using `>>`
```
geodex zone_1.geojson 15 'tms' >> tile_indices.txt
geodex zone_17.geojson 15 'tms' >> tile_indices.txt
```

GeoDex is optimized to use very little RAM. It uses a depth-first search algorithm to avoid storing large amounts of tile indices in memory. GeoDex was developed during a project to map high-voltage electricity lines that was supported by the World Bank.