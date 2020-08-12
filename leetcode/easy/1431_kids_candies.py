from typing import List


class Solution:
    def kidsWithCandies(self, candies: List[int], extraCandies: int) -> \
            List[bool]:
        candy_max = max(candies)
        res = []

        for index, value in enumerate(candies):
            res.append(value + extraCandies >= candy_max)

        return res

    def kidsWithCandies_2(self, candies: List[int], extraCandies: int) -> \
            List[bool]:
        M = max(candies)
        return [candy + extraCandies >= M for candy in candies]


candies = [2, 3, 5, 1, 3]
extraCandies = 3
# Output: [true,true,true,false,true]

res = Solution().kidsWithCandies(candies, extraCandies)
print(res)
