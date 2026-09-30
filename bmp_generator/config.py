# -*- coding: utf-8 -*-
# 统一配置加载（INI + UI widget → dict）

import os
import configparser
from bmp_generator.patterns import DEFAULT_PARAMS, INI_FIELD_MAP, INI_COLOR_FIELDS


def load_ini(filepath):
    """从 INI 文件加载参数到 dict"""
    p_cfg = configparser.ConfigParser()
    p_cfg.read(filepath, encoding='UTF-8')
    para_input = {}
    for section in DEFAULT_PARAMS:
        para_input[section] = dict(DEFAULT_PARAMS[section])
        if section not in p_cfg:
            continue
        # 读取普通字段
        if section in INI_FIELD_MAP:
            for key, ini_key in INI_FIELD_MAP[section].items():
                try:
                    raw = p_cfg.get(section, ini_key).split("//")[0].strip()
                    para_input[section][key] = int(raw)
                except Exception:
                    pass
        # 读取颜色字段
        if section in INI_COLOR_FIELDS:
            for ini_key, dict_key in INI_COLOR_FIELDS[section]:
                try:
                    raw = p_cfg.get(section, ini_key).split("//")[0].strip()
                    if ";" in raw:
                        # 多颜色列表 [[R,G,B], ...]
                        para_input[section][dict_key] = [
                            [int(x) for x in part.split(",")]
                            for part in raw.split(";")
                        ]
                    else:
                        para_input[section][dict_key] = [int(x) for x in raw.split(",")]
                except Exception:
                    pass
    return para_input


