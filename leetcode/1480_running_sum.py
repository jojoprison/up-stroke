import operator
from itertools import accumulate
from typing import List


class Solution:

    def runningSum(self, nums: List[int]) -> List[int]:

        result = []

        for count in range(0, len(nums)):
            result_num = nums[0]
            local_index = 1
            while local_index <= count:
                result_num += nums[local_index]
                local_index += 1

            result.append(result_num)

        return result

    def runningSum_2(self, nums: List[int]) -> List[int]:
        return accumulate(nums, operator.add)



nums = [1,2,3,4]
result = Solution().runningSum_2(nums)
for each in result:
    print(each)

