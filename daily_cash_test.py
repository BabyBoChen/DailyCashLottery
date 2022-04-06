from itertools import combinations
import unittest
from daily_cash_dal import JackpotHistory, DailyCashContext
from crawler_service import CrawlerService, Jackpot

class TestCrawlService(unittest.TestCase):

    def test_crawler_service(self):

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

    def test_jackpot_sort(self):
        jp = Jackpot()
        jp.first = 5
        jp.second = 4
        jp.third = 3
        jp.fourth = 2
        jp.fifth = 1
        jp.round = 1
        jp.year = 2048
        jp.date = '2048-04-08'

        actual = jp.get_numbers()
        expected = [1,2,3,4,5]
        for i in range(len(expected)):
            self.assertEqual(actual[i] , expected[i])

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


if __name__ == '__main__':
    unittest.main()