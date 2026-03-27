import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# --- DATOS FIJOS DEL USUARIO ---
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

# --- LISTA DE TUTORÍAS PROGRAMADAS (Actualizada con horarios específicos) ---
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
        "materia": "Otro",
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
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento)
    time.sleep(1)
    if texto:
        elemento.clear()
        elemento.send_keys(texto)
    else:
        driver.execute_script("arguments[0].click();", elemento)


def manejar_desplegable_upb(driver, wait, universidad):
    print("Moviendo el mouse hacia 'Elegir'...")
    try:
        dropdown = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[contains(text(), "Elegir")]/ancestor::div[@role="listbox"]')
        ))
        actions = ActionChains(driver)
        actions.move_to_element(dropdown).click().perform()
        time.sleep(4)
        opcion_xpath = '//div[@role="option"]//span[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "pontificia")]'
        opcion_upb = wait.until(EC.visibility_of_element_located((By.XPATH, opcion_xpath)))
        actions.move_to_element(opcion_upb).click().perform()
        print("UPB seleccionada correctamente.")
    except Exception as e:
        print(f"Error en UPB: {e}")


def ejecutar_bot():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    wait = WebDriverWait(driver, 20)

    for cita in TUTORIAS_PARA_ENVIAR:
        try:
            print(f"\n>>> Iniciando proceso para: {cita['dia']} - {cita['materia']}")
            driver.get(
                "https://docs.google.com/forms/d/e/1FAIpQLSfKwNOo_SyvAd2gV0-sLRYZOvK5MgqB_H2hzNfPA5czg6cn0g/viewform")

            # --- PÁGINA 1 ---
            inputs_texto = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//input[@type="text"]')))
            datos_p1 = [DATOS_FIJOS["nombre"], DATOS_FIJOS["documento"], DATOS_FIJOS["correo"], DATOS_FIJOS["celular"]]
            for i, valor in enumerate(datos_p1):
                forzar_interaccion(driver, inputs_texto[i], valor)

            for opt in [DATOS_FIJOS["corte"], DATOS_FIJOS["semestre"]]:
                radio = driver.find_element(By.XPATH, f'//div[contains(@data-value, "{opt}")]')
                forzar_interaccion(driver, radio)

            manejar_desplegable_upb(driver, wait, DATOS_FIJOS["u"])
            tipo_radio = driver.find_element(By.XPATH, f'//div[contains(@data-value, "{DATOS_FIJOS["tipo"]}")]')
            forzar_interaccion(driver, tipo_radio)
            driver.find_element(By.XPATH, '//span[text()="Siguiente"]').click()

            # --- PÁGINA 2: MATERIA Y TEMA ---
            print(f"Seleccionando materia: {cita['materia']}")
            if cita["materia"] == "Otro":
                # Lógica mejorada para Ofimática (Opción 'Otro')
                try:
                    # Buscamos el input que está dentro del div que tiene el texto "Otro"
                    campo_otro = wait.until(EC.element_to_be_clickable(
                        (By.XPATH,
                         '//div[contains(@data-value, "__other_option__")]//input[@type="text"] | //input[@aria-label="Otra respuesta"] | //input[contains(@aria-label, "Otro")]')
                    ))
                    # Usamos click antes de escribir para asegurar que Google Forms active el campo
                    driver.execute_script("arguments[0].click();", campo_otro)
                    time.sleep(1)
                    forzar_interaccion(driver, campo_otro, cita["materia_extra"])
                    print(f"Escrito '{cita['materia_extra']}' en el campo Otro.")
                except Exception as e:
                    print(f"Fallo el selector principal de Otro, intentando por tabulación...")
                    # Plan B: Si no lo encuentra, el campo 'Otro' suele ser el último input de la lista
                    inputs_p2 = driver.find_elements(By.XPATH, '//div[@role="listitem"]//input[@type="text"]')
                    forzar_interaccion(driver, inputs_p2[-1], cita["materia_extra"])
            else:
                materia_opt = wait.until(
                    EC.element_to_be_clickable((By.XPATH, f'//div[contains(@data-value, "{cita["materia"]}")]')))
                forzar_interaccion(driver, materia_opt)

            # --- PÁGINA 3 ---
            textareas = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//textarea')))

            # Escribir el horario literal (ej: el lunes de 8am a 11am)
            forzar_interaccion(driver, textareas[0], cita["horario_completo"])

            # Escribir la observación
            forzar_interaccion(driver, textareas[1], cita["obs"])

            # Botón Enviar
            boton_enviar = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//span[text()="Enviar"] | //div[@role="button"]//span[contains(text(), "Enviar")]')))
            forzar_interaccion(driver, boton_enviar)

            print(f"--- {cita['dia']} ENVIADO CON ÉXITO ---")
            time.sleep(5)

        except Exception as e:
            print(f"Error procesando {cita['dia']}: {e}")
            continue

    print("\n¡Misión cumplida! Todas las tutorías fueron registradas.")
    driver.quit()


if __name__ == "__main__":
    ejecutar_bot()