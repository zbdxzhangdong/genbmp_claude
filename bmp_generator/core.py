# -*- coding: utf-8 -*-
# 共享 BMP 图案生成算法 —— 纯函数，无 UI 依赖

import os
import math
import numpy
from PIL import Image


def generate_solid_color(params, output_dir=None, _preview=False):
    """生成纯色图"""
    bmp_width = 200 if _preview else params["bmp_width"]
    bmp_height = 200 if _preview else params["bmp_height"]
    colors = params.get("gray_value", [255, 0, 0])

    # 兼容 CLI 的多颜色列表 [[R,G,B], ...] 和 GUI 的单颜色 [R,G,B]
    if colors and isinstance(colors[0], list):
        color_list = colors
    else:
        color_list = [colors]

    for idx, color in enumerate(color_list):
        new_array = numpy.zeros((bmp_height, bmp_width, 3), dtype=numpy.uint8)
        new_array[:] = color
        new_im = Image.fromarray(new_array)
        if len(color_list) == 1:
            r, g, b = color
            if r == g == b:
                bmp_name = "Gray%d_%dRGB_%d.bmp" % (r, bmp_width, bmp_height)
            elif color.count(0) == 2:
                if r != 0:
                    bmp_name = "R%d_%dRGB_%d.bmp" % (r, bmp_width, bmp_height)
                elif g != 0:
                    bmp_name = "G%d_%dRGB_%d.bmp" % (g, bmp_width, bmp_height)
                else:
                    bmp_name = "B%d_%dRGB_%d.bmp" % (b, bmp_width, bmp_height)
            else:
                bmp_name = "R%d_G%d_B%d_%dRGB_%d.bmp" % (r, g, b, bmp_width, bmp_height)
        else:
            bmp_name = "color_%d.bmp" % idx
        if _preview:
            return new_im
        new_im.save(os.path.join(output_dir, bmp_name))


def generate_solid_color_batch(params, output_dir=None, start_r=0, start_g=0, start_b=0, stop_r=255, stop_g=255, stop_b=255, _preview=False):
    """生成纯色渐变序列（GUI 批量转功能）"""
    bmp_width = 200 if _preview else params["bmp_width"]
    bmp_height = 200 if _preview else params["bmp_height"]
    r_flag = start_r != stop_r
    g_flag = start_g != stop_g
    b_flag = start_b != stop_b
    range_val = max(abs(stop_r - start_r), abs(stop_g - start_g), abs(stop_b - start_b)) + 1

    for step in range(range_val):
        r = start_r + step if r_flag else start_r
        g = start_g + step if g_flag else start_g
        b = start_b + step if b_flag else start_b
        new_array = numpy.zeros((bmp_height, bmp_width, 3), dtype=numpy.uint8)
        new_array[:] = [r, g, b]
        new_im = Image.fromarray(new_array)
        bmp_name = "R%d_G%d_B%d_%dRGB_%d.bmp" % (r, g, b, bmp_width, bmp_height)
        if _preview:
            return new_im
        new_im.save(os.path.join(output_dir, bmp_name))


def generate_grayscale(params, output_dir=None, r_checked=True, g_checked=True, b_checked=True, _preview=False):
    """生成灰阶过渡图"""
    bmp_width = 200 if _preview else params["bmp_width"]
    bmp_height = 200 if _preview else params["bmp_height"]
    transition_type = params.get("transition_type", 0)
    max_gray = params["max_gray"]
    min_gray = params["min_gray"]
    start_gray = max(max_gray)
    stop_gray = max(min_gray)
    gray_range = abs(stop_gray - start_gray)

    new_array = numpy.zeros((bmp_height, bmp_width, 3), dtype=numpy.uint8)

    if transition_type == 1:
        # 纵向过渡
        for x in range(bmp_height):
            if stop_gray >= start_gray:
                gray = int(x * gray_range / (bmp_height - 1)) + start_gray if bmp_height > 1 else start_gray
            else:
                gray = (gray_range - int(x * gray_range / (bmp_height - 1))) + stop_gray if bmp_height > 1 else stop_gray
            R = 0 if not r_checked else gray
            G = 0 if not g_checked else gray
            B = 0 if not b_checked else gray
            new_array[x:x + 1, :] = [R, G, B]
    else:
        # 横向过渡
        for x in range(bmp_width):
            if stop_gray >= start_gray:
                gray = int(x * gray_range / (bmp_width - 1)) + start_gray if bmp_width > 1 else start_gray
            else:
                gray = (gray_range - int(x * gray_range / (bmp_width - 1))) + stop_gray if bmp_width > 1 else stop_gray
            R = 0 if not r_checked else gray
            G = 0 if not g_checked else gray
            B = 0 if not b_checked else gray
            new_array[:, x:x + 1] = [R, G, B]

    new_im = Image.fromarray(new_array)
    bmp_name = "Gray_%dRGB_%d.bmp" % (bmp_width, bmp_height)
    if _preview:
        return new_im
    new_im.save(os.path.join(output_dir, bmp_name))


