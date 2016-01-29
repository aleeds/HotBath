from lattice import Lattice
import math
class Vector:
  """This class will hold a node's position in 3d space"""
  #Positions will be initialized in init
  x = 0  #Int
  y = 0  #Int
  z = 0  #Int

  #Initializes Vector with 3 floats representing an x,y,z position in 3d space
  #[Int, Int, Int] -> [Vector]
  def __init__(self, xx, yy,zz):
    self.x = xx
    self.y = yy
    self.z = zz

  #Returns string representing Vector
  #[Unit] -> [String]
  def __str__(self):
    return "<" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ">"


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



#Global constants
water_k = InterpolationArray()
Hc = 1.0             #Heat transfer constant air->water


#air_temp = 76.0         #in main


class Node(Lattice):
  """This class will represent either a air, body, or water lattice node"""

  #All will be initialized in init
  temp = 0.0                   #Float

  state = 0                    #Int
  #Air   will be represented as 0
  #Body  will be represented as 1
  #Water will be represented as 2
  #State is a psuedo Enum

  Area = 0.0                  #Float
  Weight = 0.0                #Float
  d = 0.0                     #Float

  pos = Vector(0, 0, 0)  #Vector(Int, Int, Int)

  def __init__(self, t, s, xx, yy, zz, a, w, dd):
    self.temp = t
    self.state = s
    self.pos = Vector(xx, yy, zz)
    self.Area = a
    self.Weight = w
    self.d = dd

  #Node -> Float
  def air_water(self, n):
    q = Hc * self.Area * (self.temp - n.temp)
    return q
    #might need standard conduction
      
  #Node -> Float
  def body_water(self, n):
    print "body water"
    #TODO

  #Node -> Float
  def water_water(self, n):
    time_step = 1
    return water_k[self.temp]*self.A*(self.temp - n.temp)*time_step/self.d

  #This will update the temperature of the node based on the time step and neighboring nodes
  #[Node] -> Unit
  def update(self, neighbors):
    #body <--> water
    #air <--> water
    #water <--> water
    deltaQ = 0.0
    for n in neighbors:
      if(self.state == 0): #air
        if(n.state == 2):  #air -> water
          deltaQ += air_water(n)
      elif(self.state == 1): #body
        if(n.state == 2):         #body -> water
          deltaQ += body_water(n)     
      else:                 #water
        if(n.state == 0):   #water -> air
          deltaQ += air_water(n)
        elif(n.state == 1): #water -> body
          deltaQ += body_water(n)
        else:               #water -> water
          deltaQ += water_water(n)

    self.temp -= deltaQ/self.Weight
        

  #Returns the state mapped to the appropiate string based on earlier documentation 
  #[Unit] -> [String]
  def get_state(self):
    if(self.state == 0):
      return "Air"
    elif(self.state == 1):
      return "Body"
    else:
      return "Water"  

  #Returns string version of Node
  def __str__(self):
    return "(" + str(self.temp) + "," + self.get_state() + "," + str(self.pos) + ")"


n = Node(88.88888, 2, 1,2,3, 100,10)
print str(water_k[n.temp])

