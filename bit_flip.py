class Solution:
    def minBitFlips(self, start: int, goal: int) -> int:
        # XOR start and goal, and count the number of 1s in the binary representation
        return bin(start ^ goal).count('1')
