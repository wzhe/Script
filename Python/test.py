from dateutil import parser
now = parser.parse('Aug 22nd, 22:56')
print(now)
last = parser.parse('Aug 22nd, 22:56')
print(last)
if last == now:
    print('OK')

