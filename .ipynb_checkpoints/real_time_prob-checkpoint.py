import hmac
import hashlib
import numpy as np
import pandas as pd
from math import pow, floor
from datetime import datetime, timedelta
from time import sleep


from selenium import webdriver
from selenium.webdriver.common.keys import Keys # send keys like: Keys.ENTER

from selenium.webdriver.common.by import By # find_element_by_xpath == find_element(By.XPATH, "//div[@class='entries']/*")
from selenium.webdriver.support.ui import WebDriverWait # Explicit waits
from selenium.webdriver.support import expected_conditions as EC #conditions for explicit waits



""" ========================================================================================================
# 1 - Open blaze """

def open_blaze():
  driver = webdriver.Chrome()
  driver.set_window_size(510,690)
  driver.get("https://blaze.com/pt/games/crash")  
  return driver

def current_crashes(driver):
    # get the number of current points on crash page.
  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='entries']/*[1]")))
  total_points = driver.find_elements_by_xpath("//div[@class='entries']/span")
  return len(total_points)

def get_last_crash_point(driver):
    # explicit wait usage: checking and waiting for element to be clickable
      # (!) when page loads exactly on a transition between crashes rounds, raise an error that element cannot be clickable. Flow is crashed
  return WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='entries']/*[1]")))

def get_the_hash(driver):
    # explicit wait usage: getting hash when modal loads completely
  the_hash = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='server-roll']/*"))).text
    #close modal
  driver.back()
  return the_hash

def get_last_point_hash(driver):
  point = get_last_crash_point(driver)
  point.click()
  the_hash = get_the_hash(driver)
  return the_hash




""" ========================================================================================================
# 2 - Estimate """
client_seed = "0000000000000000000415ebb64b0d51ccee0bb55826e43846e5bea777d91966"
def generate(amount=1000, seed='492bd10144a3525e2745718fe4d25e08affbea483872d8e8b86191b20ce0a7a8'):
  clock_ini = datetime.now()
  print(f"  beginning {clock_ini.isoformat('_')}")
  chain = [seed]
  hmacs = []
  crashes = []
  #print("estanciando chain, hmacs, crashes")
  #print(chain, hmacs, crashes)
  # print("def divisible() e getPoint()")
  def divisible(hash_hmac, mod):
    #print("Inicio DIVISIBLE()")
    val = 0
    o = len(hash_hmac) % 4
    #print("estanciando val, o")
    #print(val, o)
    if o > 0:
      #print("o > 0: True")
      o -= 4
    # else:
      #print("o > 0: False")
    #print(o)
    #print(f"Inicio for x in range(0,{len(hash_hmac)},4):")
    for x in range(0,len(hash_hmac),4):
      #print(f"x = {x}     val = {val}")
      val = ((val << 16) + int(hash_hmac[x:x+4],16)) % mod
      #print("val = ((val << 16) + int(hash_hmac[x:x+4],16)) % mod")
      #print(f"({val << 16} + {int(hash_hmac[x:x+4],16)}) % {mod}")
      #print(f"val = {val}")
    # print(f"val == 0, return {val==0}")
    return val == 0
  
  def getPoint(hash_hmac):
    # print("Inicio GETPOINT()")
    # print("checando se divisible(hash_hmac, 15) retorna True")
    if divisible(hash_hmac, 15):
      # print("retornou True, script acaba aqui e retorna 0")
      return 0
    h = int(hash_hmac[0:int(52/4)], 16)
    e = int(pow(2, 52))
    # print("retornou False, estanciando h, e")
    # print(h, e)
    point = float(format((floor((100 * e - h) / (e - h)) / 100), ".2f"))
    # print(f"ponto gerado, return {point}")
    return point
  
  # print("END def divisible() e getPoint()")
  print(f"  Gerando {amount:,} seeds, começando com {chain[0][:8]}...{chain[0][int(64-8):]}")
  for x in range(amount):
    chain.append(hashlib.sha256(str.encode(chain[x])).hexdigest())
    # print(len(chain),chain[len(chain)-1])

  for seed in chain:
    hash_hmac = hmac.new(str.encode(seed), str.encode(client_seed), hashlib.sha256).hexdigest()
    hmacs.append(hash_hmac)

    point = getPoint(hash_hmac)
    crashes.append(point)
    # print(len(hmacs), hmacs[len(hmacs)-1], len(crashes), crashes[len(crashes)-1])

  # print("pd.DataFrame({'points':[crashes], 'seeds':[chain], 'hmacs':[hmacs]})")

  clock_fin = datetime.now()
  duration = (clock_fin - clock_ini).total_seconds()
  text = f"""\
  finishing {clock_fin.isoformat("_")}
  {len(chain)} in {duration} seconds"""
  print(text)

  return pd.DataFrame(
    {
      "points": crashes[::-1],
      "seeds": chain[::-1],
      "hmacs": hmacs[::-1],
    }
  )


def factors_stats(data):
  clock_ini = datetime.now()
  print(f"beginning {clock_ini.isoformat('_')}")
  # points = data[2]
  stats = []
  resume = ""
  for x in range(52): # 50 for intervaled() + 1 for zeros + 1 for above 6
    stats.append(0)

  def intervaled():
    # list with 50 intervals of 0.09 starting from 1.01 to 6
    intervals = [[0.0,1.0]]
    init = 1.01
    more = 0.09
    for x in range(50):
      intervals.append([float(f"{init:.2f}"),float(f"{init+more:.2f}")])
      init += 0.1
    intervals.append([6.01,float('inf')])
    return intervals

  intervals = intervaled()

  for x in range(len(stats)):
    for point in data:
      if point >= intervals[x][0] and point <= intervals[x][1]:
        stats[x] += 1
  
  for x in range(len(stats)):
    resume += f"""\
{intervals[x][0]:.2f} < x < {intervals[x][1]:.2f}  perc: {format((stats[x]/(len(data))*100),".7f")}%,  quant: {format(stats[x], ",")}
"""
    # print(text)


  clock_fin = datetime.now()
  duration = (clock_fin - clock_ini).total_seconds()
  text = f"""\
finishing {clock_fin.isoformat("_")}
{format(len(data), ",")} itens em {duration} segundos"""
  print(text)


  return [stats,resume]



class Caio():
  pass


class Analise():
  def __init__(self):
    print('open_blaze() in driver')
    self.driver = open_blaze()

    self.ncrashes = current_crashes(self.driver)
    print(f"{self.ncrashes} crashes on {datetime.now().isoformat('_')}")

    self.hash = get_last_point_hash(self.driver)
    print(f"the_hash of {get_last_crash_point(self.driver).text}: {self.hash}")

    self.df = generate(amount=1999, seed=self.hash)

    self.p = pd.DataFrame({"out":self.df.points.shift(periods=100), "in":self.df.points,})
    
    
    # self.p['pt100mean'] = self.p['pt'].rolling(100).mean()
    self.p['dif'] = self.p['in'] - self.p['out']
    self.p['insum'] = self.p['in'].rolling(100).sum()
    self.p['insuMin'] = self.p['insum'].rolling(100).min()
    self.p['insuMax'] = self.p['insum'].rolling(100).max()
    self.p['inprop'] = ( (self.p['insum'] - self.p['insuMin']) / (self.p['insuMax'] - self.p['insuMin']) )

    self.p['good'] = np.where(self.p['in'] > 2.20, 1, 0)
    self.p['good100sum'] = self.p['good'].rolling(100).sum()
    # self.p['good100mean'] = self.p['good'].rolling(100).mean()
    self.p['good100min'] = self.p['good100sum'].rolling(100).min()
    self.p['good100max'] = self.p['good100sum'].rolling(100).max()

    self.p = self.p[1000:].reset_index(drop=True)
    # self.goods = len(self.p[self.p['pt'] > 2.20])


  def clos(self):
    self.driver.close()

a=Analise()