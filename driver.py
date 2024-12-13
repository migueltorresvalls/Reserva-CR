from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

import time

import numpy as np

from datetime import datetime
from dateutil.relativedelta import relativedelta

import re

class Driver: 
    def __init__(self, options=Options()):
        self.driver = webdriver.Chrome(options=options)

    def busca_cr(self, fecha_ini, fecha_fin, hora_buscada, pista_buscada, duracion_buscada):        
        # Construyo URL
        url = f"https://playtomic.io/ciudad-de-la-raqueta/da78dd3c-43b3-11e8-8674-52540049669c?q=TENNIS~{fecha_ini.year}-{fecha_ini.month}-{fecha_ini.day}~~~"
        self.driver.get(url)
        self.driver.maximize_window()

        self.driver.implicitly_wait(5)
        nombre_pistas = self.driver.find_elements(by=By.XPATH, value="//div[@class='bbq2__resource__label']")

        filas_slots = self.driver.find_elements(by=By.XPATH, value="//div[@class='bbq2__slots-resource']")
        for i in range(len(filas_slots)): 
            # print(f"======\nCompruebo slots de la pista {nombre_pistas[i].text}")

            slots = filas_slots[i].find_elements(by=By.XPATH, value=".//div[@class='bbq2__slot']/div")
            # print(f"He encontrado {len(slots)} slots vacíos")

            for j in slots: 
                self.driver.implicitly_wait(5)
                self.driver.execute_script("arguments[0].click();", j)

                hora = self.driver.find_element(by=By.CLASS_NAME, value="bbq2__duration-picker__time").text

                duraciones_block = self.driver.find_elements(by=By.CLASS_NAME, value="bbq2__duration-picker__option")
                duraciones_posibles = []
                for duracion in duraciones_block:
                    hora_formateada = duracion.find_element(by=By.XPATH, value=".//div").text
                    duraciones_posibles.append(self.obtener_duracion(hora_formateada))
                    
                # print(f"He encontrado hueco en la pista {nombre_pistas[i].text} a las {hora} con duraciones posibles de {duraciones_posibles}")

                modalidad = "descubierto" if "(descubierto)" in nombre_pistas[i].text.lower() else "cubierto"
                if modalidad == pista_buscada.lower() and hora == hora_buscada and duracion_buscada in duraciones_posibles: 
                    dia_semana = self.obtener_dia_semana(fecha_ini.weekday())
                    print(f"La hora más cercana a tu modalidad de pista es el {dia_semana} {fecha_ini.day}/{fecha_ini.month}/{fecha_ini.year} a las {hora} en la pista {nombre_pistas[i].text}. Las duraciones posibles son de {duraciones_posibles} horas")

                    return 0

                # Cierro slot
                btn_cerrar = self.driver.find_element(by=By.CLASS_NAME, value="bbq2__duration-picker__close")
                self.driver.execute_script("arguments[0].click();", btn_cerrar)
        
        if fecha_ini + relativedelta(days=1) < fecha_fin: 
            self.busca_cr(fecha_ini + relativedelta(days=1), fecha_fin, hora_buscada, pista_buscada, duracion_buscada)
        return 1

    def obtener_dia_semana(self, codigo):
        dias_semana = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]

        return dias_semana[codigo]

    def obtener_duracion(self, texto):
        # Buscar el patrón de horas y minutos
        patron = r"(\d+)\s*h\s*(\d+)?\s*min"
        match = re.search(patron, texto)
        
        horas = int(match.group(1))  
        minutos = int(match.group(2)) if match.group(2) else 0  
        duracion = horas + minutos / 60
        
        return duracion

    def obtener_precio(self, texto):
        patron = r"(\d+,\d+)"
        match = re.search(patron, texto)
        precio = float(match.group(1).replace(',', '.'))

        return precio
     
    def close(self):
        self.driver.quit()
