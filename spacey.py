from math import radians, sqrt, atan2, tan, cos, sin, acos, degrees


def geocentric_radius(lat):
    """
    Implementation of geocentric radius
    φ -> latitude, a -> equatorial radius, b -> polar radius
    R(φ)^2 = ((a^2 cos(φ))^2 + (b^2 sin(φ))^2)/
                ((a cos(φ))^2 + (b sin(φ))^2)
    https://en.wikipedia.org/wiki/Earth_radius#Geocentric_radius

    Args:
        lat: latitude in decimal degrees

    Returns:
        Radius of earth with given latitude at sea level in meteres
    """
    assert type(lat) is float
    a = 6378.137e3
    b = 6356.7523e3
    radius = sqrt(
        ((a ** 2 * cos(lat)) ** 2 + (b ** 2 * sin(lat)) ** 2)
        / ((a * cos(lat)) ** 2 + (b * sin(lat)) ** 2)
    )
    return radius


def meter_distance(p1, p2):
    """
    Standard pythagorean distance implementation given two points.
    NOTE: Assumption is coordinates are projected in meteres

    Args:
        p1: array/tuple of float pair arranged in [x₁,y₁] format
        p2: array/tuple of float pair arranged in [x₂,y₂] format

    Returns:
        float: The calculated length of input points
    """
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def dec_degree_distance(p1, p2, lat_rad=False):
    """
    Implementation of haversine formulae
    φ -> latitude, λ -> longitude
    a = sin²(Δφ/2) + cos(φ1)⋅cos(φ2)⋅sin²(Δλ/2)
    tanδ = √(a) / √(1−a)

    Args:
        p1: array/tuple of float pair arranged in [x₁,y₁] format
        p2: array/tuple of float pair arranged in [x₂,y₂] format
        lat_rad: desired radius at given latitude

    Returns:
        float: The calculated length of input points in meteres
    """
    msg = "ensure latitude value used to derive radius is a float"
    assert type(lat_rad) is float or type(lat_rad) is bool, msg
    if lat_rad:
        R = geocentric_radius(lat_rad)
    else:
        R = 6371e3
    lon_dlt = radians(p1[0] - p2[0])
    lat_dlt = radians(p1[1] - p2[1])
    p1 = [radians(p1[0]), radians(p1[1])]
    p2 = [radians(p2[0]), radians(p2[1])]
    a = sin(lat_dlt / 2) ** 2 + cos(p1[1]) * cos(p2[1]) * sin(lon_dlt / 2) ** 2
    return 2 * atan2(sqrt(a), sqrt(1 - a)) * R ** 2


def euclidean_area(poly, precision=6):
    """
    An implementation of Green's theorem, an algorithm to calculate area of
    a closed polgon. This works for convex and concave polygons that do not
    intersect oneself whose vertices are described by ordered pairs.
    https://gist.github.com/rob-murray/11245628

    Args:
        poly: The polygon expressed as a list of vertices, or 2D vector points
        precision: How many decimal places to truncate for the returned result

    Returns:
        float: The calculated area of input polygon in meteres
    """
    # ensure we have a list; best to assert that it isnt a string as in python
    # several types can act as a list
    assert not isinstance(poly, str)
    total = 0.0
    N = len(poly)

    for i in range(N):
        v1, v2 = poly[i], poly[(i + 1) % N]
        total += v1[0] * v2[1] - v1[1] * v2[0]
    return float(round(abs(total / 2), precision))


def non_euclidean_area(poly, precision=6, lat_rad=False):
    """
    An implementation of the geodesy spherical excess formulae,
    an algorithm to calculate area of a closed polgon projected onto a sphere.
    https://github.com/chrisveness/geodesy/blob/master/latlon-spherical.js#L566

    Args:
        poly: The polygon expressed as a list of vertices, or 2D vector points
        precision: How many decimal places to truncate for the returned result
        lat_rad: desired radius at given latitude

    Returns:
        float: The resulting area using in meteres.
        NOTE: accuracy decreases inversely with area of polygon;
        consider calculating earth radius at longitude for larger than
        city-sized polygons
    """
    # ensure we have a list; best to assert that it isn't a string as in python
    # several types can act as a list
    assert not isinstance(poly, str)
    msg = "ensure latitude value used to derive radius is a float"
    assert type(lat_rad) is float or type(lat_rad) is bool, msg
    if lat_rad:
        R = geocentric_radius(lat_rad)
    else:
        R = 6371e3
    total = 0.0
    N = len(poly)

    for i in range(N):
        v1, v2 = poly[i], poly[(i + 1) % N]
        lon_dlt = radians(v2[0]) - radians(v1[0])
        lat1 = radians(v1[1])
        lat2 = radians(v2[1])
        total += 2 * atan2(
            tan(lon_dlt / 2) * (tan(lat1 / 2) + tan(lat2 / 2)),
            1 + tan(lat1 / 2) * tan(lat2 / 2),
        )
    return float(round(abs(total * R ** 2), precision))


def angle(s, a, b):
    """
    An application of the law of cosines, an algorithm to calculate area of
    a closed polygon.
    This expects a 2D vector point  with adjacent sibling points.

    Args:
        s: The 2D vector point used to derive theta.
        a: The subsequent point used to calculate the A dot product.
        b: The preceding point used to calculate the B dot product.
    """
    Ax = s[0] - a[0]
    Ay = s[1] - a[1]
    Bx = s[0] - b[0]
    By = s[1] - b[1]
    # get length of vectors
    lenA = sqrt(Ax ** 2 + Ay ** 2)
    lenB = sqrt(Bx ** 2 + By ** 2)
    # get dot product of the two vectors
    sclrAB = Ax * Bx + Ay * By
    # cos theta =  (Ax * Bx + Ay * By)/lenA * lenB
    try:
        return degrees(acos(round(sclrAB / (lenA * lenB), 6)))
    # report on zero division error with verbosity
    except ZeroDivisionError as e:
        e.args += f"points:[{s},{a},{b}]"
        raise e
