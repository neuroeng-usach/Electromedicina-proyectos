# Diseño y Desarrollo de un Sensor Portátil de Respuesta Galvánica de la Piel (GSR)
**Basado en ESP32 para el monitoreo de respuestas asociadas a dolor y estrés**

**Proyecto de Electromedicina**
**Autores:** Benjamín Poblete · Javier Rojas · Gustavo Vásquez  
**Profesor:** Cristian Morales Carrasco  
**Institución:** Universidad de Santiago de Chile (USACH)  
**Fecha:** 18/08/2026  

---

## Índice
1. [Problema y objetivos](#1-problema-y-objetivos)
2. [Fundamentos fisiológicos](#2-fundamentos-fisiológicos)
3. [Interpretación de la señal](#3-interpretación-de-la-señal)
4. [Principios de medición](#4-principios-de-medición)
5. [Prototipo e instrumentación](#5-prototipo-e-instrumentación)
6. [Metodología y validación](#6-metodología-y-validación)
7. [Resultados y conclusiones](#7-resultados-y-conclusiones)

---

## 1. Problema y objetivos

### Motivación y Fundamentos para el proyecto
La evaluación del dolor suele depender del autorreporte del paciente. Sin embargo, esto puede ser limitante en personas con dificultades de comunicación o cuando se requiere un monitoreo continuo. 


La actividad electrodérmica (EDA/GSR) permite capturar cambios fisiológicos asociados a la activación autonómica. Destaca por ser una medición no invasiva, de bajo costo y compatible con sistemas portátiles.

### Problema y Propuesta
* **Problema:** Se necesita un sistema simple y portable que cuantifique respuestas fisiológicas asociadas a dolor o estrés.
* **Propuesta:** Desarrollar un prototipo GSR basado en ESP32, con transmisión BLE (Bluetooth Low Energy) y procesamiento de datos en MATLAB.
* **Importante:** El objetivo del sistema no es medir el dolor directamente, sino cuantificar las respuestas electrodérmicas que están asociadas a la activación simpática.

### Planteamiento y Objetivos
**Pregunta de investigación:**  
¿El prototipo de GSR implementado sobre ESP32 con transmisión BLE logra registrar y transmitir con precisión suficiente las variaciones electrodérmicas asociadas a estímulos controlados de dolor o estrés, cumpliendo sensibilidad, estabilidad y latencia?

**Objetivo general:**  
Diseñar, desarrollar y validar un prototipo portátil basado en ESP32 capaz de registrar variaciones de conductancia electrodérmica y transmitir los datos en tiempo real mediante Bluetooth Low Energy.

**Objetivos específicos:**
1. Diseñar el circuito de acondicionamiento de señal bajo medición exosomática DC.
2. Implementar adquisición y transmisión inalámbrica usando ESP32 y BLE.
3. Desarrollar en MATLAB el filtrado, la visualización y la detección de eventos SCR.

---

## 2. Fundamentos fisiológicos

### Concepto de GSR / EDA
* **GSR** significa *Galvanic Skin Response* (respuesta galvánica de la piel). 
* **EDA** (*Electrodermal Activity*) es el término más amplio y actualmente preferido.

Este fenómeno describe los cambios en las propiedades eléctricas de la piel, los cuales están dominados por la actividad de las glándulas sudoríparas ecrinas, producto de la actividad del sistema nervioso autónomo. La magnitud más utilizada en instrumentación para este propósito es la conductancia cutánea (*Skin Conductance*, SC).

**Cadena de respuesta autónoma al estímulo:**
1. Actividad del sistema simpático.
2. Activación sudomotora y secreción de sudor.
3. Cambio en la resistencia / conductancia.
4. Generación de una señal eléctrica medible.

### Cadena Neurofisiológica
La señal empieza con la evaluación central del estímulo y termina en una respuesta periférica observable en la piel. El flujo neurofisiológico es el siguiente:
**Estímulo → Integración central → Salida simpática → Fibra sudomotora → Glándula ecrina → Piel.**

Participan estructuras cerebrales complejas como la amígdala, el hipotálamo, la corteza cingulada, la corteza prefrontal y la formación reticular. Estas estructuras modulan la salida autonómica; sin embargo, es importante destacar que no generan la conductancia directamente, sino que lo hace el sistema simpático a través de las fibras sudomotoras y las glándulas ecrinas.

![imagen](./figura%201.png)
*Figura 1. Cuadro explicativo de funcionamiento fisiológico de la sudoración - Sudoración a señal eléctrica.*

### Transducción Fisiológica
* El estrato córneo actúa como una barrera de alta resistencia.
* Los conductos sudoríparos contienen una solución iónica y atraviesan dicha barrera.
* Al aumentar la sudoración microscópica, se crean trayectos de conducción eléctrica más favorables.
* Un modelo intuitivo es pensar en múltiples resistencias variables conectadas en paralelo: **Conductos sudoríparos más llenos → Menor resistencia equivalente → Mayor conductancia total → Señal medible por un circuito.**

---

## 3. Interpretación de la señal

### ¿Qué medimos realmente?
Es importante recalcar que el prototipo no mide el dolor directamente, sino que mide una consecuencia periférica de la activación autonómica simpática.

**Variables eléctricas:**
* Resistencia cutánea: `R = V / I`
* Conductancia cutánea: `G = 1 / R` (suele expresarse en micro-Siemens, μS).

Este modelo permite cuantificar el *arousal* fisiológico, detectar cambios respecto a una línea base y complementar el contexto experimental junto con el autorreporte del paciente.  
La relación directa es: **mayor activación simpática → mayor sudoración → mayor conductancia → señal GSR más alta.** Por eso, un estímulo sorpresivo, emocional o doloroso puede producir respuestas electrodérmicas elevadas.

### Componentes de la señal: SCL y SCR
* **SCL (Skin Conductance Level):** Es el componente tónico o lento. Representa la línea base de conductancia. Depende del estado autonómico general, la hidratación, la temperatura y las condiciones individuales. Por ello, un valor absoluto de SCL no constituye un nivel universal de estrés. Se debe establecer una línea base individual y analizar cambios relativos respecto de dicha condición.
* **SCR (Skin Conductance Response):** Es el componente fásico o transitorio asociado a un evento. En este componente interesan la amplitud, la latencia, el tiempo de subida y el tiempo de recuperación.

![imagen](./figura%202.png)

*Figura 2. Comparación señal SCL (base) y SCR (respuesta a estímulo).*

---

## 4. Principios de medición

Existen dos métodos principales de medición:
1. **Endosomático:** Se registran diferencias de potencial originadas en la propia piel, sin aplicar una fuente externa. Es conceptualmente más parecido a registrar un potencial biológico.
2. **Exosomático:** Se aplica una pequeña excitación externa y se mide la respuesta del tejido. No mide un potencial eléctrico como un ECG; convierte la resistencia de la piel en una variable adquirible.

**Método propuesto para el proyecto:** Medición exosomática DC con electrodos Ag/AgCl.

---

## 5. Prototipo e instrumentación

### Principio electrónico de medición (Divisor de Voltaje)
* Se aplica un voltaje pequeño y constante (dictado por los 3,3 V de alimentación del ESP32).
* La resistencia de referencia `Rref` forma un divisor de tensión con la resistencia equivalente de la piel `Rskin`.
* El voltaje de salida `Vout` depende del valor instantáneo de `Rskin`.
* A partir de `Vout` se estima `Rskin` y posteriormente `Gskin`.
* Con este diseño (Vexc conectado a Rref y luego a Rskin hacia tierra), si `Rskin` disminuye, `Vout` también disminuye.

### Electrodos, acondicionamiento y digitalización
* **Electrodos Ag/AgCl:** Permiten la interfaz electrodo–piel con buena estabilidad. Son comunes en bioinstrumentación por su disponibilidad y comportamiento electroquímico. Se ubicarán en el dedo índice y medio de la mano no dominante.
* **Buffer / Amplificación:** Un buffer desacopla el nodo del divisor para las etapas posteriores. Si se usa una etapa no inversora, la ganancia ideal debe calcularse cuidadosamente. No conviene amplificar indiscriminadamente toda la componente DC porque puede saturar la etapa analógica.
* **ADC del ESP32:** Convierte el voltaje acondicionado en códigos digitales. Nominalmente opera con 12 bits, pero la relación código–voltaje debe calibrarse experimentalmente. Esa señal digital es la que alimenta el procesamiento y la transmisión BLE.

### Arquitectura general del sistema
1. **Captación:** Electrodos Ag/AgCl (Contacto piel–electrodo, reducción de artefactos).
2. **Acondicionamiento:** Divisor + Buffer (Conversión R a V, adaptación al ADC).
3. **Microcontrolador:** ESP32 y ADC (Muestreo, digitalización, empaquetado).
4. **Transmisión:** BLE (Baja potencia, tiempo real).
5. **Recepción y Análisis:** MATLAB (Recepción, filtrado, extracción de SCR y métricas).

![imagen](./figura%203.png)
*Figura 3: Comparación señal SCL y SCR en respuesta a estímulo [1].*


---
### Materiales a utilizar

A continuación, se detalla el listado de componentes de hardware empleados para la construcción del circuito de acondicionamiento y adquisición de la señal:

| Ítem | Componente | Cantidad | Función en el sistema |
| :--- | :--- | :---: | :--- |
| **1. Microcontrolador** | Placa de desarrollo ESP32 | 1 | Conversión analógica-digital (ADC), procesamiento inicial y transmisión inalámbrica de datos vía BLE. |
| **2. Interfaz Sensorial** | Electrodos de Ag/AgCl | 2 | Contacto directo con la piel (dedos índice y medio) para captar la variación de la resistencia cutánea. |
| **3. Acondicionamiento** | Amplificador Operacional TL072| 1 | Configurado como Buffer (seguidor de tensión) para desacoplar el circuito divisor del ADC del ESP32. |
| **4. Componentes Pasivos**| Resistencias fijas | Varios | Conformar el divisor de voltaje (estableciendo la resistencia de referencia $R_{ref}$). |
| **5. Soporte de Circuito** | Protoboard / Placa perforada | 1 | Ensamblaje e interconexión de la etapa analógica y digital del prototipo. |
| **6. Conectividad** | Cables Jumpers (M-M, M-H) | Varios | Enlace entre los electrodos, el circuito de acondicionamiento y los pines del microcontrolador. |
| **7. Alimentación** | Cable USB / Batería externa | 1 | Energizar el ESP32 y proporcionar el voltaje de excitación continuo ($V_{exc}$) para la medición exosomática. |
## 6. Metodología y validación

### Estrategia general de validación en 7 etapas:
1. **Validación eléctrica:** Uso de resistencias conocidas para verificar ecuaciones, rango y exactitud.
2. **Validación BLE:** Comprobar pérdida de paquetes, orden y latencia.
3. **Preparación del sujeto:** Ubicación de electrodos, estabilización y control de artefactos.
4. **Línea base:** Registro en reposo para estimar SCL, deriva y ruido.
5. **Estímulos controlados:** Eventos con marca temporal (eventos SCR) y tiempo de recuperación.
6. **Procesamiento:** Extracción de SCL, SCR y métricas por evento.
7. **Análisis final:** Comparación reposo vs. post-estímulo y evaluación de factibilidad.

### Detalle Metodológico I: Validación Instrumental (Etapas 1 y 2)
* **Etapa 1 (Eléctrica sin sujeto):** La piel se reemplaza por resistencias conocidas alrededor del rango de diseño. Para cada resistencia se mide Vout con multímetro y el código del ADC. Se calcula el error relativo y el RMSE. Esto valida el divisor, la orientación del circuito, el rango del amplificador y la calibración del ADC. El Error relativo y RMSE permiten cuantificar qué tan bien el sistema estima Rskin.
* **Etapa 2 (Conexión inalámbrica BLE):** Se transmite una secuencia conocida durante varios minutos. Se verifica la continuidad temporal, cantidad de muestras recibidas y el orden correcto. Se calculan la pérdida de paquetes y la latencia. 

*Solo después de validar la instrumentación tiene sentido interpretar la respuesta fisiológica.*

### Detalle Metodológico II: Protocolo con sujetos (Etapas 3 a 7)
* **Preparación:** Electrodos en los dedos índice y medio de la mano no dominante. Periodo de estabilización inicial. Se debe minimizar el movimiento y las variaciones de presión.
* **Línea base (≈ 60 s) y Estímulo:** Se registra reposo para estimar la SCL. Luego se aplican estímulos seguros y controlados con marca temporal. Debe existir un tiempo de recuperación adecuado entre eventos.
* **Análisis:** La comparación principal es el estado de reposo vs. post-estímulo. Se extraen la amplitud SCR, latencia y el cambio relativo. La relación temporal evento–respuesta es fundamental.

### Procesamiento y análisis en MATLAB
**Pipeline del sistema:**
Señal cruda → Calibración (ADC a Vout) → Conversión a Rskin y Gskin → Filtrado y separación SCL-SCR → Métricas.

* **Variables almacenadas:** Código ADC, Voltaje calibrado, Rskin y Gskin estimadas, Marcadores de estímulo.
* **Procesamientos a realizar:** Conservación de la componente tónica (SCL), Extracción de la componente fásica (SCR), Reducción de ruido y corrección de deriva.
* **Valores obtenidos:** Amplitud SCR, Latencia, Tiempo de subida, Cambio relativo, Media, Desviación estándar y RMS.

---

## 7. Resultados y conclusiones

### Resultados esperados e Hipótesis Experimental
* La hipótesis indica que ante un estímulo efectivo, habrá un *arousal* simpático donde la resistencia de la piel bajará (`Rskin ↓`) y la conductancia subirá (`Gskin ↑`), generando un evento SCR detectable.
* En reposo se espera una línea base relativamente estable con fluctuaciones espontáneas de baja magnitud.
* Ante estímulos efectivos se esperan respuestas SCR cuantificables sobre la línea base.
* Se espera que BLE entregue los datos de manera estable y que MATLAB permita visualizar y cuantificar esa respuesta.
* El resultado final esperado es demostrar la factibilidad técnica del prototipo para monitorear respuestas asociadas a dolor y estrés.

### Discusión y limitaciones
* La GSR no es específica de dolor: también responde a la emoción, sorpresa, atención o esfuerzo mental.
* Existe una variabilidad interindividual importante; por eso deben privilegiarse los cambios intra-sujeto respecto a su propia línea base.
* La señal puede contaminarse fácilmente por artefactos de movimiento, presión sobre el electrodo, variaciones de temperatura y sudoración basal.
* La repetición excesiva de estímulos puede producir habituación y reducir la amplitud de la respuesta.

### Conclusiones
* La GSR/EDA es una señal periférica útil para cuantificar cambios de activación autonómica simpática.
* Su origen fisiológico proviene de la integración central, la salida sudomotora, las glándulas ecrinas y el cambio de conductancia cutánea.
* El proyecto implementa una cadena instrumental completa que incluye: electrodos, divisor, acondicionamiento, ADC, ESP32, transmisión BLE y procesamiento en MATLAB.
* El aporte principal del prototipo es demostrar que una solución portable y de bajo costo puede monitorear de forma efectiva las respuestas asociadas al dolor y estrés.

---

### Referencias
1. G. R. Lestari and T. Abuzairi, “Design of Portable Galvanic Skin Response Sensor for Pain Sensor,” ICoSTA, 2020.
2. P. Das et al., “Design and Development of Portable Galvanic Skin Response Acquisition and Analysis System,” ICICPI, 2016.
3. A. N. Phadke, K. Harasheh and S. Gill, “Wearable IoT-Enabled GSR Device for Objective Pain and Stress Monitoring,” Sensors, 2026.
4. N. Pop-Jordanova and J. Pop-Jordanov, “Electrodermal Activity and Stress Assessment,” Prilozi, 2020.
5. R. Markiewicz et al., “Galvanic Skin Response Features in Psychiatry and Mental Disorders,” IJERPH, 2022.
6. H. Y. Y. Aldosky and D. S. Bari, “Electrodermal Activity: Simultaneous Recordings,” IntechOpen, 2019.
7. B. Vittrant, H. Ayoub and P. Brunswick, “From Sudoscan to Bedside...”, Front. Neuroanat., 2024.
8. Y. Nagai et al., “GSR / Electrodermal Biofeedback on Epilepsy,” Front. Neurol., 2019.
9. D. S. Bari et al., “Electrodermal Activity Responses for Quantitative Assessment of Felt Pain,” J. Electr. Bioimpedance, 2018.
10. D. S. Bari, “Electrodermal Activity Responses as Predictor...”, Adv. Biomed. Res., 2026.
11. J. C. Pazos-Alfonso et al., “Galvanic Skin Response Biofeedback in Child Neuropsychology...”, 2025.
```eof