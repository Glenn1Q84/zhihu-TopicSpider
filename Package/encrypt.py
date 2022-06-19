# -*- coding = utf-8 -*-
# 知乎加密
import hashlib
import random
import os
import execjs

#
# COOKIE_LIST = [
#     '"AvAQDHN4mxSPTtVyJn9kQSMi43V1kPWH_qc=|1646810832"',
#     '"ANBQa9czlRSPThnOgiTPFdnLtVpygBC7eWk=|1646390194"'
# ]


def _md5(txt: str):
    """
    MD5加密
    """
    return hashlib.md5(txt.encode(encoding='UTF-8')).hexdigest()


def encrypt(num: str, api: str):
    """
    知乎加密
    :param num: headers中的x-zse-93
    :param api: 接口及后面的参数
    :return: signature
    """
    # api="/api/v4/search_v3?t=general&q=%E4%B9%B0%E8%A3%A4%E5%AD%90%E7%9A%84%E6%B7%98%E5%AE%9D%E5%BA%97&correction=1&offset=0&limit=1&lc_idx=0&show_all_topics=0"
    cookie = "ADAd4vIt0RSPTn5rlhAFhXZA7vFD5PUj0Ak=|1650415181"
    # sxcs="3_2.0VhnTj77m-qofgh3TxTnq2_Qq2LYuDhV80wSL7eU0r6Ppb7tqXRFZQi90-LS9-hp1DufI-we8gGHPgJO1xuPZ0GxCTJHR7820XM20cLRGDJXfgGCBxupMuD_Ie8FL7AtqM6O1VDQyQ6nxrRPCHukMoCXBEgOsiRP0XL2ZUBXmDDV9qhnyTXFMnXcTF_ntRueTh738LJr9evNVcuFfG0xBpweM6ex8pgoMYTtGtqLqN9HxOBgBvCOCtJO8_9VPvLeVPwFfBDgMiqpK68pyBLSqkeS_uhgVCrS16wCfcHSM6M21D9NGFCtCxJ3YDg3pHbeL8GX16qXMHhpYxCL1TUV0thX0ogN89vL_NDwfxJrmQRt1H9tm5qfzqreBQTgp-uVqfTgq2He0BvCsTCLffq3Cb4OLYwgOtwo1Twe11D3fshN9fcHqbCFBOgNMuCtKDB3ONCx9qgO8o9o_3h2mYUeCVcXYN9H9QLpy5we83rNC"
    sign = _md5(f'{num}+{api}+{cookie}')
    path = "F:\Glenn\workspace_for_pycharm\zhihuspider"

    with open(f'{path}/Package/encrypt.js') as f:
        js_signature = execjs.compile(f.read(), cwd=f'{path}/Package/node_modules')
        signature = js_signature.call('b', sign)
        signature = '2.0_' + signature
    return signature, cookie

