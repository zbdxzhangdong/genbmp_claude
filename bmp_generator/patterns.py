# -*- coding: utf-8 -*-
# 图案类型元数据定义 —— 配置加载和控件绑定的单一数据源

PATTERN_NAMES = [
    "纯色", "灰阶过渡", "中间方形", "棋盘格", "条纹",
    "边框图", "彩带", "放射", "灰阶彩图", "钢琴键", "其它"
]

# 每个图案类型在 UI 中对应的 Tab 索引 (0-based)
PATTERN_TAB_INDEX = {
    "纯色": 0, "灰阶过渡": 1, "中间方形": 2, "棋盘格": 3,
    "条纹": 4, "边框图": 5, "彩带": 6, "放射": 7,
    "灰阶彩图": 8, "钢琴键": 9, "其它": 10
}

# 参数类型常量
TYPE_INT = "int"
TYPE_COLOR = "color"       # [R, G, B]
TYPE_COLOR_LIST = "color_list"  # [[R,G,B], ...]

# 图案参数模式定义
# params: 参数名到类型的映射
# color_groups: 四滑块颜色组 (gray/R/G/B slider + text 绑定配置)
# single_sliders: 单值 slider + text 绑定配置
PATTERN_SCHEMAS = {
    "纯色": {
        "color_groups": [
            {"gray": "Type1_gray", "r": "Type1_r", "g": "Type1_g", "b": "Type1_b",
             "gray_val": "Type1_gray_val", "r_val": "Type1_r_val",
             "g_val": "Type1_g_val", "b_val": "Type1_b_val",
             "sync_gray": True},
        ],
        "single_sliders": [],
    },
    "灰阶过渡": {
        "color_groups": [],
        "single_sliders": [
            {"slider": "Type2_start_gray", "text": "Type2_start_gray_val"},
            {"slider": "Type2_stop_gray", "text": "Type2_stop_gray_val"},
        ],
    },
    "中间方形": {
        "color_groups": [
            {"gray": "Type3_back_gray", "r": "Type3_back_r", "g": "Type3_back_g", "b": "Type3_back_b",
             "gray_val": "Type3_back_gray_val", "r_val": "Type3_back_r_val",
             "g_val": "Type3_back_g_val", "b_val": "Type3_back_b_val",
             "sync_gray": True},
            {"gray": "Type3_sub_gray", "r": "Type3_sub_r", "g": "Type3_sub_g", "b": "Type3_sub_b",
             "gray_val": "Type3_sub_gray_val", "r_val": "Type3_sub_r_val",
             "g_val": "Type3_sub_g_val", "b_val": "Type3_sub_b_val",
             "sync_gray": True},
        ],
        "single_sliders": [],
    },
    "棋盘格": {
        "color_groups": [
            {"gray": "Type4_type1_gray", "r": "Type4_type1_r", "g": "Type4_type1_g", "b": "Type4_type1_b",
             "gray_val": "Type4_type1_gray_val", "r_val": "Type4_type1_r_val",
             "g_val": "Type4_type1_g_val", "b_val": "Type4_type1_b_val",
             "sync_gray": True},
            {"gray": "Type4_type2_gray", "r": "Type4_type2_r", "g": "Type4_type2_g", "b": "Type4_type2_b",
             "gray_val": "Type4_type2_gray_val", "r_val": "Type4_type2_r_val",
             "g_val": "Type4_type2_g_val", "b_val": "Type4_type2_b_val",
             "sync_gray": True},
        ],
        "single_sliders": [],
    },
    "条纹": {
        "color_groups": [
            {"gray": "Type5_type1_gray", "r": "Type5_type1_r", "g": "Type5_type1_g", "b": "Type5_type1_b",
             "gray_val": "Type5_type1_gray_val", "r_val": "Type5_type1_r_val",
             "g_val": "Type5_type1_g_val", "b_val": "Type5_type1_b_val",
             "sync_gray": True},
            {"gray": "Type5_type2_gray", "r": "Type5_type2_r", "g": "Type5_type2_g", "b": "Type5_type2_b",
             "gray_val": "Type5_type2_gray_val", "r_val": "Type5_type2_r_val",
             "g_val": "Type5_type2_g_val", "b_val": "Type5_type2_b_val",
             "sync_gray": True},
        ],
        "single_sliders": [],
    },
    "边框图": {
        "color_groups": [
            {"gray": "Type6_back_gray", "r": "Type6_back_r", "g": "Type6_back_g", "b": "Type6_back_b",
             "gray_val": "Type6_back_gray_val", "r_val": "Type6_back_r_val",
             "g_val": "Type6_back_g_val", "b_val": "Type6_back_b_val",
             "sync_gray": True},
            {"gray": "Type6_frame_gray", "r": "Type6_frame_r", "g": "Type6_frame_g", "b": "Type6_frame_b",
             "gray_val": "Type6_frame_gray_val", "r_val": "Type6_frame_r_val",
             "g_val": "Type6_frame_g_val", "b_val": "Type6_frame_b_val",
             "sync_gray": True},
        ],
        "single_sliders": [],
    },
    "彩带": {
        "color_groups": [],
        "single_sliders": [],
    },
    "放射": {
        "color_groups": [
            {"gray": "Type8_back_gray", "r": "Type8_back_r", "g": "Type8_back_g", "b": "Type8_back_b",
             "gray_val": "Type8_back_gray_val", "r_val": "Type8_back_r_val",
             "g_val": "Type8_back_g_val", "b_val": "Type8_back_b_val",
             "sync_gray": True},
            {"gray": "Type8_line_gray", "r": "Type8_line_r", "g": "Type8_line_g", "b": "Type8_line_b",
             "gray_val": "Type8_line_gray_val", "r_val": "Type8_line_r_val",
             "g_val": "Type8_line_g_val", "b_val": "Type8_line_b_val",
             "sync_gray": True},
        ],
        "single_sliders": [],
    },
    "灰阶彩图": {
        "color_groups": [],
        "single_sliders": [
            {"slider": "Type9_start_gray", "text": "Type9_start_gray_val"},
            {"slider": "Type9_stop_gray", "text": "Type9_stop_gray_val"},
        ],
    },
    "钢琴键": {
        "color_groups": [
            {"gray": "Type10_back_gray", "r": "Type10_back_r", "g": "Type10_back_g", "b": "Type10_back_b",
             "gray_val": "Type10_back_gray_val", "r_val": "Type10_back_r_val",
             "g_val": "Type10_back_g_val", "b_val": "Type10_back_b_val",
             "sync_gray": True},
            {"gray": "Type10_btn_gray", "r": "Type10_btn_r", "g": "Type10_btn_g", "b": "Type10_btn_b",
             "gray_val": "Type10_btn_gray_val", "r_val": "Type10_btn_r_val",
             "g_val": "Type10_btn_g_val", "b_val": "Type10_btn_b_val",
             "sync_gray": True},
        ],
        "single_sliders": [],
    },
    "其它": {
        "color_groups": [],
        "single_sliders": [],
    },
}

