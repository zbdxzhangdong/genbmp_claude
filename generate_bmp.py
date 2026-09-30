# -*- coding: utf-8 -*-
# GUI BMP 生成器 (PyQt5)

import sys
import os
from PIL import Image
import numpy

from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QFileDialog, QAction, QActionGroup, QDialog)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QIntValidator

from gen_bmp_ui import Ui_MainWindow
from bmp_generator import load_ini, load_from_widgets, get_generator
from bmp_generator.core import generate_solid_color_batch


LANGUAGES = {
    "zh_CN": {
        "生成bmp": "生成bmp",
        "预览": "预览",
        "语言": "语言",
        "生成图片宽度:": "生成图片宽度:",
        "生成图片高度:": "生成图片高度:",
        "灰阶值:": "灰阶值:",
        "红分量:": "红分量:",
        "绿分量:": "绿分量:",
        "蓝分量:": "蓝分量:",
        "批量设置": "批量设置",
        "批量转？": "批量转？",
        "起始值": "起始值",
        "终止值": "终止值",
        "R:": "R:", "G:": "G:", "B:": "B:",
        "纯色图": "纯色图",
        "过渡类型:": "过渡类型:",
        "横向过渡": "横向过渡",
        "纵向过渡": "纵向过渡",
        "需要过渡的分量:": "需要过渡的分量:",
        "红": "红", "绿": "绿", "蓝": "蓝",
        "起始灰阶值:": "起始灰阶值:",
        "终止灰阶值:": "终止灰阶值:",
        "灰阶过渡图": "灰阶过渡图",
        "方形起始行:": "方形起始行:",
        "方形起始列:": "方形起始列:",
        "方形宽:": "方形宽:",
        "方形高:": "方形高:",
        "背景色设置": "背景色设置",
        "背景红分量:": "背景红分量:",
        "背景绿分量:": "背景绿分量:",
        "背景蓝分量:": "背景蓝分量:",
        "中间方形颜色设置": "中间方形颜色设置",
        "方形红分量:": "方形红分量:",
        "方形绿分量:": "方形绿分量:",
        "方形蓝分量:": "方形蓝分量:",
        "中间方形图": "中间方形图",
        "格子大小(默认宽度等于高度):": "格子大小(默认宽度等于高度):",
        "格子1颜色设置": "格子1颜色设置",
        "格子1红分量:": "格子1红分量:",
        "格子1绿分量:": "格子1绿分量:",
        "格子1蓝分量:": "格子1蓝分量:",
        "格子2颜色设置": "格子2颜色设置",
        "格子2红分量:": "格子2红分量:",
        "格子2绿分量:": "格子2绿分量:",
        "格子2蓝分量:": "格子2蓝分量:",
        "棋盘格图": "棋盘格图",
        "条纹类型:": "条纹类型:",
        "纵向条纹": "纵向条纹",
        "横向条纹": "横向条纹",
        "条纹1宽度:": "条纹1宽度:",
        "条纹2宽度:": "条纹2宽度:",
        "条纹1颜色设置": "条纹1颜色设置",
        "条纹1红分量:": "条纹1红分量:",
        "条纹1绿分量:": "条纹1绿分量:",
        "条纹1蓝分量:": "条纹1蓝分量:",
        "条纹2颜色设置": "条纹2颜色设置",
        "条纹2红分量:": "条纹2红分量:",
        "条纹2绿分量:": "条纹2绿分量:",
        "条纹2蓝分量:": "条纹2蓝分量:",
        "条纹状图": "条纹状图",
        "背景颜色": "背景颜色",
        "边框颜色": "边框颜色",
        "边框红分量:": "边框红分量:",
        "边框绿分量:": "边框绿分量:",
        "边框蓝分量:": "边框蓝分量:",
        "边框图": "边框图",
        "彩带类型:": "彩带类型:",
        "纵向彩带": "纵向彩带",
        "横向彩带": "横向彩带",
        "彩带图": "彩带图",
        "分角个数:": "分角个数:",
        "射线颜色": "射线颜色",
        "放射线红分量:": "放射线红分量:",
        "放射线绿分量:": "放射线绿分量:",
        "放射线蓝分量:": "放射线蓝分量:",
        "放射图": "放射图",
        "分割类型:": "分割类型:",
        "纵向分割": "纵向分割",
        "横向分割": "横向分割",
        "过渡条分量值设置:": "过渡条分量值设置:",
        "纵向过渡": "纵向过渡",
        "横向过渡": "横向过渡",
        "过渡色条配置": "过渡色条配置",
        "增加到列表 ->": "增加到列表 ->",
        "已有的过渡类型设置:": "已有的过渡类型设置:",
        "删除当前项 ->": "删除当前项 ->",
        "灰阶彩带图": "灰阶彩带图",
        "钢琴键个数:": "钢琴键个数:",
        "钢琴键颜色": "钢琴键颜色",
        "钢琴键红分量:": "钢琴键红分量:",
        "钢琴键绿分量:": "钢琴键绿分量:",
        "钢琴键蓝分量:": "钢琴键蓝分量:",
        "钢琴键图": "钢琴键图",
        "bmp转txt": "bmp转txt",
        "Browser": "Browser",
        "SPI332": "SPI332",
        "RGB888": "RGB888",
        "SPI111_3bit_type1": "SPI111_3bit_type1",
        "SPI111_3bit_type2": "SPI111_3bit_type2",
        "SPI111_4bit": "SPI111_4bit",
        "Gray256_F1": "Gray256_F1",
        "Gray256_F2": "Gray256_F2",
        "其它": "其它",
        "生成使能开关": "生成使能开关",
        "纯色使能": "纯色使能",
        "灰阶过渡使能": "灰阶过渡使能",
        "中间方形使能": "中间方形使能",
        "棋盘格使能": "棋盘格使能",
        "条纹状使能": "条纹状使能",
        "边框使能": "边框使能",
        "彩带使能": "彩带使能",
        "放射使能": "放射使能",
        "灰阶彩图使能": "灰阶彩图使能",
        "琴键图使能": "琴键图使能",
    },
    "zh_TW": {
        "生成bmp": "生成BMP",
        "预览": "預覽",
        "语言": "語言",
        "生成图片宽度:": "生成圖片寬度:",
        "生成图片高度:": "生成圖片高度:",
        "灰阶值:": "灰階值:",
        "红分量:": "紅分量:",
        "绿分量:": "綠分量:",
        "蓝分量:": "藍分量:",
        "批量设置": "批量設置",
        "批量转？": "批量轉？",
        "起始值": "起始值",
        "终止值": "終止值",
        "R:": "R:", "G:": "G:", "B:": "B:",
        "纯色图": "純色圖",
        "过渡类型:": "過渡類型:",
        "横向过渡": "橫向過渡",
        "纵向过渡": "縱向過渡",
        "需要过渡的分量:": "需要過渡的分量:",
        "红": "紅", "绿": "綠", "蓝": "藍",
        "起始灰阶值:": "起始灰階值:",
        "终止灰阶值:": "終止灰階值:",
        "灰阶过渡图": "灰階過渡圖",
        "方形起始行:": "方形起始行:",
        "方形起始列:": "方形起始列:",
        "方形宽:": "方形寬:",
        "方形高:": "方形高:",
        "背景色设置": "背景色設置",
        "背景红分量:": "背景紅分量:",
        "背景绿分量:": "背景綠分量:",
        "背景蓝分量:": "背景藍分量:",
        "中间方形颜色设置": "中間方形顏色設置",
        "方形红分量:": "方形紅分量:",
        "方形绿分量:": "方形綠分量:",
        "方形蓝分量:": "方形藍分量:",
        "中间方形图": "中間方形圖",
        "格子大小(默认宽度等于高度):": "格子大小(默認寬度等於高度):",
        "格子1颜色设置": "格子1顏色設置",
        "格子1红分量:": "格子1紅分量:",
        "格子1绿分量:": "格子1綠分量:",
        "格子1蓝分量:": "格子1藍分量:",
        "格子2颜色设置": "格子2顏色設置",
        "格子2红分量:": "格子2紅分量:",
        "格子2绿分量:": "格子2綠分量:",
        "格子2蓝分量:": "格子2藍分量:",
        "棋盘格图": "棋盤格圖",
        "条纹类型:": "條紋類型:",
        "纵向条纹": "縱向條紋",
        "横向条纹": "橫向條紋",
        "条纹1宽度:": "條紋1寬度:",
        "条纹2宽度:": "條紋2寬度:",
        "条纹1颜色设置": "條紋1顏色設置",
        "条纹1红分量:": "條紋1紅分量:",
        "条纹1绿分量:": "條紋1綠分量:",
        "条纹1蓝分量:": "條紋1藍分量:",
        "条纹2颜色设置": "條紋2顏色設置",
        "条纹2红分量:": "條紋2紅分量:",
        "条纹2绿分量:": "條紋2綠分量:",
        "条纹2蓝分量:": "條紋2藍分量:",
        "条纹状图": "條紋狀圖",
        "背景颜色": "背景顏色",
        "边框颜色": "邊框顏色",
        "边框红分量:": "邊框紅分量:",
        "边框绿分量:": "邊框綠分量:",
        "边框蓝分量:": "邊框藍分量:",
        "边框图": "邊框圖",
        "彩带类型:": "彩帶類型:",
        "纵向彩带": "縱向彩帶",
        "横向彩带": "橫向彩帶",
        "彩带图": "彩帶圖",
        "分角个数:": "分角個數:",
        "射线颜色": "射線顏色",
        "放射线红分量:": "放射線紅分量:",
        "放射线绿分量:": "放射線綠分量:",
        "放射线蓝分量:": "放射線藍分量:",
        "放射图": "放射圖",
        "分割类型:": "分割類型:",
        "纵向分割": "縱向分割",
        "横向分割": "橫向分割",
        "过渡条分量值设置:": "過渡條分量值設置:",
        "纵向过渡": "縱向過渡",
        "横向过渡": "橫向過渡",
        "过渡色条配置": "過渡色條配置",
        "增加到列表 ->": "增加到列表 ->",
        "已有的过渡类型设置:": "已有的過渡類型設置:",
        "删除当前项 ->": "刪除當前項 ->",
        "灰阶彩带图": "灰階彩帶圖",
        "钢琴键个数:": "鋼琴鍵個數:",
        "钢琴键颜色": "鋼琴鍵顏色",
        "钢琴键红分量:": "鋼琴鍵紅分量:",
        "钢琴键绿分量:": "鋼琴鍵綠分量:",
        "钢琴键蓝分量:": "鋼琴鍵藍分量:",
        "钢琴键图": "鋼琴鍵圖",
        "bmp转txt": "BMP轉TXT",
        "Browser": "Browser",
        "SPI332": "SPI332",
        "RGB888": "RGB888",
        "SPI111_3bit_type1": "SPI111_3bit_type1",
        "SPI111_3bit_type2": "SPI111_3bit_type2",
        "SPI111_4bit": "SPI111_4bit",
        "Gray256_F1": "Gray256_F1",
        "Gray256_F2": "Gray256_F2",
        "其它": "其它",
        "生成使能开关": "生成使能開關",
        "纯色使能": "純色使能",
        "灰阶过渡使能": "灰階過渡使能",
        "中间方形使能": "中間方形使能",
        "棋盘格使能": "棋盤格使能",
        "条纹状使能": "條紋狀使能",
        "边框使能": "邊框使能",
        "彩带使能": "彩帶使能",
        "放射使能": "放射使能",
        "灰阶彩图使能": "灰階彩圖使能",
        "琴键图使能": "琴鍵圖使能",
    },
    "en": {
        "生成bmp": "Generate BMP",
        "预览": "Preview",
        "语言": "Language",
        "生成图片宽度:": "Image Width:",
        "生成图片高度:": "Image Height:",
        "灰阶值:": "Gray Value:",
        "红分量:": "Red:",
        "绿分量:": "Green:",
        "蓝分量:": "Blue:",
        "批量设置": "Batch Settings",
        "批量转？": "Batch Convert?",
        "起始值": "Start",
        "终止值": "End",
        "R:": "R:", "G:": "G:", "B:": "B:",
        "纯色图": "Solid Color",
        "过渡类型:": "Transition:",
        "横向过渡": "Horizontal",
        "纵向过渡": "Vertical",
        "需要过渡的分量:": "Gradient Channels:",
        "红": "R", "绿": "G", "蓝": "B",
        "起始灰阶值:": "Start Gray:",
        "终止灰阶值:": "End Gray:",
        "灰阶过渡图": "Grayscale Gradient",
        "方形起始行:": "Start Row:",
        "方形起始列:": "Start Col:",
        "方形宽:": "Width:",
        "方形高:": "Height:",
        "背景色设置": "Background",
        "背景红分量:": "Bg Red:",
        "背景绿分量:": "Bg Green:",
        "背景蓝分量:": "Bg Blue:",
        "中间方形颜色设置": "Square Color",
        "方形红分量:": "Square Red:",
        "方形绿分量:": "Square Green:",
        "方形蓝分量:": "Square Blue:",
        "中间方形图": "Center Square",
        "格子大小(默认宽度等于高度):": "Cell Size:",
        "格子1颜色设置": "Cell 1 Color",
        "格子1红分量:": "Cell 1 Red:",
        "格子1绿分量:": "Cell 1 Green:",
        "格子1蓝分量:": "Cell 1 Blue:",
        "格子2颜色设置": "Cell 2 Color",
        "格子2红分量:": "Cell 2 Red:",
        "格子2绿分量:": "Cell 2 Green:",
        "格子2蓝分量:": "Cell 2 Blue:",
        "棋盘格图": "Checkerboard",
        "条纹类型:": "Stripe Type:",
        "纵向条纹": "Vertical",
        "横向条纹": "Horizontal",
        "条纹1宽度:": "Stripe 1 Width:",
        "条纹2宽度:": "Stripe 2 Width:",
        "条纹1颜色设置": "Stripe 1 Color",
        "条纹1红分量:": "Stripe 1 Red:",
        "条纹1绿分量:": "Stripe 1 Green:",
        "条纹1蓝分量:": "Stripe 1 Blue:",
        "条纹2颜色设置": "Stripe 2 Color",
        "条纹2红分量:": "Stripe 2 Red:",
        "条纹2绿分量:": "Stripe 2 Green:",
        "条纹2蓝分量:": "Stripe 2 Blue:",
        "条纹状图": "Stripes",
        "背景颜色": "Background",
        "边框颜色": "Frame Color",
        "边框红分量:": "Frame Red:",
        "边框绿分量:": "Frame Green:",
        "边框蓝分量:": "Frame Blue:",
        "边框图": "Border Frame",
        "彩带类型:": "Band Type:",
        "纵向彩带": "Vertical",
        "横向彩带": "Horizontal",
        "彩带图": "Color Bands",
        "分角个数:": "Angles:",
        "射线颜色": "Line Color",
        "放射线红分量:": "Line Red:",
        "放射线绿分量:": "Line Green:",
        "放射线蓝分量:": "Line Blue:",
        "放射图": "Radial Spray",
        "分割类型:": "Split:",
        "纵向分割": "Vertical",
        "横向分割": "Horizontal",
        "过渡条分量值设置:": "Band Channels:",
        "纵向过渡": "Vertical",
        "横向过渡": "Horizontal",
        "过渡色条配置": "Band Config",
        "增加到列表 ->": "Add ->",
        "已有的过渡类型设置:": "Bands:",
        "删除当前项 ->": "Delete ->",
        "灰阶彩带图": "Grayscale Bands",
        "钢琴键个数:": "Keys:",
        "钢琴键颜色": "Key Color",
        "钢琴键红分量:": "Key Red:",
        "钢琴键绿分量:": "Key Green:",
        "钢琴键蓝分量:": "Key Blue:",
        "钢琴键图": "Piano Keys",
        "bmp转txt": "BMP to Text",
        "Browser": "Browse",
        "SPI332": "SPI332",
        "RGB888": "RGB888",
        "SPI111_3bit_type1": "SPI111_3bit_type1",
        "SPI111_3bit_type2": "SPI111_3bit_type2",
        "SPI111_4bit": "SPI111_4bit",
        "Gray256_F1": "Gray256_F1",
        "Gray256_F2": "Gray256_F2",
        "其它": "Other",
        "生成使能开关": "Enable Switches",
        "纯色使能": "Solid Color",
        "灰阶过渡使能": "Grayscale Gradient",
        "中间方形使能": "Center Square",
        "棋盘格使能": "Checkerboard",
        "条纹状使能": "Stripes",
        "边框使能": "Border Frame",
        "彩带使能": "Color Bands",
        "放射使能": "Radial Spray",
        "灰阶彩图使能": "Grayscale Bands",
        "琴键图使能": "Piano Keys",
    },
}


