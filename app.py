
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def configurar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def buscar_producto(sku):
    st.write("🔧 Starting Selenium WebDriver...")
    try:
        driver = configurar_driver()
        st.write("✅ WebDriver initialized.")
    except Exception as e:
        st.error("❌ Selenium WebDriver initialization failed.")
        st.text(str(e))
        st.stop()

    try:
        url = f"https://www.homedepot.com.mx/search/?q={sku}"
        st.write(f"🌐 Opening URL: {url}")
        driver.get(url)
        time.sleep(3)
        resultados = driver.find_elements(By.CLASS_NAME, "product")
        productos = []
        for r in resultados:
            try:
                nombre = r.find_element(By.CLASS_NAME, "product-title").text
                precio = r.find_element(By.CLASS_NAME, "product-price").text
                productos.append((nombre, precio))
            except Exception:
                continue
        driver.quit()
        return productos
    except Exception as e:
        st.error("❌ Error while scraping Home Depot.")
        st.text(str(e))
        driver.quit()
        return None

try:
    st.title("🔎 Buscador de Productos - Home Depot México")

    sku = st.text_input("Introduce el SKU o nombre del producto")

    if st.button("Buscar"):
        if sku.strip() == "":
            st.warning("Por favor, introduce un SKU válido.")
        else:
            resultados = buscar_producto(sku)
            if resultados:
                st.success("✅ Resultados encontrados:")
                for nombre, precio in resultados:
                    st.write(f"**{nombre}** - {precio}")
            else:
                st.info("No se encontraron productos.")
except Exception as e:
    st.error("💥 Se produjo un error inesperado:")
    st.text(str(e))
