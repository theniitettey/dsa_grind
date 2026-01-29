"""
You are given two arrays a[] and b[], return the Union of both the arrays in any order.

The Union of two arrays is a collection of all distinct elements present in either of the arrays. If an element appears more than once in one or both arrays, it should be included only once in the result.

Note: Elements of a[] and b[] are not necessarily distinct.
Note that, You can return the Union in any order but the driver code will print the result in sorted order only.

Examples:

Input: a[] = [1, 2, 3, 2, 1], b[] = [3, 2, 2, 3, 3, 2]
Output: [1, 2, 3]
Explanation: Union set of both the arrays will be 1, 2 and 3.
Input: a[] = [1, 2, 3], b[] = [4, 5, 6] 
Output: [1, 2, 3, 4, 5, 6]
Explanation: Union set of both the arrays will be 1, 2, 3, 4, 5 and 6.
Input: a[] = [1, 2, 1, 1, 2], b[] = [2, 2, 1, 2, 1] 
Output: [1, 2]
Explanation: Union set of both the arrays will be 1 and 2.
Constraints:
1 ≤ a.size(), b.size() ≤ 10^6
0 ≤ a[i], b[i] ≤ 105
"""

a = list(map(int, input().split()))
b = list(map(int, input().split()))

class Solution:
    def findUnion(self, a, b):
        # since we want to find the union of two lists, the straight forward approach is to turn both lists to a set and use the inbuilt union() function and return the result as a list
        a_set = set(a)
        b_set = set(b)

        return list(a_set.union(b_set))
    

result = Solution().findUnion(a, b)
print(result)
    

