#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import random
import argparse

import cv2 as cv
import numpy as np
from tqdm import tqdm

from create_7segment_image import create_7segment_image


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--width", help='image width', type=int, default=96)
    parser.add_argument("--height", help='image height', type=int, default=96)

    parser.add_argument("--number_width_min", type=float, default=0.1)
    parser.add_argument("--number_width_max", type=float, default=0.9)
    parser.add_argument("--number_height_min", type=float, default=0.4)
    parser.add_argument("--number_height_max", type=float, default=0.9)
    parser.add_argument("--thickness_min", type=float, default=0.01)
    parser.add_argument("--thickness_max", type=float, default=0.25)
    parser.add_argument("--blank_ratio_min", type=float, default=0.0)
    parser.add_argument("--blank_ratio_max", type=float, default=0.1)
    parser.add_argument("--shear_x_min", type=int, default=-10)
    parser.add_argument("--shear_x_max", type=int, default=30)
    parser.add_argument("--shift_x_min", type=int, default=-10)
    parser.add_argument("--shift_x_max", type=int, default=10)
    parser.add_argument("--shift_y_min", type=int, default=-10)
    parser.add_argument("--shift_y_max", type=int, default=10)

    parser.add_argument("--steps", help='create steps', type=int, default=3000)
    parser.add_argument('--erase_debug_window', action='store_true')
    parser.add_argument("--seed", help='random seed', type=int, default=42)

    parser.add_argument("--start_count", type=int, default=0)

    args = parser.parse_args()

    return args


def main():
    # 引数解析 #################################################################
    args = get_args()

    image_width = args.width
    image_height = args.height

    number_width_min = args.number_width_min
    number_width_max = args.number_width_max
    number_height_min = args.number_height_min
    number_height_max = args.number_height_max
    thickness_min = args.thickness_min
    thickness_max = args.thickness_max
    blank_ratio_min = args.blank_ratio_min
    blank_ratio_max = args.blank_ratio_max
    shear_x_min = args.shear_x_min
    shear_x_max = args.shear_x_max
    shift_x_min = args.shift_x_min
    shift_x_max = args.shift_x_max
    shift_y_min = args.shift_y_min
    shift_y_max = args.shift_y_max

    steps = args.steps
    erase_debug_window = args.erase_debug_window
    seed = args.seed

    image_count = args.start_count

    random.seed(seed)

    # 格納ディレクトリ作成
    dataset_dir = 'dataset/'
    for number in range(12):
        os.makedirs(dataset_dir + '{:02}'.format(number), exist_ok=True)

    # カラーセット
    color_set_list = [
        # bg_color, line_color, line_bg_color
        [(110, 120, 120), (10, 20, 20), (90, 100, 100)],
        [(113, 167, 154), (0, 6, 0), (104, 139, 129)],
        [(2, 5, 19), (246, 247, 247), (17, 20, 35)],
        [(242, 242, 242), (2, 2, 2), (222, 222, 222)],
        [(3, 0, 12), (39, 87, 211), (68, 71, 72)],
        [(3, 0, 12), (234, 157, 9), (68, 71, 72)],
        [(3, 1, 29), (6, 0, 105), (49, 56, 63)],
        [(14, 123, 0), (235, 235, 235), (14, 123, 0)],
        [(2, 197, 147), (37, 86, 70), (2, 197, 147)],
        [(200, 219, 211), (55, 55, 55), (147, 165, 158)],
        [(64, 64, 64), (35, 233, 155), (64, 64, 64)],
        [(30, 27, 85), (235, 240, 237), (32, 23, 183)],
        [(34, 15, 49), (247, 247, 240), (164, 131, 121)],
        [(7, 0, 3), (0, 215, 238), (66, 68, 68)],
        [(0, 161, 255), (21, 98, 195), (0, 161, 255)],
        [(253, 146, 64), (238, 9, 5), (253, 146, 64)],
    ]

    for _ in tqdm(range(steps)):
        # 画像生成設定
        number_width = random.uniform(number_width_min, number_width_max)
        number_height = random.uniform(number_height_min, number_height_max)
        thickness = random.uniform(thickness_min, thickness_max)
        blank_ratio = random.uniform(blank_ratio_min, blank_ratio_max)
        shear_x = random.uniform(shear_x_min, shear_x_max)
        shift_x = random.uniform(shift_x_min, shift_x_max)
        shift_y = random.uniform(shift_y_min, shift_y_max)
        color_index = int(random.uniform(0, len(color_set_list)))

        for number_id in range(12):
            # 画像生成
            image = create_7segment_image(
                number=number_id,
                image_size=(image_width, image_height),
                bg_color=color_set_list[color_index][0],
                line_color=color_set_list[color_index][1],
                line_bg_color=color_set_list[color_index][2],
                number_width=number_width,
                number_height=number_height,
                thickness=thickness,
                blank_ratio=blank_ratio,
                shear_x=shear_x,
                shift=(shift_x, shift_y),
            )

            # 描画
            if not erase_debug_window:
                cv.imshow('7seg generator', image)
                cv.waitKey(10)

            # 画像保存
            save_path = os.path.join(dataset_dir, '{:02}'.format(number_id),
                                     '{:08}.png'.format(image_count))
            cv.imwrite(save_path, image)
            image_count += 1

    cv.destroyAllWindows()


if __name__ == '__main__':
    main()