# 默认参数
DEFAULT_PARAMS = {
    "纯色": {"gen_en": 0, "gray_value": [255, 0, 0], "bmp_width": 1080, "bmp_height": 2340},
    "灰阶过渡": {"gen_en": 0, "transition_type": 0, "max_gray": [0, 255, 0], "min_gray": [0, 0, 0], "bmp_width": 1080, "bmp_height": 2340},
    "中间方形": {"gen_en": 0, "back_color": [200, 200, 200], "center_color": [100, 100, 100], "center_start_row": 1, "center_start_col": 1, "center_width": 20, "center_height": 30, "bmp_width": 1080, "bmp_height": 2340},
    "棋盘格": {"gen_en": 0, "sub_type1_color": [255, 255, 255], "sub_type2_color": [0, 0, 0], "sub_size": 8, "bmp_width": 1080, "bmp_height": 2340},
    "条纹": {"gen_en": 0, "type": 0, "sub_band1_color": [255, 255, 255], "sub_band1_size": 10, "sub_band2_color": [0, 0, 0], "sub_band2_size": 5, "bmp_width": 1080, "bmp_height": 2340},
    "边框图": {"gen_en": 0, "back_color": [0, 0, 0], "frame_color": [255, 255, 255], "bmp_width": 1080, "bmp_height": 2340},
    "彩带": {"gen_en": 0, "band_type": 0, "bmp_width": 1080, "bmp_height": 2340},
    "放射": {"gen_en": 0, "back_color": [0, 0, 0], "angle": 6, "line_color": [0, 0, 0], "bmp_width": 1080, "bmp_height": 2340},
    "灰阶彩图": {"gen_en": 0, "type": 0, "type_list": [], "bmp_width": 1080, "bmp_height": 2340},
    "钢琴键": {"gen_en": 0, "back_color": [0, 0, 0], "btn_num": 6, "btn_color": [0, 0, 0], "bmp_width": 1080, "bmp_height": 2340},
    "其它": {"gen_en": 0},
}

INI_FIELD_MAP = {
    "纯色": {"gen_en": "gen_en", "bmp_width": "bmp_width", "bmp_height": "bmp_height"},
    "灰阶过渡": {"gen_en": "gen_en", "transition_type": "transition_type", "bmp_width": "bmp_width", "bmp_height": "bmp_height"},
    "中间方形": {"gen_en": "gen_en", "bmp_width": "bmp_width", "bmp_height": "bmp_height"},
    "棋盘格": {"gen_en": "gen_en", "sub_size": "sub_size", "bmp_width": "bmp_width", "bmp_height": "bmp_height"},
    "条纹": {"gen_en": "gen_en", "type": "type", "sub_band1_size": "sub_band1_size", "sub_band2_size": "sub_band2_size", "bmp_width": "bmp_width", "bmp_height": "bmp_height"},
    "边框图": {"gen_en": "gen_en", "bmp_width": "bmp_width", "bmp_height": "bmp_height"},
    "彩带": {"gen_en": "gen_en", "band_type": "band_type", "bmp_width": "bmp_width", "bmp_height": "bmp_height"},
    "放射": {"gen_en": "gen_en", "angle": "angle", "bmp_width": "bmp_width", "bmp_height": "bmp_height"},
}

INI_COLOR_FIELDS = {
    "纯色": [("gray_value", "gray_value")],
    "灰阶过渡": [("max_gray", "max_gray"), ("min_gray", "min_gray")],
    "中间方形": [("back_color", "back_color"), ("center_color", "center_color")],
    "棋盘格": [("sub_type1_color", "sub_type1_color"), ("sub_type2_color", "sub_type2_color")],
    "条纹": [("sub_band1_color", "sub_band1_color"), ("sub_band2_color", "sub_band2_color")],
    "边框图": [("back_color", "back_color"), ("frame_color", "frame_color")],
    "放射": [("back_color", "back_color"), ("line_color", "line_color")],
    "彩带": [],
    "灰阶彩图": [],
    "钢琴键": [],
    "其它": [],
}
