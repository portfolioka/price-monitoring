import re

def convert_price(str_price):
    """[数字以外の文字(\D)を削除=数字を抽出]"""
    return  int(re.sub(r"\D", "", str_price))

def ave(value_list):
    """[平均値計算]"""
    return int(sum(value_list) / len(value_list))