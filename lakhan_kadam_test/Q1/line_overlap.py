def isOverlapping(line1, line2):
    if type(line1) != tuple or len(line1) != 2:
        raise TypeError("Line 1 input is invalid")
    if type(line2) != tuple or len(line2) != 2:
        raise TypeError("Line 2 input is invalid")
    x1, x2 = line1
    x3, x4 = line2
    # check if x1 is between x3 and x4
    if (x3 < x1 < x4) or (x1 < x3 < x2):
        return "Line 1 overlaps with Line 2"
    return "Line 1 does not overlap with Line 2"

if __name__ == "__main__":
    line1 = (1,5)
    line2 = (2,6)
    print(isOverlapping(line1, line2))
    line1 = (1,5)
    line2 = (6,8)
    print(isOverlapping(line1, line2))