import collections
from typing import List

import leetcode.rating.rating as rating

class Solution:
    def optimalDivision(self, nums: List[int]) -> str:
        variants = collections.defaultdict(list)
        div = 1
        print(type(div))
        max = 0
        max_str = ''
        for i in range(4):
            expression = f'{1}/{2}/{3}/{4}'


        print(div)

        print(1000 // (100 // 10) // 2)

        print(variants)

nums = [1000, 100, 10, 2]
# Output: "1000/(100/10/2)"
# Other:
# 1000/(100/10)/2 = 50
# 1000/(100/(10/2)) = 50
# 1000/100/10/2 = 0.5
# 1000/100/(10/2) = 2

solution = Solution()
res = solution.optimalDivision(nums)
print(res)
# rating.rate_performance(solution, nums)