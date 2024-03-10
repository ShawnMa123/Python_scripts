class Solution:
    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        max_flower = 0
        new_list = [0] + flowerbed + [0]
        max_len = len(flowerbed)

        for i in range(1, max_len+1):
            if new_list[i-1] == 0 and new_list[i+1] == 0 and new_list[i] == 0:
                max_flower +=1
                new_list[i] = 1

        return n <= max_flower