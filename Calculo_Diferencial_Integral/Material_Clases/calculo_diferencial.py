## /// script
## requires-python = ">=3.12"
## dependencies = [
##     "marimo>=0.23.8",
##     "matplotlib>=3.10.9",
##     "numpy>=2.4.6",
## ]
## ///

import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <h1 style="text-align:center;">0101 CALCULO DIFERENCIAL E INTEGRAL</h1>

    <div>
        <table style="display: flex; justify-content: center;">
            <tr>
                <th style="text-align:center;">Martes</th>
                <th style="text-align:center;">Jueves</th>
            </tr>
            <tr>
                <td style="text-align:center;">10:00 a.m. a 12:30 p.m.</td>
                <td style="text-align:center;">10:00 a.m. a 12:30 p.m.</td>
            </tr>
            <tr>
                <td style="text-align:center;">A-2A</td>
                <td style="text-align:center;">A-2A</td>
            </tr>
        </table>
    </div>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Relaciones de Cambio y el Concepto de la Derivada
    Supongamos que $D$ es la función que mide el número de MB descargados de datos de una aplicación y que depende del tiempo $t$, medido en segundos. En otras palabras, $D(t)$ nos dice cuantos MB se han descargado en un tiempo $t$.

    ### Relaciones de Cambio

    Ni $D$ ni $t$ por sí solos nos dicen nada sobre "cambio" — son solo valores en un instante.
    $D(t_1)$ es solo "cuántos MB había descargado la app en el segundo $t_1$": un número aislado, una fotografía. Lo mismo para $D(t_2)$. Ninguno de los dos, por separado, dice si la descarga fue rápida o lenta, ni siquiera si estaba avanzando.

    Para capturar la idea de *cambio* necesitamos comparar esas dos fotografías: **restarlas**.
    $$\Delta D = D(t_2) - D(t_1)$$
    nos dice cuánto avanzó la descarga entre esos dos instantes. De la misma manera,
    $$\Delta t = t_2 - t_1$$
    nos dice cuánto tiempo transcurrió entre esos dos instantes.

    Es como calcular la velocidad de un coche: no te sirve saber solo dónde estaba a las 3:00 pm, ni solo dónde estaba a las 3:05 pm — necesitas la **distancia recorrida** (el "cuánto") y el **tiempo que tomó** (el "en cuánto"). Ambos son pasos necesarios antes de poder preguntar "¿qué tan rápido?".

    Supongamos que dos apps descargan la misma cantidad de datos, cada una midiendo su propio
    tiempo desde que inicia la descarga ($t=0$):

    - `App A`: $D_A(0) = 0$ MB, $D_A(2) = 50$ MB — descarga 50 MB en 2 segundos.
    - `App B`: $D_B(0) = 0$ MB, $D_B(60) = 50$ MB — descarga 50 MB en 60 segundos.

    Tenga en cuenta que $t_1^A = 0$, $t_2^A = 2$ y $t_1^B = 0$, $t_2^B = 60$ son los tiempos medidos de descarga de la `App A` y la `App B`, respectivamente.

    Para la App A: $\Delta D_A = D_A(t_2^A) - D_A(t_1^A) = D_A(2) - D_A(0) = 50$ MB, en un intervalo $\Delta t_A = t_2^A - t_1^A = 2$ s.

    Para la App B: $\Delta D_B = D_B(t_2^B) - D_B(t_1^B) = D_B(60) - D_B(0) = 50$ MB, en un intervalo $\Delta t_B = t_2^B - t_1^B = 60$ s.

    Ambas tienen el mismo $\Delta D = 50$ MB, pero claramente la `app A` fue mucho más rápida. El cambio absoluto $\Delta D$ no dice nada por sí solo — necesita contexto, y ese contexto es $\Delta t$.

    Para comparar estas dos descargas de manera justa necesitamos una medida que no dependa de cuánto duró el intervalo, sino que nos diga **cuánto se descargó, en promedio, por cada segundo**. Eso es exactamente lo que logra dividir:
    $$\frac{\Delta D}{\Delta t}$$
    Esta división "reparte" el cambio total entre el tiempo que tomó lograrlo, dándonos una cantidad por unidad de tiempo — una tasa, o razón de cambio. Nota que $\Delta D$ y $\Delta t$ no son cantidades independientes: ambas nacen del mismo par de instantes $(t_1, t_2)$, así que su cociente compara "cuánto cambió una cosa" contra "cuánto cambió la otra" en el mismo intervalo exacto.

    Verifiquemos con el ejemplo anterior:

    - App A: $\frac{\Delta D_A}{\Delta t_A} = \dfrac{50}{2} = 25$ MB/s
    - App B: $\frac{\Delta D_B}{\Delta t_B} = \dfrac{50}{60} \approx 0.83$ MB/s

    Ahora sí podemos decir, con un número, que la `app A` fue aproximadamente 30 veces más rápida que la `app B` — algo que el $\Delta D$ por sí solo no podía mostrarnos.

    Esto nos lleva a una definición formal: al cociente
    $$\frac{\Delta D}{\Delta t} = \frac{D(t_2)-D(t_1)}{t_2-t_1}$$
    se le llama **razón de cambio promedio** de $D$ con respecto a $t$ en el intervalo $[t_1, t_2]$.

    También se le conoce como, **velocidad promedio**:
    $$v_{\text{promedio}} = \frac{D(t_2)-D(t_1)}{t_2-t_1}$$

    Vale la pena notar algo antes de seguir: aquí el "promedio" no se calcula sumando varias velocidades y dividiendo entre cuántas, como se hace con un promedio de calificaciones. Se calcula con un solo cociente, $\Delta D/\Delta t$, usando únicamente el valor inicial y el valor final del intervalo. Aun así, el espíritu de la palabra "promedio" es el mismo que usamos siempre: un solo número que resume un comportamiento que pudo haber variado por dentro.

    ### ¿Por qué se le llama razón de cambio *promedio*?

    El cociente $\dfrac{\Delta D}{\Delta t}$ **no distingue lo que pasó dentro del intervalo** — solo ve el principio y el final. Dentro de $[t_1, t_2]$, la velocidad de descarga real pudo haber variado muchísimo: tal vez empezó lenta, se aceleró a la mitad, bajó un poco al final.

    El cociente no ve nada de eso: **aplana** todas las fluctuaciones intermedias en un único número.

    Es la misma idea que el promedio de calificaciones: si un alumno saca 10, 4 y 7 en tres exámenes, su promedio es 7 — pero ese 7 no dice *cuándo* le fue bien o mal, solo resume el desempeño total en un solo número. De la misma manera, $\dfrac{\Delta D}{\Delta t}$ resume en un solo número todo lo que pasó entre $t_1$ y $t_2$, sin importar si la velocidad real subió, bajó, o se mantuvo constante en el camino.

    Esto deja una pregunta abierta: si el promedio "esconde" lo que pasa dentro del intervalo, ¿cómo le hacemos para conocer la velocidad **en un instante específico**, sin promediar nada?

    ### La razón de cambio promedio como pendiente de una recta secante

    Si graficamos $D(t)$ y marcamos los puntos $(t_1, D(t_1))$ y $(t_2, D(t_2))$, la línea recta que une esos dos puntos se llama **recta secante**. Su pendiente es, por definición,

    $$m_{\text{sec}} = \frac{D(t_2)-D(t_1)}{t_2-t_1}$$

    que es exactamente la razón de cambio promedio que calculamos antes. No es una coincidencia: dividir "cuánto subió" entre "cuánto avanzó" es precisamente la definición de pendiente.


    Veamos el siguiente ejemplo, definamos a la función $D$ como sigue:
    $$D(t) =  -0.35(\frac{t}{5})^3 + 2.1(\frac{t}{5})^2$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    deslizadorA = mo.ui.slider(0, 19.9, 0.1)
    deslizadorB = mo.ui.slider(0.1, 20, 0.1)
    mo.vstack(
        [
            mo.md(r"#### Controles de la gráfica"),
            mo.hstack(
                [
                    mo.md(f"Mueve el punto $t_2$ = {deslizadorB}"),
                ],
                justify="center",
            ),
            mo.hstack(
                [
                    mo.md(f"Mueve el punto $t_1$ = {deslizadorA}"),
                ],
                justify="center",
            ),
            # mo.hstack(
            #    [mo.md(r"$D(t) = -0.35(\dfrac{t}{5})^3 + 1.35(\dfrac{t}{5})^2$")],
            #    justify="center",
            # ),
        ],
        gap=2.5,
    )
    return deslizadorA, deslizadorB


