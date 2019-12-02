# calculate median? I may have misunderstood the question!

import sys
import re


def solution(list1):
  length = len(list1)
  #print(length)
  half = length // 2
  median = (list1[half - 1] + list1[half]) / 2
  return median

copy_pasta = """value_predictor([1,2,3,4,5,6]) should return 3.5
value_predictor([1,1,1,6,6,6]) should return either 3.5 closer to 3.45 depending on method"""

# generate test set from copy_pasta
test_set = []
for line in copy_pasta.splitlines():
  match = re.match(r"\D+(\[[0-9,]+\])\D+([0-9\.]+)",line)
  test_case = (eval(match.group(1)),eval(match.group(2)))
  test_set.append(test_case)

#print(test_set)

# If the file is run with a list as an argument, execute the solution function using the list
# Default behaviour: execute test cases
if len(sys.argv) >= 2:
  list1 = eval(sys.argv[1])
  sys.stdout.write(repr(solution(list1)))
else:
  for test_case in test_set:
    result = solution(test_case[0])
    print(f"case: {test_case} solution: {result}")
    assert result == test_case[1], f"test failed: {test_case}"