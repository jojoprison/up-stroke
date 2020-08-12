import leetcode.rating.rating as rating


class Solution:
    def numJewelsInStones(self, J: str, S: str) -> int:
        count = 0

        for char in J:
            count += S.count(char)

        return count

    def numJewelsInStones_2(self, J, S):
        return sum(map(S.count, J))

    def numJewelsInStones_3(self, J, S):
        return sum(s in J for s in S)

    def numJewelsInStones_4(self, J, S):
        return sum(S.count(j) for j in J)

    def numJewelsInStones_5(self, J: str, S: str) -> int:
        jewels = {}

        for j in J:
            if j not in jewels:
                jewels[j] = 1

        c = 0
        for s in S:
            if s in jewels:
                c += 1

        return c

    def numJewelsInStones_6(self, J: str, S: str) -> int:
        jewels = set(J)

        c = 0
        for s in S:
            if s in jewels:
                c += 1

        return c


J = "aA"
S = "aAAbbbb"
# Output: 3

solution = Solution()

# res = solution.numJewelsInStones_3(J, S)
# print(res)

rating.rate_performance(solution, J, S)
