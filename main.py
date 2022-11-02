import itertools as it

def transaction_reader(filename: str) -> list[list[int]]:
    ans = []
    with open(filename, "r") as f:
        for line in f.readlines():
            letters = [s.strip() for s in line.strip().split(",")]
            ans.append(sorted(letters))
    return ans

def get_support_table(transaction_list: list[list[int]], k: int, min_sup: float):
    support_table = dict()
    for transaction in transaction_list:
        for item_set in it.combinations(transaction, k):
            if item_set in support_table:
                support_table[item_set] += 1
            else:
                support_table[item_set] = 1
    num_transactions = len(transaction_list)
    for key in support_table.keys():
        support_table[key] = (support_table[key], round(support_table[key] / num_transactions, 2))
    
    to_be_deleted = []
    for key in support_table.keys():
        if support_table[key][1] < min_sup:
            to_be_deleted.append(key)

    for key in to_be_deleted:
        del support_table[key]
    return support_table


def get_rule_table(transaction_list: list[list[int]], k: int, min_sup: float, min_cof: float):
    sp_tables = dict()
    i = 1
    while True:
        sp = get_support_table(transaction_list, i, min_sup)
        if len(sp) == 0:
            i -= 1
            break
        sp_tables[i] = sp
        i += 1
    
    all_keys = []
    for j in range(1, i + 1):
        all_keys.extend(list(sp_tables[j].keys()))
    max_c = i
    for k1 in all_keys:
        for k2 in all_keys:
            c1 = len(k1)
            c2 = len(k2)
            s1 = set(k1)
            s2 = set(k2)
            if (c1 + c2 <= max_c):
                kx = tuple(sorted(list(k1 + k2)))
                t1 = sp_tables[c1][k1][0]
                t2 = sp_tables[c2][k2][0]
                if kx in sp_tables[c1 + c2]:
                    tx = sp_tables[c1 + c2][kx][0]
                    if not (round(tx / t1, 2) < min_cof):
                        print(s1, s2, round(tx / t1, 2))

def main():
    transaction_list = transaction_reader("transactions.txt")
    print("--- transaction list ---")
    for transaction in transaction_list:
        print(transaction)
    support_table = get_support_table(transaction_list, 2, 0.3)
    print("--- support table (k = 2) ---")
    for key in support_table:
        print(key, support_table[key])
    print("--- rule table ---")
    get_rule_table(transaction_list, 4, 0.3, 0.7)
    pass

if __name__ == '__main__':
    main()