def generate_center_square(params, output_dir=None, _preview=False):
    """生成中间方形图"""
    bmp_width = 200 if _preview else params["bmp_width"]
    bmp_height = 200 if _preview else params["bmp_height"]
    new_array = numpy.zeros((bmp_height, bmp_width, 3), dtype=numpy.uint8)
    new_array[:] = params["back_color"]
    sr = params["center_start_row"]
    sc = params["center_start_col"]
    new_array[sr:sr + params["center_height"], sc:sc + params["center_width"]] = params["center_color"]
    new_im = Image.fromarray(new_array)
    bmp_name = "square_%dRGB_%d.bmp" % (bmp_width, bmp_height)
    if _preview:
        return new_im
    new_im.save(os.path.join(output_dir, bmp_name))


def generate_checkerboard(params, output_dir=None, _preview=False):
    """生成棋盘格图"""
    bmp_width = 200 if _preview else params["bmp_width"]
    bmp_height = 200 if _preview else params["bmp_height"]
    sub_size = params["sub_size"]
    color1 = params["sub_type1_color"]
    color2 = params["sub_type2_color"]

    new_array = numpy.zeros((bmp_height, bmp_width, 3), dtype=numpy.uint8)
    for i in range(bmp_height):
        data1 = [color1] * sub_size
        data2 = [color2] * sub_size
        even_data = (data1 + data2) * bmp_width
        odd_data = (data2 + data1) * bmp_width
        type_start_row = i * sub_size
        type_stop_row = type_start_row + sub_size
        if type_start_row >= bmp_height:
            break
        if type_stop_row >= bmp_height:
            row_data = even_data[0:bmp_width] if i % 2 == 0 else odd_data[0:bmp_width]
            new_array[type_start_row:bmp_height] = numpy.array([numpy.array(row_data)] * (bmp_height - type_start_row))
            break
        row_data = even_data[0:bmp_width] if i % 2 == 0 else odd_data[0:bmp_width]
        new_array[type_start_row:type_stop_row] = numpy.array([numpy.array(row_data)] * sub_size)

    new_im = Image.fromarray(new_array)
    bmp_name = "dot%d_%dRGB_%d.bmp" % (sub_size, bmp_width, bmp_height)
    if _preview:
        return new_im
    new_im.save(os.path.join(output_dir, bmp_name))


