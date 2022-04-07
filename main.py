from daily_cash_service import DailyCashService, Jackpot

def main() -> None:
    service = DailyCashService()
    jackpots:list[Jackpot] = get_jackpot_history()
    list_all_combinations(jackpots)
    return

def get_jackpot_history() -> list[Jackpot]:
    jackpots:list[Jackpot] = []
    service = DailyCashService()
    jackpots = service.load_jackpots_history_from_db()
    return jackpots

def is_three_consecutive(combination:tuple[int]) -> bool:
    is_consecutive = False
    for i in range(3):
        if combination[i]+1 == combination[i+1] and combination[i]+2 == combination[i+2]:
            is_consecutive = True
            break
    return is_consecutive

def is_four_consecutive(combination:tuple[int]) -> bool:
    is_consecutive = False
    for i in range(2):
        if combination[i]+1 == combination[i+1] and combination[i]+2 == combination[i+2] and combination[i]+3 == combination[i+3]:
            is_consecutive = True
            break
    return is_consecutive

def is_five_consecutive(combination:tuple[int]) -> bool:
    is_consecutive = False
    for i in range(1):
        if combination[i]+1 == combination[i+1] and combination[i]+2 == combination[i+2] and combination[i]+3 == combination[i+3] and combination[i]+4 == combination[i+4]:
            is_consecutive = True
            break
    return is_consecutive

def list_all_combinations(jackpot_histories:list[Jackpot]) -> list[tuple]:

    numbers:list[int] = []
    for i in range(39):
        numbers.append(i+1)
    
    service = DailyCashService()
    three_consecutive_count = 0
    four_consecutive_count = 0
    five_consecutive_count = 0
    all_combinations:list[tuple] = []
    for i in numbers[0:35]:
        filtered0:list[Jackpot] = service.filter_jackpots(jackpot_histories, lambda jp : (jp.first == i))
        for j in numbers[(numbers.index(i)+1):36]:
            filtered1:list[Jackpot] = service.filter_jackpots(filtered0, lambda jp : (jp.second==j))
            for k in numbers[(numbers.index(j)+1):37]:
                filtered2:list[Jackpot] = service.filter_jackpots(filtered1, lambda jp : (jp.third==k))
                for l in numbers[(numbers.index(k)+1):38]:
                    filtered3:list[Jackpot] = service.filter_jackpots(filtered2, lambda jp : (jp.fourth==l))
                    for m in numbers[(numbers.index(l)+1):39]:

                        filtered4:list[Jackpot] = service.filter_jackpots(filtered3, lambda jp : (jp.fifth==m))
                        if len(filtered4) > 0:
                            continue
                        
                        if is_five_consecutive((i,j,k,l,m)):
                            five_consecutive_count += 1
                            continue
                        if is_four_consecutive((i,j,k,l,m)):
                            four_consecutive_count += 1
                            continue
                        if is_three_consecutive((i,j,k,l,m)):
                            three_consecutive_count += 1
                            continue

                        all_combinations.append((i,j,k,l,m))
                        
    return all_combinations

if __name__ == '__main__':
    main()