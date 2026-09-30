#!/usr/bin/python3
"""Calculadora Grafica 2.0 — versión con PySide6 (Qt).

Mismas funciones que pract2_calc.py (la versión con Tkinter), pero construida
con PySide6: los colores de fondo se aplican bien en macOS, por lo que aquí sí
se pueden usar botones normales (QPushButton) con el tema oscuro.

La primera línea (shebang) apunta a /usr/bin/python3 porque es el intérprete
del sistema que tiene PySide6 instalado; así el archivo se ejecuta con doble
clic. Si en el futuro instalas PySide6 en otro Python, cambia esa línea.

Formas de ejecutarlo:

    /usr/bin/python3 "calculadora grafica 2.0.py"     Abre la ventana.
    /usr/bin/python3 "calculadora grafica 2.0.py" --captura   Guarda un PNG.

En plataformas online (Colab, JupyterLite, Replit sin pantalla) no hay
monitor, por lo que la ventana no se vería. En ese caso el programa dibuja la
interfaz sin pantalla y guarda una imagen PNG en lugar de abrir la ventana.
"""

import argparse
import ast
import operator
import os
import sys

try:
    import PySide6
except ModuleNotFoundError:
    print("PySide6 no está instalado en este intérprete de Python.\n")
    print("Este archivo necesita PySide6, que no es compatible con Python 3.14.")
    print("Prueba con una de estas dos opciones:\n")
    print("  1) Ejecutarlo con el Python del sistema:")
    print("     /usr/bin/python3 \"" + os.path.basename(__file__) + "\"")
    print("  2) Abrir Calculadora 2.0.app con doble clic.\n")
    print("En una plataforma online, instálalo antes con:  pip install PySide6")
    raise SystemExit(1)

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QFontDatabase, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

MAX_HISTORIAL = 5

FONDO_ALTO = "#0b1b2b"
FONDO_BAJO = "#1c4257"
FONDO_PANEL = "#0f2a3a"
FONDO_ENTRADA = "#071620"
TEXTO = "#e9f7fa"
TEXTO_SUAVE = "#7fb6c4"
COLOR_ERROR = "#ff7b7b"
COLOR_OPERADOR = "#2ec5ce"
COLOR_OPERADOR_HOVER = "#57dbe3"
COLOR_OPERADOR_PULSADO = "#1ea3ab"
COLOR_IGUAL = "#ff7b54"
COLOR_IGUAL_HOVER = "#ff9a79"
COLOR_IGUAL_PULSADO = "#e05f39"
COLOR_TECLA = "#15384a"
COLOR_TECLA_HOVER = "#1d4d63"
COLOR_TECLA_PULSADO = "#0e2a38"
BORDE = "rgba(255, 255, 255, 0.12)"

FUENTE_UI = ("Avenir Next", "Helvetica Neue", "Helvetica")
FUENTE_CIFRA = ("Menlo", "SF Mono", "Courier New")

OPERACIONES = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

SIMBOLOS = "+-*/%"
ACCIONES = ("C", "(", ")", "±")
TECLAS_VISIBLES = {"×": "*", "÷": "/", "−": "-"}

