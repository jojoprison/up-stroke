import collections
from typing import List

import leetcode.rating.rating as rating

class Solution:
    def groupThePeople(self, groupSizes: List[int]) -> List[List[int]]:

        # groups = collections.defaultdict(list)

        groups = {}
        for i in range(max(groupSizes)):
            groups[i + 1] = list()

        for inx, val in enumerate(groupSizes):
            groups[val].append(inx)

        result = []
        for group_index, group_values in groups.items():
            for i in range(0, len(group_values), group_index):
                result.append(group_values[i: i + group_index])

        return result

    # BEST
    def groupThePeople_3(self, groupSizes: List[int]) -> List[List[int]]:

        sizeToGroup, res = collections.defaultdict(list), []

        for i, size in enumerate(groupSizes):
            sizeToGroup[size].append(i)

            if len(sizeToGroup[size]) == size:
                res.append(sizeToGroup.pop(size))

        return res

    def groupThePeople_4(self, groupSizes):
        d = {}
        for i, v in enumerate(groupSizes):
            if v in d:
                d[v].append(i)
            else:
                d[v] = [i]
        return [d[i][j:j + i] for i in d for j in range(0, len(d[i]), i)]

    # как мое, упрощенное плюшками языка
    def groupThePeople_5(self, groupSizes):
        count = collections.defaultdict(list)
        for i, size in enumerate(groupSizes):
            count[size].append(i)
        return [l[i:i + s]for s, l in count.items() for i in range(0, len(l), s)]


# groupSizes = [3,3,3,3,3,1,3]
# Output: [[5],[0,1,2],[3,4,6]]
# Other: [[2,1,6],[5],[0,4,3]] and [[5],[0,6,2],[4,3,1]].

groupSizes = [2,1,3,3,3,2]
# Output: [[1],[0,5],[2,3,4]]

solution = Solution()
# res = solution.groupThePeople_3(groupSizes)
# print(res)
rating.rate_performance(solution, groupSizes)
