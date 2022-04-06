from daily_cash_dal import JackpotHistory, DailyCashContext
from crawler_service import CrawlerService

def main() -> None:
    get_jackpot_history()
    return

def get_jackpot_history():
    service = CrawlerService()
    for i in range(112-107):
        service.load_jackpots_history_to_db(i+107)

if __name__ == '__main__':
    main()