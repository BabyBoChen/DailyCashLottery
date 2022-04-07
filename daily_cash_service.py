import datetime
from pyclbr import Function
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
        pass

    def sort(self) -> "Jackpot":
        numbers = [self.first, self.second, self.third, self.fourth, self.fifth]
        numbers = sorted(numbers, key=lambda n:n)
        j = Jackpot()
        j.first = numbers[0]
        j.second = numbers[1]
        j.third = numbers[2]
        j.fourth = numbers[3]
        j.fifth = numbers[4]
        j.year = self.year
        j.round = self.round
        j.date = self.date
        return j

    def to_tuple(self) -> tuple[int]:
        numbers = [self.first, self.second, self.third, self.fourth, self.fifth]
        numbers = sorted(numbers, key=lambda n:n)
        return tuple(numbers)

    def __repr__(self) -> str:
        string_value = f'{self.year}年第{self.round}期: {self.first}, {self.second}, {self.third}, {self.fourth}, {self.fifth} 日期:{self.date}'
        return string_value

class DailyCashService(object):

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
    
    @staticmethod
    def is_three_consecutive(combination:tuple[int]) -> bool:
        is_consecutive = False
        for i in range(3):
            if combination[i]+1 == combination[i+1] and combination[i]+2 == combination[i+2]:
                is_consecutive = True
                break
        return is_consecutive

    @staticmethod
    def is_four_consecutive(combination:tuple[int]) -> bool:
        is_consecutive = False
        for i in range(2):
            if combination[i]+1 == combination[i+1] and combination[i]+2 == combination[i+2] and combination[i]+3 == combination[i+3]:
                is_consecutive = True
                break
        return is_consecutive

    @staticmethod
    def is_five_consecutive(combination:tuple[int]) -> bool:
        is_consecutive = False
        for i in range(1):
            if combination[i]+1 == combination[i+1] and combination[i]+2 == combination[i+2] and combination[i]+3 == combination[i+3] and combination[i]+4 == combination[i+4]:
                is_consecutive = True
                break
        return is_consecutive

    def __init__(self) -> None:
        self.year = datetime.date.today().year
        self.url = "http://www.olo.com.tw/histNo/mainT539.php"

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
            jackpot.round = DailyCashService.int_try_parse(tds[0].get_text())
            jackpot.first = DailyCashService.int_try_parse(tds[1].get_text())
            jackpot.second = DailyCashService.int_try_parse(tds[2].get_text())
            jackpot.third = DailyCashService.int_try_parse(tds[3].get_text())
            jackpot.fourth = DailyCashService.int_try_parse(tds[4].get_text())
            jackpot.fifth = DailyCashService.int_try_parse(tds[5].get_text())
            jackpot.date = tds[6].get_text()
            jackpots.append(jackpot)
        return jackpots
    
    def load_jackpots_history_to_db(self, year:int) -> "list[Jackpot]":
        jackpots = self.get_jackpots_by_year(year)
        db = DailyCashContext()
        db.open()
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
        return jackpots
    
    def load_jackpots_history_from_db(self) -> "list[Jackpot]":
        jackpots:list[Jackpot] = []
        db = DailyCashContext()
        db.open()
        jp_hists = db.get_jackpots()
        db.close()
        for jp_hist in jp_hists:
            jp = Jackpot()
            jp.year = jp_hist.year
            jp.round = jp_hist.round
            jp.first = jp_hist.first
            jp.second = jp_hist.second
            jp.third = jp_hist.third
            jp.fourth = jp_hist.fourth
            jp.fifth = jp_hist.fifth
            jp.date = jp_hist.date
            jackpots.append(jp)
        return jackpots

    def filter_jackpots(self, items:"list[Jackpot]", func:Function) -> list[Jackpot]:
        newItems = []
        for i in items:
            j = i.sort()
            isValid:bool = func(j)
            if isValid == True:
                newItems.append(j)
        return newItems
    
    def list_all_combinations(self) -> list[tuple]:
        numbers:list[int] = []
        for i in range(39):
            numbers.append(i+1)
        all_combinations:list[tuple] = []
        for i in numbers[0:35]:
            for j in numbers[(numbers.index(i)+1):36]:
                for k in numbers[(numbers.index(j)+1):37]:
                    for l in numbers[(numbers.index(k)+1):38]:
                        for m in numbers[(numbers.index(l)+1):39]:
                            all_combinations.append((i,j,k,l,m))
        return all_combinations