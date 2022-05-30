from collections import Counter


def remov_duplicates(input):
    # split input string separated by space
    input = input.split(" ")

    # joins two adjacent elements in iterable way
    for i in range(0, len(input)):
        input[i] = "".join(input[i])

        # now create dictionary using counter method
    # which will have strings as key and their
    # frequencies as value
    UniqW = Counter(input)

    # joins two adjacent elements in iterable way
    s = " ".join(UniqW.keys())
    print(s)


# Driver program
if __name__ == "__main__":
    tier_1 = ["techmahindra","hcl"]
    input = 'Python is great and Java is also great techmahindra hcl hcl hcl'
    for x in tier_1:
        str_contains = str.__contains__(input, x)
        if str_contains is True:
            remov_duplicates(input)