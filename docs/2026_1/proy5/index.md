# Diseño, Implementación y Validación Preliminar de un Sistema Inalámbrico de Adquisición de Electromiografía de Superficie (SEMG) Basado en ESP32, con Electrodos Pasivos y Módulo Comercial de Acondicionamiento EMG

## Etapa de Validación en Bíceps Braquial — Hacia Aplicaciones TMS-EMG

## 1. Contexto General y Marco Teórico

El monitoreo de biopotenciales (electrocardiografía/ECG, electromiografía/EMG y electroencefalografía/EEG) constituye una herramienta diagnóstica central en electromedicina, permitiendo evaluar la actividad eléctrica cardíaca, muscular y cerebral de forma no invasiva [1]. Los sistemas basados en electrodos pasivos —como el implementado en este proyecto— dependen de un cable entre el electrodo y el amplificador remoto para transportar una señal de alta impedancia (µV a mV), lo que los hace susceptibles a artefactos por movimiento de cable, capacitancias parásitas e interferencia de modo común, particularmente cuando el cable es largo o el sujeto se mueve [1].

El registro de electromiografía de superficie (SEMG) inducida por Estimulación Magnética Transcraneal (TMS) representa una herramienta relevante en neurofisiología clínica e investigación cognitiva para evaluar la excitabilidad corticoespinal y determinar el Umbral Motor (Motor Threshold) [2]. Este procedimiento introduce desafíos de adquisición particularmente exigentes —artefacto de inducción por el pulso magnético y artefactos de movimiento por el espasmo muscular involuntario— que motivaron originalmente explorar un diseño de electrodo activo (con buffer de alta impedancia integrado en el sitio del electrodo) para minimizar la longitud de cable expuesta a interferencia [2]. Dicho enfoque de electrodo activo no se implementó en la versión final del prototipo: por razones de tiempo y complejidad de ensamblaje, se optó por electrodos pasivos convencionales conectados directamente a una placa comercial de acondicionamiento EMG (EGBO), que concentra en un único módulo la amplificación diferencial y el filtrado pasa-banda.

La literatura de electrodos activos —integrando un buffer de alta impedancia directamente en el sitio del electrodo para reducir la sensibilidad a artefactos de movimiento y ruido— se mantiene como referencia y como posible mejora futura del sistema, pero no describe la arquitectura efectivamente construida en esta etapa del proyecto.

Paralelamente, microcontroladores de bajo costo con conectividad inalámbrica integrada como el ESP32 (procesador dual-core, conversores ADC de 12 bits y radios Wi-Fi/Bluetooth) han democratizado el desarrollo de sistemas biomédicos portátiles, permitiendo transmitir de forma inalámbrica la señal ya acondicionada por un módulo externo, como se hizo en este proyecto con la placa EGBO.

El sistema construido busca así demostrar la viabilidad de una cadena de adquisición inalámbrica de bajo costo (electrodo pasivo → placa comercial de acondicionamiento → ESP32 → visualización en tiempo real), como paso previo a evaluar mejoras como la incorporación de un buffer activo en el electrodo o la aplicación en protocolos de TMS-EMG.

## 2. Pregunta de Investigación, Hipótesis y Objetivos

### Pregunta de Investigación

¿En qué medida un sistema inalámbrico basado en ESP32, que integra electrodos pasivos convencionales con un módulo comercial de acondicionamiento EMG, permite registrar señales de SEMG de superficie con una calidad suficiente para su visualización y análisis en tiempo real, como base para futuras mejoras (electrodo activo, aplicación en TMS-EMG)?

### Hipótesis de Trabajo

> "La integración de electrodos pasivos con una placa comercial de acondicionamiento EMG (EGBO) y un nodo inalámbrico ESP32, alimentado mediante una arquitectura de doble fuente (baterías de 9V para la etapa analógica y batería LiPo regulada para la etapa digital), permite registrar y transmitir señales de SEMG de superficie con calidad suficiente para su visualización en tiempo real y la detección de umbrales de activación muscular, sentando una base funcional sobre la cual evaluar en el futuro la incorporación de amplificación activa en el electrodo y la aplicación en protocolos de TMS-EMG."

### Objetivo General

