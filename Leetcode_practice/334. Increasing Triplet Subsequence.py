class Solution:
    def increasingTriplet(self, nums) -> bool:
        min1 = float('inf')
        min2 = float('inf')

        for num in nums:
            if num <= min1:
                min1 = num
            elif num <= min2:
                min2 = num
            else:
                return True

        return False


if __name__ == "__main__":
    demo = Solution()
    nums = [20, 100, 10, 12, 5, 13]
    print(demo.increasingTriplet(nums))
