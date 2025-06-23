def compress(chars) -> int:
    ans = 0
    i = 0

    while i < len(chars):
        curr_char = chars[i]
        cnt = 0
        while i < len(chars) and chars[i] == curr_char:
            i += 1
            cnt += 1
        chars[ans] = curr_char
        ans += 1
        if cnt > 1:
            for c in str(cnt):
                chars[ans] = c
                print(f"replace {c}")
                ans += 1

    return ans


for i in str(5):
    print(i)