Diseñar, construir y validar un prototipo de sistema inalámbrico de adquisición de SEMG de superficie, de bajo costo, basado en el microcontrolador ESP32, que integre electrodos pasivos con un módulo comercial de acondicionamiento EMG, como etapa previa a evaluar mejoras de diseño (electrodo activo) y aplicaciones en TMS-EMG.

### Objetivos Específicos

1. Integrar electrodos pasivos comerciales con la placa EGBO de acondicionamiento EMG (amplificación diferencial y filtrado pasa-banda 20 Hz–500 Hz), verificando la correcta captación de la señal muscular.
2. Implementar la arquitectura de alimentación del sistema: dos baterías de 9V para la placa EGBO, y una batería LiPo de 3.7V con módulo cargador y regulador elevador (boost) a 5V para el ESP32.
3. Programar el firmware del ESP32 para un muestreo temporizado a 1000 Hz de la salida analógica de la placa EGBO, y desarrollar una interfaz gráfica con despliegue en tiempo real de la señal adquirida.
4. Validar experimentalmente la cadena completa de adquisición registrando SEMG de superficie del bíceps braquial durante contracción voluntaria.

## 3. Arquitectura del Sistema

El sistema efectivamente implementado consta de dos cadenas funcionales —una analógica y una digital— con fuentes de alimentación independientes:

- **Cadena de adquisición analógica:** los electrodos pasivos (broche/gel conductor) se conectan mediante cable directamente a las entradas de la placa comercial EGBO, la cual realiza la amplificación diferencial y el filtrado pasa-banda de la señal muscular. No existe amplificación ni buffer local en el electrodo; toda la etapa analógica de acondicionamiento ocurre en la placa EGBO. Esta placa se alimenta con dos baterías de 9V, en configuración de fuente dual (±9V), típica para los amplificadores operacionales de instrumentación que integra.
- **Cadena digital:** la salida analógica de la placa EGBO se conecta al ADC del ESP32 (GPIO34), que realiza el muestreo, la detección de umbral y la transmisión vía Wi-Fi. El ESP32 se alimenta con una batería LiPo de 3.7V, conectada primero a un módulo cargador (tipo TP4056) que gestiona la carga y protección de la batería, y luego a un regulador de voltaje elevador (boost) que convierte los 3.7V a 5V antes de llegar al pin de alimentación del ESP32.

Al no existir un buffer local en el electrodo, el tramo de cable entre el electrodo pasivo y la placa EGBO transporta una señal de alta impedancia, por lo que el sistema es en principio más sensible a artefactos de movimiento de cable e interferencia electromagnética que un electrodo activo verdadero. Esta característica se documenta como una limitación conocida del diseño actual, coherente con lo discutido en la sección 1, y como una posible línea de mejora futura.

## 4. Presupuesto y Lista de Materiales

Lista de componentes efectivamente utilizados en la construcción del prototipo. Los costos son aproximados, ya que no se registró el precio exacto de cada componente adquirido:

| Componente / Material | Especificación | Función en el Sistema | Costo Aprox. (USD) |
|---|---|---|---|
| Electrodos Pasivos | Broche/botón estándar con gel conductor | Interfaz con la piel del sujeto; conectados directo a la placa EGBO | $0.50 / par |
| Placa EGBO (comercial) | Módulo de acondicionamiento EMG | Amplificación diferencial y filtrado pasa-banda de la señal captada por los electrodos pasivos | ~$20.00 |
| Baterías 9V (x2) | Batería alcalina 9V, conexión dual | Alimentación ±9V de los amplificadores operacionales de la placa EGBO | ~$5.00 |
| Microcontrolador | ESP32 (WROOM/DevKit) | Muestreo ADC de la salida de la placa EGBO, procesamiento y transmisión Bluetooth | $4.00 |
| Batería LiPo | LiPo 1S (3.7V, 150–250 mAh) | Alimentación del ESP32 | $3.50 |
| Módulo Cargador LiPo | Tipo TP4056 o similar | Carga y protección de la batería LiPo 3.7V | $1.00 |
| Regulador de Voltaje (Boost) | Convertidor 3.7V → 5V | Eleva el voltaje de la LiPo al nivel requerido por el ESP32 | $1.00 |
| Cableado | Cable flexible y macho-macho | Interconexión entre módulos | $1.00 |
| Protoboard | De 400 puntos | Interconexión entre ESP32 y EGBO | $2.00 |

