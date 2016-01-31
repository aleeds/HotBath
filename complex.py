import math
import matplotlib.pyplot as pyplot

air_temp = 20
body_temp = 37
water_temp = 50
faucet_temp = 50
water_area = 10
water_mass = 1000
body_area = 3
faucet_size = 10
faucet_b = False
Hc_water_air = 3.0

second_water_temp = 50


class InterpolationArray:
  """Class to hold values and interpolation between them with float indicies"""
  values = {0: 561.0, 10: 580.0, 20: 598.4, 30: 615.4, 40: 630.5,
            50: 643.5, 60: 654.3, 70: 663.1, 80: 670.0, 90: 675.3, 100: 679.1}
  #Float -> Float
  def __getitem__(self, i):
    i_below = math.floor(i/10.0)*10
    i_above = math.ceil(i/10.0)*10
    i -= i_below
    i /= 10
    return self.values[i_below]*i + self.values[i_above]*(1-i)

water_k = InterpolationArray()

def UpdateAirWater(water):
    q = Hc_water_air * water_area * (air_temp - water)
    return q

def UpdateWaterBody(water):
    q = water_k[water_temp]/1000.0*body_area*(body_temp - water)/(10)
    return q

def UpdateWaterFaucet():
    q = water_k[water_temp]/150.0*faucet_size*(faucet_temp - water_temp)/(3)
    return q

def UpdateSecondWaterWater(water_one,water_two):
    q = water_k[water_two]/150.0*water_area*(water_one - water_two)/(3)
    return q

def Mix(prop):
    global water_temp
    global second_water_temp
    water_one_t = prop * water_temp + (1 - prop) * second_water_temp
    water_two_t = prop * second_water_temp + (1 - prop) * water_temp
    water_temp = water_one_t
    second_water_temp = water_two_t

def ChangeWaterTemp():
    global water_temp
    global second_water_temp
    q = UpdateAirWater(water_temp) + UpdateWaterBody(water_temp)
    q += UpdateSecondWaterWater(second_water_temp,water_temp)
    q_two = UpdateSecondWaterWater(water_temp,second_water_temp) + UpdateWaterBody(second_water_temp)
    q_two += UpdateAirWater(second_water_temp)
    if faucet_b:
        q += UpdateWaterFaucet()

    water_temp = water_temp + q / water_mass
    second_water_temp = second_water_temp + q_two / (1 * water_mass)

def execute(i,def_t = 50,inc = 5,faucet_temp_max = 70,freq = 10,prop = .7):

    temps = []
    second_temps = []
    faucet_temps = []
    global water_temp
    global second_water_temp
    global faucet_b
    global faucet_temp
    for k in range(0,i):
        temps += [water_temp]
        second_temps += [second_water_temp]
        faucet_temps += [faucet_temp]
        if k > i / 4:
            faucet_b = True
            faucet_temp += inc
            if faucet_temp > faucet_temp_max:
                inc = 0
        else:
            faucet_temp = water_temp

        ChangeWaterTemp()

        if k % freq == 0:
            Mix(prop)

    water_temp = def_t
    second_water_temp = def_t
    return (temps,second_temps,faucet_temps)

def executeMan(i,def_t,incs,maxs,freqs,props):
    fig = pyplot.figure()
    #ax0 = fig.add_subplot(311)
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    for j in range(0,len(incs)):
        (temps,second_temps,faucet_temps) = execute(i,def_t,incs[j],maxs[j],freqs[j],props[j])
        ax1.plot(temps)
        ax2.plot(second_temps)
        #ax0.plot(faucet_temps)
    pyplot.show()
    (temps,second_temps,faucet_temps) = execute(i,def_t,incs[4],maxs[4],freqs[4],props[4])
    pyplot.plot(temps)
    pyplot.plot(second_temps)
    pyplot.show()

#executeMan(500,50,[1,2,3,5,0,1,2,3,5,0],[70,70,70,70,70,90,90,90,90,50])

executeMan(500,50,[1,1,1,1,1],[70,70,70,70,70],[10 * (2 ** n) for n in range(0,4)] + [2],[.5,.5,.5,.5,.5])
