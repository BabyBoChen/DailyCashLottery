from crawler_service import CrawlerService, Jackpot

def main() -> None:
    jackpots:list[Jackpot] = get_jackpot_history()
    all_combinations = list_all_combinations(jackpots)
    return

def get_jackpot_history() -> list[Jackpot]:
    jackpots:list[Jackpot] = []
    service = CrawlerService()
    for i in range(112-107):
        jackpots.extend(service.load_jackpots_history_to_db(i+107))
    return jackpots

def list_all_combinations(jackpot_histories:list[Jackpot]) -> list[tuple]:

    def filter_list(items:list, func) -> list:
        newItems = []
        for i in items:
            isValid:bool = func(i)
            if isValid == True:
                newItems.append(i)
        return newItems

    numbers:list[int] = []
    for i in range(39):
        numbers.append(i+1)
    
    all_combinations:list[tuple] = []
    for i in numbers[0:35]:
        # temp = filter_list(jackpot_histories, lambda jp : jp.get_numbers()[0] == i)
        for j in numbers[(numbers.index(i)+1):36]:
            for k in numbers[(numbers.index(j)+1):37]:
                for l in numbers[(numbers.index(k)+1):38]:
                    for m in numbers[(numbers.index(l)+1):39]:
                        all_combinations.append((i,j,k,l,m))
    return all_combinations

if __name__ == '__main__':
    main()