**Costo Total Estimado del Hardware: ~$38.00 USD**

## 5. Firmware del Microcontrolador (ESP32)

El firmware del ESP32 en C++ para Arduino IDE a continuación crea un punto de acceso WiFi propio ("EMG_ESP32_Red") y levanta un servidor HTTP (puerto 80) que sirve la página HTML, junto con un servidor WebSocket (puerto 81) que transmite los datos y recibe los comandos de activación/desactivación de filtros desde el navegador. En el loop principal, se muestrea el pin analógico EMG_PIN cada 1000 µs (1000 Hz) y cada muestra pasa por una cadena de procesamiento: primero un filtro de mediana de 3 puntos (despiker) para eliminar picos de interferencia RF del WiFi, luego se centra la señal restando el offset de 2047.5 (punto medio del ADC de 12 bits), y después se aplica en cascada una serie de filtros IIR biquad con coeficientes precalculados para Fs=1000Hz: pasa-altos 20Hz (elimina deriva DC), notch 50Hz (elimina interferencia de red eléctrica), y pasa-bajos 450Hz o 150Hz (anti-aliasing o suavizado, según cuál esté activo). Las muestras filtradas se acumulan en un buffer de 20 valores (BATCH_SIZE) y, una vez lleno, se envían todas juntas como un string separado por comas vía WebSocket para reducir la sobrecarga de transmisión, mientras que los toggles de filtro llegan como texto plano ("HP", "NOTCH", etc.) que invierten el estado booleano correspondiente.


```cpp
#include <WiFi.h>
#include <WebServer.h>
#include <WebSocketsServer.h>

const char* ssid = "EMG_ESP32_Red";
const char* password = "password123";

WebServer server(80);
WebSocketsServer webSocket = WebSocketsServer(81);

const int EMG_PIN = 34;

// --- Muestreo a 1000 Hz ---
unsigned long lastSampleMicros = 0;
const unsigned long sampleIntervalUs = 1000; 

// --- Buffer de transmisión WiFi ---
const int BATCH_SIZE = 20; 
float txBuffer[BATCH_SIZE];
int bufferIndex = 0;

// --- Estados de Filtros ---
bool f_despike_on = true; // Despiker (Anti-picos WiFi)
bool f_hp_on = true;      // Pasa-Altos 20Hz
bool f_notch_on = true;   // Notch 50Hz
bool f_lp450_on = true;   // Pasa-Bajos 450Hz
bool f_lp150_on = false;  // Pasa-Bajos 150Hz

// --- Filtro Despiker (Filtro de Mediana 3) ---
float processDespike(float in) {
  static float m0 = 0, m1 = 0, m2 = 0;
  m2 = m1; m1 = m0; m0 = in;
  float a = m0, b = m1, c = m2;
  if ((a <= b && b <= c) || (c <= b && b <= a)) return b;
  if ((b <= a && a <= c) || (c <= a && a <= b)) return a;
  return c;
}

// --- Estructura para Filtros Biquad (IIR) ---
struct Biquad {
  float b0, b1, b2, a1, a2;
  float x1 = 0, x2 = 0, y1 = 0, y2 = 0;
  
  float process(float in) {
    float out = b0*in + b1*x1 + b2*x2 - a1*y1 - a2*y2;
    x2 = x1; x1 = in;
    y2 = y1; y1 = out;
    return out;
  }
};

// Coeficientes precalculados (Fs = 1000 Hz)
Biquad f_hp    = {0.9113, -1.8227, 0.9113, -1.8227, 0.8372}; // HP 20Hz
Biquad f_notch = {0.9948, -1.8923, 0.9948, -1.8923, 0.9897}; // Notch 50Hz
Biquad f_lp450 = {0.6389,  1.2779, 0.6389,  0.9760, 0.5798}; // LP 450Hz
Biquad f_lp150 = {0.1311,  0.2622, 0.1311, -0.7478, 0.2722}; // LP 150Hz

void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length) {
  if (type == WStype_TEXT) {
    String text = String((char*)payload);
    if (text == "DESPIKE") f_despike_on = !f_despike_on;
    else if (text == "HP") f_hp_on = !f_hp_on;
    else if (text == "NOTCH") f_notch_on = !f_notch_on;
    else if (text == "LP450") f_lp450_on = !f_lp450_on;
    else if (text == "LP150") f_lp150_on = !f_lp150_on;
  }
}

void handleRoot() {
  server.send(200, "text/html", index_html);
}

void setup() {
  Serial.begin(115200);
  pinMode(EMG_PIN, INPUT);

  WiFi.softAP(ssid, password);
  
  server.on("/", handleRoot);
  server.begin();
  
  webSocket.begin();
  webSocket.onEvent(webSocketEvent);
}

void loop() {
  server.handleClient();
  webSocket.loop();

  unsigned long now = micros();
  if (now - lastSampleMicros >= sampleIntervalUs) {
    lastSampleMicros = now;

    float val = analogRead(EMG_PIN);

    // 1. Eliminar picos de RF de la antena WiFi antes de cualquier filtro
    if (f_despike_on) val = processDespike(val);

    // 2. Centrar señal en 0
    val -= 2047.5; 

    // 3. Aplicar Filtros Digitales Cascada
    if (f_hp_on)    val = f_hp.process(val);
    if (f_notch_on) val = f_notch.process(val);
    if (f_lp450_on) val = f_lp450.process(val);
    if (f_lp150_on) val = f_lp150.process(val);

    // 4. Llenar Buffer para transmisión por WiFi
    txBuffer[bufferIndex] = val;
    bufferIndex++;

    if (bufferIndex >= BATCH_SIZE) {
      String payload = "";
      for (int i = 0; i < BATCH_SIZE; i++) {
        payload += String(txBuffer[i], 1);
        if (i < BATCH_SIZE - 1) payload += ",";
      }
      webSocket.broadcastTXT(payload);
      bufferIndex = 0;
    }
  }
}

```

