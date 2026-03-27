import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# ==========================================
# CONFIGURACIÓN DE DATOS DEL ESTUDIANTE
# ==========================================
DATOS_FIJOS = {
    "nombre": "Daniel Montiel",
    "documento": "1032249398",
    "correo": "daniel.montielm@upb.edu.co",
    "celular": "3242986755",
    "corte": "2025",
    "semestre": "3",
    "u": "Universidad Pontificia Bolivariana (UPB)",
    "tipo": "Tutoría individual"
}

# ==========================================
# CALENDARIO DE TUTORÍAS A PROGRAMAR
# ==========================================
# Cada diccionario representa una solicitud de formulario completa
TUTORIAS_PARA_ENVIAR = [
    {
        "dia": "Lunes",
        "materia": "Programación orientada a objetos",
        "tema": "Polimorfismo e interfaces",
        "horario_completo": "el lunes de 8am a 11am",
        "obs": "No"
    },
    {
        "dia": "Martes",
        "materia": "Álgebra lineal",
        "tema": "Multiplicación por bloque y una introducción a determinantes",
        "horario_completo": "el martes de 8am a 11am",
        "obs": "Si por favor las tutorías de álgebra lineal me las pueden agendar con el tutor daniel patiño"
    },
    {
        "dia": "Miércoles",
        "materia": "Otro",  # Activa lógica de campo de texto extra
        "materia_extra": "Ofimática",
        "tema": "Macros",
        "horario_completo": "el miércoles de 8am a 11am",
        "obs": "No"
    },
    {
        "dia": "Jueves",
        "materia": "Álgebra lineal",
        "tema": "Inversa de multiplicación por bloques y determinantes de una matriz",
        "horario_completo": "el jueves de 8am a 11am",
        "obs": "Si por favor las tutorías de álgebra lineal me las pueden agendar con el tutor daniel patiño"
    },
    {
        "dia": "Domingo 5 de Abril",
        "materia": "Álgebra lineal",
        "tema": "Todo lo que tenga que ver con determinante de una matriz",
        "horario_completo": "el domingo 5 de abril de 8am a 11am",
        "obs": "Si por favor las tutorías de álgebra lineal me las pueden agendar con el tutor daniel patiño"
    }
]


def forzar_interaccion(driver, elemento, texto=None):
    """
    Asegura la interacción con un elemento desplazándolo a la vista.
    Si recibe 'texto', escribe en el campo; si no, hace clic.
    """
    # Scroll suave hasta el elemento para evitar que otros objetos lo tapen
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento)
    time.sleep(1)
    if texto:
        elemento.clear()
        elemento.send_keys(texto)
    else:
        # Clic mediante JavaScript para evitar errores de 'ElementClickIntercepted'
        driver.execute_script("arguments[0].click();", elemento)


def manejar_desplegable_upb(driver, wait, universidad):
    """
    Lógica compleja para el menú desplegable de Google Forms.
    Usa simulación de mouse (ActionChains) para abrir el menú y seleccionar UPB.
    """
    print("Moviendo el mouse hacia 'Elegir'...")
    try:
        # Localiza el contenedor del listbox de universidades
        dropdown = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[contains(text(), "Elegir")]/ancestor::div[@role="listbox"]')
        ))
        # Simula clic físico del mouse
        actions = ActionChains(driver)
        actions.move_to_element(dropdown).click().perform()
        time.sleep(4)  # Espera a que la lista despliegue las opciones

        # Busca la opción que contenga 'pontificia' ignorando mayúsculas
        opcion_xpath = '//div[@role="option"]//span[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "pontificia")]'
        opcion_upb = wait.until(EC.visibility_of_element_located((By.XPATH, opcion_xpath)))

        # Mueve el mouse a la opción encontrada y hace clic
        actions.move_to_element(opcion_upb).click().perform()
        print("UPB seleccionada correctamente.")
    except Exception as e:
        print(f"Error en UPB: {e}")


