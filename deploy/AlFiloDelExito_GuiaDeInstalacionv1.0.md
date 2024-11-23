# Stock Track - Guia de Instalación

## Versión
- **Versión**: 1.0
- **Fecha de última actualización**: 23 de noviembre de 2024

## Descripción

Este proyecto está configurado para ser ejecutado en un servidor web utilizando Django. A continuación, se detallan los pasos necesarios para configurar el entorno e iniciar la aplicación.

# Configuración

*Nota: Los valores dentro de los corchetes angulares <> debe ser remplazado y los corchetes eliminados*

## 1.Requisitos

- **IDE de Desarrollo (App desarrollada en VSC)**
- **Python** (versión 3.12.4 o superior)
- **Git** para el versionamiento de cambios

## 2.Descarga del Proyecto
### Clonar el repositorio

1. Clonar el proyecto del repositorio anfitrion: `https://github.com/JoelDefaz/stock-track.git`.

## 3.Configuración

Sigue los pasos a continuación para configurar el servidor en **Django**

1. En el ambiente/carpeta preparada donde se encuentra el proyecto abrir la consola para crear un ambiente en python y que asi las libreraias no sean un problema, asi que ejecutamos el siguiente comando:
```
python -m venv <Nombre del ambiente>
```
Despues de ejecutar el comando, se deberia crear una carpeta con el nombre que declaramos, este es el ambiente.

*Nota: Si se diera un problema de que no se puede ejectar Scripts (En Windows) revisar*
[Problemas de ejecución de Scripts](#problemas-de-ejecución-de-scripts)


3. Una vez creado el ambiente vamos a activar el ambiente para realizar las instalaciones de las dependecias necesarias, asi que ejecutamos el siguiente comando:
comando
```
<Nombre del ambiente>/Scripts/Active
```
*Nota:Echo esto deberia mostrarse el nombre del ambiente a la derecha de la ruta actual de  trabajo*
```
(<Nombre del ambiente>) <Ruta actual de trabajo>
```
4. Activado el ambiente pasamos a instalar las dependecias necesarias, para ellos buscamos el archivo llamado **requirements.txt**, y en la consola ejecutamos el siguiente comando:
```
pip install -r <ruta>\requirements.txt 
```
5. Una vez termine de instalar las dependecias, ya se puede pasar a ejecutar el proyecto

## 4. Ejecutar el Proyecto

1. Para ejecutar el proyecto se necesita identificar el archivo **manage.py**. Una vez hecho, en la consola se ejecuta el siguiente comando:
```
python <ruta>/manage.py runserver
```
2. Asi generalmente ya se encuentra ejecutando el servidor y se podra visitar la pagina web en la direccion `http://localhost:8000/` o `http://127.0.0.1:8000/`

## Problemas con Django
Para cualquie problema relacionado con Django se puede buscar toda la documentación en: `https://docs.djangoproject.com/es/5.1/`

## Problemas de ejecución de Scripts

Si es un problema de permisos en el sistema que impide ejecutar scripts, es posible que la política de ejecución de PowerShell esté restringiendo la ejecución de scripts.

### Solución:
1. Verificar la Política de Ejecución en PowerShell
   - Abrir **PowerShell** como administrador.
   - Escribir el siguiente comando para ver la política de ejecución actual:
     ```powershell
     Get-ExecutionPolicy
     ```
   - Si se ve que la política está configurada en `Restricted`, significa que los scripts están bloqueados.

2. Cambiar la Política de Ejecución
   - Para permitir la ejecución de scripts locales, cambiar la política de ejecución a `RemoteSigned`. Esto permitirá ejecutar scripts locales sin restricciones.
   - Ejecutar el siguiente comando en PowerShell (también debe estar abierto como administrador):
     ```powershell
     Set-ExecutionPolicy RemoteSigned
     ```
   - Finalmente confirmar el cambio.

3. Con esto deberia solucionarse y se puede continuar la [configuración](#configuración)