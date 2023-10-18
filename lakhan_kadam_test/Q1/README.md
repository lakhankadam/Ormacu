"""
Question A 
Your goal for this question is to write a program that accepts two lines (x1,x2) and (x3,x4) on the x-axis
and returns whether they overlap. As an example, (1,5) and (2,6) overlaps but not (1,5) and (6,8). 
"""

For Question A, for the two lines to overlap, either line's starting point must be between the other line's starting and ending point.
So, to check if lines overlap on x axis, just check if the starting line of either line is between the other line's starting and ending point.
Hence, the code below checks if the lines overlap on x axis.