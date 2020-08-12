from typing import List
import leetcode.rating.rating as rating

class Solution:

    def smallerNumbersThanCurrent(self, nums: List[int]) -> List[int]:
        res = [0] * len(nums)
        for i, v in enumerate(nums):
            for j, jv in enumerate(nums):
                if i != j and v > jv:
                    res[i] += 1
        return res

    def smallerNumbersThanCurrent_2(self, nums: List[int]) -> List[int]:
        # do it before so that dont do it into list comprehension
        sorted_nums = sorted(nums)
        return [sorted_nums.index(num) for num in nums]

    def smallerNumbersThanCurrent_3(self, nums: List[int]) -> List[int]:
        dct = {}
        for i, n in enumerate(sorted(nums)):
            if n not in dct:
                dct[n] = i
        return [dct[n] for n in nums]

    def smallerNumbersThanCurrent_4(self, nums):
        return [*map(sorted(nums).index, nums)]

    # 1.3698570000000014

    def smallerNumbersThanCurrent_5(self, nums: List[int]) -> List[int]:
        result = []
        tempNums = nums.copy()
        nums.sort()
        for n in tempNums:
            result.append(nums.index(n))
        return result

    def smallerNumbersThanCurrent_6(self, nums: List[int]) -> List[int]:
        indices = {}
        for idx, num in enumerate(sorted(nums)):
            indices.setdefault(num, idx)
        return [indices[num] for num in nums]


nums = [8,1,2,2,3]
# Output: [4,0,1,1,3]

# nums = [7,7,7,7]
# Output: [0,0,0,0]

solution = Solution()

# res = solution.smallerNumbersThanCurrent_7(nums)
# print(res)
rating.rate_performance(solution, nums)
