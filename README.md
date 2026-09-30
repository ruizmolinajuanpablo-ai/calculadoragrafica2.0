CALCULADORA GRAFICA 2.0
========================

Descripcion
-----------
Calculadora de escritorio escrita en Python con PySide6 (Qt). Admite las
operaciones +, -, *, /, %, parentesis, cambio de signo y borrado. Muestra la
expresion en curso, guarda las ultimas 5 operaciones en un historial y avisa
cuando la expresion no es valida (por ejemplo, al dividir entre cero).

Es la misma calculadora que pract2_calc.py, pero con PySide6 en lugar de
Tkinter. En macOS, tk.Button ignora el color de fondo, por lo que los botones
oscuros con texto blanco se veian blancos sobre blanco. Con PySide6 los colores
si se aplican y por eso aqui los botones se dibujan con QPushButton y un tema
oscuro propio (fondo degradado azul petroleo, operadores turquesa, igual coral).

El archivo es autonomo: no necesita imagenes, sonidos ni ningun otro archivo de
datos. Por eso se puede copiar tal cual a otro equipo.


Libreria utilizada
------------------
PySide6 (la biblioteca que aporta los widgets de la interfaz). Es la diferencia
respecto de la version 1, que usa Tkinter.

Bibliotecas estandar de apoyo:
  ast        analiza y evalua la expresion de forma segura (no usa eval).
  operator   aplica las operaciones aritmeticas.
  argparse   procesa la opcion --captura y --help.
  os         comprueba si hay pantalla y cual es el nombre del archivo.


Requisitos
----------
Un Python con PySide6 instalado. PySide6 no tiene versiones para Python 3.14,
asi que en este equipo se usa el Python 3.9.6 del sistema (/usr/bin/python3),
que es el unico que lo tiene instalado:

  /usr/bin/python3 -m pip install --user PySide6      Instalar (una sola vez)
  /usr/bin/python3 -c "import PySide6"               Comprobar

Atencion: en este Mac hay dos Pythons y solo uno sirve.

  /usr/bin/python3        3.9.6    PySide6 6.9.3  --> este es el correcto
  /usr/local/bin/python3  3.14.4   sin PySide6   --> no sirve para la 2.0

Por eso el shebang de la primera linea del archivo apunta a /usr/bin/python3, y
por eso hay que lanzar el programa con ese Python y no con "python3" a secas.


Como ejecutarlo en este Mac
--------------------------
1) Doble clic en "Calculadora 2.0.app" (la forma mas comoda).
2) Visual Studio Code: abrir la carpeta, elegir la configuracion "2.0 - PySide6"
   en el desplegable de depuracion y pulsar F5.
3) Terminal:
     /usr/bin/python3 "calculadora grafica 2.0.py"
4) Desde la propia carpeta, gracias al shebang y al permiso de ejecucion:
     "./calculadora grafica 2.0.py"


Opciones del programa
---------------------
  --captura              Guarda la interfaz en un PNG y no abre la ventana.
  --captura ruta.png     Guarda la imagen con ese nombre.
  --help                 Muestra la ayuda.

Sin argumentos, en un equipo con pantalla, abre la ventana.


Visual Studio Code
------------------
La carpeta .vscode/ trae la configuracion ya hecha:

  .vscode/settings.json   Fija /usr/bin/python3 como interprete del proyecto.
  .vscode/launch.json     Dos configuraciones de depuracion:
                            "2.0 - PySide6"  -> /usr/bin/python3
                            "1.0 - Tkinter"  -> /usr/local/bin/python3

Las dos son necesarias porque la 1.0 necesita Tk 8.6, que no trae el Python
3.9 del sistema, y la 2.0 necesita PySide6, que no tiene version para 3.14.

Si el boton de ejecutar (>) no responde la primera vez, hay que elegir el
interprete a mano una sola vez: Cmd+Shift+P, "Python: Select Interpreter" y
/usr/bin/python3. A partir de ahi se recuerda solo.


Ejecutarlo en otros dispositivos
--------------------------------
El archivo se copia tal cual. Lo unico que cambia es el comando de instalacion
y el de ejecucion, porque cada sistema tiene susPython y sus librerias.

macOS (otro equipo)
  /usr/bin/python3 -m pip install --user PySide6
  /usr/bin/python3 "calculadora grafica 2.0.py"
  Si el Python del sistema no sirve, instalar uno propio (python.org) y usar
  la ruta completa de ese Python. El archivo "Calculadora 2.0.app" y su icono
  son opcionales: son solo una comodidad del Finder.

Windows
  py -m pip install PySide6
  py "calculadora grafica 2.0.py"
  El archivo .app y su lanzador son de macOS y no se usan. Se puede crear un
  acceso directo apuntando a pythonw.exe con el archivo como argumento, para
  que no aparezca la ventana de consola.
  Si la consola muestra caracteres raros en vez de tildes, usar:
     chcp 65001
     py -X utf8 "calculadora grafica 2.0.py"
  El archivo esta guardado en UTF-8 y contiene tildes, por eso conviene no
  guardarlo con otra codificacion al editarlo.

Linux
  sudo apt install python3 python3-pip
  pip install PySide6      (o: pip install --break-system-packages PySide6)
  python3 "calculadora grafica 2.0.py"
  Si la ventana no abre y Qt se queja del plugin de pantalla, faltan librerias
  del sistema:
     sudo apt install libgl1 libegl1 libxkbcommon-x11-0 libxcb-cursor0 \
                      libxcb-icccm4 libxcb-keysyms1 libxcb-shape0 \
                      libdbus-1-3 libfontconfig1
  En un servidor sin monitor, genera automaticamente un PNG en vez de ventana.

