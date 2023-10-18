def basic_input_check(version):
    #Check if version is string
    if type(version) != str:
        raise TypeError("Version input is invalid for "+ version)
    #Check if version is empty
    if version == "":
        raise ValueError("Version input is empty for "+ version)

def check_version_format(version):
    #Check if version string contains only numbers and dots
    import re
    pattern = re.compile(r'^[0-9.]+$')
    if not pattern.match(version):
        raise ValueError("Version input is invalid for "+ version)
    version_list = version.split(".")
    for v in version_list:
        if v == "":
            raise ValueError("Version input is invalid for "+ version)

def test_compareVersion(version1, version2):
    #Testing version input and format
    basic_input_check(version1)
    basic_input_check(version2)
    check_version_format(version1)
    check_version_format(version2)

def compareVersion(version1, version2):
    test_compareVersion(version1, version2)
    version1_list = version1.split(".")
    version2_list = version2.split(".")
    #Compare each digit of version1 and version2
    #Take min length of version1 and version2
    length = min(len(version1_list), len(version2_list))
    i = 0
    #Compare each digit of version1 and version2
    while i < length:
        if int(version1_list[i]) > int(version2_list[i]):
            return version1 + " is greater than " + version2
        elif int(version1_list[i]) < int(version2_list[i]):
            return version1 + " is less than " + version2
        i += 1
    #If all digits are equal yet, then compare the rest of version1 and version2
    while i < len(version1_list):
        if int(version1_list[i]) > 0:
            return version1 + " is greater than " + version2
        i += 1
    while i < len(version2_list):
        if int(version2_list[i]) > 0:
            return version1 + " is less than " + version2
        i += 1
    return version1 + " is equal to " + version2

if __name__ == "__main__":
    version1 = "1.1.110"
    version2 = "1.1.101"
    print(compareVersion(version1, version2))