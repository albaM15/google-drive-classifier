# 🗂️ Google Drive Classifier

Clasificador automático de archivos de Google Drive utilizando IA (Google Gemini API). Este proyecto extrae el contenido de tus archivos en Google Drive y los clasifica automáticamente en categorías relevantes.

## 📋 Requisitos

- Python 3.8 o superior
- Una cuenta de Google
- Acceso a Google Cloud Console
- API Key de Google Gemini

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd google-drive-classifier
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Linux/macOS
# o
venv\Scripts\activate  # En Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## ⚙️ Configuración

### 1. Configurar Google Cloud Console

#### a) Crear un proyecto en Google Cloud

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Anota el ID del proyecto

#### b) Habilitar la API de Google Drive

1. En el menú lateral, ve a **"APIs y servicios"** → **"Biblioteca"**
2. Busca **"Google Drive API"**
3. Haz clic en **"Habilitar"**

#### c) Crear credenciales OAuth 2.0

1. Ve a **"APIs y servicios"** → **"Credenciales"**
2. Haz clic en **"+ CREAR CREDENCIALES"**
3. Selecciona **"ID de cliente de OAuth"**
4. Tipo de aplicación: **"Aplicación de escritorio"**
5. Dale un nombre (ejemplo: "Drive Classifier")
6. Haz clic en **"Crear"**
7. Descarga el archivo JSON de credenciales

#### d) Configurar la pantalla de consentimiento OAuth

1. Ve a **"APIs y servicios"** → **"Pantalla de consentimiento de OAuth"**
2. Selecciona **"Externo"** (o "Interno" si tienes Google Workspace)
3. Completa la información básica:
   - Nombre de la aplicación
   - Correo electrónico de asistencia
   - Correo electrónico del desarrollador
4. Haz clic en **"Guardar y continuar"**
5. En **"Ámbitos"**, puedes omitir por ahora y hacer clic en **"Guardar y continuar"**
6. **IMPORTANTE**: En la sección **"Usuarios de prueba"**:
   - Haz clic en **"+ AGREGAR USUARIOS"**
   - Agrega tu dirección de correo electrónico de Google
   - Haz clic en **"Guardar"**

#### e) Guardar las credenciales

1. Renombra el archivo descargado a `credentials.json`
2. Muévelo a la raíz del proyecto:
   ```bash
   mv ~/Downloads/client_secret_*.json ./credentials.json
   ```

### 2. Configurar la API de Gemini

#### a) Obtener API Key de Gemini

1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Haz clic en **"Create API Key"**
3. Copia la clave generada

#### b) Crear archivo de variables de entorno

1. Crea un archivo `.env` en la raíz del proyecto:
   ```bash
   touch .env
   ```

2. Abre el archivo y agrega tu API key:
   ```
   GEMINI_API_KEY=tu_api_key_aqui
   ```

## 🔐 Autenticación

Antes de usar la aplicación por primera vez, debes autenticarte con Google:

```bash
python auth.py
```

**Pasos:**
1. Se abrirá una ventana del navegador
2. Selecciona tu cuenta de Google (debe ser la misma que agregaste como usuario de prueba)
3. Si aparece una advertencia "Google hasn't verified this app", haz clic en **"Continuar"** o **"Advanced"** → **"Go to [app name]"**
4. Acepta los permisos solicitados
5. Cuando veas el mensaje "The authentication flow has completed", cierra la ventana
6. Se habrá generado el archivo `token.json`

> **Nota:** El archivo `token.json` contiene tus credenciales de acceso y se renovará automáticamente cuando expire.

## 🎯 Uso

Ejecuta el clasificador:

```bash
python main.py
```

El script:
1. Se conectará a tu Google Drive
2. Obtendrá una lista de archivos (por defecto, los primeros 10)
3. Extraerá el contenido de cada archivo
4. Usará IA para clasificarlo en categorías
5. Mostrará los resultados en la consola

### Ejemplo de salida

```
Archivo: Reporte_Ventas_2024.pdf -> Categoría: Finanzas
Archivo: Receta_Pastel.docx -> Categoría: Recetas
Archivo: Tarea_Matemáticas.pdf -> Categoría: Educación
```

## 📁 Estructura del proyecto

```
google-drive-classifier/
│
├── auth.py              # Script de autenticación OAuth
├── main.py              # Script principal
├── config.py            # Configuración y variables
├── drive_utils.py       # Utilidades para Google Drive
├── ai_classifier.py     # Clasificador con IA (Gemini)
├── requirements.txt     # Dependencias del proyecto
│
├── .env                 # Variables de entorno (NO COMMITEAR)
├── credentials.json     # Credenciales OAuth (NO COMMITEAR)
├── token.json          # Token de acceso (NO COMMITEAR)
│
└── venv/               # Entorno virtual
```

## 🔧 Solución de problemas

### Error: `ModuleNotFoundError: No module named 'google_auth_oauthlib'`

**Solución:** Asegúrate de haber activado el entorno virtual e instalado las dependencias:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Error: `403: access_denied` durante la autenticación

**Solución:** Debes agregar tu cuenta como usuario de prueba en Google Cloud Console:
1. Ve a **"APIs y servicios"** → **"Pantalla de consentimiento de OAuth"**
2. En la sección **"Usuarios de prueba"**, agrega tu correo electrónico
3. Guarda los cambios
4. Vuelve a ejecutar `python auth.py`

### Error: `No encuentro 'credentials.json'`

**Solución:** Asegúrate de haber descargado las credenciales OAuth desde Google Cloud Console y de haberlas guardado como `credentials.json` en la raíz del proyecto.

### El navegador no se abre automáticamente

**Solución:** Copia manualmente la URL que aparece en la terminal y ábrela en tu navegador.

## 🔒 Seguridad

> ⚠️ **ADVERTENCIA:** Nunca compartas ni subas a repositorios públicos los siguientes archivos:
> - `.env` (contiene tu API key)
> - `credentials.json` (contiene tus credenciales OAuth)
> - `token.json` (contiene tu token de acceso)

Estos archivos ya están incluidos en el `.gitignore` para evitar subirlos accidentalmente.

## 📝 Licencia

Este proyecto es de código abierto. Siéntete libre de usarlo y modificarlo según tus necesidades.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request para sugerencias y mejoras.

---

**Desarrollado con ❤️ usando Python, Google Drive API y Google Gemini AI**
