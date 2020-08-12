import re

import leetcode.rating.rating as rating


class Solution:

    def defangingIPaddr(self, address: str) -> str:
        return address.replace('.', '[.]')

    def defangingIPaddr_2(self, address: str) -> str:

        list_str = list(address)

        # with i argument enumerate generate tuple for each element
        for idx, val in enumerate(list_str):
            # !faster than list_str[idx] == "."
            if val == ".":
                list_str[idx] = "[.]"

        return "".join(list_str)

    # Convert the ip address into a list of the numbers using the split method.
    # Add the "[.]" chars between the numbers using the join method.
    def defangingIPaddr_3(self, address: str) -> str:
        return "[.]".join(address.split("."))

    def defangingIPaddr_4(self, address: str) -> str:
        ans = []
        for ch in address:
            if ch.isdigit():
                ans.append(ch)
            else:
                ans.append("[.]")

        return "".join(ans)

    def defangingIPaddr_5(self, address: str) -> str:
        return re.sub('..', '[.]', address)


address = "1.1.1.1"
# res: "1[.]1[.]1[.]1"

# address = "255.100.50.0"
# res: "255[.]100[.]50[.]0"

solution = Solution()

# res = solution.defangingIPaddr(address)
# print(res)

rating.check_time(solution.defangingIPaddr, address)
# rating.check_memory(solution.defangingIPaddr, address)