## 6. Software de Visualización y Registro (Python)

El código del software de visualización de la señal a continuación, define una página web (embebida como string en el firmware del ESP32) que sirve como interfaz de monitoreo para señales EMG en tiempo real. La página se conecta mediante WebSocket al puerto 81 del dispositivo para recibir continuamente muestras de voltaje (convertidas de valores ADC crudos a un rango de ±4.5V), las cuales se visualizan en dos gráficos dibujados en canvas: un osciloscopio que muestra los últimos ~0.8 segundos de la señal en el dominio del tiempo, y un espectro FFT (implementado con el algoritmo Cooley-Tukey y ventana de Hanning) que muestra el contenido de frecuencia hasta 500 Hz. La interfaz también incluye botones para activar/desactivar filtros en el firmware (anti-picos WiFi, pasa-altos 20Hz, notch 50Hz, pasa-bajos 450Hz y 150Hz) enviando comandos por WebSocket, y una función de exportación que acumula un buffer de 60,000 muestras (1 minuto a 1000 Hz) y las descarga como archivo CSV con columnas de tiempo y voltaje.

```cpp
const char index_html[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Monitor EMG - Escalas y Exportación</title>
  <style>
    body { font-family: 'Segoe UI', Tahoma, sans-serif; background: #0a0a0a; color: #00ff88; text-align: center; margin: 0; padding: 10px; }
    .container { display: flex; flex-direction: column; align-items: center; gap: 12px; }
    .controls { background: #1a1a1a; padding: 12px; border-radius: 8px; border: 1px solid #333; display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; width: 920px; }
    .btn { background: #2a2a2a; color: #888; border: 1px solid #444; padding: 8px 12px; font-weight: bold; border-radius: 5px; cursor: pointer; transition: 0.2s; }
    .btn.active { background: #00ff88; color: #121212; border-color: #00ff88; box-shadow: 0 0 8px rgba(0,255,136,0.3); }
    .btn-export { background: #ffaa00; color: #121212; border: none; font-size: 14px; margin-left: 15px; }
    .btn-export:hover { background: #ffcc00; }
    canvas { background: #050505; border: 1px solid #333; border-radius: 6px; }
    h3 { margin: 2px 0; color: #ccc; font-size: 15px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="controls">
      <button id="btn_despike" class="btn active" onclick="toggleFilter('DESPIKE')">Anti-Picos WiFi</button>
      <button id="btn_hp" class="btn active" onclick="toggleFilter('HP')">HP 20Hz (DC/Zero)</button>
      <button id="btn_notch" class="btn active" onclick="toggleFilter('NOTCH')">Notch 50Hz (Red)</button>
      <button id="btn_lp450" class="btn active" onclick="toggleFilter('LP450')">LP 450Hz (AntiAlias)</button>
      <button id="btn_lp150" class="btn" onclick="toggleFilter('LP150')">LP 150Hz (Suavizado)</button>
      <button class="btn btn-export" onclick="exportCSV()">📥 Exportar 1 Minuto a Excel</button>
    </div>

    <div>
      <h3>Osciloscopio EMG (Tiempo vs Voltaje)</h3>
      <canvas id="scopeCanvas" width="920" height="320"></canvas>
    </div>

    <div>
      <h3>Espectro FFT 1000Hz (Frecuencia vs Magnitud)</h3>
      <canvas id="fftCanvas" width="920" height="220"></canvas>
    </div>
  </div>

  <script>
    const ws = new WebSocket('ws://' + window.location.hostname + ':81/');
    
    // --- Osciloscopio ---
    const sCanvas = document.getElementById('scopeCanvas');
    const sCtx = sCanvas.getContext('2d');
    const scopeSamples = 800; // ~0.8 segundos en pantalla
    let scopeData = new Array(scopeSamples).fill(0);

    // --- Buffer para 1 Minuto (60,000 muestras a 1000 Hz) ---
    const maxExportSamples = 60000;
    let history60s = [];

    // --- FFT ---
    const fCanvas = document.getElementById('fftCanvas');
    const fCtx = fCanvas.getContext('2d');
    const fftSize = 512;
    let fftBuffer = new Array(fftSize).fill(0);
    const cosTable = new Float32Array(fftSize);
    const sinTable = new Float32Array(fftSize);
    for (let i = 0; i < fftSize; i++) {
        cosTable[i] = Math.cos(-2 * Math.PI * i / fftSize);
        sinTable[i] = Math.sin(-2 * Math.PI * i / fftSize);
    }

    ws.onmessage = function(event) {
      let values = event.data.split(',');
      for (let i = 0; i < values.length; i++) {
        if(values[i] === "") continue;
        let v = parseFloat(values[i]);
        let volts = (v / 2047.5) * 4.5; // Escala ±4.5V

        scopeData.push(volts);
        scopeData.shift();

        fftBuffer.push(volts);
        fftBuffer.shift();

        history60s.push(volts);
        if (history60s.length > maxExportSamples) history60s.shift();
      }
      requestAnimationFrame(drawAll);
    };

    function toggleFilter(type) {
      ws.send(type);
      let btn = document.getElementById('btn_' + type.toLowerCase());
      btn.classList.toggle('active');
    }

    function drawAll() {
      drawScope();
      drawFFT();
    }

    function drawScope() {
      const padL = 55, padR = 20, padT = 20, padB = 35;
      const w = sCanvas.width - padL - padR;
      const h = sCanvas.height - padT - padB;

      sCtx.fillStyle = '#050505';
      sCtx.fillRect(0, 0, sCanvas.width, sCanvas.height);

      // Rejilla y Escala Y (Voltaje)
      sCtx.textAlign = "right";
      sCtx.font = "11px sans-serif";
      const vTicks = [-4.5, -3.0, -1.5, 0.0, 1.5, 3.0, 4.5];
      vTicks.forEach(v => {
        let y = padT + h/2 - (v / 4.5) * (h/2);
        sCtx.strokeStyle = (v === 0) ? '#00aa55' : '#1e1e1e';
        sCtx.beginPath(); sCtx.moveTo(padL, y); sCtx.lineTo(padL + w, y); sCtx.stroke();
        sCtx.fillStyle = (v === 0) ? '#00ff88' : '#777';
        sCtx.fillText((v >= 0 ? "+" : "") + v.toFixed(1) + "V", padL - 8, y + 4);
      });

      // Rejilla y Escala X (Tiempo)
      sCtx.textAlign = "center";
      const tTicks = [-0.8, -0.6, -0.4, -0.2, 0.0];
      tTicks.forEach((t, idx) => {
        let x = padL + (idx / (tTicks.length - 1)) * w;
        sCtx.strokeStyle = '#1e1e1e';
        sCtx.beginPath(); sCtx.moveTo(x, padT); sCtx.lineTo(x, padT + h); sCtx.stroke();
        sCtx.fillStyle = '#777';
        sCtx.fillText(t.toFixed(1) + "s", x, padT + h + 18);
      });

      // Trazo de Señal EMG
      sCtx.save();
      sCtx.rect(padL, padT, w, h);
      sCtx.clip();
      sCtx.beginPath();
      sCtx.strokeStyle = '#00ff88';
      sCtx.lineWidth = 1.5;
      for (let i = 0; i < scopeData.length; i++) {
        let x = padL + (i / scopeSamples) * w;
        let y = padT + h/2 - (scopeData[i] / 4.5) * (h/2);
        if (i === 0) sCtx.moveTo(x, y); else sCtx.lineTo(x, y);
      }
      sCtx.stroke();
      sCtx.restore();
    }

    function drawFFT() {
      const padL = 55, padR = 20, padT = 15, padB = 35;
      const w = fCanvas.width - padL - padR;
      const h = fCanvas.height - padT - padB;

      fCtx.fillStyle = '#050505';
      fCtx.fillRect(0, 0, fCanvas.width, fCanvas.height);

      // Algoritmo FFT Cooley-Tukey
      let real = new Float32Array(fftSize), imag = new Float32Array(fftSize);
      for (let i = 0; i < fftSize; i++) {
        real[i] = fftBuffer[i] * (0.5 * (1 - Math.cos(2 * Math.PI * i / (fftSize - 1))));
      }
      let bits = Math.log2(fftSize);
      for (let i = 0; i < fftSize; i++) {
        let j = 0, x = i;
        for (let b = 0; b < bits; b++) { j = (j << 1) | (x & 1); x >>= 1; }
        if (j > i) { let t = real[i]; real[i] = real[j]; real[j] = t; }
      }
      for (let len = 2; len <= fftSize; len *= 2) {
        let half = len / 2, step = fftSize / len;
        for (let i = 0; i < fftSize; i += len) {
          for (let j = i, k = 0; j < i + half; j++, k += step) {
            let tr = real[j+half]*cosTable[k] - imag[j+half]*sinTable[k];
            let ti = real[j+half]*sinTable[k] + imag[j+half]*cosTable[k];
            real[j+half] = real[j] - tr; imag[j+half] = imag[j] - ti;
            real[j] += tr; imag[j] += ti;
          }
        }
      }

      // Escala X (Frecuencias 0-500 Hz)
      fCtx.textAlign = "center"; fCtx.fillStyle = '#777'; fCtx.font = "11px sans-serif";
      const freqTicks = [0, 100, 200, 300, 400, 500];
      freqTicks.forEach((f, idx) => {
        let x = padL + (idx / (freqTicks.length - 1)) * w;
        fCtx.strokeStyle = '#1e1e1e';
        fCtx.beginPath(); fCtx.moveTo(x, padT); fCtx.lineTo(x, padT + h); fCtx.stroke();
        fCtx.fillText(f + "Hz", x, padT + h + 18);
      });

      // Dibujar barras del espectro
      let bars = fftSize / 2;
      let barW = w / bars;
      fCtx.fillStyle = '#ff00aa';
      for (let i = 0; i < bars; i++) {
        let mag = Math.sqrt(real[i]*real[i] + imag[i]*imag[i]);
        let barH = Math.min((mag * 2.0), h);
        fCtx.fillRect(padL + i * barW, padT + h - barH, barW - 0.5, barH);
      }
    }

    function exportCSV() {
      if (history60s.length === 0) {
        alert("Aún no hay datos para exportar.");
        return;
      }
      let csv = "Tiempo (s),Voltaje (V)\n";
      let dt = 0.001;
      for (let i = 0; i < history60s.length; i++) {
        let t = (i * dt).toFixed(3);
        csv += t + "," + history60s[i].toFixed(4) + "\n";
      }
      let blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      let link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.setAttribute("download", "Medicion_EMG_1Min.csv");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  </script>
</body>
</html>
)rawliteral";
```


