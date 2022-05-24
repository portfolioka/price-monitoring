import requests

def send_notice(scraping_obj):
    """[LINEに通知を送信]"""
    TOKEN = '' #LINE Notify APIのアクセストークンを''内に記載する
    api_url = 'https://notify-api.line.me/api/notify'

    message = f"""
    商品が買い時です！

    商品名：{scraping_obj.name}
    本日の価格：{scraping_obj.price}円
    平均価格：{scraping_obj.ave_price}円
    最高価格：{scraping_obj.max_price}円
    最低価格：{scraping_obj.min_price}円
    URL：{scraping_obj.url}
    """

    TOKEN_dic = {'Authorization' : 'Bearer' + ' ' + TOKEN}
    send_dic = {'message' : message}

    requests.post(api_url, headers=TOKEN_dic, data=send_dic)