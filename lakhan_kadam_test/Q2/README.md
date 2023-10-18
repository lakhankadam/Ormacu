"""
Question B 
The goal of this question is to write a software library that accepts 2 version string as input and returns whether one is greater than, equal, or less than the other.
As an example: “1.2” is greater than “1.1”. Please provide all test cases you could think of. 
"""

A version string is a string that represents a version number. A version string consists of numbers and dots only.
So to check, out of two version strings, which one is greater, equal or less than the other, we can compare the numbers in the version strings.
But first we need to test:
Basic test:
1. The provided input for version strings are strings.
2. The provided input for version strings are not empty.
Checking version format:
3. The provided input for version strings contain only numbers and dots.
4. The provided input for version strings do not have two or more dots in a row.

Now, to compare the version strings, we need to compare the numbers in the version strings.
1. We will split the version strings by dot.
2. We will compare the numbers in the version strings one by one.
3. We will take the minimum length of the two version strings.
4. We will compare the numbers in the version strings by converting them to integers.
5. When the strings are typecasted to integers, if the strings contain leading zeros, the leading zeros will be removed.
6. If any of the numbers in the version string is greater than the other, we return our result.
7. When all the numbers in the version strings are equal, we return our result based on the remaining length of the version strings.
8. We check if the remaining length of any version string is greater than 0. If it is, then the version string with the greater length is greater than the other.
9. Finally, if none of the conditions in 6, 7 and 8 are met, then the version strings are equal.
