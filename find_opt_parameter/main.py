import os

# 定义参数列表
params = [i/100 for i in range(10,26)]

for param in params:
    os.system('python find_opt_parameter.py {}'.format(str(param)))
