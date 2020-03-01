import re

match = r"<property name=\"pixel_size\">[0-9]{1,}</property>"

file = open("main.glade", "r")
text = file.read()
file.close()

print(re.findall(r"[0-9]{1,}", re.findall(match, text)))
