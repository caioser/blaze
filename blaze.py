import time
import numpy as nu
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys # send keys like: Keys.ENTER

from selenium.webdriver.common.by import By # find_element_by_xpath == find_element(By.XPATH, "//div[@class='entries']/*")
from selenium.webdriver.support.ui import WebDriverWait # Explicit waits
from selenium.webdriver.support import expected_conditions as EC #conditions for explicit waits

# 1 - open https://blaze.com/pt/games/crash
def open_blaze():
  driver = webdriver.Chrome()
  driver.get("https://blaze.com/pt/games/crash")
  print("Ok, ready to go now!")
  return driver


# 2 - click in last crash factor to open modal
def get_last_crash_factor(driver):
    # explicit wait usage: checking and waiting for element to be clickable
      # (!) when page loads exactly on a transition between crashes rounds, raise an error that element cannot be clickable. Flow is crashed
  return WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='entries']/*[1]"))) 

def onload_n_crashes(driver):
    # get the number of [total, goods, bads] crashes when page load. Return dictionary
  total_factors = driver.find_elements_by_xpath("//div[@class='entries']/span")
  goods = driver.find_elements_by_xpath("//div[@class='entries']/span[@class='good']")
  bads = driver.find_elements_by_xpath("//div[@class='entries']/span[@class='bad']")
  print(f"goods:{len(goods)}, bads:{len(bads)} ---> total:{len(total_factors)}")
  return {
    "goods":len(goods),
    "bads":len(bads),
    "total":len(total_factors)
  }


# 3 - take the $HASH of the crash
def get_the_hash(driver):
    # explicit wait usage: getting hash when modal loads completely
  the_hash = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='server-roll']/*"))).text
  print(f"captured hash '{the_hash}'")
    #close modal
  driver.back()
  return the_hash


# 4 - open in new window https://o5orm2mmrq.csb.app/
def open_script():
  another = webdriver.Chrome()
  another.get("https://o5orm2mmrq.csb.app/")
  return another


# 5 - enter the server seed of your game
def paste_hash(another, the_hash):
    # explicit wait usage: wait load to send keys with $HASH to first input
  WebDriverWait(another, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[1]"))).send_keys(the_hash)
  print("pasted")


# 6 - enter number of crashes
def digit_ninenine(another, nines):
    # explicit wait usage: precaution when acessing the second input and clearing text field
  WebDriverWait(another, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[2]"))).clear()
    # send keys with ['99' || '999' || '9999']
  another.find_element_by_xpath("//input[2]").send_keys(nines)


# 7 - dispose each item of 'Crash point' column of generated table in a $ARRAY
def get_list_factors(another):
    # explicit wait usage: wait for generate all crash points
  list_ok = WebDriverWait(another, 10).until(EC.element_to_be_clickable((By.XPATH, "//td[@style]"))).text
  print(list_ok)
    # getting all crash factors entries as <class WebElement>
  factor_entries_list = another.find_elements_by_xpath("//td[@style]")
  print(f"{len(factor_entries_list)} entries to analize...")
  return factor_entries_list

def get_list_seeds(another):
    # explicit wait usage: wait for generate all crash points
  list_ok = WebDriverWait(another, 10).until(EC.element_to_be_clickable((By.XPATH, "//tr/td[2]"))).text
  print(list_ok)
    # getting all crash seeds as <class WebElement>
  seed_list = another.find_elements_by_xpath("//tr/td[2]")
  for x in range(len(seed_list)):
    seed_list[x] = seed_list[x].text
  print(f"{len(seed_list)} entries to analize...")
  return seed_list


def intervaled():
    # list with 50 intervals of 0.09 starting from 1.01 to 6
  intervals = []
  init = 1.01
  more = 0.09
  for x in range(50):
    intervals.append([float(f"{init:.2f}"),float(f"{init+more:.2f}")])
    init += 0.1
  return intervals


def parse_float_list(factor_entries_list):
    # from WebElement to Float class
  for i in range(len(factor_entries_list)):
    factor_entries_list[i] = float(factor_entries_list[i].text)
  return factor_entries_list
"""
def classify_factors(factor_entries_list, between):
  stats = []
  for x in range(52): # 50 for intervaled() + 1 for zeros + 1 for above 6
    stats.append(0)

  for i in range(len(factor_entries_list)):
    #factor_entries_list[i] = float(factor_entries_list[i].text)
    if float(factor_entries_list[i].text) < 1.01:

      FAZER CONDIÇÕES PARA CONTAR OS FATORES E INSERI-LOS EM RESPECTIVOS SLOTS DE 'stats'
"""



def see_list():
  print(f"{factor_entries_list[0]}+{factor_entries_list[1]}={factor_entries_list[0]+factor_entries_list[1]}")
  for factor in range(5):
    print(f"{type(factor_entries_list[factor])} - {factor_entries_list[factor]}")


def get_last_seed(another):
  tds = another.find_elements_by_xpath("//tr/td[2]")
  return tds[len(tds)-1].text


""" AUTOBOT """
def main():
  def close_all():
    driver.quit()
    another.quit()
  driver = open_blaze()
  n_crashes = onload_n_crashes(driver)
  last = get_last_crash_factor(driver)
  last.click()
  print(f"clicked in {last}")
  the_hash = get_the_hash(driver)

  another = open_script()
  paste_hash(another, the_hash)
  digit_ninenine(another, '999')
  factor_entries_list = get_list_factors(another)
  
  #get the last seed of list factors
  last_hash = get_last_seed(another)
  #past_hash again
  WebDriverWait(another, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[1]"))).clear()
  paste_hash(another, last_hash)
  #get a second factor entries list
  second_factor_entries_list = get_list_factors(another)
    #pop first item, because it exist in first list
  second_factor_entries_list.pop(0)
  #count each factor with 'intervaled()' conditions
  between = intervaled()
    #get quantity and percentage

  return {
    "blaze": driver,
    "ini crashes": n_crashes,
    "factor": last,
    "hash": the_hash,
    "another": another,
    "thousand_entries": factor_entries_list,
    "closeall": close_all
  }

init_hash = '492bd10144a3525e2745718fe4d25e08affbea483872d8e8b86191b20ce0a7a8'

def fixedHash(hash):    
  vezes = int(10000000/10000)
  seeds = []

  another = open_script()
  
  for x in range(10):
    if x == 0:
      paste_hash(another, hash)
      digit_ninenine(another, '9999') 
      seeds.extend(get_list_seeds(another))#10000 entries, first + 9999
      last_hash = seeds[len(seeds)-1]
      digit_ninenine(another, '10000')
      """print(f\"\"\"length: {len(seeds)},
        seed[0] == {hash} : {seeds[0].text == hash}
        seed[{len(seeds)-1} == {last_hash} : {seeds[len(seeds)-1].text == last_hash}\"\"\"
      """
    else:
      #past_hash again
      WebDriverWait(another, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[1]"))).clear()
      paste_hash(another, last_hash)
      #get a second list
      next_list = get_list_seeds(another) #10001 entries, first + 10000
      #pop first item, because it exist in main list
      next_list.pop(0) #10000 entries, less first + 10000
      seeds.extend(next_list) # first + 9999 + 10000 = 20000
      last_hash = seeds[len(seeds)-1]
      """print(f"length: {len(seeds)},
      seed[{len(seeds)-1} == {last_hash} : {seeds[len(seeds)-1].text == last_hash}")
      """

  return seeds




# function that listen to new crash rounds... but manually yet
def listening(times = 400):
  last_entry = driver.find_element_by_xpath("//div[@class='entries']/*[1]").text
  n_entries = len(driver.find_elements_by_xpath("//div[@class='entries']/*"))
  cnt = n_entries
  seconds = 0
  for x in range(1, times):
    last_entry = driver.find_element_by_xpath("//div[@class='entries']/*[1]").text
    n_entries = len(driver.find_elements_by_xpath("//div[@class='entries']/*"))
    if n_entries > cnt:
      apostado = driver.find_element_by_xpath("//div[@class='totals']/div[@class='right']/span").text
      print(f"""second: {x} 
        n_entries: {n_entries}
        last_entry: {last_entry}
        total apostado: {apostado}
        seconds: {seconds}""")
      cnt = n_entries
      seconds = 0
    else:
      seconds += 1
    time.sleep(1)






print("all functions loaded")
#main = main()