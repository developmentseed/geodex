# GeoDex

GeoDex is tool to find tile indices for geospatial work. Given (1) a geojson file containing a boundary and (2)a zoom level, GeoDex will return all tile indices that at least partially overlap the boundary. Returned tile indices can be written to a text file for further processing.


Basic usage:
```
geodex geodex/test/roi_single.geojson
```
Returns:
```

```

Typical usage:
```
# Write output of boundary to text file
# Note that this will OVERWRITE `tile_indices.txt` if it exists
geodex -g boundary.geojson -z 15 > tile_indices.txt


# Append multiple outputs to text file
geodex -g zone_1.geojson -z 15 >> tile_indices.txt
geodex -g zone_17.geojson -z 15 >> tile_indices.txt

```


GeoDex is optimized to use very little RAM. It uses a depth-first search algorithm to avoid storing large amounts of tile indices in memory. GeoDex was developed during a project to map high-voltage electricity lines that was supported by the World Bank.