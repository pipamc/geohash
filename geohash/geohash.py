# coding: utf-8

# system packages

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
    return res, max_latitude, max_longitude, min_latitude, min_longitude


def neighbors(latitude, longitude, precision):
    self_code = encode(latitude, longitude, precision)
    latitude_delta = self_code[1] - self_code[3]
    longitude_delta = self_code[2] - self_code[4]
    up = encode(latitude + latitude_delta / 2, longitude, precision)
    down = encode(latitude - latitude_delta / 2, longitude, precision)
    left = encode(latitude, longitude - longitude_delta / 2, precision)
    right = encode(latitude, longitude + longitude_delta / 2, precision)
    left_up = encode(latitude + latitude_delta / 2,
                     longitude - longitude_delta / 2, precision)
    left_down = encode(latitude - latitude_delta / 2,
                       longitude - longitude_delta / 2, precision)
    right_up = encode(latitude + latitude_delta / 2,
                      longitude + longitude_delta / 2, precision)
    right_down = encode(latitude + latitude_delta / 2,
                        longitude - longitude_delta / 2, precision)
    return up, down, left, right, left_up, left_down, right_up, right_down


def main():
    latitude = 42.6
    longitude = -5.6
    precision = 5
    code, max_latitude, max_longitude, min_latitude, min_longitude = \
        encode(latitude, longitude, precision)
    print(code, max_latitude, max_longitude, min_latitude, min_longitude)
    print(neighbors(latitude, longitude, precision))
main()
