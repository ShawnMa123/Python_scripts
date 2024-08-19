class Solution:
    def get_prodct(self, in_nums):
        ans = 1
        for i in in_nums:
            ans = i * ans
        return ans

    def productExceptSelf(self, nums):
        ans = []
        all_p = self.get_prodct(nums)

        for i in nums.copy():
            if i == 1:
                ans.append(all_p)
            elif i == -1:
                ans.append(-1*all_p)
            elif i != 0:
                ans.append(int(all_p/i))
            else:
                tmp = nums.copy()
                tmp.remove(i)
                t_ans = ans.append(self.get_prodct(tmp))
                if t_ans:
                    ans.append(t_ans)

        return ans


if __name__ == "__main__":
    nums = [-1,1,0,-3,3]

    demo = Solution()
    print(demo.productExceptSelf(nums))
