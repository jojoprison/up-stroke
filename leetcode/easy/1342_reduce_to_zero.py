import leetcode.rating.rating as rating

class Solution:

    def numberOfSteps(self, num: int) -> int:
        steps = 0

        while num > 0:
            if num % 2 == 0:
                num //= 2
            else:
                num -= 1

            steps += 1

        return steps

    def numberOfSteps_4(self, num: int) -> int:
        cnt = 0
        while num > 0:
            cnt += 1 if num % 2 == 0 or num == 1 else 2
            num //= 2
        return cnt

    def numberOfSteps_2(self, num: int) -> int:
        digits = f'{num:b}'
        return digits.count('1') - 1 + len(digits)

    # FASTEST
    def numberOfSteps_3(self, num: int) -> int:
        digits = f'{num:b}'
        return digits.count('1') * 2

    def numberOfSteps_5(self, num: int) -> int:
        # s = bin(num) = '0b1110'
        s = bin(num)[2:]
        return s.count('1') + len(s) - 1


num = 14
# Output: 6

# num = 8
# Output: 4

# num = 123
# Output: 12

solution = Solution()

# res = solution.numberOfSteps_2(num)
# print(res)

rating.check_time(solution.numberOfSteps_5, num)
# rating.check_time(solution.numberOfSteps_3, num)
# rating.check_time(solution.numberOfSteps_2, num)