@app.cell
def _(mo, t1, t2):
    mo.md(f"""
    entonces, para $t_1 = {t1:.2f}$ y para $t_2 = {t2:.2f}$
    """)
    return


@app.cell
def _(m, mo, t1, t2, y1, y2):
    mo.md(f"""
    $$m_{{sec}} = \\dfrac{{\\Delta D}}{{\\Delta t}} = \\dfrac{{D(t_2) - D(t_1)}}{{t_2 - t_1}} = \\dfrac{{{y2:.2f} - {y1:.2f}}}{{{t2:.2f} - {t1:.2f}}} \\approx {m:.2f} $$
    """)
    return


@app.cell(hide_code=True)
def _(np):
    # Se define la funcion f:
    def funcion_D(t):
        return -0.35 * (t / 5) * (t / 5) * (t / 5) + 2.1 * (t / 5) * (t / 5)


    # Se obtiene el rango de la funcion f:
    funcion_D_rango = [i for i in np.arange(0, 20, 0.1)]

    # Se calcula la imagen de la funcion f:
    funcion_D_imagen = [funcion_D(i) for i in funcion_D_rango]
    return funcion_D, funcion_D_imagen, funcion_D_rango


@app.cell(hide_code=True)
def _(funcion_D_imagen, funcion_D_rango, lr, m, plt, t1, t2, y1, y2):
    plt.plot(
        funcion_D_rango,
        funcion_D_imagen,
        label=r"$D(t) = -0.35(\frac{t}{5})^3 + 2.1(\frac{t}{5})^2$",
    )
    plt.plot(funcion_D_rango, lr, label=f"Recta Secante, pendiente m = {m:.2f}")
    plt.plot(
        t1,
        y1,
        marker="o",
        color="red",
        markeredgecolor="black",
        markeredgewidth=1,
        label=f"$t_1 = {t1}$, $D(t_1) = {y1:.2f}$",
    )
    plt.plot(
        t2,
        y2,
        marker="o",
        color="red",
        markeredgecolor="black",
        markeredgewidth=1,
        label=f"$t_2 = {t2}$, $D(t_2) = {y2:.2f}$",
    )
    plt.title("Descarga de datos en función del tiempo")
    plt.legend()
    plt.ylim(0, 12)  # Ejes fijos para que no "salte"
    plt.xlim(0, 20)
    plt.grid(True)
    plt.gcf()  # en marimo, devuelve la figura para mostrarla
    return


