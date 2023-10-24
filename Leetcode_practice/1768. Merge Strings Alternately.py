class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        ans = ""
        max_len = max(len(word1), len(word2))
        for i in range(max_len):
            if i < len(word1):
                ans += word1[i]
            if i < len(word2):
                ans += word2[i]

        return ans


if __name__ == "__main__":
    demo = Solution()

    word1 = "abcd"
    word2 = "pq"
    print(demo.mergeAlternately(word1, word2))
