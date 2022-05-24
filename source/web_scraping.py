from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
"""[自作モジュール]"""
import calc, excel, notice, log

class Scrap:
    def __init__(self, id, name, url, xpath):
        self.id = id
        self.name = name
        self.url = url
        self.xpath = xpath
        self.price = self.ave_price = self.max_price = self.min_price = ''

    def driver_set(chrome_driver):
        """[ブラウザ自動操縦ドライバの設定]"""
        option = Options()
        option.add_argument('--headless')
        driver = webdriver.Chrome(chrome_driver,options=option)
        return driver

    def get(self, driver, url, xpath) -> int:
        """[商品ページへアクセスし、本日の価格を取得する]

        Args:
            driver ([selenium.webdriver.chrome.webdriver.WebDriver]): [ブラウザ操縦ドライバ]
            url ([str]): [商品ページのurl]
            xpath ([str]): [取得したい価格が記載されている箇所のxpath]

        Raises:
            TypeError: [int_priceが数値型ではない場合に例外を出力]

        Returns:
            int: [本日の商品価格]
        """
        driver.get(url)
        wait = WebDriverWait(driver=driver, timeout=30)
        wait.until(EC.presence_of_all_elements_located)# 要素が全て検出できるまで待機する
        elem = driver.find_element_by_xpath(xpath)
        str_price = elem.text
        int_price: int = calc.convert_price(str_price)

        if type(int_price) != int:
            raise TypeError('値段が正しい形式(数値)ではありません')

        return int_price  

def main():
    """[メイン処理]"""
    run_num = success_num = error_num = 0
    scraping_obj = []
    scraping_list = excel.get_info(excel.SCRAP_LIST_SHEET)
    chrome_driver = ChromeDriverManager().install()

    for i, s in enumerate(scraping_list):
        run_num += 1
        #今回、Excelデータは正しく入力されていることを前提とする(入力されていない場合のエラー処理は実装しない。)
        scraping_obj.append(Scrap(s[0].value, s[1].value, s[2].value, s[3].value))

        try:
            driver = Scrap.driver_set(chrome_driver)
            scraping_obj[i].price = scraping_obj[i].get(driver, scraping_obj[i].url, scraping_obj[i].xpath)
        except (WebDriverException, TypeError, Exception) as e:
            excel.write(excel.ERROR_LOG_SHEET, str(e), scraping_obj[i].id, scraping_obj[i].name)
            error_num += 1
            continue
        else:
            success_num += 1
        finally:
          try:
              driver.quit()
              time.sleep(1)
          except UnboundLocalError as e:
              log.logger.error(e)
              break

        excel.write(excel.PRICE_LOG_SHEET, scraping_obj[i].price, scraping_obj[i].id, scraping_obj[i].name)
        price_log_row_list = excel.get_info(excel.PRICE_LOG_SHEET)
        price_list = excel.get_cell_value_list(scraping_obj[i].id, price_log_row_list)
        scraping_obj[i].ave_price = calc.ave(price_list)

        #本日の価格が平均価格より安ければ通知送信
        if (scraping_obj[i].price < scraping_obj[i].ave_price):
            scraping_obj[i].max_price = max(price_list)
            scraping_obj[i].min_price = min(price_list)
            notice.send_notice(scraping_obj[i])

    log.logger.info(f'実行:{run_num}件 | 成功:{success_num}件 | 失敗:{error_num}件')
    
if __name__ == '__main__':
    main()