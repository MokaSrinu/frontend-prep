# Python regular expressions

# Regular expressions allow you to locate and change strings in a very powerful way.

# Regular expressions (Regex) are used to
# 1. Search for a specific string in a large amount of data
# 2. Verify that string has the proper format (eg: mobile, email ..etc)
# 3. Find a string and replace it with another string.
# 4. Formatting data into proper format for importing.

# import a regex module
import re

if re.search('ape', 'The ape was at the apex'):
    print('Match for ape found...')


# -----------Get All matches------------
# findall() returns a list of matches 
# . is used to match any 1 character or a space
allApes =  re.findall('ape.', 'The ape was at apex')

for i in allApes:
    print(i)


