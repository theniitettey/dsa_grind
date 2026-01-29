"""
time_spent: 1 minutes (doesn't mean i'm a genius)
difficulty: EASY
topic: SETS, ARRAYS
problem_link: https://www.geeksforgeeks.org/problems/union-of-two-arrays3538/1
tries: 1

NOTES:
i tried to use solve it using just the arrays but it was getting too complicated
so I used sets to make it easier
basically we convert both arrays to sets to remove duplicates
then the set union method is used to find the union of both sets, 
this is inbuilt in python which makes it easy
finally we convert the result back to a list and return it
"""
class Solution:
    def findUnion(self, a, b):
        a_set = set(a)
        b_set = set(b)

        return list(a_set.union(b_set))

a = list(map(int, input().split()))
b = list(map(int, input().split()))
solution = Solution()
result = solution.findUnion(a, b)
print(result)

