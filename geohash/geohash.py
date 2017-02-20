# coding: utf-8

# system packages
from functools import partial
# third-party packages

# own packages
from constant import const


"""
geohash精度的设定参考 http://en.wikipedia.org/wiki/Geohash
geohash length	lat bits	lng bits	lat error	lng error	km error
1				2			3			±23			±23			±2500
2				5			5			± 2.8		± 5.6		±630
3				7			8			± 0.70		± 0.7		±78
4				10			10			± 0.087		± 0.18		±20
5				12			13			± 0.022		± 0.022		±2.4
6				15			15			± 0.0027	± 0.0055	±0.61
7				17			18			±0.00068	±0.00068	±0.076
8				20			20			±0.000085	±0.00017	±0.019
"""


class EncodedPoint(object):
    def __init__(self, code=0, max_latitude=90.0, max_longitude=180.0,
                 min_latitude=-90.0, min_longitude=-180.0):
        self.code = code
        self.max_latitude = max_latitude
        self.max_longitude = max_longitude
        self.min_latitude = min_latitude
        self.min_longitude = min_longitude

    def __str__(self):
        return "{} {} {} {} {}".format(self.code, self.max_latitude,
                                       self.max_longitude,
                                       self.min_latitude, self.min_longitude)


def encode(latitude, longitude, precision):
    length = 0
    bit = ""
    total_bits = 0
    max_latitude = const.MAX_LATITUDE
    max_longitude = const.MAX_LONGITUDE
    min_latitude = const.MIN_LATITUDE
    min_longitude = const.MIN_LONGITUDE
    res = ""
    while length < precision:
        if total_bits % 2 == 0:
            mid = float(max_longitude + min_longitude) / 2
            if longitude > mid:
                bit += "1"
                min_longitude = mid
            else:
                bit += "0"
                max_longitude = mid
        else:
            mid = float(max_latitude + min_latitude) / 2
            if latitude > mid:
                bit += "1"
                min_latitude = mid
            else:
                bit += "0"
                max_latitude = mid
        total_bits += 1
        if len(bit) == 5:
            res += const.BASE32[int(bit, base=2)]
            bit = ""
            length += 1
    return EncodedPoint(res, max_latitude, max_longitude,
                        min_latitude, min_longitude)


def neighbors(latitude, longitude, precision):
    self_code = encode(latitude, longitude, precision)
    latitude_delta = (self_code.max_latitude - self_code.min_latitude) / 2
    longitude_delta = (self_code.max_longitude - self_code.min_longitude) / 2

    direction = [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1),
                 (1, -1), (1, 1)]

    partial_func = partial(encode, precision=precision)
    return list(map(lambda item: partial_func(item[0] * latitude_delta,
                                         item[1] * longitude_delta), direction))


def main():
    latitude = 42.6
    longitude = -5.6
    precision = 5
    encoded_point = \
        encode(latitude, longitude, precision)
    print(encoded_point)
    for item in neighbors(latitude, longitude, precision):
        print(item)


if __name__ == "__main__":
    main()
