from typing import List


class Solution:
    def shuffle(self, nums: List[int], n: int) -> List[int]:
        first = nums[:n]

        second = nums[n:]
        for i in range(0, len(nums), 2):
            first.insert(i + 1, second[i // 2])

        return first


nums = [2, 5, 1, 3, 4, 7]
n = 3
# res = [2, 3, 5, 4, 1, 7]

res = Solution().shuffle(nums, n)

print(res)