## 7. Protocolo de Validación Experimental (Fase Actual)

La validación realizada hasta la fecha corresponde a un ensayo de SEMG de superficie durante contracción voluntaria del bíceps braquial, con el objetivo de verificar la funcionalidad de la cadena de adquisición completa (electrodos pasivos → placa EGBO → ESP32 → visualización → registro). El protocolo comprendió, de forma general:

- Colocación del par de electrodos pasivos sobre el vientre muscular del bíceps braquial, conectados directamente a la placa EGBO, y un electrodo de referencia en una zona ósea cercana.
- Registro de la señal durante contracciones voluntarias (flexión de codo) y períodos de reposo, para observar cualitativamente el contraste entre actividad muscular y línea base.
- Verificación en tiempo real, mediante la interfaz en pyqtgraph, de la correcta transmisión Bluetooth y de la activación del indicador LED de umbral ante contracciones de suficiente amplitud.
- Exportación de 1 minuto de datos en como archivo CSV con columnas de tiempo y voltaje, para un futuro análisis de la señal registrada.

## 8. Conclusiones: Limitaciones y Trabajo Futuro

1. **Hardware:** placa EGBO y ESP32 integrados y funcionando, con arquitectura de alimentación dual (2 baterías de 9V para EGBO; LiPo 3.7V + módulo cargador + regulador boost a 5V para el ESP32).
2. **Electrodos:** pasivos, sin buffer activo local; toda la amplificación ocurre en la placa EGBO. Incorporar un buffer en el sitio del electrodo (electrodo activo propiamente dicho) queda como mejora futura para reducir la sensibilidad a artefactos de movimiento de cable.
3. **Firmware y visualización:** funcionando y verificados durante el ensayo de SEMG en bíceps braquial.
4. **Exportación de datos a Excel:** funcionando, permite la descarga de e minuti de datos.
5. **Validación con TMS y cuantificación de SNR/CMRR:** pendientes, sujetas a disponibilidad de un equipo de TMS y de un sistema de referencia cableado para comparación.

