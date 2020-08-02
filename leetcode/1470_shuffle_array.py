from typing import List


class Solution:

    def shuffle(self, nums: List[int], n: int) -> List[int]:
        first = nums[:n]
        second = nums[n:]

        print(first)
        print(second)

        print(len(first))

        for i in range(0, len(first)):
            first.insert(i + 1, second[i])

        print(first)


nums = [2, 5, 1, 3, 4, 7]
n = 3

Solution().shuffle(nums, n)
