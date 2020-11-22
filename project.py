# Linfeng Li
# Xing Qian
# CS 415 Final Project
# University of Illinois at Chicago
# 11/13/2020

import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import os
import math


def update_group(sym, a, b, c, current_group):
    codes = a
    if codes[sym] == "StartA":
        return a
    elif codes[sym] == "StartB":
        return b
    elif codes[sym] == "StartC":
        return c
    elif codes[sym] == "CodeA":
        return a
    elif codes[sym] == "CodeB":
        return b
    elif codes[sym] == "CodeC":
        return c
    return current_group


def get_bits(img):
    width, height = img.size
    basewidth = 4 * width
    img = img.resize((basewidth, height), Image.ANTIALIAS)
    hor_line_bw = img.crop((0, int(height / 2), basewidth, int(height / 2) + 1)).convert('L')
    hor_data = np.asarray(hor_line_bw, dtype="int32")[0]
    hor_data = 255 - hor_data
    avg = np.average(hor_data)

    plt.plot(hor_data)
    plt.show()

    pos1, pos2 = -1, -1
    bits = ""
    for p in range(basewidth - 2):
        if hor_data[p] < avg < hor_data[p + 1]:
            bits += "1"
            if pos1 == -1:
                pos1 = p
            if bits == "101":
                pos2 = p
                break
        if hor_data[p] > avg > hor_data[p + 1]:
            bits += "0"

    bit_width = int((pos2 - pos1) / 3)
    bits = ""
    for p in range(basewidth - 2):
        if hor_data[p] > avg > hor_data[p + 1]:
            interval = p - pos1
            cnt = interval / bit_width
            bits += "1" * int(round(cnt))
            pos1 = p
        if hor_data[p] < avg < hor_data[p + 1]:
            interval = p - pos1
            cnt = interval / bit_width
            bits += "0" * int(round(cnt))
            pos1 = p
    return bits


