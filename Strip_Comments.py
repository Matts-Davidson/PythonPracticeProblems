# Function to remove specific characters (markers) of a string plus all characters to the right of that character
# Markers should be a list of single characters in strings format
# White spaces before removed markers should also be deleted
# New lines to be interpretted individually

def solution(string,markers):
    new_string = string.split('\n')
    for m in markers:
        new_string = [s.split(m)[0].rstrip() for s in new_string]
    return '\n'.join(new_string)