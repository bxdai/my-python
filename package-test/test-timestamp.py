import time

# 获取当前时间
current_time = int(time.time())
print(current_time) # 1631186249
# 转换为localtime
localtime = time.localtime(current_time)
# 利用strftime()函数重新格式化时间
dt = time.strftime('%Y:%m:%d %H:%M:%S', localtime)
print(dt) # 返回当前时间：2021:09:09 19:17:29


from dateutil.parser import parse

# 输入时间格式
a = parse('2019-10-30 23:43:10.123')
b = parse("2019-10-28/09:08:13.56212")

print((a-b).days)      # 获取天数的时间差
print((a-b).seconds)       # 获取时间差中的秒数，也就是23:43:10到09:08:13，不包括前面的天数和秒后面的小数
print((a-b).total_seconds())     # 包括天数，小时，微秒等在内的所有秒数差
print((a-b).microseconds)      # 秒小数点后面的差值

import datetime

t = time.time()

print (t)                       #原始时间数据
print (int(t))                  #秒级时间戳
print (int(round(t * 1000)))    #毫秒级时间戳





