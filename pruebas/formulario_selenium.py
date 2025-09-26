from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select # Necesario para manejar los tags <select>
import time

# ⚠️ Asegúrate de que esta URL sea la correcta para tu frontend Vite
VITE_APP_URL = "http://localhost:5173/" 

class E2E_DiagnosticoEmpresarialTest(LiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Nota: Has cambiado a la ruta directa. Asegúrate de que esta ruta sea 100% correcta.
        DRIVER_PATH = r"C:\Users\JuanVanegas\Documents\JuanFelipe\SENA2025\SENAVANZA\edgedriver_win32\msedgedriver.exe"
        service = EdgeService(DRIVER_PATH)
        
        # Eliminamos el modo headless para que puedas ver lo que hace la prueba
        options = webdriver.EdgeOptions()
        # options.add_argument("--headless") # Descomentar para modo invisible
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        cls.selenium = webdriver.Edge(service=service, options=options)
        # Usamos 15 segundos como tiempo máximo de espera
        cls.wait = WebDriverWait(cls.selenium, 15) 

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_diagnostico_empresarial(self):
        """
        Simula el inicio de sesión de una empresa, accede al formulario 
        de diagnóstico, lo llena, lo envía y navega a los resultados.
        """

        # --- 1. LOGIN DE EMPRESA ---
        self.selenium.get(VITE_APP_URL + "login")
        
        # Asumiendo que el login es igual, pero con credenciales de empresa
        username = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Nombre de usuario']"))
        )
        password = self.selenium.find_element(By.ID, "passwordType")
        login_btn = self.selenium.find_element(By.CLASS_NAME, "iniciar-sesion")
        
        # AJUSTA las credenciales a una cuenta de tipo 'empresa'
        username.send_keys("Pipe") 
        password.send_keys("hola1")
        login_btn.click()

        # Esperar a que llegue al home de la empresa (o ruta de destino)
        self.wait.until(EC.url_contains("/home"))
        print("Login de Empresa correcto")
        
        # --- 2. NAVEGAR AL DIAGNÓSTICO ---
        # Navegamos directamente a la URL de diagnóstico
        self.selenium.get(VITE_APP_URL + "diagnostico-empresarial")
        
        # Esperar a que la URL se cargue
        self.wait.until(EC.url_contains("/diagnostico-empresarial"))
        
        # --- 3. ABRIR EL POPUP DE DIAGNÓSTICO ---
        print("Buscando botón de Diagnóstico...")
        diagnostico_button = self.wait.until(
            # Buscamos el botón por su clase o por el texto que contiene
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'diagnostico-button')]"))
        )
        diagnostico_button.click()
        print(" Botón de Diagnóstico pulsado, esperando popup...")
        
        # --- 4. LLENAR EL POPUP DE DIAGNÓSTICO (Popup_Diagnostico) ---
        
        # Esperar a que el POPUP aparezca. Buscamos el título o el overlay.
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "popup2"))
        )
        print("Popup de Diagnóstico visible.")

        # --- Selección de nivel (Primer <select>) ---
        # Buscamos el <select> y usamos la clase Select de Selenium
        select_nivel = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//select[contains(@class, 'input-box-select')]"))
        )
        Select(select_nivel).select_by_value("tecnologo")
        
        # --- Campo Tareas (Descripción) ---
        # Buscamos por placeholder
        input_descripcion = self.selenium.find_element(
            By.XPATH, "//input[@placeholder='¿Cuáles serían las tareas que le va a delegar al aprendiz en su empresa?']"
        )
        input_descripcion.send_keys("Desarrollo de nuevas funcionalidades en la plataforma de React y gestión de APIs.")
        
        # --- Campo Herramientas ---
        # Buscamos por placeholder
        input_herramientas = self.selenium.find_element(
            By.XPATH, "//input[@placeholder='¿Cuáles son las herramientas que el aprendiz debe utilizar en el cargo?']"
        )
        input_herramientas.send_keys("React, Node.js, PostgreSQL, Docker y Git.")

        # --- Campo Habilidades ---
        # Buscamos por placeholder
        input_habilidades = self.selenium.find_element(
            By.XPATH, "//input[@placeholder='¿Qué conocimientos básicos debería tener el aprendiz que va a ocupar el cargo?']"
        )
        input_habilidades.send_keys("Conocimiento en JavaScript, HTML, CSS y bases de datos relacionales.")

        # --- 5. ENVIAR EL FORMULARIO DE DIAGNÓSTICO ---
        enviar_btn = self.selenium.find_element(By.CLASS_NAME, "submit-btn")
        enviar_btn.click()
        print("Diagnóstico enviado.")

        # --- 6. ESPERAR POPUP DE ÉXITO Y NAVEGAR A RESULTADOS ---
        
       
        # Esperar a que aparezca el Popup de Éxito (popup1)
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "popup1"))
        )
        print("Popup de Éxito visible.")

        # Botón 'Resultados' dentro del Popup de Éxito
        # Importante: Buscamos este elemento AHORA
        resultados_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'resultados')]"))
        )
        
        # Clic en Resultados (ocurre la navegación/re-renderización)
        resultados_btn.click()
        print("Botón 'Resultados' pulsado.")
        # 1. Esperar que la URL de resultados se haya cargado completamente
        self.wait.until(EC.url_contains("/resultado-diagnostico"))
        
        # 2. Volver a buscar el elemento DENTRO de la nueva página.
        print("Buscando el título de la nueva página de resultados...")
        
        #  CORRECCIÓN del XPath: Buscamos solo por la primera parte del texto sin el salto de línea (\n)
        resultado_title = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Conoce el programa de formación')]"))
        )
        
        # 3. Normalizar el texto y realizar la aserción
        texto_esperado = "Conoce el programa de formación más recomendado para ti"
        # Esto elimina el '\n' que genera el <br /> en el código React
        texto_normalizado = resultado_title.text.replace('\n', ' ') 
        
        # Usamos assertEqual para una verificación estricta del texto limpio
        self.assertEqual(texto_esperado, texto_normalizado) 
        print("Prueba E2E 'Diagnóstico Empresarial' completada con éxito.")

# python manage.py test pruebas.formulario_selenium --keepdb