import os

# define params
# params = [i/100 for i in range(10,90)]
# params = [0.5,0.7,0.9]
params = [0.3, 0.35, 0.4, 0.45, 0.55, 0.6, 0.65, 0.75, 0.8, 0.85]

for param in params:
    os.system('python find_opt_parameter.py {}'.format(str(param)))
