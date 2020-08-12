from typing import List

import leetcode.rating.rating as rating

class Solution:
    def sortArrayByParity(self, A: List[int]) -> List[int]:
        even = []
        odd = []

        for elem in A:
            if not elem % 2:
                even.append(elem)
            else:
                odd.append(elem)

        # even.extend(odd)

        return even + odd

    def sortArrayByParity_2(self, A):
        return sorted(A, key=lambda x: x % 2)

    # INTERESTED
    def sortArrayByParity_3(self, A: List[int]) -> List[int]:
        i, j = 0, len(A) - 1
        while i < j:
            if A[i] % 2 == 1 and A[j] % 2 == 0:
                A[i], A[j] = A[j], A[i]

            i, j = i + 1 - A[i] % 2, j - A[j] % 2
        return A


A = [3,1,2,4]
# Output: [2,4,3,1]

solution = Solution()
res = solution.sortArrayByParity_3(A)
print(res)

# rating.rate_performance(solution, A)