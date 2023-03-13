#!/usr/bin/python3


string = {"hannah", "racecar", "nathan todd"}
def is_palindrome(string):
    for j in range(int(len(string)/2)):
        if string[j] != string[len(string) - j - 1]:
            return False
    else:
        return True
for i in string:
    print(i)
    print(is_palindrome(i))
    print()
    