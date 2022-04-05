import datetime
from typing import Optional
import requests
from bs4 import BeautifulSoup
from daily_cash_dal import JackpotHistory, DailyCashContext

class Jackpot(object):
    
    def __init__(self) -> None:
        self.year = 0
        self.round = 0
        self.first = 0
        self.second = 0
        self.third = 0
        self.fourth = 0
        self.fifth = 0
        self.date = "1900-01-01"
        self.numbers = [self.first, self.second, self.third, self.fourth, self.fifth]
        pass

    def __repr__(self) -> str:
        string_value = f'{self.year}年第{self.round}期: {self.first}, {self.second}, {self.third}, {self.fourth}, {self.fifth} 日期:{self.date}'
        return string_value

class CrawlerService(object):

    def __init__(self) -> None:
        self.year = datetime.date.today().year
        self.url = "http://www.olo.com.tw/histNo/mainT539.php"

    @staticmethod
    def int_try_parse(s:str) -> Optional[int]:
        res = None
        try:
            s = s.replace(",","")
            res = int(s)
        except Exception as ex:
            # print(ex)
            pass
        return res
    
    def get_jackpots_by_year(self, year:int) -> "list[Jackpot]":
        jackpots = []
        self.year = year
        params = {
            "cp": self.year
        }
        r = requests.get(self.url, params)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        jackpot_table = soup.find_all("table")[0]
        nav = jackpot_table.find_all("table")
        nav[0].extract()
        rounds = jackpot_table.find_all("tr")
        rounds = rounds[2:]
        for round in rounds:
            jackpot = Jackpot()
            jackpot.year = year
            tds = round.find_all("td")
            jackpot.round = CrawlerService.int_try_parse(tds[0].get_text())
            jackpot.first = CrawlerService.int_try_parse(tds[1].get_text())
            jackpot.second = CrawlerService.int_try_parse(tds[2].get_text())
            jackpot.third = CrawlerService.int_try_parse(tds[3].get_text())
            jackpot.fourth = CrawlerService.int_try_parse(tds[4].get_text())
            jackpot.fifth = CrawlerService.int_try_parse(tds[5].get_text())
            jackpot.date = tds[6].get_text()
            jackpots.append(jackpot)
        return jackpots


def main() -> int:
    service = CrawlerService()

    db = DailyCashContext()
    db.open()
    for i in range(112-107):
        
        jackpots = service.get_jackpots_by_year(i+107)

        for j in jackpots:
            jh = JackpotHistory()
            jh.year = j.year
            jh.round = j.round
            jh.first = j.first
            jh.second = j.second
            jh.third = j.third
            jh.fourth = j.fourth
            jh.fifth = j.fifth
            jh.date = j.date
            is_success = db.insert_jackpot(jh)
            if is_success == False:
                print(j)
                print("failed!")
                break

    db.commit()
    db.close()
   
    return 0

if __name__ == '__main__':
    main()