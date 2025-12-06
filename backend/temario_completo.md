# Temario Completo de Electronica Digital

> Documento listo para usarse tanto en Markdown como tras convertirlo a HTML. Incluye tablas, pseudo-esquemas ASCII y mini-ejercicios para reforzar cada concepto.

## Indice rapido

1. [Unidad 1 - Sistemas Digitales](#unidad-1---aspectos-generales-de-los-sistemas-digitales)
2. [Unidad 2 - Circuitos Combinacionales](#unidad-2---circuitos-combinacionales)
3. [Unidad 3 - Circuitos Secuenciales](#unidad-3---circuitos-secuenciales)
4. [Unidad 4 - Unidad Aritmetico-Logica](#unidad-4---unidad-aritmetico-logica-alu)

---

## Unidad 1 - Aspectos Generales de los Sistemas Digitales

### Vista general

```
Capas:
 1) Fisica  -> niveles electricos, ruido, tecnologia
 2) Logica  -> algebra de Boole, puertas, simplificacion
 3) Sistema -> modulos combinacionales y secuenciales
 4) Aplic.  -> microcontroladores, SoC, firmware
```

### 1. Introduccion

- Los sistemas digitales usan rangos de tension (0/1) y margenes de ruido para garantizar interpretaciones confiables.
- Ventajas frente a sistemas analogicos:

| Caracteristica  | Analogico                         | Digital                                      |
|-----------------|-----------------------------------|----------------------------------------------|
| Representacion  | Continua                          | Discreta (bits)                              |
| Ruido           | Afecta directamente la seAal      | Absorbido por margenes VIH/VIL               |
| Reconfiguracion | Requiere rehacer hardware         | Firmware o HDL                               |
| Complejidad     | Limitada por componentes pasivos  | Escala con integracion VLSI y SoC            |
| Ejemplos        | Audio, RF                         | Control, IA embebida, comunicaciones digitales|

- Evolucion: relays -> tubos -> TTL -> CMOS -> FPGA/SoC -> aceleradores IA.
- Idea clave: modularidad y abstraccion (describe cada bloque con entradas/salidas bien definidas).

### 2. Informacion Binaria y Sistemas Numericos

- Terminologia basica:
  - Bit, nibble (4 bits), byte (8 bits), palabra (n bits s/arquitectura).
  - MSB (bit mas significativo) y LSB (menos significativo).
- Codigos frecuentes:
  - ASCII / Unicode: texto.
  - BCD: representacion decimal en hardware (4 bits por digito).
  - Gray: solo cambia un bit entre estados consecutivos (sensores, codificadores rotativos).
  - Hamming: deteccion y correccion de errores (7,4) o (15,11).
- Conversiones:

```
Decimal a binario -> dividir entre 2, recoger residuos (de abajo arriba)
Binario a decimal -> sumar 2^posicion donde haya 1
Hex a binario     -> grupos de 4 bits
Octal a binario   -> grupos de 3 bits
```

- Enteros con signo:

| Metodo         | Descripcion                      | Pros                       | Contras                        |
|----------------|----------------------------------|-----------------------------|--------------------------------|
| Signo-magnitud | Bit MSB indica signo             | Intuitivo                  | Dos representaciones de cero  |
| Complemento a 1| Invertir bits para negativo      | Facil de entender          | Aun dos ceros                 |
| Complemento a 2| Invertir + sumar 1               | Unico cero, suma directa   | Rango asimetrico              |
| Exceso-N       | Desplaza rango                   | Facil en hardware binario  | Interpretacion menos intuitiva|

- Fraccionarios punto fijo: formato Qm.n (m bits enteros, n bits fraccion). Escalado = valor entero / 2^n.
- Consideraciones practicas: resolucion (rango/2^n), error por cuantizacion (~0.5 LSB), saturacion y overflow.

#### Mini-lab

1. Convierte 173 decimal a binario, hex y BCD.
2. Representa -37 en complemento a 2 usando 8 bits.
3. Calcula la resolucion de un ADC de 12 bits con rango 0-3.3 V.

### 3. Algebra de Boole y Fundamentos Logicos

- Operaciones basicas y tablas de verdad.
- Leyes importantes: conmutativa, asociativa, distributiva, identidades de neutro y complemento, idempotencia, involucion.
- Teoremas: De Morgan, absorcion, consenso, dualidad, Shannon (particion de funciones).
- Formas SOP/POS para facilitar automatizacion con K-map o herramientas EDA.
- Nota: se introduce logica multi-valuada como curiosidad (ej. logica ternaria balanceada).

#### Ejemplo

```
F(A,B,C) = Sigma m(1,3,5,7)
 -> SOP: F = A'B'C + A'BC + AB'C + ABC
 -> POS: F = (A + B + C)(A + B' + C)(A' + B + C)
```

### 4. Puertas Logicas y Familias Tecnologicas

| Familia | Tension | Velocidad | Consumo | Notas |
|---------|---------|-----------|---------|-------|
| TTL     | 5 V     | Alta      | Medio   | Fan-out limitado, usa resistencias |
| CMOS    | 1.2-5 V | Media/Alta| Bajo    | Muy usada en SoC/FPGAs              |
| BiCMOS  | 3.3-5 V | Muy alta  | Bajo    | Combina transistores bipolares + MOS|

- Puertas universales:

```
NOT A = NAND(A, A)
AND   = inversion doble de NAND
OR    = inversion doble de NOR
```

- Uso de HDL:

```
-- VHDL
Y <= (A and B) or (not C);
```

### 5. Simplificacion de Funciones Booleanas

- Mapas de Karnaugh (2 a 6 variables) para visualizar agrupaciones y detectar hazards.
- Quine-McCluskey: tabular, sistematico; usado en scripts.
- Espresso: heuristico, empleado en sintetizadores.
- Algebra manual: combinacion de identidades para funciones pequenas.

| Objetivo | Tecnica recomendada                        |
|----------|--------------------------------------------|
| Poca variables | K-map                                |
| Muchas variables | Quine-McCluskey + post-procesado   |
| DiseAo industrial | Herramientas CAD (Espresso, ABC)  |

- Hazards: pulso espurio por diferentes caminos. Se corrige con terminos de consenso o registro de salida.

### 6. DiseAo de Circuitos Combinacionales

Pasos sugeridos:

1. Especificacion textual/tabla.
2. Diagrama de entrada-salida.
3. Tabla de verdad o ecuaciones iniciales.
4. Simplificacion.
5. Implementacion en puertas, HDL o dispositivos programables.
6. Verificacion (simulacion, testbench, prototipado).

Casos de estudio:
- Sumador/restador de 4 bits usando XOR en operandos.
- Detector de paridad con red de XOR.
- Controlador BCD -> 7 segmentos usando tabla y K-map.

### 7. Parametros Electricos de las Puertas Logicas

- Niveles: VIH/VIL (entrada), VOH/VOL (salida). Margen de ruido = min(VOH - VIH, VIL - VOL).
- Fan-in/fan-out: cantidad de puertas que puede manejar una salida.
- Retardos: tpHL, tpLH, tiempo de subida/bajada, jitter.
- Potencia: estatica (corrientes de fuga) vs dinamica (C*V^2*f).
- Compatibilidad entre familias: usar buffers, adaptadores de nivel, resistencias pull-up/down para colector abierto.

### 8. Puertas Tri-State y Buses Compartidos

```
Enable = 1 -> salida activa
Enable = 0 -> estado Z (alta impedancia)
```

- Uso: buses de datos, memorias, perifericos, microcontroladores.
- Precauciones: arbitraje para evitar colisiones, resistencias de guardia para evitar flotantes.
- Alternativas: multiplexores dedicados, switches analogicos, buses serie (_SPI, I2C, LVDS_).

---

## Unidad 2 - Circuitos Combinacionales

### Mapa mental + metas rapidas

```
Entradas -> (Selecciones) -> (Traducciones) -> (Comparaciones)
            MUX/DEMUX        Codific/Decod      Aritmetica
                         \--> Control de hazards
```

| Objetivo didactico | Indicador de dominio |
|--------------------|----------------------|
| Identificar funciones basadas solo en entradas actuales | Puede decidir cuando usar combinacional o secuencial |
| Disenar bloques reutilizables (MUX, decod, comparadores) | Presenta tablas de verdad y ecuaciones optimizadas |
| Evaluar impacto temporal | Calcula retardo maximo y fan-out permitido |
| Mitigar hazards | Propone al menos dos estrategias de correccion |

---

### 1. Introduccion

- Los circuitos combinacionales no almacenan memoria: cada salida depende exclusivamente de las entradas vigentes.
- Tres pilares de analisis:
  1. **Retardos de propagacion**: suma de los retardos de cada compuerta a lo largo de las rutas criticas.
  2. **Capacidad/fan-out**: cuanta carga soporta una salida sin deformar el nivel logico.
  3. **Consumo**: potencia estatica (fugas) y dinamica (C*V^2*f) al conmutar.
- Verificacion practica:
  - Simuladores logicos (Logisim, Vivado, ModelSim).
  - Analizador logico para observar patrones.
  - Generador de funciones/arbitros para probar buses.

#### Mini-check

1. Explica en una frase por que un sumador combinacional no puede detectar rebotes de un boton.
2. Determina el retardo total si una ruta pasa por 3 NAND de 8 ns y 1 XOR de 12 ns.

---

### 2. Multiplexores (MUX)

#### Conceptos clave

- Seleccionan un dato entre N entradas usando lineas de seleccion.
- Tamano clasico: 2:1, 4:1, 8:1, 16:1, 32:1. Para aumentar tamano se construyen arboles o cascadas.
- Ecuacion general (para 4:1):

```
Y = D0 * S1' * S0' +
    D1 * S1' * S0  +
    D2 * S1  * S0' +
    D3 * S1  * S0
```

#### Estrategias de uso

- Generadores de funciones: si conectas minterminos en las entradas, el selector define la funcion.
- Seleccion de buses: el MUX actua como puente entre varios modulos y una sola linea compartida.
- Direccionamiento: elegir cual sensor o memoria se conecta al ADC o CPU.
- Multiplexacion temporal (time-sharing) vs espacial (multiples caminos paralelos).

#### Laboratorio sugerido

1. Construye un MUX 4:1 unicamente con compuertas NAND.
2. Simula y mide el retardo desde D2 hasta Y cuando S1=1 y S0=0.

---

### 3. Demultiplexores (DEMUX)

- Inverso del MUX: recibe un dato y lo encamina hacia una de varias salidas.
- Implementacion tipica: decodificador + compuertas AND para habilitar la salida deseada.
- Aplicaciones:
  - Distribuir senales de reloj o sincronizacion.
  - Encender lineas de un display de forma secuencial.
  - Actuar sobre bancos de actuadores/relays con un unico pin de datos.
- Cuida los transitorios al cambiar selectores: usa buffers o staggered enable.

```
Entrada ----> AND ----> Salida0
            /
Select ----+----> AND ----> Salida1
```

---

### 4. Decodificadores

| Tipo | Entradas | Salidas | Caso de uso | CI de referencia |
|------|----------|---------|-------------|------------------|
| 2 a 4| 2        | 4       | Seleccion rapida de perifericos | 74HC139 |
| 3 a 8| 3        | 8       | Direccionamiento basico | 74HC138 |
| 4 a 16| 4       | 16      | Memorias, chips en paralelo | 74HC154 |
| BCD a 7 seg | 4 | 7 (+DP) | Visualizacion numerica | CD4511 |

- Entradas enable permiten desactivar el bloque o conectarlo en cascada.
- Usos creativos: secuencias de activacion, generadores PWM discretos, seleccion de paginas de memoria.

#### Ejercicio guiado

1. Disena un decodificador 2 a 4 con salidas activas en bajo.
2. Agrega una entrada de inhibicion para poder apagarlo desde un microcontrolador.

---

### 5. Codificadores

- Convertir multiples lineas one-hot o sensores en una salida binaria.
- Tipos:
  - Codificador simple.
  - Codificador con prioridad (manejo de interrupciones).
  - Termometro a binario (comparadores en cadena).
  - Lectura de teclado matricial (escaneo de filas/columnas).
- Senales auxiliares: bit de validez V y bandera de error E para detectar situaciones no permitidas.

#### Pseudoflujo (prioridad)

```
if I7=1 -> code=111, V=1
else if I6=1 -> code=110, V=1
...
else -> code=000, V=0 (sin entrada valida)
```

---

### 6. Comparadores Digitales

- Deciden si A > B, A = B o A < B.
- Tecnicas:
  - Cascada de comparadores de 1 bit (propagan banderas mayor/igual/menor).
  - Restador + analisis de carry o borrow.
  - Uso de ALU en modo resta y lectura de flags.
- CI util: 74HC85 (4 bits) con entradas de cascada.
- Aplicaciones: ventanas de tension, PWM por comparacion, saltos condicionales en controladores simples.

#### Mini-desafio

Disena un comparador de 3 bits usando solo compuertas XOR/AND/OR y estima su retardo.

---

### 7. Aritmetica Binaria

#### Sumadores

| Tipo | Ventaja | Consideracion |
|------|---------|---------------|
| Half adder | Bloque elemental | Genera suma y acarreo sin entrada |
| Full adder | Incluye acarreo de entrada | Base de los sumadores n bits |
| Ripple-carry | Diseno simple | Retardo crece lineal con n |
| Carry lookahead | Calcula acarreo anticipado | Mayor area pero rapido |
| Carry select | Duplica sumas y selecciona | Compromiso velocidad/area |
| Carry save | Mantiene sumas parciales separadas | Ideal en multiplicadores |

#### Otros bloques

- Restadores directos o basados en complemento a 2.
- Incrementadores/decrementadores optimizados.
- Detectores de paridad (XOR) y de cero (NOR).
- Multiplicadores combinacionales: arreglos, Wallace, Dadda.

#### Ejercicio

1. Calcula el retardo de un sumador ripple de 4 bits si cada full adder tarda 10 ns.
2. Modifica ese sumador para que reste cuando SUB=1 invirtiendo el segundo operando y sumando 1.

---

### 8. Manejo de Hazard y Glitch

```
Entrada cambia -> rutas con retardo distinto -> pulso espurio en salida
```

- Tipos: estatico, dinamico y funcional.
- Causas: rutas con longitudes diferentes, cambios simultaneos de multiples entradas, gating incompleto.
- Estrategias:
  1. Anadir terminos de consenso a la funcion.
  2. Registrar la salida o sincronizarla con el reloj.
  3. Anadir retardos controlados o filtros RC (casos extremos).
  4. Disenar logica monotona en sistemas asincronos.
- Buenas practicas: documentar ruta critica, usar herramientas de analisis de hazards y validar en hardware real.

---
## Unidad 3 - Circuitos Secuenciales

### Vision global y metas

```
Tiempo -> Eventos -> Estado -> Respuesta
          (sincronizacion y control del reloj)
```

| Objetivo | Indicador |
|----------|-----------|
| Diferenciar asincrono vs sincrono | Puede explicar ventajas/desventajas y dar ejemplos |
| Dominar latches y flip-flops | Construye tablas de excitacion y analiza tiempos |
| Crear pipelines y contadores | Disena registros y contadores modulo-N sin glitches |
| Describir FSM completas | Define estados, codificacion y ecuaciones de salida |

---

### 1. Introduccion y Modelos de Temporizacion

- Circuitos secuenciales dependen de entradas **y** del estado previo (memoria).
- Dos familias principales:
  - **Asincronos**: respuesta inmediata a cambios de entrada, analisis complejo por condiciones de carrera.
  - **Sincronos**: coordinados por un reloj comun, mas previsibles y faciles de sintetizar.
- Elementos clave del analisis temporal:
  1. **Setup**: tiempo antes del flanco donde la entrada debe estar estable.
  2. **Hold**: tiempo despues del flanco durante el cual no se debe cambiar la entrada.
  3. **Clock-to-Q**: retardo desde el flanco hasta que la salida se estabiliza.
  4. **Skew y jitter**: diferencias y variaciones en la llegada del reloj a cada punto.
- Representaciones: tablas de transicion, diagramas ASM, grafos de estado, descripciones HDL.

#### Mini-check

1. Por que un circuito sincrono tolera mejor los rebotes que uno puramente combinacional?
2. Identifica que sucede si se viola el tiempo de hold en un flip-flop D.

---

### 2. Latches

- Latch = celda de memoria sensible al **nivel** del reloj o de una Senal enable.
- Tipos basicos: SR, D, JK, T (versiones con NAND/NOR).
- Implementaciones clasicas:

```
 latch SR con NAND cruzadas

 S ---->o              )---- Q
 R ---->o/  
```

- Ventajas: sencillos, consumen menos recursos.
- Riesgos: transparencia cuando enable = 1, posibilidad de condiciones de carrera/metastabilidad si entradas cambian cerca del borde.
- Buenas practicas: encadenar latches maestro-esclavo para evitar transparencia, filtrar entradas asincronas antes del latch.

#### Ejercicio guiado
1. Completa la tabla de funcionamiento de un latch D transparente cuando EN=1 y EN=0.
2. Dibuja un latch SR implementado solo con puertas NAND e indica estados prohibidos.

---

### 3. Flip-Flops

- Capturan datos en un **flanco** del reloj (subida o bajada).
- Tipos mas usados: D, JK, T y SR edge-triggered.
- Parametros temporales fundamentales: setup, hold, clock-to-Q, tiempos de recuperacion/remocion para preset/clear.
- Variantes: con enable, preset/clear asincronos, salida complementaria, doble flanco.
- Usos practicos: registros, pipelines de procesadores, divisores de frecuencia, sincronizacion entre dominios de reloj.

#### Tabla de excitacion rapida (JK)

| J | K | Proximo Q |
|---|---|-----------|
| 0 | 0 | Q (mantiene)
| 0 | 1 | 0
| 1 | 0 | 1
| 1 | 1 | Q' (toggle)

#### Laboratorio sugerido
Construye un flip-flop JK edge-triggered usando dos latches (maestro-esclavo) y analiza el retardo total medido en simulacion.

---

### 4. Registros

- Agrupan flip-flops para almacenar palabras completas o desplazar datos.
- Clasificacion:
  - Paralelo-paralelo: entrada y salida simultanea de todos los bits.
  - Serie-serie (shift register): desplaza bit a bit por cada pulso de reloj.
  - Serie-paralelo / paralelo-serie: conversion entre formatos, utiles en interfaces como SPI o UART.
  - Registros universales: permiten desplazamiento bidireccional y carga paralela.
- Aplicaciones: buffers, pipelines, controladores de display (ej. 74HC595), filtros digitales, generadores de secuencias (LFSR).
- Optimizaciones energeticas: clock gating, habilitacion selectiva, particionar por dominios de reloj.

#### Ejercicio
Disena un registro de desplazamiento de 4 bits con carga paralela. Especifica la tabla de control (Load, Shift, Direction).

---

### 5. Contadores

- Secuencias de estados recurrentes generadas por flip-flops.
- Tipos comunes:
  - Ripple (asincronos): cada flip-flop es excitado por la salida del anterior; faciles pero con retardo acumulado.
  - Sincronos: todos los flip-flops comparten el reloj, y las entradas se calculan para lograr la secuencia deseada.
  - Johnson (twisted ring), Gray, BCD, modulo-N arbitrario, programables.
- Tecnicas de diseno:
  1. Definir la secuencia deseada.
  2. Elaborar tabla de transicion y tabla de excitacion (segun tipo de flip-flop).
  3. Simplificar ecuaciones (K-map) para obtener las entradas necesarias.
  4. Anadir logica de reset para garantizar arranque en estado valido.
- Aplicaciones: temporizadores, divisores de frecuencia, generadores PWM, direccionamiento circular, maquinas de juego.

#### Mini-desafio
Crea un contador modulo 10 sincrono usando flip-flops JK. Indica la logica de reset para pasar de 1001 a 0000.

---

### 6. Maquinas de Estados Finitos (FSM)

```
[Especificacion] -> [Definir estados] -> [Codificar] -> [Derivar ecuaciones] -> [Implementar y verificar]
```

- Modelos clasicos:
  - **Moore**: salidas dependen solo del estado -> mas estable, latencia fija.
  - **Mealy**: salidas dependen de estado e inputs -> respuesta mas rapida, pero sensible al ruido.
- Flujo recomendado:
  1. Redactar requisitos y dibujar diagrama de estados.
  2. Definir codificacion (binaria, Gray, one-hot).
  3. Obtener ecuaciones de proximo estado y salidas (tablas + simplificacion).
  4. Implementar en flip-flops + logica combinacional.
  5. Verificar con simulacion temporal y cobertura de estados.
- Ejemplos: semaforos, controladores de comunicacion (UART, SPI), secuenciadores de arranque, control de ascensor.

#### Ejercicio
Define una FSM tipo Moore para un detector de secuencia 10110 con solapamiento. Entrega tabla de transicion y describe como codificar los estados.

---

### 7. Sincronizacion y Temporizacion

- **Distribucion del reloj**: usar arboles balanceados o redes en H para minimizar skew.
- **Sincronizadores**: doble flip-flop para entradas asincronas; FIFOs o handshake cuando hay dos dominios de reloj distintos.
- **PLL/DLL**: generan relojes derivados y compensan desfases; ideales para multiplicar o dividir frecuencia.
- **Osciladores**: cuarzo para alta precision, RC calibrado para bajo costo.
- **Metastabilidad**: riesgo cuando una Senal asincrona se captura cerca del flanco; se mitiga con sincronizadores y presupuestando MTBF (mean time between failure).

#### Checklist rapido
- Documentaste tiempos de setup/hold y ruta critica?
- Sincronizaste todas las entradas externas?
- Verificaste resets (sincronos vs asincronos)?
- Analizaste el consumo anadido por el arbol de reloj?

---
## Unidad 4 - Unidad Aritmetico-Logica (ALU)

### Vision general

```
Registros fuente -> Seleccion -> Bloque aritmetico/logico -> Flags -> Registros destino
                     (sumadores, logica, desplazamientos)
```

| Objetivo | Indicador |
|----------|-----------|
| Entender el papel de la ALU | Explica como conecta unidades de registro con buses y control |
| Dominar operaciones aritmetico-logicas | Implementa suma, resta, logica y desplazamientos en HDL o puertas |
| Optimizar rutas criticas | Compara arquitecturas (ripple, lookahead, carry save) y calcula retardo |
| Integrar flags y control | Define Zero, Carry, Overflow, Sign y describe como afectan flujo de control |

---

### 1. Funciones Principales

- Operaciones aritmeticas: suma, resta, incremento, decremento, saturacion, multiplicacion parcial, comparaciones basadas en resta.
- Operaciones logicas: AND, OR, XOR, NOT, enmascaramientos, deteccion de bits, rotaciones, desplazamientos logicos y aritmeticos.
- Flags comunes:
  - **Z (Zero)**: salida = 0.
  - **C (Carry)**: acarreo fuera del bit mas significativo (sumas) o ausencia de prestamo (restas).
  - **V (Overflow)**: overflow aritmetico en representacion con signo.
  - **S (Sign)**: bit mas significativo del resultado.
  - **P (Parity)** o **N (Negative)** segun arquitectura.
- Flujo basico de control:
```
ALU_OP -> Selecciona operacion -> Ejecuta -> Actualiza flags -> Control decide siguiente paso
```

#### Mini-check
1. Diferencia entre flag Carry y Overflow en complemento a 2.
2. Que operacion usarias para detectar si un numero es potencia de 2? Explica.

---

### 2. Arquitectura Interna

- Componentes principales:
  1. **Bancos de registros**: suministran operandos A y B; incluyen multiplexores para seleccionar fuentes (registros, constantes, inmediatos).
  2. **Unidad aritmetica**: sumadores/restadores, incremento/decremento, generadores de saturacion.
  3. **Unidad logica**: puertas AND/OR/XOR/NOT, comparadores bit a bit.
  4. **Unidad de desplazamientos**: shifters logicos, aritmeticos y barriles (rotaciones).
  5. **Generador de carry**: ripple, lookahead, select, save, segun requisitos de velocidad.
  6. **Registro de flags**: latchea Zero, Carry, Overflow, Sign, etc., y alimenta la unidad de control.
  7. **Buses internos**: pueden ser tri-state, multiplexados o crossbar segun arquitectura.
- Estilos de implementacion:
  - **Bit-slice**: repetir una celda de 1 bit (como el 74LS181) y encadenar carries.
  - **Bloques**: grupos de 4 bits con carry lookahead para acelerar.
  - **Pipeline**: dividir la ALU en etapas (preparacion de operandos, ejecucion, normalizacion).
- Ejemplo simplificado de celda 1 bit:
```
   Cin ---->o-----------------+
            |                 |
A ---->XOR--+--> Sum bit ----> MUX (elige logica/arit)
B ---->XOR--|
            +--> Generador de carry -> Cout
```

#### Ejercicio
Dibuja el diagrama de bloques para una ALU de 8 bits que incluya sumador/restador, AND/OR y shifter logico. Indica donde se generan los flags.

---

### 3. Metodos de Implementacion

#### 3.1 Componentes discretos
- Serie 74xx: 74LS181 (ALU 4 bits), 74LS182 (carry lookahead), 74HC283 (sumador), 74HC barrel shifters.
- Ventajas: visualizacion fisica, aprendizaje. Desventajas: area y consumo altos.

#### 3.2 HDL (VHDL/Verilog)
- Ejemplo generico:
```
process(A, B, op)
begin
  case op is
    when "000" => Y <= A + B;        -- suma
    when "001" => Y <= A - B;        -- resta
    when "010" => Y <= A and B;     -- logica
    when "011" => Y <= A or B;
    when "100" => Y <= A xor B;
    when "101" => Y <= shift_left(A, 1);
    when "110" => Y <= shift_right(A, 1);
    when others => Y <= (others => '0');
  end case;
end process;
```
- Recomendaciones: crear testbench, incluir verificacion de flags, usar tipos unsigned/signed adecuados.

#### 3.3 Optimizaciones
- **Carry lookahead**: predice generacion y propagacion para acelerar sumas largas.
- **Carry select**: calcula con carry=0 y carry=1 en paralelo, luego selecciona.
- **Carry save**: mantiene sumas parciales; clave en multiplicadores/dsp.
- **Wallace/Dadda trees**: reducen vectores parciales de multiplicacion.
- **Pipeline**: divide la ALU en etapas para aumentar frecuencia maxima.
- **Clock gating**: desactiva secciones cuando no se usan.

#### Mini-desafio
Implementa en HDL un modulo `alu_flags` que reciba resultado y carry/overflow y genere Z, C, V, N. Escribe las expresiones booleanas para cada flag.

---

### 4. Integracion y Casos de Uso

- **Microcontroladores educativos**: ALU de 8 bits con operaciones basicas + desplazamientos; se controla mediante Senales ALU_OP y SRC/DST.
- **DSP**: unidades MAC (multiply-accumulate) con saturacion y redondeo, soporte para precision fija.
- **Criptografia**: ALU modulares para operaciones modulo n, rotaciones controladas, mezclas bitwise.
- **SIMD / vectoriales**: ejecutan la misma operacion sobre multiples datos (ej. NEON, AVX), requieren anchos mayores y alineacion.
- **Precision mixta**: combinan operaciones de 8/16/32 bits segun carga; comun en IA embebida.
- **Integracion con buses**: la ALU escribe resultados en registros destino o memoria a traves de buses internos; los flags alimentan la unidad de control para saltos condicionales.

#### Ejercicio final
Disena una ALU de 4 bits que soporte: suma/resta, AND, OR, XOR, desplazamiento a la izquierda, comparacion (A>B). Proporciona tabla que mapee `op[2:0]` a cada funcion e indica como se actualizan Z y C.

---

# Fin del archivo
