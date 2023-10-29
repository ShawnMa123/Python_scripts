class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        len1, len2 = len(str1), len(str2)
        for i in range(min(len1, len2), 0, -1):
            if self.valid_str(i, str1, str2):
                return str1[:i]
        return ""

    def valid_str(self, valid_len, str1, str2):
        if (len(str1) % valid_len != 0) or (len(str2) % valid_len != 0):
            return False
        else:
            k1, k2 = len(str1) // valid_len, len(str2) // valid_len
            test_str = str1[:valid_len]

            return (str1 == k1 * test_str) and (str2 == k2 * test_str)


if __name__ == "__main__":
    demo = Solution()
    str1 = "TAUXXTAUXXTAUXXTAUXXTAUXX"
    str2 = "TAUXXTAUXXTAUXXTAUXXTAUXXTAUXXTAUXXTAUXXTAUXX"
    print(demo.gcdOfStrings(str1, str2))