def load_from_widgets(ui, para_input):
    """从 UI widgets 读取参数到 dict"""
    # 纯色
    para_input["纯色"]["gen_en"] = 1 if ui.Type1_en.isChecked() else 0
    para_input["纯色"]["gray_value"] = [
        int(ui.Type1_r_val.text()), int(ui.Type1_g_val.text()), int(ui.Type1_b_val.text())]
    para_input["纯色"]["bmp_width"] = int(ui.Type1_width.text())
    para_input["纯色"]["bmp_height"] = int(ui.Type1_height.text())
    # 灰阶过渡
    R_max = int(ui.Type2_start_gray_val.text()) if ui.Type2_r.isChecked() else 0
    G_max = int(ui.Type2_start_gray_val.text()) if ui.Type2_g.isChecked() else 0
    B_max = int(ui.Type2_start_gray_val.text()) if ui.Type2_b.isChecked() else 0
    R_min = int(ui.Type2_stop_gray_val.text()) if ui.Type2_r.isChecked() else 0
    G_min = int(ui.Type2_stop_gray_val.text()) if ui.Type2_g.isChecked() else 0
    B_min = int(ui.Type2_stop_gray_val.text()) if ui.Type2_b.isChecked() else 0
    para_input["灰阶过渡"]["gen_en"] = 1 if ui.Type2_en.isChecked() else 0
    para_input["灰阶过渡"]["transition_type"] = 1 if ui.Type2_sub_type.currentIndex() == 1 else 0
    para_input["灰阶过渡"]["max_gray"] = [R_max, G_max, B_max]
    para_input["灰阶过渡"]["min_gray"] = [R_min, G_min, B_min]
    para_input["灰阶过渡"]["bmp_width"] = int(ui.Type2_width.text())
    para_input["灰阶过渡"]["bmp_height"] = int(ui.Type2_height.text())
    # 中间方形
    para_input["中间方形"]["gen_en"] = 1 if ui.Type3_en.isChecked() else 0
    para_input["中间方形"]["back_color"] = [
        int(ui.Type3_back_r_val.text()), int(ui.Type3_back_g_val.text()), int(ui.Type3_back_b_val.text())]
    para_input["中间方形"]["center_color"] = [
        int(ui.Type3_sub_r_val.text()), int(ui.Type3_sub_g_val.text()), int(ui.Type3_sub_b_val.text())]
    para_input["中间方形"]["center_start_row"] = int(ui.Type3_start_r.text())
    para_input["中间方形"]["center_start_col"] = int(ui.Type3_start_c.text())
    para_input["中间方形"]["center_width"] = int(ui.Type3_sub_width.text())
    para_input["中间方形"]["center_height"] = int(ui.Type3_sub_height.text())
    para_input["中间方形"]["bmp_width"] = int(ui.Type3_width.text())
    para_input["中间方形"]["bmp_height"] = int(ui.Type3_height.text())
    # 棋盘格
    para_input["棋盘格"]["gen_en"] = 1 if ui.Type4_en.isChecked() else 0
    para_input["棋盘格"]["sub_type1_color"] = [
        int(ui.Type4_type1_r_val.text()), int(ui.Type4_type1_g_val.text()), int(ui.Type4_type1_b_val.text())]
    para_input["棋盘格"]["sub_type2_color"] = [
        int(ui.Type4_type2_r_val.text()), int(ui.Type4_type2_g_val.text()), int(ui.Type4_type2_b_val.text())]
    para_input["棋盘格"]["sub_size"] = int(ui.Type4_sub_size.text())
    para_input["棋盘格"]["bmp_width"] = int(ui.Type4_width.text())
    para_input["棋盘格"]["bmp_height"] = int(ui.Type4_height.text())
    # 条纹
    para_input["条纹"]["gen_en"] = 1 if ui.Type5_en.isChecked() else 0
    para_input["条纹"]["type"] = 1 if ui.Type5_sub_type.currentIndex() == 1 else 0
    para_input["条纹"]["sub_band1_color"] = [
        int(ui.Type5_type1_r_val.text()), int(ui.Type5_type1_g_val.text()), int(ui.Type5_type1_b_val.text())]
    para_input["条纹"]["sub_band1_size"] = int(ui.Type5_type1_width.text())
    para_input["条纹"]["sub_band2_color"] = [
        int(ui.Type5_type2_r_val.text()), int(ui.Type5_type2_g_val.text()), int(ui.Type5_type2_b_val.text())]
    para_input["条纹"]["sub_band2_size"] = int(ui.Type5_type2_width.text())
    para_input["条纹"]["bmp_width"] = int(ui.Type5_width.text())
    para_input["条纹"]["bmp_height"] = int(ui.Type5_height.text())
    # 边框图
    para_input["边框图"]["gen_en"] = 1 if ui.Type6_en.isChecked() else 0
    para_input["边框图"]["back_color"] = [
        int(ui.Type6_back_r_val.text()), int(ui.Type6_back_g_val.text()), int(ui.Type6_back_b_val.text())]
    para_input["边框图"]["frame_color"] = [
        int(ui.Type6_frame_r_val.text()), int(ui.Type6_frame_g_val.text()), int(ui.Type6_frame_b_val.text())]
    para_input["边框图"]["bmp_width"] = int(ui.Type6_width.text())
    para_input["边框图"]["bmp_height"] = int(ui.Type6_height.text())
    # 彩带
    para_input["彩带"]["gen_en"] = 1 if ui.Type7_en.isChecked() else 0
    para_input["彩带"]["band_type"] = 1 if ui.Type7_sub_type.currentIndex() == 1 else 0
    para_input["彩带"]["bmp_width"] = int(ui.Type7_width.text())
    para_input["彩带"]["bmp_height"] = int(ui.Type7_height.text())
    # 放射
    para_input["放射"]["gen_en"] = 1 if ui.Type8_en.isChecked() else 0
    para_input["放射"]["angle"] = int(ui.Type8_angle_num.text())
    para_input["放射"]["back_color"] = [
        int(ui.Type8_back_r_val.text()), int(ui.Type8_back_g_val.text()), int(ui.Type8_back_b_val.text())]
    para_input["放射"]["line_color"] = [
        int(ui.Type8_line_r_val.text()), int(ui.Type8_line_g_val.text()), int(ui.Type8_line_b_val.text())]
    para_input["放射"]["bmp_width"] = int(ui.Type8_width.text())
    para_input["放射"]["bmp_height"] = int(ui.Type8_height.text())
    # 灰阶彩图
    para_input["灰阶彩图"]["gen_en"] = 1 if ui.Type9_en.isChecked() else 0
    para_input["灰阶彩图"]["type"] = 1 if ui.Type9_sub_type.currentIndex() == 1 else 0
    list_tup = []
    for num in range(ui.Type9_sub_list.count() - 1, -1, -1):
        list_tup.append(ui.Type9_sub_list.itemText(num))
    para_input["灰阶彩图"]["type_list"] = list_tup
    para_input["灰阶彩图"]["bmp_width"] = int(ui.Type9_width.text())
    para_input["灰阶彩图"]["bmp_height"] = int(ui.Type9_height.text())
    # 钢琴键
    para_input["钢琴键"]["gen_en"] = 1 if ui.Type10_en.isChecked() else 0
    para_input["钢琴键"]["back_color"] = [
        int(ui.Type10_back_r_val.text()), int(ui.Type10_back_g_val.text()), int(ui.Type10_back_b_val.text())]
    para_input["钢琴键"]["btn_color"] = [
        int(ui.Type10_btn_r_val.text()), int(ui.Type10_btn_g_val.text()), int(ui.Type10_btn_b_val.text())]
    para_input["钢琴键"]["btn_num"] = int(ui.Type10_btn_num.text())
    para_input["钢琴键"]["bmp_width"] = int(ui.Type10_width.text())
    para_input["钢琴键"]["bmp_height"] = int(ui.Type10_height.text())
    # 其它
    para_input["其它"]["gen_en"] = 1 if ui.Type11_en.isChecked() else 0
