"""Find Token IDs for ens domains"""

import sys
import json
from itertools import combinations_with_replacement

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def concat_and_format(combo):
    as_list = list(combo)
    joined_str = ''.join(as_list)
    return joined_str

OUT_PATH = "./ens_dict_three_lettered.json"

POSSIBLE_CHARS = ['a', 'b', 'c', 'd', 'e', 'f',
                  'g', 'h', 'i', 'j', 'k', 'l', 
                  'm', 'n', 'o', 'p', 'q', 'r',
                  's', 't', 'u', 'v', 'w', 'x',
                  'y', 'z']

ALL_BASE_DOMAINS = combinations_with_replacement(POSSIBLE_CHARS, 3)

ALL_BASE_DOMAINS = list(ALL_BASE_DOMAINS)

ALL_BASE_DOMAINS = [concat_and_format(combo) for combo in ALL_BASE_DOMAINS]

print(len(ALL_BASE_DOMAINS))

out_dict = {}

#Create Driver
driver = webdriver.Chrome()

"""
for index in range(token_index_start, token_index_stop + 1):
    ind_as_str = str(index)

    if len(ind_as_str) < 4:
        padded_zeros_to_add = 4 - len(ind_as_str)
        pad = '0' * padded_zeros_to_add
        ind_as_str = pad + ind_as_str
"""

for base_domain in ALL_BASE_DOMAINS:    

    try:
        #driver.get(f"https://www.ens.vision/{ind_as_str}.eth")
        driver.get(f"https://www.ens.vision/{base_domain}.eth")

        wait = WebDriverWait(driver, 10)
        id_element = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "a.text-accent:nth-child(2)")))

        token_id = id_element.text

        out_dict[base_domain] = token_id

    except:
        out_dict[base_domain] = 'ERROR'

with open(OUT_PATH, 'w') as json_out:
    json.dump(out_dict, json_out)
