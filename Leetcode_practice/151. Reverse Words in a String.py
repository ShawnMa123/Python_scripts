class Solution:
    def reverseWords(self, s: str) -> str:
        all_words = s.split()
        ans_str = []
        for i in all_words[::-1]:
            ans_str.append(i)
        return (" ").join(ans_str)