def _bmp2txt_internal(dirpath, s1, s2, s3, s4, s5, s6, s7, output_dir, status_callback=None):
    """BMP 转文本（独立函数，在工作线程中调用）"""
    filelistall = os.listdir(dirpath)
    filelist = [f for f in filelistall if f.endswith('.bmp')]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for item in filelist:
        if s1:
            file_path = os.path.join(output_dir, item.lower()).replace('.bmp', '_spi332.txt')
            with open(file_path, 'w') as f:
                img = Image.open(os.path.join(dirpath, item))
                data = numpy.array(img)
                for r in range(len(data)):
                    for c in range(len(data[0])):
                        rgb = data[r][c]
                        val = int('{0:08b}'.format(rgb[0])[0:3] +
                                  '{0:08b}'.format(rgb[1])[0:3] +
                                  '{0:08b}'.format(rgb[2])[0:2], 2)
                        f.write('%02x\n' % val)

        if s2 or s7:
            img = Image.open(os.path.join(dirpath, item))
            data = numpy.array(img)
            h, w = len(data), len(data[0])

            if s2:
                f1_path = os.path.join(output_dir, item.lower()).replace('.bmp', '_rgb888.txt')
                f2_path = os.path.join(output_dir, item.lower()).replace('.bmp', '_rgb8_8_8.txt')
                with open(f1_path, 'w') as f1, open(f2_path, 'w') as f2:
                    for r in range(h):
                        for c in range(w):
                            rgb = data[r][c]
                            f1.write('%02x%02x%02x\n' % (rgb[0], rgb[1], rgb[2]))
                            f2.write('%02x\n%02x\n%02x\n' % (rgb[0], rgb[1], rgb[2]))

            if s7:
                f_path = os.path.join(output_dir, item.lower()).replace(
                    '.bmp', '_gray256f2_%d.txt' % (h * w))
                with open(f_path, 'w') as f:
                    for r in range(h):
                        for c in range(w):
                            f.write('%02x\n' % (data[r][c][1]))

        if s3 or s4 or s5 or s6:
            img = Image.open(os.path.join(dirpath, item))
            data = numpy.array(img)
            h, w = len(data), len(data[0])

            f3 = f4 = f5 = f6 = None
            if s3:
                f3 = open(os.path.join(output_dir, item.lower()).replace(
                    '.bmp', '_spi111_3bit_type1_%d.txt' % (h * w // 2)), 'w')
            if s4:
                f4 = open(os.path.join(output_dir, item.lower()).replace(
                    '.bmp', '_spi111_3bit_type2_%d.txt' % (h * w // 2)), 'w')
            if s5:
                f5 = open(os.path.join(output_dir, item.lower()).replace(
                    '.bmp', '_spi111_4bit_%d.txt' % (h * w // 2)), 'w')
            if s6:
                f6 = open(os.path.join(output_dir, item.lower()).replace(
                    '.bmp', '_gray256f1_%d.txt' % (h * w // 2)), 'w')

            for r in range(h):
                if status_callback:
                    status_callback("generating = %d/%d" % (r + 1, h))
                for c in range(w // 2):
                    if f3:
                        v = (data[r][c*2][0]>>7)*32 + (data[r][c*2][1]>>7)*16 + (data[r][c*2][2]>>7)*8 + \
                            (data[r][c*2+1][0]>>7)*4 + (data[r][c*2+1][1]>>7)*2 + (data[r][c*2+1][2]>>7)*1
                        f3.write("%02x\n" % v)
                    if f4:
                        v = (data[r][c*2][0]>>7)*64 + (data[r][c*2][1]>>7)*32 + (data[r][c*2][2]>>7)*16 + \
                            (data[r][c*2+1][0]>>7)*4 + (data[r][c*2+1][1]>>7)*2 + (data[r][c*2+1][2]>>7)*1
                        f4.write("%02x\n" % v)
                    if f5:
                        v = (data[r][c*2][0]>>6)*64 + (data[r][c*2][1]>>7)*32 + (data[r][c*2][2]>>7)*16 + \
                            (data[r][c*2+1][0]>>6)*4 + (data[r][c*2+1][1]>>7)*2 + (data[r][c*2+1][2]>>7)*1
                        f5.write("%02x\n" % v)
                    if f6:
                        bit5 = 32 if data[r][c*2][0] >= 0x80 else 0
                        bit4 = 16 if data[r][c*2][1] >= 0x80 else 0
                        bit3 = 8 if data[r][c*2][2] >= 0x80 else 0
                        bit2 = 4 if data[r][c*2+1][0] >= 0x80 else 0
                        bit1 = 2 if data[r][c*2+1][1] >= 0x80 else 0
                        bit0 = 1 if data[r][c*2+1][2] >= 0x80 else 0
                        f6.write("%02x\n" % (bit5+bit4+bit3+bit2+bit1+bit0))
            for f in [f3, f4, f5, f6]:
                if f:
                    f.close()


class my_main_UI(QMainWindow):
    def __init__(self):
        super(my_main_UI, self).__init__()
        self.win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.win)
        self.win.show()
        self._current_lang = "zh_CN"
        self._translations = LANGUAGES["zh_CN"]
        self.init_ui()
        self._setup_language_switcher()

    # ------------------------------------------------------------------ #
    # 滑块绑定工厂方法
    # ------------------------------------------------------------------ #

    def _bind_color_group(self, widget_map, sync_gray=True):
        """为四滑块颜色组（gray/R/G/B）自动创建 slider <-> text 连接"""
        gs = widget_map["gray_slider"]
        gt = widget_map["gray_text"]
        rs = widget_map["r_slider"]
        rt = widget_map["r_text"]
        g_s = widget_map["g_slider"]
        g_t = widget_map["g_text"]
        bs = widget_map["b_slider"]
        bt = widget_map["b_text"]

        if sync_gray:
            def on_gray_slider(val):
                gt.setText(str(val))
                rt.setText(str(val))
                g_t.setText(str(val))
                bt.setText(str(val))

            def on_gray_text(text):
                try:
                    v = int(text, 10) if text else 0
                    gs.setValue(v)
                    rs.setValue(v)
                    g_s.setValue(v)
                    bs.setValue(v)
                except Exception:
                    gs.setValue(0)
                    rs.setValue(0)
                    g_s.setValue(0)
                    bs.setValue(0)
            gs.valueChanged.connect(on_gray_slider)
            gt.textChanged.connect(on_gray_text)

        def make_on_slider_changed(text_widget):
            def handler(val):
                text_widget.setText(str(val))
            return handler

        def make_on_text_changed(slider_widget):
            def handler(text):
                try:
                    slider_widget.setValue(int(text, 10) if text else 0)
                except Exception:
                    slider_widget.setValue(0)
            return handler

        rs.valueChanged.connect(make_on_slider_changed(rt))
        g_s.valueChanged.connect(make_on_slider_changed(g_t))
        bs.valueChanged.connect(make_on_slider_changed(bt))
        rt.textChanged.connect(make_on_text_changed(rs))
        g_t.textChanged.connect(make_on_text_changed(g_s))
        bt.textChanged.connect(make_on_text_changed(bs))

    def _bind_single_slider(self, slider, text_widget):
        """为单值 slider + text 创建连接"""
        slider.valueChanged.connect(lambda val: text_widget.setText(str(val)))
        text_widget.textChanged.connect(
            lambda text: slider.setValue(int(text, 10) if text else 0))

    # ------------------------------------------------------------------ #
    # 语言切换
    # ------------------------------------------------------------------ #

    def _setup_language_switcher(self):
        menubar = self.win.menuBar()
        self._lang_menu = menubar.addMenu(self.tr("语言"))
        self._lang_group = QActionGroup(self)
        self._lang_group.setExclusive(True)
        for code, label in [("zh_CN", u"简体中文"), ("zh_TW", u"繁體中文"), ("en", "English")]:
            action = QAction(label, self, checkable=True)
            self._lang_group.addAction(action)
            self._lang_menu.addAction(action)
            action.triggered.connect(lambda checked, c=code: self._change_language(c))
            if code == "zh_CN":
                action.setChecked(True)

    def _change_language(self, code):
        if code == self._current_lang:
            return
        self._current_lang = code
        self._translations = LANGUAGES[code]
        self._apply_language()

    def tr(self, source):
        """翻译字符串，找不到时返回原文"""
        return self._translations.get(source, source)

    def _apply_language(self):
        """重新设置所有 UI 控件的文本"""
        tr = self.tr
        self._lang_menu.setTitle(tr("语言"))
        self.ui.Generate.setText(tr("生成bmp"))
        if hasattr(self, '_preview_btn'):
            self._preview_btn.setText(tr("预览"))
        self.ui.label_2.setText(tr("生成图片宽度:"))
        self.ui.label_3.setText(tr("生成图片高度:"))
        self.ui.label_4.setText(tr("灰阶值:"))
        self.ui.label_5.setText(tr("红分量:"))
        self.ui.label_6.setText(tr("绿分量:"))
        self.ui.label_7.setText(tr("蓝分量:"))
        self.ui.groupBox_20.setTitle(tr("批量设置"))
        self.ui.Type1_some_en.setText(tr("批量转？"))
        self.ui.groupBox_18.setTitle(tr("起始值"))
        self.ui.label_40.setText(tr("R:"))
        self.ui.label_41.setText(tr("G:"))
        self.ui.label_42.setText(tr("B:"))
        self.ui.groupBox_19.setTitle(tr("终止值"))
        self.ui.label_43.setText(tr("R:"))
        self.ui.label_44.setText(tr("G:"))
        self.ui.label_45.setText(tr("B:"))
        self.ui.Tab_all.setTabText(0, tr("纯色图"))
        self.ui.label_10.setText(tr("生成图片宽度:"))
        self.ui.label_9.setText(tr("生成图片高度:"))
        self.ui.label.setText(tr("过渡类型:"))
        self.ui.Type2_sub_type.setItemText(0, tr("横向过渡"))
        self.ui.Type2_sub_type.setItemText(1, tr("纵向过渡"))
        self.ui.groupBox.setTitle(tr("需要过渡的分量:"))
        self.ui.Type2_r.setText(tr("红"))
        self.ui.Type2_g.setText(tr("绿"))
        self.ui.Type2_b.setText(tr("蓝"))
        self.ui.label_8.setText(tr("起始灰阶值:"))
        self.ui.label_23.setText(tr("终止灰阶值:"))
        self.ui.Tab_all.setTabText(1, tr("灰阶过渡图"))
        self.ui.label_26.setText(tr("生成图片宽度:"))
        self.ui.label_24.setText(tr("生成图片高度:"))
        self.ui.label_32.setText(tr("方形起始行:"))
        self.ui.label_33.setText(tr("方形起始列:"))
        self.ui.label_35.setText(tr("方形宽:"))
        self.ui.label_34.setText(tr("方形高:"))
        self.ui.groupBox_3.setTitle(tr("背景色设置"))
        self.ui.label_12.setText(tr("灰阶值:"))
        self.ui.label_25.setText(tr("背景红分量:"))
        self.ui.label_27.setText(tr("背景绿分量:"))
        self.ui.label_28.setText(tr("背景蓝分量:"))
        self.ui.groupBox_4.setTitle(tr("中间方形颜色设置"))
        self.ui.label_11.setText(tr("灰阶值:"))
        self.ui.label_31.setText(tr("方形红分量:"))
        self.ui.label_30.setText(tr("方形绿分量:"))
        self.ui.label_29.setText(tr("方形蓝分量:"))
        self.ui.Tab_all.setTabText(2, tr("中间方形图"))
        self.ui.label_67.setText(tr("格子大小(默认宽度等于高度):"))
        self.ui.groupBox_5.setTitle(tr("格子1颜色设置"))
        self.ui.label_14.setText(tr("灰阶值:"))
        self.ui.label_65.setText(tr("格子1红分量:"))
        self.ui.label_62.setText(tr("格子1绿分量:"))
        self.ui.label_61.setText(tr("格子1蓝分量:"))
        self.ui.groupBox_6.setTitle(tr("格子2颜色设置"))
        self.ui.label_13.setText(tr("灰阶值:"))
        self.ui.label_59.setText(tr("格子2红分量:"))
        self.ui.label_63.setText(tr("格子2绿分量:"))
        self.ui.label_66.setText(tr("格子2蓝分量:"))
        self.ui.Tab_all.setTabText(3, tr("棋盘格图"))
        self.ui.label_98.setText(tr("条纹类型:"))
        self.ui.Type5_sub_type.setItemText(0, tr("纵向条纹"))
        self.ui.Type5_sub_type.setItemText(1, tr("横向条纹"))
        self.ui.label_73.setText(tr("条纹1宽度:"))
        self.ui.label_77.setText(tr("条纹2宽度:"))
        self.ui.groupBox_7.setTitle(tr("条纹1颜色设置"))
        self.ui.label_16.setText(tr("灰阶值:"))
        self.ui.label_75.setText(tr("条纹1红分量:"))
        self.ui.label_69.setText(tr("条纹1绿分量:"))
        self.ui.label_70.setText(tr("条纹1蓝分量:"))
        self.ui.groupBox_8.setTitle(tr("条纹2颜色设置"))
        self.ui.label_15.setText(tr("灰阶值:"))
        self.ui.label_74.setText(tr("条纹2红分量:"))
        self.ui.label_76.setText(tr("条纹2绿分量:"))
        self.ui.label_71.setText(tr("条纹2蓝分量:"))
        self.ui.Tab_all.setTabText(4, tr("条纹状图"))
        self.ui.label_85.setText(tr("生成图片宽度:"))
        self.ui.label_78.setText(tr("生成图片高度:"))
        self.ui.groupBox_9.setTitle(tr("背景颜色"))
        self.ui.label_18.setText(tr("灰阶值:"))
        self.ui.label_84.setText(tr("背景红分量:"))
        self.ui.label_83.setText(tr("背景绿分量:"))
        self.ui.label_81.setText(tr("背景蓝分量:"))
        self.ui.groupBox_10.setTitle(tr("边框颜色"))
        self.ui.label_17.setText(tr("灰阶值:"))
        self.ui.label_79.setText(tr("边框红分量:"))
        self.ui.label_82.setText(tr("边框绿分量:"))
        self.ui.label_80.setText(tr("边框蓝分量:"))
        self.ui.Tab_all.setTabText(5, tr("边框图"))
        self.ui.label_88.setText(tr("彩带类型:"))
        self.ui.Type7_sub_type.setItemText(0, tr("纵向彩带"))
        self.ui.Type7_sub_type.setItemText(1, tr("横向彩带"))
        self.ui.Tab_all.setTabText(6, tr("彩带图"))
        self.ui.label_91.setText(tr("分角个数:"))
        self.ui.groupBox_11.setTitle(tr("背景颜色"))
        self.ui.label_20.setText(tr("灰阶值:"))
        self.ui.label_96.setText(tr("背景红分量:"))
        self.ui.label_95.setText(tr("背景绿分量:"))
        self.ui.label_93.setText(tr("背景蓝分量:"))
        self.ui.groupBox_12.setTitle(tr("射线颜色"))
        self.ui.label_19.setText(tr("灰阶值:"))
        self.ui.label_90.setText(tr("放射线红分量:"))
        self.ui.label_94.setText(tr("放射线绿分量:"))
        self.ui.label_92.setText(tr("放射线蓝分量:"))
        self.ui.Tab_all.setTabText(7, tr("放射图"))
        self.ui.label_21.setText(tr("分割类型:"))
        self.ui.Type9_sub_type.setItemText(0, tr("纵向分割"))
        self.ui.Type9_sub_type.setItemText(1, tr("横向分割"))
        self.ui.groupBox_2.setTitle(tr("过渡条分量值设置:"))
        self.ui.Type9_r.setText(tr("红"))
        self.ui.Type9_g.setText(tr("绿"))
        self.ui.Type9_b.setText(tr("蓝"))
        self.ui.Type9_sub_band_type1.setText(tr("纵向过渡"))
        self.ui.Type9_sub_band_type2.setText(tr("横向过渡"))
        self.ui.label_22.setText(tr("起始灰阶值:"))
        self.ui.label_36.setText(tr("终止灰阶值:"))
        self.ui.groupBox_13.setTitle(tr("过渡色条配置"))
        self.ui.Type9_add_btn.setText(tr("增加到列表 ->"))
        self.ui.label_37.setText(tr("已有的过渡类型设置:"))
        self.ui.Type9_del_btn.setText(tr("删除当前项 ->"))
        self.ui.Tab_all.setTabText(8, tr("灰阶彩带图"))
        self.ui.label_103.setText(tr("钢琴键个数:"))
        self.ui.groupBox_14.setTitle(tr("背景颜色"))
        self.ui.label_38.setText(tr("灰阶值:"))
        self.ui.label_105.setText(tr("背景红分量:"))
        self.ui.label_106.setText(tr("背景绿分量:"))
        self.ui.label_104.setText(tr("背景蓝分量:"))
        self.ui.groupBox_15.setTitle(tr("钢琴键颜色"))
        self.ui.label_39.setText(tr("灰阶值:"))
        self.ui.label_109.setText(tr("钢琴键红分量:"))
        self.ui.label_108.setText(tr("钢琴键绿分量:"))
        self.ui.label_107.setText(tr("钢琴键蓝分量:"))
        self.ui.Tab_all.setTabText(9, tr("钢琴键图"))
        self.ui.groupBox_17.setTitle(tr("bmp转txt"))
        self.ui.Type11_browser_btn.setText(tr("Browser"))
        self.ui.Type11_subtype1.setText(tr("SPI332"))
        self.ui.Type11_subtype2.setText(tr("RGB888"))
        self.ui.Type11_subtype3.setText(tr("SPI111_3bit_type1"))
        self.ui.Type11_subtype4.setText(tr("SPI111_3bit_type2"))
        self.ui.Type11_subtype5.setText(tr("SPI111_4bit"))
        self.ui.Type11_subtype6.setText(tr("Gray256_F1"))
        self.ui.Type11_subtype7.setText(tr("Gray256_F2"))
        self.ui.Tab_all.setTabText(10, tr("其它"))
        self.ui.groupBox_16.setTitle(tr("生成使能开关"))
        self.ui.Type1_en.setText(tr("纯色使能"))
        self.ui.Type2_en.setText(tr("灰阶过渡使能"))
        self.ui.Type3_en.setText(tr("中间方形使能"))
        self.ui.Type4_en.setText(tr("棋盘格使能"))
        self.ui.Type5_en.setText(tr("条纹状使能"))
        self.ui.Type6_en.setText(tr("边框使能"))
        self.ui.Type7_en.setText(tr("彩带使能"))
        self.ui.Type8_en.setText(tr("放射使能"))
        self.ui.Type9_en.setText(tr("灰阶彩图使能"))
        self.ui.Type10_en.setText(tr("琴键图使能"))
        self.ui.Type11_en.setText(tr("其它"))
        self.ui.label_64.setText(tr("生成图片宽度:"))
        self.ui.label_60.setText(tr("生成图片高度:"))
        self._update_title()

    # ------------------------------------------------------------------ #
    # 动态标题
    # ------------------------------------------------------------------ #

    def _update_title(self):
        tab_idx = self.ui.Tab_all.currentIndex()
        tab_text = self.ui.Tab_all.tabText(tab_idx)
        title = "%s - %s [%s]" % (self.tr("生成bmp"), tab_text, self._current_lang)
        self.win.setWindowTitle(title)

    # ------------------------------------------------------------------ #
    # UI 初始化
    # ------------------------------------------------------------------ #

    def init_ui(self):
        self.para_input = {
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

        self.ui.Generate.clicked.connect(self.gen_bmp_start)
        self.ui.Type9_add_btn.clicked.connect(self.Type9_add_item)
        self.ui.Type9_del_btn.clicked.connect(self.Type9_del_item)

        # 在 Generate 按钮旁添加"预览"按钮
        from PyQt5.QtWidgets import QPushButton
        from bmp_generator.preview_dialog import PreviewDialog
        grid = self.ui.centralwidget.layout()
        h_layout = grid.itemAtPosition(7, 0).layout()
        self._preview_btn = QPushButton(self.tr("预览"), self.ui.centralwidget)
        h_layout.addWidget(self._preview_btn)
        self._preview_btn.clicked.connect(self._show_preview)

        # 使能复选框 -> Tab 切换
        enable_tabs = [
            (self.ui.Type1_en, 0), (self.ui.Type2_en, 1), (self.ui.Type3_en, 2),
            (self.ui.Type4_en, 3), (self.ui.Type5_en, 4), (self.ui.Type6_en, 5),
            (self.ui.Type7_en, 6), (self.ui.Type8_en, 7), (self.ui.Type9_en, 8),
            (self.ui.Type10_en, 9), (self.ui.Type11_en, 10),
        ]
        for cb, idx in enable_tabs:
            cb.clicked.connect(lambda checked, i=idx: self.ui.Tab_all.setCurrentIndex(i))

        # 输入校验器
        res_validator = QIntValidator(0, 255, self)
        w_validator = QIntValidator(0, 2000, self)
        h_validator = QIntValidator(0, 3000, self)

        # 绑定颜色组滑块
        self._bind_color_group({
            "gray_slider": self.ui.Type1_gray, "gray_text": self.ui.Type1_gray_val,
            "r_slider": self.ui.Type1_r, "r_text": self.ui.Type1_r_val,
            "g_slider": self.ui.Type1_g, "g_text": self.ui.Type1_g_val,
            "b_slider": self.ui.Type1_b, "b_text": self.ui.Type1_b_val,
        }, sync_gray=True)
        self._bind_color_group({
            "gray_slider": self.ui.Type3_back_gray, "gray_text": self.ui.Type3_back_gray_val,
            "r_slider": self.ui.Type3_back_r, "r_text": self.ui.Type3_back_r_val,
            "g_slider": self.ui.Type3_back_g, "g_text": self.ui.Type3_back_g_val,
            "b_slider": self.ui.Type3_back_b, "b_text": self.ui.Type3_back_b_val,
        }, sync_gray=True)
        self._bind_color_group({
            "gray_slider": self.ui.Type3_sub_gray, "gray_text": self.ui.Type3_sub_gray_val,
            "r_slider": self.ui.Type3_sub_r, "r_text": self.ui.Type3_sub_r_val,
            "g_slider": self.ui.Type3_sub_g, "g_text": self.ui.Type3_sub_g_val,
            "b_slider": self.ui.Type3_sub_b, "b_text": self.ui.Type3_sub_b_val,
        }, sync_gray=True)
        self._bind_color_group({
            "gray_slider": self.ui.Type4_type1_gray, "gray_text": self.ui.Type4_type1_gray_val,
            "r_slider": self.ui.Type4_type1_r, "r_text": self.ui.Type4_type1_r_val,
            "g_slider": self.ui.Type4_type1_g, "g_text": self.ui.Type4_type1_g_val,
            "b_slider": self.ui.Type4_type1_b, "b_text": self.ui.Type4_type1_b_val,
        }, sync_gray=True)
        self._bind_color_group({
            "gray_slider": self.ui.Type4_type2_gray, "gray_text": self.ui.Type4_type2_gray_val,
            "r_slider": self.ui.Type4_type2_r, "r_text": self.ui.Type4_type2_r_val,
            "g_slider": self.ui.Type4_type2_g, "g_text": self.ui.Type4_type2_g_val,
            "b_slider": self.ui.Type4_type2_b, "b_text": self.ui.Type4_type2_b_val,
        }, sync_gray=True)
        self._bind_color_group({
            "gray_slider": self.ui.Type5_type1_gray, "gray_text": self.ui.Type5_type1_gray_val,
            "r_slider": self.ui.Type5_type1_r, "r_text": self.ui.Type5_type1_r_val,
            "g_slider": self.ui.Type5_type1_g, "g_text": self.ui.Type5_type1_g_val,
            "b_slider": self.ui.Type5_type1_b, "b_text": self.ui.Type5_type1_b_val,
        }, sync_gray=True)
        self._bind_color_group({
            "gray_slider": self.ui.Type5_type2_gray, "gray_text": self.ui.Type5_type2_gray_val,
            "r_slider": self.ui.Type5_type2_r, "r_text": self.ui.Type5_type2_r_val,
            "g_slider": self.ui.Type5_type2_g, "g_text": self.ui.Type5_type2_g_val,
            "b_slider": self.ui.Type5_type2_b, "b_text": self.ui.Type5_type2_b_val,
        }, sync_gray=True)
        self._bind_color_group({
            "gray_slider": self.ui.Type6_back_gray, "gray_text": self.ui.Type6_back_gray_val,
            "r_slider": self.ui.Type6_back_r, "r_text": self.ui.Type6_back_r_val,
            "g_slider": self.ui.Type6_back_g, "g_text": self.ui.Type6_back_g_val,
            "b_slider": self.ui.Type6_back_b, "b_text": self.ui.Type6_back_b_val,
        }, sync_gray=True)
        self._bind_color_group({
            "gray_slider": self.ui.Type6_frame_gray, "gray_text": self.ui.Type6_frame_gray_val,
            "r_slider": self.ui.Type6_frame_r, "r_text": self.ui.Type6_frame_r_val,
            "g_slider": self.ui.Type6_frame_g, "g_text": self.ui.Type6_frame_g_val,
            "b_slider": self.ui.Type6_frame_b, "b_text": self.ui.Type6_frame_b_val,
        }, sync_gray=True)
        self._bind_color_group({
            "gray_slider": self.ui.Type8_back_gray, "gray_text": self.ui.Type8_back_gray_val,
            "r_slider": self.ui.Type8_back_r, "r_text": self.ui.Type8_back_r_val,
            "g_slider": self.ui.Type8_back_g, "g_text": self.ui.Type8_back_g_val,
            "b_slider": self.ui.Type8_back_b, "b_text": self.ui.Type8_back_b_val,
        }, sync_gray=True)
        self._bind_color_group({
            "gray_slider": self.ui.Type8_line_gray, "gray_text": self.ui.Type8_line_gray_val,
            "r_slider": self.ui.Type8_line_r, "r_text": self.ui.Type8_line_r_val,
            "g_slider": self.ui.Type8_line_g, "g_text": self.ui.Type8_line_g_val,
            "b_slider": self.ui.Type8_line_b, "b_text": self.ui.Type8_line_b_val,
        }, sync_gray=True)
        self._bind_color_group({
            "gray_slider": self.ui.Type10_back_gray, "gray_text": self.ui.Type10_back_gray_val,
            "r_slider": self.ui.Type10_back_r, "r_text": self.ui.Type10_back_r_val,
            "g_slider": self.ui.Type10_back_g, "g_text": self.ui.Type10_back_g_val,
            "b_slider": self.ui.Type10_back_b, "b_text": self.ui.Type10_back_b_val,
        }, sync_gray=True)
        self._bind_color_group({
            "gray_slider": self.ui.Type10_btn_gray, "gray_text": self.ui.Type10_btn_gray_val,
            "r_slider": self.ui.Type10_btn_r, "r_text": self.ui.Type10_btn_r_val,
            "g_slider": self.ui.Type10_btn_g, "g_text": self.ui.Type10_btn_g_val,
            "b_slider": self.ui.Type10_btn_b, "b_text": self.ui.Type10_btn_b_val,
        }, sync_gray=True)

        # 绑定单值滑块
        self._bind_single_slider(self.ui.Type2_start_gray, self.ui.Type2_start_gray_val)
        self._bind_single_slider(self.ui.Type2_stop_gray, self.ui.Type2_stop_gray_val)
        self._bind_single_slider(self.ui.Type9_start_gray, self.ui.Type9_start_gray_val)
        self._bind_single_slider(self.ui.Type9_stop_gray, self.ui.Type9_stop_gray_val)

        # 设置校验器
        for w in [self.ui.Type1_width, self.ui.Type2_width, self.ui.Type3_width,
                  self.ui.Type4_width, self.ui.Type5_width, self.ui.Type6_width,
                  self.ui.Type7_width, self.ui.Type8_width, self.ui.Type9_width,
                  self.ui.Type10_width]:
            w.setValidator(w_validator)
        for h in [self.ui.Type1_height, self.ui.Type2_height, self.ui.Type3_height,
                  self.ui.Type4_height, self.ui.Type5_height, self.ui.Type6_height,
                  self.ui.Type7_height, self.ui.Type8_height, self.ui.Type9_height,
                  self.ui.Type10_height]:
            h.setValidator(h_validator)

        self.ui.Type11_browser_btn.clicked.connect(self.open_bmp_dir)

        # 动态标题
        self.ui.Tab_all.currentChanged.connect(self._update_title)
        self._update_title()

    # ------------------------------------------------------------------ #
    # Tab 9 灰阶彩带 辅助操作
    # ------------------------------------------------------------------ #

    def Type9_add_item(self):
        R_en = "R1" if self.ui.Type9_r.isChecked() else "R0"
        G_en = "G1" if self.ui.Type9_g.isChecked() else "G0"
        B_en = "B1" if self.ui.Type9_b.isChecked() else "B0"
        start_val = self.ui.Type9_start_gray_val.text()
        stop_val = self.ui.Type9_stop_gray_val.text()
        sub_type = "_1" if self.ui.Type9_sub_band_type1.isChecked() else "_0"
        self.ui.Type9_sub_list.insertItem(
            self.ui.Type9_sub_list.currentIndex(),
            R_en + G_en + B_en + "_" + start_val + "_" + stop_val + sub_type)
        self.ui.Type9_sub_list.setCurrentIndex(0)

    def Type9_del_item(self):
        self.ui.Type9_sub_list.removeItem(self.ui.Type9_sub_list.currentIndex())

    # ------------------------------------------------------------------ #
    # Tab 11 其它
    # ------------------------------------------------------------------ #

    def open_bmp_dir(self):
        try:
            name = QFileDialog.getExistingDirectory(self, 'load bmp file', '')
            self.ui.Type11_dir.setText(name)
        except Exception as e:
            print('save_file_open---exception:%e' % e)

    # ------------------------------------------------------------------ #
    # 预览
    # ------------------------------------------------------------------ #

    _preview_name_map = {
        u"纯色": u"纯色", u"灰阶过渡": u"灰阶过渡", u"中间方形": u"中间方形",
        u"棋盘格": u"棋盘格", u"条纹": u"条纹", u"边框图": u"边框图",
        u"彩带": u"彩带", u"放射": u"放射",
        u"灰阶彩图": u"灰阶彩图", u"钢琴键": u"钢琴键",
    }

    def _show_preview(self):
        from bmp_generator.preview_dialog import PreviewDialog
        load_from_widgets(self.ui, self.para_input)
        jobs = []
        for name, params in self.para_input.items():
            if not params.get("gen_en"):
                continue
            if name == u"灰阶过渡":
                jobs.append((name, params.copy(), {
                    "r_checked": self.ui.Type2_r.isChecked(),
                    "g_checked": self.ui.Type2_g.isChecked(),
                    "b_checked": self.ui.Type2_b.isChecked(),
                }))
            else:
                jobs.append((name, params.copy(), {}))
        if not jobs:
            self._on_status(u"没有启用的图案")
            return
        dlg = PreviewDialog(jobs, self._preview_name_map, self.win)
        if dlg.exec_() == QDialog.Accepted:
            self.gen_bmp_start()
        dlg.deleteLater()

    # ------------------------------------------------------------------ #
    # 生成流程
    # ------------------------------------------------------------------ #

    def gen_bmp_start(self):
        self.ui.progressBar.setRange(0, 100)
        load_from_widgets(self.ui, self.para_input)
        output_dir = os.path.join(os.getcwd(), "bmp_out")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 构建作业列表，在 UI 线程捕获所有控件状态
        jobs = []
        for name, params in self.para_input.items():
            if not params.get("gen_en"):
                continue
            if name == "纯色" and self.ui.Type1_some_en.isChecked():
                jobs.append((name, params.copy(), {
                    "batch_mode": True,
                    "start_r": int(self.ui.Type1_start_r.text()),
                    "start_g": int(self.ui.Type1_start_g.text()),
                    "start_b": int(self.ui.Type1_start_b.text()),
                    "stop_r": int(self.ui.Type1_end_r.text()),
                    "stop_g": int(self.ui.Type1_end_g.text()),
                    "stop_b": int(self.ui.Type1_end_b.text()),
                }))
            elif name == "灰阶过渡":
                jobs.append((name, params.copy(), {
                    "r_checked": self.ui.Type2_r.isChecked(),
                    "g_checked": self.ui.Type2_g.isChecked(),
                    "b_checked": self.ui.Type2_b.isChecked(),
                }))
            elif name == "其它":
                jobs.append((name, params.copy(), {
                    "dir": self.ui.Type11_dir.text(),
                    "s1": self.ui.Type11_subtype1.isChecked(),
                    "s2": self.ui.Type11_subtype2.isChecked(),
                    "s3": self.ui.Type11_subtype3.isChecked(),
                    "s4": self.ui.Type11_subtype4.isChecked(),
                    "s5": self.ui.Type11_subtype5.isChecked(),
                    "s6": self.ui.Type11_subtype6.isChecked(),
                    "s7": self.ui.Type11_subtype7.isChecked(),
                }))
            else:
                jobs.append((name, params.copy(), {}))

        self._worker = GenWorker(jobs, output_dir, self)
        self._worker.progress_signal.connect(self._on_progress)
        self._worker.status_signal.connect(self._on_status)
        self._worker.finished_signal.connect(self._on_generation_finished)
        self._worker.start()
        self._on_status("Start_generate_bmp")

    def _on_progress(self, current, total):
        self.ui.progressBar.setValue((current/total)*100)
        self.win.setWindowTitle("%s - %d/%d [%s]" % (
            self.tr("生成bmp"), current, total, self._current_lang))

    def _on_status(self, msg):
        self.ui.statusbar.showMessage(msg)

    def _on_generation_finished(self):
        self._update_title()
        self._on_status("Generate Finished!")
        self._worker = None


class GenWorker(QThread):
    progress_signal = pyqtSignal(int, int)   # (current, total)
    status_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, jobs, output_dir, parent=None):
        super(GenWorker, self).__init__(parent)
        self._jobs = jobs
        self._output_dir = output_dir
        self._stopped = False

    def stop(self):
        self._stopped = True

    def run(self):
        total = len(self._jobs)
        for idx, (name, params, extras) in enumerate(self._jobs):
            if self._stopped:
                break
            self.status_signal.emit(u"正在生成 %s..." % name)
            try:
                if name == u"纯色" and extras.get("batch_mode"):
                    generate_solid_color_batch(
                        params, self._output_dir,
                        extras["start_r"], extras["start_g"], extras["start_b"],
                        extras["stop_r"], extras["stop_g"], extras["stop_b"])
                elif name == u"灰阶过渡":
                    gen_fn = get_generator(name)
                    if gen_fn:
                        gen_fn(params, self._output_dir,
                               r_checked=extras.get("r_checked", True),
                               g_checked=extras.get("g_checked", True),
                               b_checked=extras.get("b_checked", True))
                elif name == u"其它":
                    _bmp2txt_internal(
                        extras["dir"], extras["s1"], extras["s2"],
                        extras["s3"], extras["s4"], extras["s5"],
                        extras["s6"], extras["s7"],
                        self._output_dir, self.status_signal.emit)
                else:
                    gen_fn = get_generator(name)
                    if gen_fn:
                        gen_fn(params, self._output_dir)
            except Exception as e:
                print(e)
            self.progress_signal.emit(idx + 1, total)
        self.status_signal.emit("Generate Finished!")
        self.finished_signal.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    loader = my_main_UI()
    sys.exit(app.exec_())
