import sys
import time

db_file_csv = input('ENTER THE PATH AND NAME OF THE FILE:')
minSupport = float(input('ENTER MINIMUM SUPPORT:'))
minConfidence = float(input('ENTER MINIMUM CONFIDENCE:'))

with open(db_file_csv) as f:
    db_trans = []
    for l in f:
        db_ = l.replace('\n', '').split(",")
        db_trans.append(db_)
    print('#####---------------TRANSACTIONS INPUTS---------------#####')
    for tran in db_trans:
        print(tran)


class Rule:

    def __init__(self, left, right, all):
        self.left = list(left)
        self.left.sort()
        self.right = list(right)
        self.right.sort()
        self.all = all

    def __str__(self):
        return ",".join(self.left)+" --->> "+",".join(self.right) + " | "

    def __hash__(self):
        """
        Store support value to dict
        :return: hash value in the object
        """
        return hash(str(self))


def search_check(db_trans, chk):
    cnt = {}
    for nb in chk:
        cnt[nb]=0
    for t in db_trans:
        for frequent_set in chk:
            if frequent_set.issubset(t):
                cnt[frequent_set] += 1
    n = len(db_trans)
    return {frequent_set: support/n for frequent_set, support in cnt.items() if support/n >= minSupport}


def c_generate(gk):
    c_g_res = []
    len_gk = len(gk)
    for i in range(len_gk):
        for j in range(i+1, len(gk)):
            num, num1 = gk[i], gk[j]
            n1, n2 = list(num), list(num1)
            n1.sort()
            n2.sort()
            if n1[:len(num)-1] == n2[:len(num)-1]:
                c_g_res.append(num | num1)
    return c_g_res


def gen_FreqAndSupp():
    support = {}
    cand = [[]]
    gk = [[]]
    c_ = set()
    for t in db_trans:
        for item in t:
            c_.add(frozenset([item]))

    cand.append(c_)
    cnt = search_check(db_trans, c_)
    gk.append(list(cnt.keys()))
    support.update(cnt)

    k = 1
    while len(gk[k]) > 0:
        cand.append(c_generate(gk[k]))
        cnt = search_check(db_trans, cand[k+1])
        support.update(cnt)
        gk.append(list(cnt.keys()))
        k += 1
    return gk, support


def generate_sub_rule(fs, rights, a_res, support):
    right_size = len(rights[0])
    total_size = len(fs)
    if total_size-right_size > 0:
        rights = c_generate(rights)
        new_right = []
        for right in rights:
            left = fs - right
            if len(left) == 0:
                continue
            confidence = support[fs] / support[left]
            if confidence >= minConfidence:
                a_res.append([Rule(left, right, fs), support[fs],  confidence])
                new_right.append(right)

        if len(new_right) > 1:
            generate_sub_rule(fs, new_right, a_res, support)


def generate_rules(fq, sup):
    all_res = []
    for i in range(2, len(fq)):
        if len(fq[i]) == 0:
            break
        freq_sets = fq[i]

        for fs in freq_sets:
            for right in [frozenset([val]) for val in fs]:
                left = fs-right
                confidence = sup[fs] / sup[left]
                if confidence >= minConfidence:
                    all_res.append([Rule(left, right, fs), sup[fs], confidence])

        if len(freq_sets[0]) != 2:

            for fs in freq_sets:
                right = [frozenset([val]) for val in fs]
                generate_sub_rule(fs, right, all_res, sup)

    all_res.sort(key=lambda val: str(val[0]))
    return all_res


if __name__ == '__main__':
    prog_start_time_ = time.time()
    freq, s = gen_FreqAndSupp()
    res_val = generate_rules(freq, s)
    prog_end_time_ = time.time()
    print("\n---RULES---SUPPORT---CONFIDENCE:---")
    for r in res_val:
        a_ = str(r[0])
        a_r = str(r[1])
        a_r2 = str(r[2])
        print(a_, 'SUPPORT: '+a_r, "CONFIDENCE: "+a_r2)
    print("\n-----------------------------------------------------------------------")
    print("TIME TAKEN:"+str(prog_end_time_ - prog_start_time_) + "s")