def ejecutar_bot():
    """
    Función principal que orquesta el ciclo de envío de todas las tutorías.
    """
    # Inicializa el navegador y el manejador de esperas inteligentes
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    wait = WebDriverWait(driver, 20)

    # Itera sobre cada tutoría en la lista programada
    for cita in TUTORIAS_PARA_ENVIAR:
        try:
            print(f"\n>>> Iniciando proceso para: {cita['dia']} - {cita['materia']}")
            driver.get(
                "https://docs.google.com/forms/d/e/1FAIpQLSfKwNOo_SyvAd2gV0-sLRYZOvK5MgqB_H2hzNfPA5czg6cn0g/viewform")

            # --- PÁGINA 1: DATOS PERSONALES ---
            # Llena Nombre, Documento, Correo y Celular
            inputs_texto = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//input[@type="text"]')))
            datos_p1 = [DATOS_FIJOS["nombre"], DATOS_FIJOS["documento"], DATOS_FIJOS["correo"], DATOS_FIJOS["celular"]]
            for i, valor in enumerate(datos_p1):
                forzar_interaccion(driver, inputs_texto[i], valor)

            # Selecciona radio buttons de Corte y Semestre
            for opt in [DATOS_FIJOS["corte"], DATOS_FIJOS["semestre"]]:
                radio = driver.find_element(By.XPATH, f'//div[contains(@data-value, "{opt}")]')
                forzar_interaccion(driver, radio)

            # Maneja el desplegable de Universidad y el tipo de tutoría
            manejar_desplegable_upb(driver, wait, DATOS_FIJOS["u"])
            tipo_radio = driver.find_element(By.XPATH, f'//div[contains(@data-value, "{DATOS_FIJOS["tipo"]}")]')
            forzar_interaccion(driver, tipo_radio)

            # Navega a la siguiente página
            driver.find_element(By.XPATH, '//span[text()="Siguiente"]').click()

            # --- PÁGINA 2: MATERIA Y TEMA ---
            print(f"Seleccionando materia: {cita['materia']}")
            if cita["materia"] == "Otro":
                # Lógica especial para materias no listadas (ej. Ofimática)
                try:
                    # Intenta localizar el campo de texto de la opción 'Otro'
                    campo_otro = wait.until(EC.element_to_be_clickable(
                        (By.XPATH,
                         '//div[contains(@data-value, "__other_option__")]//input[@type="text"] | //input[@aria-label="Otra respuesta"] | //input[contains(@aria-label, "Otro")]')
                    ))
                    # Activa el campo con un clic y luego escribe
                    driver.execute_script("arguments[0].click();", campo_otro)
                    time.sleep(1)
                    forzar_interaccion(driver, campo_otro, cita["materia_extra"])
                except Exception:
                    # Plan de respaldo: selecciona el último input de texto de la página
                    inputs_p2 = driver.find_elements(By.XPATH, '//div[@role="listitem"]//input[@type="text"]')
                    forzar_interaccion(driver, inputs_p2[-1], cita["materia_extra"])
            else:
                # Selecciona materia normal de la lista
                materia_opt = wait.until(
                    EC.element_to_be_clickable((By.XPATH, f'//div[contains(@data-value, "{cita["materia"]}")]')))
                forzar_interaccion(driver, materia_opt)

            # Llena el tema de la tutoría (textarea único en esta página)
            tema_box = driver.find_element(By.XPATH, '//textarea')
            forzar_interaccion(driver, tema_box, cita["tema"])
            driver.find_element(By.XPATH, '//span[text()="Siguiente"]').click()

            # --- PÁGINA 3: HORARIOS Y CIERRE ---
            # Localiza los dos cuadros de texto grandes (textareas) de la última página
            textareas = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//textarea')))

            # Escribe el horario específico en el primer cuadro [0]
            forzar_interaccion(driver, textareas[0], cita["horario_completo"])

            # Escribe la observación/tutor preferido en el segundo cuadro [1]
            forzar_interaccion(driver, textareas[1], cita["obs"])

            # Localiza y presiona el botón final de Enviar
            boton_enviar = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//span[text()="Enviar"] | //div[@role="button"]//span[contains(text(), "Enviar")]')))
            forzar_interaccion(driver, boton_enviar)

            print(f"--- {cita['dia']} ENVIADO CON ÉXITO ---")
            time.sleep(5)  # Pausa de cortesía entre envíos

        except Exception as e:
            # Si una tutoría falla, informa el error y continúa con la siguiente de la lista
            print(f"Error procesando {cita['dia']}: {e}")
            continue

    print("\n¡Misión cumplida! Todas las tutorías fueron registradas.")
    driver.quit()


if __name__ == "__main__":
    # Punto de entrada del script
    ejecutar_bot()