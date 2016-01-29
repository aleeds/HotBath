def equil(t_one,t_two):
    Q = .6 * 1 * (t_one - t_two) / .01
    # this is the same as joules, cause 1 second
    t_one_new = t_one - Q / 10000
    t_two_new = t_two + Q / 10000
    return (t_one_new,t_two_new)

ls = [(1,(50,100))]
for t in range(1,1000):
    v = ls[t - 1]
    a = v[1][0]
    b = v[1][1]
    ls += [(t,equil(a,b))]

import matplotlib.pyplot as plt

ls_time = [t for (t,temp) in ls]
ls_temp = [a for (t,(a,b)) in ls]
plt.plot(ls_time,ls_temp)
ls_temp_b = [b for (t,(a,b)) in ls]

plt.plot(ls_time,ls_temp_b)
plt.show()

def equil_two(t_one,t_two):
    Q = .6 * 1 * abs(t_one - t_two) / .01
    # this is the same as joules, cause 1 second
    t_one_new = t_one - Q / 100000
    t_two_new = t_two + Q / 100000
    return (t_one_new,t_two_new)

ls = [(1,(100,50))]
for t in range(1,1000):
    v = ls[t - 1]
    a = v[1][0]
    b = v[1][1]
    ls += [(t,equil_two(a,b))]

ls_time = [t for (t,temp) in ls]
ls_temp_b = [b for (t,(a,b)) in ls]
ls_temp = [a for (t,(a,b)) in ls]
plt.plot(ls_time,ls_temp)
plt.plot(ls_time,ls_temp_b)
plt.show()