@app.cell(hide_code=True)
def _(deslizadorA, deslizadorB, funcion_D, funcion_D_rango):
    t1 = min(deslizadorA.value, deslizadorB.value)
    t2 = max(deslizadorA.value, deslizadorB.value)
    y1 = funcion_D(t1)
    y2 = funcion_D(t2)
    m = (funcion_D(t2) - funcion_D(t1)) / (t2 - t1)

    b = y1 - m * t1


    def recta(x, m, b):
        return m * x + b


    lr = [recta(i, m, b) for i in funcion_D_rango]
    return lr, m, t1, t2, y1, y2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Esto nos da una tercera forma de leer el mismo número: $\dfrac{\Delta D}{\Delta t}$ es, a la vez,

    - una **razón de cambio promedio** (el lenguaje algebraico),
    $$\dfrac{\Delta D}{\Delta t} = \frac{D(t_2)-D(t_1)}{t_2-t_1}$$
    - una **velocidad promedio de descarga** (el lenguaje físico, en MB/s),
    $$v_{\text{promedio}} = \frac{D(t_2)-D(t_1)}{t_2-t_1}$$
    - y la **pendiente de la secante** entre $(t_1, D(t_1))$ y $(t_2, D(t_2))$ (el lenguaje geométrico).
    $$m_{\text{sec}} = \frac{D(t_2)-D(t_1)}{t_2-t_1}$$

    Tres maneras distintas de decir exactamente lo mismo.

    ### De la secante a la tangente: la razón de cambio instantánea

    Habíamos dejado una pregunta pendiente: si la razón de cambio promedio "aplana" todo lo que pasa dentro del intervalo $[t_1, t_2]$, ¿cómo podemos conocer la velocidad de descarga **en un instante preciso**, sin promediar nada?

    La idea es *encoger el intervalo*: en vez de dejar a $t_2$ fijo y lejos de $t_1$, lo acercamos cada vez más, hasta casi tocarlo. Es decir, hacemos $t_2 \to t_1$ o lo que es lo mismo $\Delta t \to 0$.

    Geométricamente, esto tiene un efecto muy claro: conforme $t_2$ se acerca a $t_1$ y $\Delta t$ se acerca a 0, entonces la recta secante gira y se va "pegando" cada vez más a la curva, hasta convertirse — en el límite — en la **recta tangente** a la gráfica de $D$ en el punto $(t_1, D(t_1))$.

    Numéricamente, esto significa calcular el límite del cociente de diferencias:

    $$\lim_{\Delta t \to 0} \frac{\Delta D}{\Delta t} = \lim_{t_2 \to t_1} \frac{D(t_2)-D(t_1)}{t_2-t_1}$$

    Este límite se puede interpretar como:

    - la **razón de cambio instantánea** de $D$ con respecto a $t$ en $t_1$,
    - la **velocidad instantánea** de descarga en el instante $t_1$ (en MB/s),
    $$v(t_1) = \lim_{t_2 \to t_1} \frac{D(t_2)-D(t_1)}{t_2-t_1}$$
    - y la **pendiente de la recta tangente** a la gráfica de $D$ en el punto $(t_1, D(t_1))$.
    $$m_{\text{tan}} = \lim_{t_2 \to t_1} \frac{D(t_2)-D(t_1)}{t_2-t_1}$$

    La misma trinidad de antes — algebraica, física, geométrica — mantiene su estructura; lo único que cambió es que ya no promediamos sobre un intervalo, sino que capturamos el instante exacto.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Visualizando la secante convirtiéndose en tangente


    En vez de mover $t_1$ y $t_2$ de forma independiente, ahora fijamos un punto de interés $t_1$ y controlamos qué tan lejos está $t_2$ mediante un pequeño incremento $\Delta t$, de modo que $t_2 = t_1 + \Delta t$. Luego se puede reescribir la **pendiente de la recta tangente** al punto $(t_1, D(t_1))$ como:

    $$m_{\text{tan}} = \lim_{\Delta t \to 0} \frac{D(t_1 + \Delta t)-D(t_1)}{\Delta t}$$

    Mueve el slider de $\Delta t$ hacia valores cada vez más pequeños y observa cómo la recta secante (línea punteada) se va acercando a la recta tangente (línea sólida) — ambas calculadas en el mismo punto $t_1$.
    """)
    return


@app.cell
def _(mo):
    deslizador_t1_tan = mo.ui.slider(0, 15, 0.1, value=7)
    deslizador_h = mo.ui.slider(0.05, 5, 0.05, value=5)
    mo.vstack(
        [
            mo.md(r"#### Controles: punto de tangencia y tamaño del incremento"),
            mo.hstack(
                [mo.md(f"Punto de interés $t_1$ = {deslizador_t1_tan}")],
                justify="center",
            ),
            mo.hstack(
                [mo.md(f"Incremento $h$ (así $t_2 = t_1+h$) = {deslizador_h}")],
                justify="center",
            ),
        ],
        gap=2.5,
    )
    return deslizador_h, deslizador_t1_tan


@app.cell
def _(deslizador_h, deslizador_t1_tan, funcion_D, funcion_D_rango):
    t1_tan = deslizador_t1_tan.value
    h = deslizador_h.value
    t2_tan = t1_tan + h

    y1_tan = funcion_D(t1_tan)
    y2_tan = funcion_D(t2_tan)
    m_sec_tan = (y2_tan - y1_tan) / (t2_tan - t1_tan)


    def funcion_D_prime(t):
        return -0.21 * (t / 5) * (t / 5) + 0.84 * (t / 5)


    m_tan = funcion_D_prime(t1_tan)

    b_sec_tan = y1_tan - m_sec_tan * t1_tan
    b_tan = y1_tan - m_tan * t1_tan


    def recta2(x, m, b):
        return m * x + b


    lr_sec_tan = [recta2(i, m_sec_tan, b_sec_tan) for i in funcion_D_rango]
    lr_tan = [recta2(i, m_tan, b_tan) for i in funcion_D_rango]
    return (
        h,
        lr_sec_tan,
        lr_tan,
        m_sec_tan,
        m_tan,
        t1_tan,
        t2_tan,
        y1_tan,
        y2_tan,
    )


@app.cell
def _(h, m_sec_tan, m_tan, mo, t1_tan, t2_tan):
    mo.md(f"""
    Con $t_1 = {t1_tan:.2f}$ y $h = {h:.2f}$ (por lo tanto $t_2 = {t2_tan:.2f}$):

    $$m_{{sec}} = {m_sec_tan:.4f} \\qquad\\qquad m_{{tan}} = {m_tan:.4f}$$

    Diferencia entre ambas pendientes: $|m_{{sec}} - m_{{tan}}| = {abs(m_sec_tan - m_tan):.4f}$

    Conforme $\\Delta t \\to 0$, $m_{{sec}} \\to m_{{tan}}$.
    """)
    return


@app.cell
def _(
    funcion_D_imagen,
    funcion_D_rango,
    lr_sec_tan,
    lr_tan,
    m_sec_tan,
    m_tan,
    plt,
    t1_tan,
    t2_tan,
    y1_tan,
    y2_tan,
):
    plt.plot(funcion_D_rango, funcion_D_imagen, label="$D(t)$", color="tab:blue")
    plt.plot(
        funcion_D_rango,
        lr_sec_tan,
        "--",
        color="tab:orange",
        label=f"Secante, m={m_sec_tan:.3f}",
    )
    plt.plot(
        funcion_D_rango, lr_tan, color="tab:green", label=f"Tangente, m={m_tan:.3f}"
    )

    plt.plot(
        t1_tan,
        y1_tan,
        marker="o",
        color="black",
        markersize=8,
        zorder=5,
        label=f"$t_1={t1_tan:.2f}$",
    )
    plt.plot(
        t2_tan,
        y2_tan,
        marker="o",
        color="red",
        markersize=6,
        zorder=5,
        label=f"$t_2={t2_tan:.2f}$",
    )

    plt.title("Secante acercándose a la tangente conforme $h \\to 0$")
    plt.legend()
    plt.ylim(0, 12)
    plt.xlim(0, 20)
    plt.grid(True)
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Para resumir lo que se ha visto, los límites de la forma:
    $$\lim_{\Delta t \to 0} \frac{f(a + \Delta t)-f(a)}{\Delta t}$$
    aparecen cuando se calcula una razón de cambio en cualquiera de las ciencias o en la ingeniería — particularmente en Ingeniería de la Computación, la velocidad de descarga de datos en una aplicación, como la que acabamos de estudiar, o también el costo marginal de cómputo al escalar un sistema, o la latencia de un servidor conforme aumenta el número de usuarios conectados. Ya que esta clase de límite sucede, muy seguido, se le da un nombre y notación especial.

    **Definición.** La **derivada de una función $f$ en un número $a$**, se indica mediante f'(a), es:

    $$f'(a) = \lim_{\Delta t \to 0} \frac{f(a + \Delta t)-f(a)}{\Delta t}$$

    **si este límite existe**.

    Considere la sustitución $x = a + \Delta t$ y además que $\Delta t = x - a$, tenga en cuenta que $\Delta t$ se aproxima a 0 si y sólo si $x$ se aproxima a $a$. En consecuencia, una manera equivalente de establecer la deﬁnición de la derivada, es

    $$f'(a) = \lim_{x \to a} \frac{f(x)-f(a)}{x - a}$$

    Dado cualquier número $x$ para el cual este límite exista, se le asigna a $x$ el número $f'(x)$. De modo que se puede considerar a $f'$ como una nueva función, llamada **derivada de $f$** y definida por medio de la expresión vista anteriormente. Dado que el valor de $f'$ en $x$, $f'(x)$, se puede interpretar geométricamente como la pendiente de la recta tangente a la gráfica de $f$ en el punto $(x, f(x))$.

    La función $f'$ se conoce como la derivada de $f$, porque se ha ``derivado'' de $f$ por medio de la operación de hallar el límite en la expresión que acabamos de definir. El dominio de $f'$ es el conjunto
    $$
    \operatorname{Dom}f' = \{\, x \mid f'(x) \text{ existe} \,\}
    $$
    y puede ser menor que el dominio de $f$.

    También se puede generalizar la interpretación de la derivada de una función $f$ en un punto $a$:

    - La recta tangente a $y = f(x)$ en $(a, f(a))$ es la recta tangente a través de $(a, f(a))$ cuya pendiente es igual a $f'(a)$, la derivada de $f$ en $a$.
    $$ m_{\text{tan}} = f'(a) = \lim_{x \to a} \frac{f(x)-f(a)}{x - a}$$

    **Nota**: Si usa la forma punto pendiente de la ecuación de una recta, puede escribir una ecuación de la recta tangente a la curva $y = f(x)$ en el punto $(a, f(a))$:

    $$
    y - f(a) = f'(a)(x - a)
    $$

    - La derivada $f'(a)$ es la velocidad instantánea en el instante $x=a$.
    $$ v(a) = f'(a) = \lim_{x \to a} \frac{f(x)-f(a)}{x - a}$$

    - La derivada $f'(a)$ es la razón de cambio instantánea de $y = f(x)$ con respecto a x cuando $x = a$.
    $$ f'(a) = \lim_{\Delta x \to 0} \frac{\Delta f}{\Delta x} = \lim_{x \to a} \frac{f(x)-f(a)}{x - a}$$

    ### Formas de denotar la derivada

    Si usa la notación tradicional $y = f(x)$ para indicar que la variable independiente es $x$ y la dependiente es $y$, en tal caso algunas otras notaciones comunes para la derivada son:

    $$
    f'(x) = y'= \dfrac{dy}{dx} = \dfrac{df}{dx} = \dfrac{d}{dx}f(x) = Df(x) = D_{x}f(x)
    $$

    Los símbolos $D$ y $\dfrac{d}{dx}$ se llaman operadores de derivación porque indican la operación de derivación, que es el proceso de calcular una derivada.

    El símbolo $\dfrac{dy}{dx}$ introducido por Leibniz no debe considerarse como una razón (por el momento); es sencillamente un sinónimo de $f'(x)$. Esta es una notación muy útil, por ejemplo, cuando se usa en la notación de incrementos:

    $$
    \dfrac{dy}{dx} = \lim_{\Delta x \to 0} \dfrac{\Delta y}{\Delta x}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Ejercicios

    1. Una empresa de servicios en la nube cobra a sus clientes por el uso de almacenamiento. El costo de almacenar $x$ gigabytes (GB) de datos en un mes es $C(x)$ pesos.

        (a) ¿Cuál es el significado de la derivada $C'(x)$? ¿Cuáles son sus unidades?

        (b) En términos prácticos, ¿qué significa decir que $C'(1000) = 22$?

        (c) ¿Qué le hace pensar que es más grande, $C'(50)$ o $C'(500)$? ¿Qué hay respecto a $C'(5000)$?

    2. Una curva tiene la ecuación $y=f(x)$.

        (a) Escriba una expresión para la pendiente de la recta secante
    que pasa por los puntos $P(3,f(3))$ y $Q(x,f(x))$.

        (b) Escriba una expresión para la pendiente de la recta
    tangente en $P$.

    4. Si una pelota se lanza al aire hacia arriba, con una velocidad de 40 m/s, su altura (en m) una vez que transcurren $t$ segundos, está dada por $y = 40t - 16t^2$. Encuentre la velocidad después de $t=2$ segundos.
    """)
    return


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import math

    return mo, np, plt


if __name__ == "__main__":
    app.run()