def generate_stripes(params, output_dir=None, _preview=False):
    """生成条纹图"""
    bmp_width = 200 if _preview else params["bmp_width"]
    bmp_height = 200 if _preview else params["bmp_height"]
    stripe_type = params.get("type", 0)
    band1_color = params["sub_band1_color"]
    band1_size = params["sub_band1_size"]
    band2_color = params["sub_band2_color"]
    band2_size = params["sub_band2_size"]

    new_array = numpy.zeros((bmp_height, bmp_width, 3), dtype=numpy.uint8)

    if stripe_type == 1:
        # 横向条纹
        i = 0
        while i < bmp_height:
            band1_start = i * (band1_size + band2_size)
            band1_stop = band1_start + band1_size
            band2_start = band1_stop
            band2_stop = band1_stop + band2_size
            if band1_stop > bmp_height:
                new_array[band1_start:bmp_height] = band1_color
            else:
                new_array[band1_start:band1_stop] = band1_color
            if band2_stop > bmp_height:
                new_array[band2_start:bmp_height] = band2_color
            else:
                new_array[band2_start:band2_stop] = band2_color
            i += 1
    else:
        # 纵向条纹
        i = 0
        while i < bmp_width:
            band1_start = i * (band1_size + band2_size)
            band1_stop = band1_start + band1_size
            band2_start = band1_stop
            band2_stop = band1_stop + band2_size
            if band1_stop > bmp_width:
                new_array[:, band1_start:bmp_width] = band1_color
            else:
                new_array[:, band1_start:band1_stop] = band1_color
            if band2_stop > bmp_width:
                new_array[:, band2_start:bmp_width] = band2_color
            else:
                new_array[:, band2_start:band2_stop] = band2_color
            i += 1

    new_im = Image.fromarray(new_array)
    bmp_name = "stripe_%dRGB_%d.bmp" % (bmp_width, bmp_height)
    if _preview:
        return new_im
    new_im.save(os.path.join(output_dir, bmp_name))


def generate_border_frame(params, output_dir=None, _preview=False):
    """生成边框图"""
    bmp_width = 200 if _preview else params["bmp_width"]
    bmp_height = 200 if _preview else params["bmp_height"]
    new_array = numpy.zeros((bmp_height, bmp_width, 3), dtype=numpy.uint8)
    new_array[:] = params["back_color"]
    new_array[0] = params["frame_color"]
    new_array[bmp_height - 1] = params["frame_color"]
    new_array[:, 0] = params["frame_color"]
    new_array[:, bmp_width - 1] = params["frame_color"]
    new_im = Image.fromarray(new_array)
    bmp_name = "border_%dRGB_%d.bmp" % (bmp_width, bmp_height)
    if _preview:
        return new_im
    new_im.save(os.path.join(output_dir, bmp_name))


def generate_color_bands(params, output_dir=None, _preview=False):
    """生成彩带图（8色）"""
    bmp_width = 200 if _preview else params["bmp_width"]
    bmp_height = 200 if _preview else params["bmp_height"]
    band_type = params.get("band_type", 0)
    colors = [
        [255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0],
        [255, 0, 255], [0, 255, 255], [255, 255, 255], [0, 0, 0]
    ]
    new_array = numpy.zeros((bmp_height, bmp_width, 3), dtype=numpy.uint8)

    if band_type == 1:
        per_line = bmp_height // 8
        left_line = bmp_height - per_line * 8
        for i in range(8):
            start = per_line * i
            stop = per_line * (i + 1) if i < 7 else per_line * 8 + left_line
            new_array[start:stop] = colors[i]
    else:
        per_line = bmp_width // 8
        left_line = bmp_width - per_line * 8
        for i in range(8):
            start = per_line * i
            stop = per_line * (i + 1) if i < 7 else per_line * 8 + left_line
            new_array[:, start:stop] = colors[i]

    new_im = Image.fromarray(new_array)
    bmp_name = "color_band_%dRGB_%d.bmp" % (bmp_width, bmp_height)
    if _preview:
        return new_im
    new_im.save(os.path.join(output_dir, bmp_name))


def generate_radial_spray(params, output_dir=None, _preview=False):
    """生成放射图"""
    bmp_width = 200 if _preview else params["bmp_width"]
    bmp_height = 200 if _preview else params["bmp_height"]
    angle = params["angle"]
    back_color = params["back_color"]
    line_color = params["line_color"]

    im = Image.new("RGB", (bmp_width, bmp_height))
    t = 1
    valid_angle = []
    per_angle = 360 // angle
    while t * per_angle < 90:
        valid_angle.append(t * per_angle)
        t += 1

    cx, cy = bmp_width // 2, bmp_height // 2
    for i in range(bmp_height):
        for j in range(bmp_width):
            if j == cx or i == cy:
                im.putpixel((j, i), (line_color[0], line_color[1], line_color[2]))
            for a in valid_angle:
                tan_val = math.tan(a * math.pi / 180)
                if tan_val == 0:
                    continue
                if abs(j - cx) == math.ceil(abs(i - cy) / tan_val):
                    im.putpixel((j, i), (line_color[0], line_color[1], line_color[2]))
                    break
                else:
                    im.putpixel((j, i), (back_color[0], back_color[1], back_color[2]))

    bmp_name = "spray_%dRGB_%d.bmp" % (bmp_width, bmp_height)
    if _preview:
        return im
    im.save(os.path.join(output_dir, bmp_name))


