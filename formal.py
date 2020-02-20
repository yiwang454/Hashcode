# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 17:54:29 2020

@author: wangyi66
"""

import numpy as np

with open('b_read_on.txt') as file:
    a = file.read().splitlines()
    
[total_books, libraries, days_left] = list(map(int, a[0].split(' ')))
scores = list(map(int, a[1].split(' ')))

lib_dict = {}
for li in range(libraries):
    lib_dict[li] = {}
    lib_dict[li]['info'] = list(map(int, a[2 + li * 2].split(' ')))
    lib_dict[li]['books'] = list(map(int, a[3 + li * 2].split(' ')))

lib_score_list = []
award_lists = {}

for num, lib in lib_dict.items():

    lib_score = 0
    book_num = lib["info"][0]
    sign_up_time = lib["info"][1]
    ship_speed = lib["info"][2]
    book_list = lib["books"]
    award_list = []
    for i in book_list:
        award_list.append([i, scores[i]])
        award_list.sort(key = lambda x: x[1], reverse = True)
    if book_num/ship_speed > days_left - sign_up_time:
        award_list = award_list[:ship_speed * (days_left - sign_up_time)]
    award_lists[num] = award_list
    # print(award_list)
    lib_score = list(map(sum,zip(*award_list)))[1]
    # print(lib_score)
    lib_score /= sign_up_time
    lib_score_list.append([num, lib_score])
        
def choose_lib(lib_dict, lib_score_list):
    for item in lib_score_list:
        lib_score_list.sort(key = lambda x: x[1], reverse = True)
    lib_idx = []
    sum_day = 0
    for libs in lib_score_list:
        sum_day += lib_dict[libs[0]]["info"][1]
        if sum_day <= days_left:
            lib_idx.append(libs[0])
            lib_dict[libs[0]]['starting'] = sum_day
        else:
            break
    return lib_idx

def main_f(lib_idx, award_lists, lib_dict):
    result = [[idx, []] for idx in lib_idx]
    book_set = set()
    total_scores = 0
    for day in range(days_left):
        for j, idx in enumerate(lib_idx):
            starting = lib_dict[idx]['starting']
            ship_speed = lib["info"][2]
            if day >= starting:
                nw_books = award_lists[idx]
                for book in nw_books:
                    if book[0] not in book_set:
                        book_set.add(book[0])                        
                        result[j][1].append(book[0])
                        total_scores += book[1]
    
    return result, total_scores 


lib_idx = choose_lib(lib_dict, lib_score_list)

    
RESULT, total_score = main_f(lib_idx, award_lists, lib_dict)
# print(RESULT)

with open('output_b.txt', 'w+') as write_file:
    write_file.write(str(len(RESULT)) + '\n')
    for re in RESULT:
        write_file.write(str(re[0]) + ' ' + str(len(re[1])) + '\n')
        books_str = list(map(str, re[1]))
        write_file.write(' '.join(books_str) + '\n')

print(total_score)