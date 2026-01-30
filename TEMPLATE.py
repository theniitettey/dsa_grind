"""
time_spent: ?
difficulty: ?
topic: ?
problem_link: {problem_link}
tries: 1
created: {created}

notes:
- what’s the input/output?
- patterns?
- first idea (even if it’s bad)
- final approach + why it works

time_complexity: ?
space_complexity: ?

edge_cases_tested:
- ?

learned:
- ?

alternatives:
- ?
"""


class Solution:
    def solve(self, *args, **kwargs):
        """
        NOTE:
        - Function name is auto-generated from the problem title (snake_case).
        - Rename/adjust the signature to match the platform before submitting.
        """
        return None


if __name__ == "__main__":
    # Read input from stdin
    try:
        input_line = input().strip()
        if input_line:
            # Try to parse as integers or strings based on content
            try:
                args = list(map(int, input_line.split()))
            except ValueError:
                args = input_line.split()
            
            solution = Solution()
            result = solution.solve(args)
            if result is not None:
                print(result)
    except EOFError:
        pass