## Referencias Bibliográficas

[1] Chen, S., Chen, Y., Huang, J., Liu, C., & Luo, K. (2025). Open-source low-cost non-contact ECG monitoring system using active dry electrodes. *HardwareX*, 24, Artículo e00718. https://doi.org/10.1016/j.ohx.2025.e00718

[2] Inafuco, A. T. P., Machoski, P., Campos, D. P., Pichorim, S. F., & Mendes Junior, J. J. A. (2025). MOT: A Low-Latency, Multichannel Wireless Surface Electromyography Acquisition System Based on the AD8232 Front-End. *Sensors*, 25(12), 3600. https://doi.org/10.3390/s25123600

[3] Mendes Junior, J. J. A., Campos, D. P., Biassio, L. C. d. A. V. D., Passos, P. C., Júnior, P. B., Lazzaretti, A. E., & Krueger, E. (2023). AD8232 to Biopotentials Sensors: Open Source Project and Benchmark. *Electronics*, 12(4), 833. https://doi.org/10.3390/electronics12040833

[4] Abdul Azim Al-Khadrawi. (2026). Real-Time Electrocardiogram Monitoring System Using Internet of Things Technology and ESP32 Microcontroller for Remote Healthcare Applications. *Razi Medical Journal*. https://doi.org/10.69667/rmj.26204

[5] Joutsen, A., Cömert, A., Kaappa, E., Vanhatalo, K., Riistama, J., Vehkaoja, A., & Eskola, H. (2024). ECG signal quality in intermittent long-term dry electrode recordings with controlled motion artifacts. *Scientific Reports*, 14(1). https://doi.org/10.1038/s41598-024-56595-0

[6] An, X., & K. Stylios, G. (2020). Comparison of Motion Artefact Reduction Methods and the Implementation of Adaptive Motion Artefact Reduction in Wearable Electrocardiogram Monitoring. *Sensors*, 20(5), 1468. https://doi.org/10.3390/s20051468
