#!/usr/bin/python3

#based on https://github.com/aboood40091/BNTX-Extractor/blob/master/swizzle.py

def DIV_ROUND_UP(n, d):
    return (n + d - 1) // d

def round_up(x, y):
    return ((x - 1) | (y - 1)) + 1


def _swizzle(width, height, blkWidth, blkHeight, bpp, tileMode, size_range, data, toSwizzle):
    block_height = 1 << size_range

    width = DIV_ROUND_UP(width, blkWidth)
    height = DIV_ROUND_UP(height, blkHeight)

    if tileMode == 1:
        if roundPitch == 1:
            pitch = round_up(width * bpp, 32)
        else:
            pitch = width * bpp
        surfSize = round_up(pitch * height, 32)

    else:
        pitch = round_up(width * bpp, 64)
        surfSize = pitch * round_up(height, block_height * 8)

    result = bytearray(surfSize)

    for y in range(height):
        for x in range(width):
            if tileMode == 1:
                pos = y * pitch + x * bpp

            else:
                pos = getAddrBlockLinear(x, y, width, bpp, 0, block_height)

            pos_ = (y * width + x) * bpp

            if pos + bpp <= surfSize:
                if toSwizzle == 1:
                    result[pos:pos + bpp] = data[pos_:pos_ + bpp]

                else:
                    result[pos_:pos_ + bpp] = data[pos:pos + bpp]
    size = width * height * bpp
    return result[:size]


def deswizzle(width, height, blkWidth, blkHeight, bpp, tileMode, size_range, data):
    return _swizzle(width, height, blkWidth, blkHeight, bpp, tileMode, size_range, bytes(data), 0)


def swizzle(width, height, blkWidth, blkHeight, bpp, tileMode, size_range, data):
    return _swizzle(width, height, blkWidth, blkHeight, bpp, tileMode, size_range, bytes(data), 1)


def getAddrBlockLinear(x, y, image_width, bytes_per_pixel, base_address, block_height):
    """
    From the Tegra X1 TRM
    """
    image_width_in_gobs = DIV_ROUND_UP(image_width * bytes_per_pixel, 64)

    GOB_address = (base_address
                   + (y // (8 * block_height)) * 512 * block_height * image_width_in_gobs
                   + (x * bytes_per_pixel // 64) * 512 * block_height
                   + (y % (8 * block_height) // 8) * 512)

    x *= bytes_per_pixel

    Address = (GOB_address + ((x % 64) // 32) * 256 + ((y % 8) // 2) * 64
               + ((x % 32) // 16) * 32 + (y % 2) * 16 + (x % 16))

    return Address