def generate_grayscale_bands(params, output_dir=None, _preview=False):
    """生成灰阶彩带图（多段灰阶过渡拼接）"""
    bmp_width = params["bmp_width"]
    bmp_height = params["bmp_height"]
    transition_type = params.get("type", 0)
    type_list = params.get("type_list", [])

    new_array = numpy.zeros((bmp_height, bmp_width, 3), dtype=numpy.uint8)

    if transition_type == 1:
        perline1 = bmp_height // max(len(type_list), 1)
        perline2 = bmp_height % max(len(type_list), 1)
    else:
        perline1 = bmp_width // max(len(type_list), 1)
        perline2 = bmp_width % max(len(type_list), 1)

    sub_band_start_line = 0
    for band_i in range(len(type_list)):
        lines_per_band = perline1 + perline2 if band_i == (len(type_list) - 1) else perline1
        item = type_list[band_i]
        parts = item.split("_")
        R_checked = parts[0][1] == "1"
        G_checked = parts[0][3] == "1"
        B_checked = parts[0][5] == "1"
        start_gray_val = int(parts[1])
        stop_gray_val = int(parts[2])
        sub_band_type = int(parts[3])
        gray_range = abs(stop_gray_val - start_gray_val)

        if transition_type == 1:
            # 横向分割
            if sub_band_type == 1:
                perline = lines_per_band // (gray_range + 1) if gray_range >= 0 else 1
                left_line = lines_per_band % (gray_range + 1) if gray_range >= 0 else 0
                left_times = 1
                line_used = 0
                for i in range(gray_range + 1):
                    R = 0 if not R_checked else (start_gray_val + (-i if start_gray_val > stop_gray_val else i))
                    G = 0 if not G_checked else (start_gray_val + (-i if start_gray_val > stop_gray_val else i))
                    B = 0 if not B_checked else (start_gray_val + (-i if start_gray_val > stop_gray_val else i))
                    line_num = perline + 1 if left_times < left_line else perline
                    if line_num == 0 and i < gray_range:
                        new_array[line_used + sub_band_start_line:] = [R, G, B]
                        break
                    if i == gray_range:
                        new_array[line_used + sub_band_start_line:] = [R, G, B]
                    else:
                        new_array[line_used + sub_band_start_line:line_used + line_num + sub_band_start_line] = [R, G, B]
                    line_used += line_num
                    left_times += 1
            else:
                perline = bmp_width // (gray_range + 1) if gray_range >= 0 else 1
                left_line = bmp_width % (gray_range + 1) if gray_range >= 0 else 0
                left_times = 1
                line_used = 0
                for i in range(gray_range + 1):
                    R = 0 if not R_checked else (start_gray_val + (-i if start_gray_val > stop_gray_val else i))
                    G = 0 if not G_checked else (start_gray_val + (-i if start_gray_val > stop_gray_val else i))
                    B = 0 if not B_checked else (start_gray_val + (-i if start_gray_val > stop_gray_val else i))
                    line_num = perline + 1 if left_times < left_line else perline
                    if line_num == 0 and i < gray_range:
                        new_array[lines_per_band * band_i:, line_used:] = [R, G, B]
                        break
                    if i == gray_range:
                        new_array[lines_per_band * band_i:, line_used:] = [R, G, B]
                    else:
                        new_array[lines_per_band * band_i:, line_used:line_used + line_num] = [R, G, B]
                    line_used += line_num
                    left_times += 1
        else:
            if sub_band_type == 1:
                perline = bmp_height // (gray_range + 1) if gray_range >= 0 else 1
                left_line = bmp_height % (gray_range + 1) if gray_range >= 0 else 0
                left_times = 1
                line_used = 0
                for i in range(gray_range + 1):
                    R = 0 if not R_checked else (start_gray_val + (-i if start_gray_val > stop_gray_val else i))
                    G = 0 if not G_checked else (start_gray_val + (-i if start_gray_val > stop_gray_val else i))
                    B = 0 if not B_checked else (start_gray_val + (-i if start_gray_val > stop_gray_val else i))
                    line_num = perline + 1 if left_times < left_line else perline
                    if line_num == 0 and i < gray_range:
                        new_array[line_used:, lines_per_band * band_i:] = [R, G, B]
                        break
                    if i == gray_range:
                        new_array[line_used:, lines_per_band * band_i:] = [R, G, B]
                    else:
                        new_array[line_used:line_used + line_num, lines_per_band * band_i:] = [R, G, B]
                    line_used += line_num
                    left_times += 1
            else:
                perline = lines_per_band // (gray_range + 1) if gray_range >= 0 else 1
                left_line = lines_per_band % (gray_range + 1) if gray_range >= 0 else 0
                left_times = 1
                line_used = 0
                for i in range(gray_range + 1):
                    R = 0 if not R_checked else (start_gray_val + (-i if start_gray_val > stop_gray_val else i))
                    G = 0 if not G_checked else (start_gray_val + (-i if start_gray_val > stop_gray_val else i))
                    B = 0 if not B_checked else (start_gray_val + (-i if start_gray_val > stop_gray_val else i))
                    line_num = perline + 1 if left_times < left_line else perline
                    if line_num == 0 and i < gray_range:
                        new_array[:, line_used + sub_band_start_line:] = [R, G, B]
                        break
                    if i == gray_range:
                        new_array[:, line_used + sub_band_start_line:] = [R, G, B]
                    else:
                        new_array[:, line_used + sub_band_start_line:line_used + line_num + sub_band_start_line] = [R, G, B]
                    line_used += line_num
                    left_times += 1
        sub_band_start_line += lines_per_band

    new_im = Image.fromarray(new_array)
    bmp_name = "gray_band_%dRGB_%d.bmp" % (bmp_width, bmp_height)
    if _preview:
        return new_im
    new_im.save(os.path.join(output_dir, bmp_name))


