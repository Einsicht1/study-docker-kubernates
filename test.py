from math import ceil
def solution(progresses, speeds):
    days = [] # 7, 3, 9
    answer = []
    a, b = 0, 0
    for i in range(len(progresses)):
        remain_day = ceil((100 - progresses[i]) / speeds[i])
        days.append(remain_day)
    for i in range(len(days)):
        pop_value = days.pop(0)



progresses = [93, 30, 55]
speeds = [1, 30, 5]
# progresses = [95, 90, 99, 99, 80, 99]
# speeds = [1, 1, 1, 1, 1, 1]

