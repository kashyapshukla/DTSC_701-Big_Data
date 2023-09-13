# Diagnostic Problem 1:

# Sample Input#1
# abcaaabbb
# Sample Output#1
# abca3b3
# Sample Input#2
# abcd
# Sample Output#2
# abcd


s="aabbcc"
def string_compression(s):

        if not s:
            return s

        compressed = []
        current_char = s[0]
        count = 1

        for i in range(1, len(s)):
            if s[i] == current_char:
                count += 1
            else:
                compressed.append(current_char)
                if count > 1:
                    compressed.append(str(count))
                current_char = s[i]
                count = 1

        compressed.append(current_char)
        if count > 1:
            compressed.append(str(count))

        return ''.join(compressed)

# Sample Input #1
input_str1 = "abcaaabbb"
output_str1 = string_compression(input_str1)
print(output_str1)  # Output: "abca3b3"
# Sample Input #
input_str2 = "abcd"
output_str2 = string_compression(input_str2)
print(output_str2)  # Output: "abcd"

