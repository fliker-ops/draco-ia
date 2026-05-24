import sys
import webbrowser
import threading
import speech_recognition
import speech_recognition as sr
import pyttsx3
import wikipedia
import requests
import pywhatkit
import speech_recognition as sr

from youtubesearchpython import VideosSearch

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QTextEdit
)

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QPen, QFont


# =====================================
# MOTOR DE VOZ
# =====================================

engine = pyttsx3.init()
engine.setProperty('rate', 170)

voices = engine.getProperty('voices')

if len(voices) > 0:
    engine.setProperty('voice', voices[0].id)


def hablar(texto):

    print(f"DRACO: {texto}")

    engine.say(texto)
    engine.runAndWait()


# =====================================
# CIRCULO FUTURISTA
# =====================================

class Circulo(QWidget):

    def __init__(self):

        super().__init__()

        self.angle = 0
        self.wave = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar)
        self.timer.start(30)

    def actualizar(self):

        self.angle += 3
        self.wave += 2

        if self.wave > 70:
            self.wave = 0

        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)

        center_x = self.width() // 2
        center_y = self.height() // 2

        # Ondas
        for i in range(5):

            radius = 90 + self.wave + (i * 25)

            alpha = 150 - (i * 20)

            pen = QPen(QColor(0, 255, 255, alpha))
            pen.setWidth(4)

            painter.setPen(pen)

            painter.drawEllipse(
                center_x - radius // 2,
                center_y - radius // 2,
                radius,
                radius
            )

        # Núcleo central
        pen = QPen(QColor(0, 255, 255))
        pen.setWidth(8)

        painter.setPen(pen)

        painter.drawEllipse(center_x - 55, center_y - 55, 110, 110)


# =====================================
# IA DRACO
# =====================================