ESTILO = f"""
QWidget {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {FONDO_ALTO}, stop:1 {FONDO_BAJO});
    color: {TEXTO};
}}
QLineEdit {{
    background-color: {FONDO_ENTRADA};
    color: {TEXTO};
    border: 1px solid {BORDE};
    border-radius: 18px;
    padding: 12px 18px;
    selection-background-color: {COLOR_OPERADOR};
}}
QFrame#panel {{
    background-color: {FONDO_PANEL};
    border: 1px solid {BORDE};
    border-radius: 18px;
}}
QLabel#titulo {{
    color: {TEXTO_SUAVE};
}}
QLabel#estado {{
    color: {TEXTO_SUAVE};
}}
QListWidget {{
    background-color: transparent;
    color: {TEXTO};
    border: none;
    outline: none;
}}
QListWidget::item {{
    padding: 6px 8px;
    border-radius: 10px;
}}
QListWidget::item:selected {{
    background-color: {FONDO_ENTRADA};
    color: {COLOR_OPERADOR};
}}
QListWidget::item:hover {{
    background-color: rgba(255, 255, 255, 0.05);
}}
QPushButton {{
    background-color: {COLOR_TECLA};
    color: {TEXTO};
    border: 1px solid {BORDE};
    border-radius: 24px;
    padding: 10px 16px;
}}
QPushButton:hover {{
    background-color: {COLOR_TECLA_HOVER};
    border-color: {COLOR_OPERADOR};
}}
QPushButton:pressed {{
    background-color: {COLOR_TECLA_PULSADO};
    color: {COLOR_OPERADOR_HOVER};
}}
QPushButton#operador {{
    background-color: {COLOR_OPERADOR};
    color: {FONDO_ENTRADA};
    border-color: transparent;
}}
QPushButton#operador:hover {{
    background-color: {COLOR_OPERADOR_HOVER};
    border-color: {TEXTO};
}}
QPushButton#operador:pressed {{
    background-color: {COLOR_OPERADOR_PULSADO};
}}
QPushButton#igual {{
    background-color: {COLOR_IGUAL};
    color: #2b0f06;
    border-color: transparent;
}}
QPushButton#igual:hover {{
    background-color: {COLOR_IGUAL_HOVER};
    border-color: {TEXTO};
}}
QPushButton#igual:pressed {{
    background-color: {COLOR_IGUAL_PULSADO};
}}
QPushButton#plano {{
    background-color: transparent;
    color: {TEXTO_SUAVE};
    border: 1px solid {BORDE};
    border-radius: 14px;
    padding: 6px 12px;
}}
QPushButton#plano:hover {{
    background-color: {COLOR_TECLA};
    color: {TEXTO};
    border-color: {COLOR_OPERADOR};
}}
QPushButton#plano:pressed {{
    background-color: {COLOR_TECLA_PULSADO};
}}
"""


def familia_disponible(candidatos):
    instaladas = set(QFontDatabase.families())
    for nombre in candidatos:
        if nombre in instaladas:
            return nombre
    return candidatos[-1]


def fuente(candidatos, tamano, peso=QFont.Weight.Normal, espaciado=0.0):
    objeto = QFont(familia_disponible(candidatos))
    objeto.setPointSize(tamano)
    objeto.setWeight(peso)
    if espaciado:
        objeto.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, espaciado)
    return objeto


def evaluar(expresion):
    def visitar(nodo):
        if isinstance(nodo, ast.Constant) and isinstance(nodo.value, (int, float)):
            return nodo.value
        if isinstance(nodo, ast.BinOp) and type(nodo.op) in OPERACIONES:
            return OPERACIONES[type(nodo.op)](visitar(nodo.left), visitar(nodo.right))
        if isinstance(nodo, ast.UnaryOp):
            valor = visitar(nodo.operand)
            if isinstance(nodo.op, ast.UAdd):
                return +valor
            if isinstance(nodo.op, ast.USub):
                return -valor
        raise ValueError("Expresión no permitida")

    return visitar(ast.parse(expresion, mode="eval").body)


def formatear(valor):
    if isinstance(valor, float):
        if valor.is_integer():
            return str(int(valor))
        return f"{valor:g}"
    return str(valor)


def presentar(texto):
    return texto.replace("*", "×").replace("/", "÷").replace("-", "−")