def generate_piano_keys(params, output_dir=None, _preview=False):
    """生成钢琴键图"""
    bmp_width = 200 if _preview else params["bmp_width"]
    bmp_height = 200 if _preview else params["bmp_height"]
    key_num = params["btn_num"]
    key_width = bmp_height // (key_num * 2) if key_num > 0 else 1
    new_array = numpy.zeros((bmp_height, bmp_width, 3), dtype=numpy.uint8)
    new_array[:] = params["back_color"]
    for i in range(key_num):
        start_row = key_width * i * 2
        end_row = key_width * i * 2 + key_width
        if end_row > bmp_height:
            end_row = bmp_height
        new_array[start_row:end_row, :bmp_width // 2] = params["btn_color"]
    new_im = Image.fromarray(new_array)
    bmp_name = "key_%dRGB_%d.bmp" % (bmp_width, bmp_height)
    if _preview:
        return new_im
    new_im.save(os.path.join(output_dir, bmp_name))


# 生成器映射表
GENERATOR_MAP = {
    "纯色": generate_solid_color,
    "灰阶过渡": generate_grayscale,
    "中间方形": generate_center_square,
    "棋盘格": generate_checkerboard,
    "条纹": generate_stripes,
    "边框图": generate_border_frame,
    "彩带": generate_color_bands,
    "放射": generate_radial_spray,
    "灰阶彩图": generate_grayscale_bands,
    "钢琴键": generate_piano_keys,
}


def get_generator(pattern_type):
    """根据图案类型获取对应的生成函数"""
    return GENERATOR_MAP.get(pattern_type)
