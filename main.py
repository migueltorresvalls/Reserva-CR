from datetime import datetime
from dateutil.relativedelta import relativedelta

from selenium.webdriver.chrome.options import Options

import time

from driver import Driver

def main(): 
    # Cargo driver de chrome
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")


    driver = Driver(options)
    print("Driver de Chrome lanzado correctamente")

    fecha_ini = datetime.now() + relativedelta(days=1)
    fecha_fin = datetime.now() + relativedelta(days=7)

    horas_buscada = ["10:00", "11:00", "12:00"]
    pista_buscada = "cubierto"
    duracion_buscada = [1, 1.5, 2]

    driver.busca_cr(fecha_ini, fecha_fin, horas_buscada, pista_buscada, duracion_buscada)

    # time.sleep(5)

    driver.close()

if __name__ == "__main__":
    main()