Replit
  Usar la plantilla "GUI" (Python) para tener pantalla. En la Shell:
     pip install PySide6
  Con esa plantilla funciona la ventana con normalidad. Sin ella, el programa
  genera el PNG.

Google Colab / JupyterLite / otros cuadernos
  No hay monitor, asi que la ventana no se veria. El programa lo detecta y
  guarda la interfaz en un PNG, asi que se puede pegar y ejecutar tal cual:
     %pip install PySide6
     !python "calculadora grafica 2.0.py" --captura calculadora.png
     from IPython.display import Image, display; display(Image("calculadora.png"))
  El PNG tambien se puede ver en el explorador de archivos de Colab.

Android / iPad
  En Android, Pydroid 3 permite instalar PySide6 desde el propio gestor de
  paquetes (Settings -> Pip). En iPad no hay PySide6; habria que usar una
  aplicacion web o Servo, que ya expone la version web en un navegador.


Sugerencias para que funcione bien
----------------------------------
1) Ejecutar siempre con un Python que tenga PySide6. Si aparece
   "No module named 'PySide6'", casi siempre es que se esta usando el
   interprete equivocado: se comprueba con
   /usr/bin/python3 -c "import PySide6; print(PySide6.__version__)".
2) No editar la copia que hay dentro de "Calculadora 2.0.app". La app usa el
   archivo de la carpeta cuando macOS le deja leerlo, y solo recurre a la copia
   interna cuando no puede. Si se edita el equivocado, el cambio no se ve.
3) Guardar el archivo en UTF-8. Contiene tildes y el signo de multiplicar y
   division; si se guarda en otra codificacion aparecen caracteres raros.
4) Mantener el shebang de la primera linea apuntando a un Python con PySide6 si
   se quiere seguir usando el doble clic o "./archivo.py".
5) No renombrar el archivo de la copia interna de la app sin cambiar tambien
   el lanzador, que la busca con el mismo nombre.
6) Para subir la version 2.0 a la carpeta, basta con copiar el .py. No depende
   del icono ni de la app.
7) Comprobacion rapida de que todo sigue bien:
     /usr/bin/python3 "calculadora grafica 2.0.py" --captura /tmp/prueba.png
   Si crea el PNG, el interprete, PySide6 y la interfaz estan bien.


Problemas frecuentes y su solucion
----------------------------------
  "No module named 'PySide6'"
      Se esta usando un Python sin PySide6 ( casi siempre el 3.14 ).
      Solucion: usar /usr/bin/python3, o instalar PySide6 en ese Python.

  "qt.qpa.plugin: Could not load the Qt platform plugin xcb"
      Faltan librerias del sistema en Linux.
      Solucion: instalar las librerias del apartado de Linux.

  "could not connect to display" / "no $DISPLAY environment variable"
      El equipo no tiene monitor (servidor, contenedor, cuaderno online).
      Solucion: el programa ya lo detecta y guarda un PNG. Tambien se puede
      forzar con --captura.

  La ventana sale en blanco
      En Linux suele ser el mismo problema del plugin xcb. En macOS, comprobar
      que se abrio con Python y no con doble clic sobre el .py, que el Finder
      abre en el editor.

  La app no arranca y dice "Operation not permitted"
      macOS no deja que una app del Escritorio lea archivos de ~/Desktop.
      Solucion: el codigo esta tambien dentro de
      Calculadora 2.0.app/Contents/Resources/, que es la copia que se usa.

  Los acentos se ven como simbolos raros en la consola de Windows
      Solucion: chcp 65001, o ejecutar con python -X utf8.


Archivos del proyecto
---------------------
  calculadora grafica 2.0.py   Codigo fuente de la version 2.0 (PySide6)
  .vscode/settings.json        Interprete del proyecto para Visual Studio Code
  .vscode/launch.json          Configuraciones de depuracion de VS Code
  README 2.0.txt               Este documento
  Calculadora 2.0.app          Aplicacion de macOS (comodidad para el Finder)
  Practica 1
    pract2_calc.py             Version 1 con Tkinter (tambien genera la app)
    README.txt                 Documentacion de la version 1
    Calculadora.app            Aplicacion de la version 1
    Calculadora.icns           Icono de la aplicacion
    Calculadora.iconset/       Icono en varios tamanos


Notas tecnicas
--------------
- Las expresiones se validan con el modulo ast, nunca con eval, asi que no se
  puede ejecutar codigo arbitrario desde el teclado.
- Solo se permiten numeros y los operadores + - * / % con parentesis. Cualquier
  otra cosa se rechaza con "Expresion no valida".
- La division por cero se captura aparte para poder decir "No se puede dividir
  entre cero" en lugar de un error generico.
- Por dentro se trabaja con los operadores de ASCII (* / -) y al mostrarlos se
  convierten a x, division y menos tipografico, que se ven mejor en pantalla.
- El tema se define en una hoja de estilos (ESTILO) aplicada a toda la ventana,
  con QSizePolicy para que los botones crezcan con la ventana.
- En modo --captura se usa la plataforma "offscreen" de Qt, que dibuja la
  interfaz sin necesidad de monitor, y ventana.grab() devuelve la imagen.
