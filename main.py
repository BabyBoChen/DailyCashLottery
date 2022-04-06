from daily_cash_dal import JackpotHistory, DailyCashContext
from crawler_service import CrawlerService

def main() -> None:
    
    return

def get_jackpot_history():

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
    return

