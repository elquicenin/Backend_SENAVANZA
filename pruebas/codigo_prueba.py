from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
# Importaciones para edge
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

VITE_APP_URL = "http://localhost:5173/inicio" # URL del front

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

    def test_react_page_loads_correctly(self):
        """Verifica que el Hero se carga mostrando algún texto esperado."""
        self.selenium.get(VITE_APP_URL)

        try:
            # Busca el párrafo del Hero
            heading = self.selenium.find_element(By.CLASS_NAME, 'texto-ayuda')
            
            # Validar que tenga alguna de las palabras clave
            expected_words = ["SENAVANZA", "¿Necesitas personal?"]
            self.assertTrue(
                any(word in heading.text for word in expected_words),
                f"Texto inesperado en Hero: '{heading.text}'"
            )
            print("Prueba de carga exitosa. Texto válido encontrado.")
        except Exception as e:
            self.fail(f"Fallo: No se encontró el texto esperado. Error: {e}")

