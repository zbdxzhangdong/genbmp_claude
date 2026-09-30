# -*- coding: utf-8 -*-
# CLI BMP 生成器

import os
from bmp_generator import load_ini, get_generator


class gen_bmp():
    def __init__(self):
        self.para_input = {}
        self.output_dir = os.path.join(os.getcwd(), "bmp_out")

    def load_ini(self):
        ini_path = os.path.join(os.getcwd(), "config", "cfg.ini")
        self.para_input = load_ini(ini_path)

    def ensure_output_dir(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def gen_data(self):
        self.ensure_output_dir()
        name_map = {
            "纯色": "纯色图(color)",
            "灰阶过渡": "灰阶过渡(gray)",
            "中间方形": "中间方形(square)",
            "棋盘格": "棋盘格(dot)",
            "条纹": "条纹(stripe)",
            "边框图": "边框图(frame)",
            "彩带": "彩带(color_band)",
            "放射": "放射(spray)",
        }
        for pattern_type, params in self.para_input.items():
            if not params.get("gen_en"):
                continue
            display_name = name_map.get(pattern_type, pattern_type)
            print("正在生成%s……" % display_name)
            generator = get_generator(pattern_type)
            if generator:
                generator(params, self.output_dir)
                print("%s已生成!" % display_name)


if __name__ == '__main__':
    try:
        print("ChipWealth_VESA_v0.0_20220811")
        model = gen_bmp()
        model.load_ini()
        model.gen_data()
        print("按回车继续！")
        input()
    except Exception as e:
        print(e)
        print("按回车继续！")
        input()