def read_barcode():
    barcode_path = './12.jpg'
    img = Image.open(barcode_path)
    bits = get_bits(img)
    # print(bits)
    CODE128_CHART = """
    0       212222  space   space   00
    1       222122  !       !       01
    2       222221  "       "       02
    3       121223  #       #       03
    4       121322  $       $       04
    5       131222  %       %       05
    6       122213  &       &       06
    7       122312  '       '       07
    8       132212  (       (       08
    9       221213  )       )       09
    10      221312  *       *       10
    11      231212  +       +       11
    12      112232  ,       ,       12
    13      122132  -       -       13
    14      122231  .       .       14
    15      113222  /       /       15
    16      123122  0       0       16
    17      123221  1       1       17
    18      223211  2       2       18
    19      221132  3       3       19
    20      221231  4       4       20
    21      213212  5       5       21
    22      223112  6       6       22
    23      312131  7       7       23
    24      311222  8       8       24
    25      321122  9       9       25
    26      321221  :       :       26
    27      312212  ;       ;       27
    28      322112  <       <       28
    29      322211  =       =       29
    30      212123  >       >       30
    31      212321  ?       ?       31
    32      232121  @       @       32
    33      111323  A       A       33
    34      131123  B       B       34
    35      131321  C       C       35
    36      112313  D       D       36
    37      132113  E       E       37
    38      132311  F       F       38
    39      211313  G       G       39
    40      231113  H       H       40
    41      231311  I       I       41
    42      112133  J       J       42
    43      112331  K       K       43
    44      132131  L       L       44
    45      113123  M       M       45
    46      113321  N       N       46
    47      133121  O       O       47
    48      313121  P       P       48
    49      211331  Q       Q       49
    50      231131  R       R       50
    51      213113  S       S       51
    52      213311  T       T       52
    53      213131  U       U       53
    54      311123  V       V       54
    55      311321  W       W       55
    56      331121  X       X       56
    57      312113  Y       Y       57
    58      312311  Z       Z       58
    59      332111  [       [       59
    60      314111  \       \       60
    61      221411  ]       ]       61
    62      431111  ^       ^       62
    63      111224  _       _       63
    64      111422  NUL     `       64
    65      121124  SOH     a       65
    66      121421  STX     b       66
    67      141122  ETX     c       67
    68      141221  EOT     d       68
    69      112214  ENQ     e       69
    70      112412  ACK     f       70
    71      122114  BEL     g       71
    72      122411  BS      h       72
    73      142112  HT      i       73
    74      142211  LF      j       74
    75      241211  VT      k       75
    76      221114  FF      l       76
    77      413111  CR      m       77
    78      241112  SO      n       78
    79      134111  SI      o       79
    80      111242  DLE     p       80
    81      121142  DC1     q       81
    82      121241  DC2     r       82
    83      114212  DC3     s       83
    84      124112  DC4     t       84
    85      124211  NAK     u       85
    86      411212  SYN     v       86
    87      421112  ETB     w       87
    88      421211  CAN     x       88
    89      212141  EM      y       89
    90      214121  SUB     z       90
    91      412121  ESC     {       91
    92      111143  FS      |       92
    93      111341  GS      }       93
    94      131141  RS      ~       94
    95      114113  US      DEL     95
    96      114311  FNC3    FNC3    96
    97      411113  FNC2    FNC2    97
    98      411311  ShiftB  ShiftA  98
    99      113141  CodeC   CodeC   99
    100     114131  CodeB   FNC4    CodeB
    101     311141  FNC4    CodeA   CodeA
    102     411131  FNC1    FNC1    FNC1
    103     211412  StartA  StartA  StartA
    104     211214  StartB  StartB  StartB
    105     211232  StartC  StartC  StartC
    106     2331112 Stop    Stop    Stop
    """.split()

    VALUES = [int(value) for value in CODE128_CHART[0::5]]
    # WEIGHTS = dict(zip(VALUES, CODE128_CHART[1::5]))
    flip_wights = dict(zip(CODE128_CHART[1::5], VALUES))
    CODE128A = dict(zip(CODE128_CHART[1::5], CODE128_CHART[2::5]))
    CODE128B = dict(zip(CODE128_CHART[1::5], CODE128_CHART[3::5]))
    CODE128C = dict(zip(CODE128_CHART[1::5], CODE128_CHART[4::5]))

    sym_len = 11
    symbols = [bits[i:i + sym_len] for i in range(0, len(bits), sym_len)]

    weight_array = []
    for sym in symbols:
        pre = sym[0]
        count = 0
        result = ""
        for char in sym:
            if char != pre:
                result += str(count)
                pre = char
                count = 1
            else:
                count += 1
        result += str(count)
        weight_array.append(result)
    weight_array[len(weight_array) - 2: len(weight_array)] = [''.join(weight_array[len(weight_array) - 2: len(weight_array)])]
    # print(weight_array)
    str_out = ""
    array_out = []
    current_group = update_group(weight_array[0], CODE128A, CODE128B, CODE128C, CODE128A)
    be_ignored_start = ["StartA", "StartB", "StartC"]
    be_ignored_code = ["CodeA", "CodeB", "CodeC", "Stop"]
    running_sum = 0
    position = 1
    weight_values = []
    for sym in weight_array:
        if current_group[sym] not in be_ignored_start and current_group[sym] not in be_ignored_code:
            array_out.append(current_group[sym])
            weight_values.append(sym)
            running_sum += (flip_wights[sym] * position)
            position += 1
        current_group = update_group(sym, CODE128A, CODE128B, CODE128C, current_group)
    running_sum += flip_wights[weight_array[0]]
    running_sum -= flip_wights[weight_values[len(weight_values) - 1]] * (position - 1)
    if running_sum % 103 == flip_wights[weight_array[len(weight_array) - 2]]:
        print("verification pass")
        str_out = ''.join(array_out[:len(array_out) - 1])
    else:
        print(array_out)
    print(str_out)
    return


def main():
    read_barcode()
    return


if __name__ == '__main__':
    main()