class Calculadora(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora Grafica 2.0")
        self.setStyleSheet(ESTILO)

        self.expresion = ""
        self.error = False
        self.recien_igual = False

        self._construir()
        self._atajos()
        self._tipografia()
        self._pintar()

    def _construir(self):
        raiz = QVBoxLayout(self)
        raiz.setContentsMargins(14, 14, 14, 14)
        raiz.setSpacing(10)

        self.entrada = QLineEdit()
        self.entrada.setReadOnly(True)
        self.entrada.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.entrada.setMinimumHeight(64)
        raiz.addWidget(self.entrada)

        self.estado = QLabel("")
        self.estado.setObjectName("estado")
        self.estado.setMinimumHeight(18)
        raiz.addWidget(self.estado)

        cuerpo = QHBoxLayout()
        cuerpo.setSpacing(10)
        raiz.addLayout(cuerpo)

        cuerpo.addWidget(self._panel_historial())
        cuerpo.addWidget(self._panel_botones(), 1)

    def _panel_historial(self):
        panel = QFrame()
        panel.setObjectName("panel")
        panel.setFixedWidth(210)

        vertical = QVBoxLayout(panel)
        vertical.setContentsMargins(10, 10, 10, 10)
        vertical.setSpacing(8)

        titulo = QLabel("H I S T O R I A L")
        titulo.setObjectName("titulo")
        self.titulo = titulo
        vertical.addWidget(titulo)

        self.historial = QListWidget()
        self.historial.setFocusPolicy(Qt.NoFocus)
        vertical.addWidget(self.historial, 1)

        limpiar = QPushButton("Limpiar historial")
        limpiar.setObjectName("plano")
        limpiar.setCursor(Qt.PointingHandCursor)
        limpiar.clicked.connect(self._limpiar_historial)
        self.limpiar = limpiar
        vertical.addWidget(limpiar)

        return panel

    def _panel_botones(self):
        marco = QWidget()
        rejilla = QGridLayout(marco)
        rejilla.setContentsMargins(0, 0, 0, 0)
        rejilla.setSpacing(6)

        distribucion = [
            ("C", "C", ""), ("⌫", "⌫", ""),
            ("%", "%", ""), ("÷", "/", "operador"),
            ("7", "7", ""), ("8", "8", ""),
            ("9", "9", ""), ("×", "*", "operador"),
            ("4", "4", ""), ("5", "5", ""),
            ("6", "6", ""), ("−", "-", "operador"),
            ("1", "1", ""), ("2", "2", ""),
            ("3", "3", ""), ("+", "+", "operador"),
            ("0", "0", ""), (".", ".", ""),
            ("±", "±", ""), ("=", "=", "igual"),
        ]

        for indice, (etiqueta, valor, estilo) in enumerate(distribucion):
            fila, columna = divmod(indice, 4)
            boton = QPushButton(etiqueta)
            if estilo:
                boton.setObjectName(estilo)
            boton.setCursor(Qt.PointingHandCursor)
            boton.setFocusPolicy(Qt.NoFocus)
            boton.clicked.connect(lambda _=False, v=valor: self._presionar(v))
            boton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            rejilla.addWidget(boton, fila, columna)

        for columna in range(4):
            rejilla.setColumnStretch(columna, 1)
        for fila in range(5):
            rejilla.setRowStretch(fila, 1)

        return marco

    def _tipografia(self):
        self.entrada.setFont(fuente(FUENTE_CIFRA, 30, QFont.Weight.Bold, 1.0))
        self.titulo.setFont(fuente(FUENTE_UI, 10, QFont.Weight.Bold, 3.0))
        self.estado.setFont(fuente(FUENTE_UI, 11))
        self.historial.setFont(fuente(FUENTE_CIFRA, 13))
        self.limpiar.setFont(fuente(FUENTE_UI, 11, QFont.Weight.DemiBold, 0.6))

        for boton in self.findChildren(QPushButton):
            if boton is self.limpiar:
                continue
            if boton.objectName() == "operador":
                boton.setFont(fuente(FUENTE_UI, 20, QFont.Weight.Bold, 0.5))
            elif boton.objectName() == "igual":
                boton.setFont(fuente(FUENTE_UI, 22, QFont.Weight.Black, 0.5))
            else:
                boton.setFont(fuente(FUENTE_UI, 20, QFont.Weight.DemiBold, 0.5))

    def _atajos(self):
        combinaciones = {
            "Return": self._igual,
            "Enter": self._igual,
            "Esc": lambda: self._presionar("C"),
            "Backspace": lambda: self._presionar("⌫"),
            "Ctrl+L": lambda: self._presionar("C"),
        }
        for secuencia, accion in combinaciones.items():
            atajo = QShortcut(QKeySequence(secuencia), self)
            atajo.setContext(Qt.WindowShortcut)
            atajo.activated.connect(accion)

    def keyPressEvent(self, evento):
        tecla = evento.text()
        if tecla:
            tecla = TECLAS_VISIBLES.get(tecla, tecla)
            if tecla.isdigit() or tecla in ".+-*/%()±":
                self._presionar(tecla)
                return
        super().keyPressEvent(evento)

    def demostracion(self):
        for valor in ["(", "2", "+", "3", ")", "×", "4", "=",
                      "7", "+", "8", "×", "9", "="]:
            self._presionar(valor)

    def _presionar(self, valor):
        if valor == "C":
            self.expresion = ""
            self.error = False
            self.recien_igual = False
            self._estado("")
        elif valor == "⌫":
            self.error = False
            self.expresion = self.expresion[:-1]
        elif valor == "=":
            self._igual()
            return
        elif valor == "±":
            self._cambiar_signo()
            return
        else:
            self._ingresar(valor)
        self._pintar()

    def _ingresar(self, caracter):
        actual = self.expresion
        if self.error or (self.recien_igual and caracter not in SIMBOLOS):
            actual = ""

        if actual == "-0" and (caracter.isdigit() or caracter == "."):
            actual = ""

        if caracter == ".":
            if not actual or actual[-1] in SIMBOLOS:
                actual += "0"
            elif actual[-1] == ".":
                return
        elif caracter in SIMBOLOS and actual and actual[-1] in SIMBOLOS:
            actual = actual[:-1] + caracter

        self.expresion = actual + caracter
        self.error = False
        self.recien_igual = False
        self._estado("")

    def _cambiar_signo(self):
        texto = self.expresion
        if not texto:
            self.expresion = "-0"
            self._pintar()
            return

        inicio = len(texto)
        while inicio > 0 and (texto[inicio - 1].isdigit() or texto[inicio - 1] == "."):
            inicio -= 1

        numero = texto[inicio:]
        if not numero or numero == ".":
            self._estado("No hay un número al final")
            return

        self.expresion = f"{texto[:inicio]}(-{numero})"
        self.error = False
        self.recien_igual = False
        self._estado("")
        self._pintar()

    def _igual(self):
        expresion = self.expresion.rstrip(SIMBOLOS)
        if not expresion:
            return

        try:
            resultado = formatear(evaluar(expresion))
        except ZeroDivisionError:
            self._fallo("No se puede dividir entre cero")
            return
        except (SyntaxError, ValueError, TypeError, OverflowError):
            self._fallo("Expresión no válida")
            return

        self.historial.insertItem(0, f"{presentar(expresion)} = {resultado}")
        while self.historial.count() > MAX_HISTORIAL:
            self.historial.takeItem(self.historial.count() - 1)

        self.expresion = resultado
        self.error = False
        self.recien_igual = True
        self._estado("")
        self._pintar()

    def _fallo(self, mensaje):
        self.expresion = ""
        self.error = True
        self.recien_igual = False
        self._estado(mensaje)
        self._pintar()

    def _limpiar_historial(self):
        self.historial.clear()

    def _estado(self, mensaje):
        self.estado.setText(mensaje)
        self.estado.setStyleSheet(f"color: {COLOR_ERROR if mensaje else TEXTO_SUAVE};")

    def _pintar(self):
        self.entrada.setText(presentar(self.expresion) or "0")


def hay_pantalla():
    if sys.platform == "darwin" or sys.platform == "win32":
        return True
    if os.environ.get("QT_QPA_PLATFORM") == "offscreen":
        return False
    return bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))


def guardar_imagen(aplicacion, ventana, destino):
    ventana.resize(600, 460)
    ventana.show()
    ventana.demostracion()
    aplicacion.processEvents()
    if not ventana.grab().save(destino):
        print("No se pudo guardar la imagen en", destino)
        return 1
    print("Imagen de la calculadora guardada en", os.path.abspath(destino))
    return 0


def main():
    opciones = argparse.ArgumentParser(description="Calculadora Grafica 2.0")
    opciones.add_argument(
        "--captura",
        metavar="ARCHIVO",
        nargs="?",
        const="calculadora_2.0.png",
        help="Guarda la interfaz como imagen PNG en vez de abrir la ventana.",
    )
    argumentos = opciones.parse_args()

    if argumentos.captura or not hay_pantalla():
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

    aplicacion = QApplication([sys.argv[0]])
    aplicacion.setStyle("Fusion")
    ventana = Calculadora()
    ventana.setMinimumSize(560, 420)

    if argumentos.captura or not hay_pantalla():
        return guardar_imagen(aplicacion, ventana, argumentos.captura or "calculadora_2.0.png")

    ventana.show()
    return aplicacion.exec()


if __name__ == "__main__":
    raise SystemExit(main())