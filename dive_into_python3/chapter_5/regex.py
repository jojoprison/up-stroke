import re

s = '100 NORTH MAIN ROAD'
# $ matches the end of a string
print(re.sub('ROAD$', 'RD.', s))
# ^ matches the start of a string
print(re.sub('^ROAD', 'RD.', s))

