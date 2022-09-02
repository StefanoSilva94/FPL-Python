import os
import re

file = "TRUVL_SFTTRA_BKENGB_R00012-220421_437901-0"
# WRITE FILE AS A REGEX: [A-Z]+_[A-Z]+_[A-Z]+_

y = re.findall("[0-9]{6}", file)[-1]
y = '_' + str(int(y) + 1)
file = re.sub("_[0-9]{6}", y, file)

a = "Chelsea FC"
b = re.sub("e", "9",a,-1)
print(b)