class Draco(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("DRACO")

        self.resize(1000, 700)

        # transparente
        self.setAttribute(Qt.WA_TranslucentBackground)

        # sin bordes
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setWindowOpacity(0.96)

        layout = QVBoxLayout()

        layout.setContentsMargins(30, 30, 30, 30)

        # titulo
        self.titulo = QLabel("DRACO")

        self.titulo.setAlignment(Qt.AlignCenter)

        self.titulo.setFont(QFont("Arial", 30))

        self.titulo.setStyleSheet("""
            color: cyan;
            font-weight: bold;
        """)

        # circulo animado
        self.circulo = Circulo()
        self.circulo.setMinimumHeight(350)

        # chat visual estilo IA

        self.chat = QTextEdit()

        self.chat.setReadOnly(True)

        self.chat.setStyleSheet("""
            QTextEdit{
                background-color: rgba(0,0,0,120);
                border: 2px solid cyan;
                border-radius: 20px;
                color: white;
                padding: 15px;
                font-size: 16px;
            }
        """)

        self.chat.setHtml(
            "<span style='color:cyan;font-size:18px;'>DRACO iniciado...</span><br><br>"
        )

        # caja texto
        self.input = QLineEdit()

        self.input.setPlaceholderText("Habla con Draco...")

        self.input.returnPressed.connect(self.ejecutar)

        self.input.setStyleSheet("""
            QLineEdit{
                background-color: rgba(0,0,0,140);
                border: 3px solid cyan;
                border-radius: 18px;
                padding: 18px;
                color: white;
                font-size: 18px;
            }
        """)

        # boton microfono
        self.boton_microfono = QPushButton("🎤")

        self.boton_microfono.clicked.connect(self.activar_microfono)

        self.boton_microfono.setStyleSheet("""
            QPushButton{
                background-color: rgba(0,255,255,80);
                border-radius: 25px;
                color: white;
                font-size: 24px;
                padding: 12px;
            }

            QPushButton:hover{
                background-color: rgba(0,255,255,150);
            }
        """)

        layout.addWidget(self.titulo)
        layout.addWidget(self.circulo)
        layout.addWidget(self.chat)
        layout.addStretch()
        layout.addWidget(self.input)
        layout.addWidget(self.boton_microfono, alignment=Qt.AlignRight)

        self.setLayout(layout)

        hablar("Draco iniciado")

    # =====================================
    # EJECUTAR
    # =====================================

    def ejecutar(self):

        texto = self.input.text().lower().strip()

        self.chat.append(
            f"<div style='margin:10px;'>"
            f"<span style='color:#00ffff;font-weight:bold;'>TÚ:</span><br>"
            f"<span style='color:white;'>{texto}</span>"
            f"</div><br>"
        )

        self.input.clear()

        threading.Thread(target=self.procesar, args=(texto,)).start()

    # =====================================
    # PROCESAR
    # =====================================

    def procesar(self, texto):

        # ---------------------------------
        # ABRIR GOOGLE
        # ---------------------------------

        if "abre google" in texto:

            hablar("Abriendo Google")

            webbrowser.open("https://google.com")

        # ---------------------------------
        # ABRIR YOUTUBE
        # ---------------------------------

        elif "abre youtube" in texto:

            hablar("Abriendo YouTube")

            webbrowser.open("https://youtube.com")

        # ---------------------------------
        # BUSCAR EN GOOGLE
        # ---------------------------------

        elif "busca" in texto:

            busqueda = texto.replace("busca", "")

            hablar(f"Buscando {busqueda}")

            url = f"https://www.google.com/search?q={busqueda}"

            webbrowser.open(url)

        # ---------------------------------
        # REPRODUCIR MUSICA
        # ---------------------------------
        elif "pon" in texto or "reproduce" in texto:

            try:

                cancion = texto.lower()

                cancion = cancion.replace("pon", "")
                cancion = cancion.replace("reproduce", "")
                cancion = cancion.strip()

                hablar(f"Reproduciendo {cancion}")

                query = cancion.replace(" ", "%20")

                url = f"spotify:search:{query}"

                webbrowser.open(url)
            except Exception as e:

             print(e)

             hablar("No encontré la canción")
        # ---------------------------------
        # HORA
        # ---------------------------------

        elif "hora" in texto:

            from datetime import datetime

            hora = datetime.now().strftime("%H:%M")

            hablar(f"La hora es {hora}")

        # ---------------------------------
        # SALIR
        # ---------------------------------

        elif "salir" in texto:

            hablar("Hasta luego")

            sys.exit()

        # ---------------------------------
        # PREGUNTAS GENERALES
        # ---------------------------------

        else:

            try:

                wikipedia.set_lang("es")

                hablar("Investigando")

                respuesta = wikipedia.summary(texto, sentences=3)

                self.chat.append(
                    f"<div style='margin:10px;'>"
                    f"<span style='color:cyan;font-weight:bold;'>DRACO:</span><br>"
                    f"<span style='color:white;'>{respuesta}</span>"
                    f"</div><br>"
                )

                hablar(respuesta)

            except:

                try:

                    hablar("Buscando en internet")

                    url = f"https://www.google.com/search?q={texto}"

                    webbrowser.open(url)

                    hablar("No encontré una respuesta exacta pero abrí Google")

                except:

                    hablar("No entendí el comando")

    # =====================================
    # MICROFONO
    # =====================================

    def activar_microfono(self):

        threading.Thread(target=self.escuchar).start()

    def escuchar(self):

        recognizer = sr.Recognizer()

        with sr.Microphone() as source:

            hablar("Te escucho")

            recognizer.adjust_for_ambient_noise(source)

            audio = recognizer.listen(source)

            try:

                texto = recognizer.recognize_google(audio, language='es-ES')

                print(f"TÚ: {texto}")

                self.input.setText(texto)

                self.ejecutar()

            except:

                hablar("No entendí")


# =====================================
# INICIO
# =====================================

app = QApplication(sys.argv)

ventana = Draco()

ventana.show()

sys.exit(app.exec_())
