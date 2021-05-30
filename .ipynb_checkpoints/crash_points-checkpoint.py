import hmac
import hashlib
import numpy as np
import pandas as pd
from math import pow, floor
from datetime import datetime, timedelta

client_seed = "0000000000000000000415ebb64b0d51ccee0bb55826e43846e5bea777d91966"



def app(amount=10, seed='492bd10144a3525e2745718fe4d25e08affbea483872d8e8b86191b20ce0a7a8'):
  clock_ini = datetime.now()
  print(f"INICIO {clock_ini.isoformat('_')}")

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


  print(f"Gerando {amount:,} seeds, começando com {chain[0][:8]}...{chain[0][int(64-8):]}")
  for x in range(amount):
    chain.append(hashlib.sha256(str.encode(chain[x])).hexdigest())
    # print(len(chain),chain[len(chain)-1])

  for seed in chain:
    hash_hmac = hmac.new(str.encode(seed), str.encode(client_seed), hashlib.sha256).hexdigest()
    hmacs.append(hash_hmac)

    point = getPoint(hash_hmac)
    crashes.append(point)
    # print(len(hmacs), hmacs[len(hmacs)-1], len(crashes), crashes[len(crashes)-1])


  print("retornando [chain, hmacs, crashes]")

  clock_fin = datetime.now()
  duration = (clock_fin - clock_ini).total_seconds()

  text = f"""\
  FIM {clock_fin.isoformat("_")}
  {len(chain)} seeds levou {duration} segundos"""
  print(text)

  return [chain, hmacs, crashes]



def see(data, index=0, leng=30):
  for x in range(index, index+leng):
    print(f"{data[0].index(data[0][x])}  -  {data[2][x]}  -  {data[0][x]}  -  {data[1][x]}")


def factors_stats(data):
  clock_ini = datetime.now()
  print(f"BEGIN {clock_ini.isoformat('_')}")
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
END {clock_fin.isoformat("_")}
{format(len(data), ",")} itens em {duration} segundos"""
  print(text)


  return [stats,resume]



df = pd.read_pickle("data/data.pkl")
spoints = df.points

stats = factors_stats(spoints)
"""

crypto.createHash("sha256").update(chain[chain.length - 1]).digest("hex")
seed = hashlib.sha256(b"492bd10144a3525e2745718fe4d25e08affbea483872d8e8b86191b20ce0a7a8").hexdigest()



hmac = method(seed, clientSeed, sha256).digest("hex)
hmac2 = hmac.new(b"07d922bcfbf90c15fe50bb5d9aa84549e1131c97cf0a586845ccd231c83844df", b"0000000000000000000415ebb64b0d51ccee0bb55826e43846e5bea777d91966", hashlib.sha256).hexdigest()



f"{number:020,.2f}"
'0,001,234,567,890.00'
which demonstrates (1) how to do zero-padding (of length 20), (2) the thousands comma, (3) round to 2 significant figures. All useful weapons to be able to draw from the top of your head
"""
