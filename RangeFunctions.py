def combine_bounds(my_list):
    intersection_count = 0
    continuity_count = 0
    sorted_list = sorted(my_list)
    for x in sorted_list:
        if sorted_list.index(x) < len(sorted_list) -1:
            y = sorted_list[sorted_list.index(x) + 1]
            if x[1] + 1 > y[0]:
                intersection_count += 1
            if x[1] + 1 == y[0]:
                continuity_count += 1
        else:
            if intersection_count == len(sorted_list) -1:
                return (max([x[0] for x in sorted_list]),min([x[1] for x in sorted_list]))
            elif intersection_count + continuity_count == len(sorted_list) -1:
                return (min([x[0] for x in sorted_list]),max([x[1] for x in sorted_list]))
            else:
                return "NULL"
