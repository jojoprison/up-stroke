from typing import List
import leetcode.rating.rating as rating


class Solution:

    def restoreString(self, s: str, indices: List[int]) -> str:
        str_res = ''
        for i in range(len(indices)):
            str_res += s[indices.index(i)]
        return str_res

    # MINE
    def restoreString_2(self, s: str, indices: List[int]) -> str:
        res = [''] * len(indices)
        for i in indices:
            res[i] = s[indices.index(i)]
        return ''.join(res)

    def restoreString_3(self, s: str, indices: List[int]) -> str:
        res = [''] * len(s)
        for index, char in enumerate(s):
            res[indices[index]] = char
        return ''.join(res)

    def restoreString_4(self, s: str, indices: List[int]) -> str:
        a = [''] * len(s)
        for i, idx in enumerate(indices):
            a[idx] = s[i]
        return ''.join(a)

    def restoreString_5(self, s: str, indices: List[int]) -> str:
        ans = [''] * len(s)
        for c, i in zip(s, indices):
            ans[i] = c
        return "".join(ans)

    def restoreString_6(self, s: str, indices: List[int]) -> str:
        res = list(s)
        for c, idx in zip(s, indices):
            res[idx] = c
        return "".join(res)


s = "aiohn"
indices = [3, 1, 4, 2, 0]
# Output: "nihao"

solution = Solution()

# res = solution.restoreString_8(s, indices)
# print(res)

rating.rate_performance(solution, s, indices)
