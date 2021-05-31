import sys
import time

db_file_csv = input('ENTER THE PATH AND NAME OF THE FILE:')
minSupport = float(input('ENTER MINIMUM SUPPORT:'))
minConfidence = float(input('ENTER MINIMUM CONFIDENCE:'))


with open("Vishal_databases/main_db.csv") as f:
    itm = f.read().replace("\n", "").split(",")
    itm.sort()


with open(db_file_csv) as f:
    db_trans = []
    for l in f:
        db_ = l.replace('\n', '').split(",")
        db_trans.append(db_)
    print('#####---------------TRANSACTIONS INPUTS---------------#####')
    for tran in db_trans:
        print(tran)


def k_item_gen(itm, k):
    if k == 1:
        return [[j] for j in itm]

    all_res = []
    for i in range(len(itm)-(k-1)):
        for sub in k_item_gen(itm[i+1:], k-1):
            tmp = [itm[i]]
            tmp.extend(sub)
            all_res.append(tmp)
    return all_res


def search_check(db_trans, chk):
    cnt = 0
    for t in db_trans:
        if set(chk).issubset(t):
            cnt =cnt + 1
    return cnt


def gen_FreqAndSupp():
    frequent = []
    support = {}
    len_itm = len(itm)+1
    for k in range(1, len_itm):
        current = []
        for comb in k_item_gen(itm, k):
            cnt = search_check(db_trans, comb)
            div_ = cnt/len(db_trans)
            if div_ >= minSupport:
                support[frozenset(comb)] = div_
                current.append(comb)
        len_curr = len(current)
        if len_curr == 0:
            break
        frequent.append(current)
    return frequent, support


class Rule:

    def __init__(self, left, right, all):
        self.left = list(left)
        self.left.sort()
        self.right = list(right)
        self.right.sort()
        self.all = all

    def __str__(self):
        return ",".join(self.left) + " --->> " + ",".join(self.right) + " | "

    def __hash__(self):
        return hash(str(self))


def generate_rules(frequent, support):
    all_rule = set()
    all_res = []
    for k_freq in frequent:
        if len(k_freq) == 0:
            continue
        if len(k_freq[0]) < 2:
            continue
        for freq in k_freq:
            for i in range(1, len(freq)):
                for left in k_item_gen(freq, i):
                    tmp = freq.copy()
                    right = [val for val in tmp if val not in left]
                    all_rule.add(Rule(left, right, freq))
    for rule in all_rule:
        confidence = support[frozenset(rule.all)] / support[frozenset(rule.left)]
        if confidence >= minConfidence:
            all_res.append([rule, support[frozenset(rule.all)], confidence])

    all_res.sort(key=lambda val: str(val[0]))

    return all_res


if __name__ == '__main__':
    prog_start_time_ = time.time()
    freq, s = gen_FreqAndSupp()
    res_val = generate_rules(freq, s)
    prog_end_time_ = time.time()
    print("\n---RULES---SUPPORT---CONFIDENCE---")
    for r in res_val:
        a_ = str(r[0])
        a_r = str(r[1])
        a_r2 = str(r[2])
        print(a_, 'SUPPORT: ' + a_r, "CONFIDENCE: " + a_r2)
    print("\n-----------------------------------------------------------------------")
    print("TIME TAKEN:" + str(prog_end_time_ - prog_start_time_) + "s")

