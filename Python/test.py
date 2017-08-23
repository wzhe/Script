from dateutil import parser
import copy
now = parser.parse('Aug 23nd, 22:00')
print(now)
last = parser.parse('Aug 22nd, 22:53')
print(last)
print(last == now)
print(now > last)
#last = now
last=copy.deepcopy(now)
print(last == now)
print(last is now)


