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

def UpdateAirWater():
    q = Hc_water_air * water_area * (air_temp - water_temp)
    return q

def UpdateAirBody():
    q = water_k[water_temp]/1000.0*body_area*(body_temp - water_temp)/(10)
    return q

def UpdateWaterFaucet():
    q = water_k[water_temp]/150.0*faucet_size*(faucet_temp - water_temp)/(3)
    return q

def ChangeWaterTemp():
    global water_temp
    q = UpdateAirWater() + UpdateAirBody()
    if faucet_b:
        q += UpdateWaterFaucet()
    water_temp = water_temp + q / water_mass

def execute(i,def_t = 50,inc = 5,faucet_temp_max = 70):

    temps = []
    global water_temp
    global faucet_b
    global faucet_temp
    for k in range(0,i):
        temps += [water_temp]
        if k > i / 4:
            faucet_b = True
            faucet_temp += inc
            if faucet_temp > faucet_temp_max:
                inc = 0
        else:
            faucet_temp = water_temp

        ChangeWaterTemp()
    water_temp = def_t
    return temps

def executeMan(i,def_t,incs,maxs):
    for j in range(0,len(incs)):
        temps = execute(i,def_t,incs[j],maxs[j])
        pyplot.plot(temps)
    pyplot.show()

executeMan(500,50,[1,2,3,5,0,1,2,3,5,0],[70,70,70,70,70,90,90,90,90,50])
