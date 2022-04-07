from itertools import combinations
import unittest
from daily_cash_dal import JackpotHistory, DailyCashContext
from daily_cash_service import DailyCashService, Jackpot

class TestCrawlService(unittest.TestCase):

    def test_crawler_service(self):
        service = DailyCashService()
        for i in range(112-107):
            service.load_jackpots_history_to_db(i+107)
        return

    def test_generate_all_combinations(self):
        
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
        
        self.assertEqual(575757, len(all_combinations))
        
    def test_filter_jackpots(self):
        service = DailyCashService()
        jackpots = []
        jp1 = Jackpot()
        jp1.first = 1
        jp1.second = 2
        jp1.third = 3
        jp1.fourth = 4
        jp1.fifth = 5
        jackpots.append(jp1)
        jp2 = Jackpot()
        jp2.first = 1
        jp2.second = 2
        jp2.third = 3
        jp2.fourth = 4
        jp2.fifth = 39
        jackpots.append(jp2)
        jp3 = Jackpot()
        jp3.first = 5
        jp3.second = 6
        jp3.third = 7
        jp3.fourth = 4
        jp3.fifth = 8
        jackpots.append(jp3)
        jackpots2 = service.filter_jackpots(jackpots, lambda jp : (jp.first==1 and jp.second==2 and jp.third==3 and jp.fourth==4))
        print(jackpots2)
        self.assertEqual(2, len(jackpots2))

if __name__ == '__main__':
    unittest.main()