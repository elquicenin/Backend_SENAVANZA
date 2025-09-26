from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

VITE_APP_URL = "http://localhost:5173/"

class E2E_CrearEmpresaTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        service = EdgeService(r"C:\Users\JuanVanegas\Documents\JuanFelipe\SENA2025\SENAVANZA\edgedriver_win32\msedgedriver.exe")
        options = webdriver.EdgeOptions()
        cls.selenium = webdriver.Edge(service=service, options=options)
        cls.wait = WebDriverWait(cls.selenium, 15)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_crear_empresa(self):
        """Login admin -> Ir a Crear Empresa -> Llenar formulario -> Enviar"""

        # --- LOGIN ---
        self.selenium.get(VITE_APP_URL + "login")

        username = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Nombre de usuario']"))
        )
        password = self.selenium.find_element(By.ID, "passwordType")
        login_btn = self.selenium.find_element(By.CLASS_NAME, "iniciar-sesion")

        username.send_keys("admin")
        password.send_keys("123456789Ju")
        login_btn.click()

        # Esperar a que llegue al adminhome
        self.wait.until(EC.url_contains("/adminhome"))
        print(" Login correcto")

        # --- NAVEGAR AL MENÚ EMPRESAS > CREAR EMPRESA ---
        menu_empresas = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//li[p[text()='Empresas']]"))
        )
        menu_empresas.click()

        crear_empresa_link = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//ul[@class='subMenu']//li[contains(text(),'Crear Empresa')]"))
        )
        crear_empresa_link.click()

        # Confirmar que está en la vista de Crear Empresa
        self.wait.until(EC.url_contains("/crear-empresa"))
        print(" Página Crear Empresa abierta")

        # --- LLENAR FORMULARIO ---
        # Tipo documento
        tipo_doc = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "select")))
        tipo_doc.send_keys("nit")

        # Número documento
        self.selenium.find_element(
            By.XPATH, "//input[@placeholder='Ingrese el número de documento (De 9 dígitos)']"
        ).send_keys("123456789")

        # Rol
        rol_select = self.selenium.find_elements(By.TAG_NAME, "select")[1]
        rol_select.send_keys("empresa")

        # Usuario y contraseña
        self.selenium.find_element(
            By.XPATH, "//input[@placeholder='Ingrese el nombre de usuario (Sin espacioes)']"
        ).send_keys("empresaTest")

        self.selenium.find_element(
            By.XPATH, "//input[@placeholder='Contraseña minimo 8 carácteres']"
        ).send_keys("ClaveSegura1")

        # Razón social
        self.selenium.find_element(
            By.XPATH, "//input[@placeholder='Ingrese la razón social']"
        ).send_keys("Mi Empresa Test")

        # Teléfono
        self.selenium.find_element(
            By.XPATH, "//input[@placeholder='Ingrese el número de teléfono']"
        ).send_keys("3123456789")

        # Correo
        self.selenium.find_element(
            By.XPATH, "//input[@placeholder='Ingrese el correo electrónico']"
        ).send_keys("empresa@test.com")

        # Dirección
        self.selenium.find_element(
            By.XPATH, "//input[@placeholder='Ingrese la dirección actual']"
        ).send_keys("Calle Falsa 123")

        # Actividad económica
        self.selenium.find_element(
            By.XPATH, "//input[@placeholder='Ingrese la actividad Económica']"
        ).send_keys("Tecnología")

        # --- ENVIAR FORMULARIO ---
        crear_btn = self.selenium.find_element(By.CLASS_NAME, "btn-create")
        crear_btn.click()

        # Esperar el toast o la redirección
        time.sleep(3)  # da tiempo a que se procese
        print(" Empresa enviada para creación")

# python manage.py test pruebas.crear_empresa_selenium --keepdb
