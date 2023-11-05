class Solution:
    def kidsWithCandies(self, candies: List[int], extraCandies: int) -> List[bool]:
        max_candy = max(candies)
        ans = []
        for i in candies:
            tmp = i+extraCandies
            ans.append((tmp >= max_candy))
        return ans