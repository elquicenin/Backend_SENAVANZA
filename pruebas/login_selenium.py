from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
# Importaciones para edge
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

VITE_APP_URL = "http://localhost:5173/" # URL del front

class E2E_ReactEdgeTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        try:
            # Configuracion del driver edge
            service = EdgeService(r"C:\Users\JuanVanegas\Documents\JuanFelipe\SENA2025\SENAVANZA\edgedriver_win32\msedgedriver.exe")

            options = webdriver.EdgeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            cls.selenium = webdriver.Edge(service=service, options=options)
            cls.selenium.implicitly_wait(10)
        except Exception as e:
            print (f"No se pudo iniciar {e}")
            raise

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login_successful(self):
        """Verifica que el login redirige a adminhome y carga las palabras clave."""
        self.selenium.get(VITE_APP_URL + "login")

        # --- Paso 1: ingresar credenciales ---
        username_input = self.selenium.find_element(
            By.XPATH, "//input[@placeholder='Nombre de usuario']"
        )
        password_input = self.selenium.find_element(By.ID, "passwordType")

        username_input.send_keys("admin")          # <-- cambia por usuario real
        password_input.send_keys("123456789Ju")    # <-- cambia por contraseña real

        login_button = self.selenium.find_element(By.CLASS_NAME, "iniciar-sesion")
        login_button.click()

        # --- Paso 2: esperar redirección a /adminhome a---
        try:
            WebDriverWait(self.selenium, 10).until(
                EC.url_contains("/adminhome")
            )

            # --- Paso 3: validar palabras clave en adminhome ---
            expected_words = ["Empresas Registradas", "Dashboard", "Listar Usuarios", "Crear Empresas"]

            # Espera hasta que aparezca alguna palabra clave en el body
            WebDriverWait(self.selenium, 10).until(
                lambda driver: any(word in driver.find_element(By.TAG_NAME, "body").text for word in expected_words)
            )

            page_text = self.selenium.find_element(By.TAG_NAME, "body").text
            print("Login exitoso. Texto encontrado:", page_text[:200])  # muestra primeros 200 caracteres

        except Exception as e:
            current_url = self.selenium.current_url
            page_text = self.selenium.find_element(By.TAG_NAME, "body").text
            self.fail(f"Fallo en login: {e}\nURL actual: {current_url}\nTexto en pantalla: {page_text[:200]}")