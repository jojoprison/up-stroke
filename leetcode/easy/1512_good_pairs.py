import collections
from typing import List


class Solution:
    def numIdenticalPairs(self, nums: List[int]) -> int:
        lenn = len(nums)
        sum = 0

        for i in range(lenn):
            for j in range(i + 1, lenn):
                if nums[i] == nums[j]:
                    sum += 1

        return sum

    def numIdenticalPairs_2(self, nums: List[int]) -> int:

        pairs = set()
        for num in nums:
            # trying to use list comprehension
            result = [i for i, e in enumerate(nums) if e == num]
            # cast to tuple cause set cant store mutable list
            pairs.add(tuple(result))

        # Gausses function to count pairs (factorial with add instead mul)
        def gauss_sum(n):
            return n * (n + 1) // 2

        # count pairs in every tuple in set
        count = 0
        for pair_tuple in pairs:
            count += gauss_sum(len(pair_tuple) - 1)

        return count

    def numIdenticalPairs_3(self, nums: List[int]) -> int:
        # collections.Counter(nums).values() count all possible values of list
        # and collect them into dictionary Counter
        print(collections.Counter(nums).values())
        return sum(k * (k - 1) // 2 for k in collections.Counter(nums).values())


# nums = [1, 1, 1, 1]
# res = 6

nums = [1, 2, 3, 1, 1, 3]
# res = 4

# nums = [1,2,3]
# res = 0

# res = Solution().numIdenticalPairs_2(nums)
# res = Solution().numIdenticalPairs(nums)
res = Solution().numIdenticalPairs_3(nums)
print(res)
