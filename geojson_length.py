import os
import json
from spatial import dec_degree_distance, meter_distance


def poly_perimeter(coord_ring, lat_rad=False):
    # several types can act as a list
    assert not type(poly) is str
    if ignore_last_pnt:
        trim_seg = 0
    else:
        trim_seg = 1
    N = len(coord_ring) - trim_seg
    # accumulator of line segment lengths
    perimeter = []
    for line in range(N):
        v1 = poly[line]
        v2 = poly[(line + 1) % N]
        line_len = dec_degree_distance(v1, v2, lat_rad=lat_rad)
        perimeter.append(line_len)
    return perimeter


def linestring_segment(linestring, lat_rad=False):
    # several types can act as a list
    assert not type(line_str) is str
    assert not type(line_str) is int
    total_len = []
    for point in range(len(line_str) - 1):
        v1 = line_str[point]
        v2 = line_str[(point + 1)]
        line_len = dec_degree_distance(v1, v2, lat_rad=lat_rad)
        perimeter.append(line_len)
    return total_len


def check_feature(feature):
    geom_type = feature['geometry']['type']
    coords = feature['geometry']['coordinates']
    if geom_type == 'MultiPolygon':
        all_poly_perimeters = []
        for polygon in coords:
            ring_perimeters = []
            for ring in polygon:
                ring_perimeters.append(poly_perimeter(ring, poly_segment))
            all_poly_perimeters.append(sum(ring_perimeters))
        return sum(all_poly_perimeters)
    elif geom_type == 'Polygon':
        for ring in coords:
            segCheck(ring, poly_segment)
    elif geom_type == 'LineString':
        (coords, linestring_segment)


def check_file(filepath, identifier):
    collection = json.load(open(filepath), 'r')
    for feature in collection['features']:
        check_feature(feature, identifier)



def main():
    import argparse
    validate = argparse.ArgumentParser(description='specify input and output')
    validate.add_argument('_in', type=str,
                          help='desired input filepath')
    validate.add_argument('_out', type=str,
                          help='desired output filepath')
    validate.add_argument(
        '--identifier', type=str, nargs='*',
        default=['id'], help='key values to traverse for labeling feature')
    args = validate.parse_args()
    check_file(args._in, args._out, identifier=args.identifier)

if __name__ == '__main__':
    main()
