# RiskTracker Chatbot API

Este repositorio contiene el código fuente para el backend del Asistente Virtual (Chatbot) del proyecto RiskTracker. Es una API construida con **Python** y **FastAPI** que utiliza modelos de **Inteligencia Artificial** (`sentence-transformers`) para realizar búsqueda semántica sobre una base de conocimiento en formato JSON.

Su función principal es recibir una pregunta de un usuario, entender su significado (en lugar de solo buscar palabras clave) y encontrar la respuesta más relevante dentro de su base de conocimiento.

## 1. Prerrequisitos

Antes de comenzar, asegúrate de tener instalado el siguiente software en tu máquina:

- **Docker:** El motor para ejecutar contenedores. [Descargar Docker Desktop](https://www.docker.com/products/docker-desktop/).
- **Docker Compose:** La herramienta para orquestar aplicaciones multi-contenedor. Usualmente viene incluida con Docker Desktop.
- **Git:** Para clonar este repositorio.

### Requisito Fundamental

Este servicio está diseñado para funcionar como un microservicio que se conecta a un **API Gateway Kong existente**. Por lo tanto, es **indispensable** que el entorno principal de Docker del proyecto RiskTracker (que incluye a Kong) esté **en ejecución antes de iniciar este chatbot**.

## 2. Instalación y Puesta en Marcha

Sigue estos pasos para configurar y ejecutar el chatbot por primera vez.

### Paso 1: Clonar el Repositorio

Abre una terminal y clona este proyecto en tu máquina.

```bash
git clone <URL_del_repositorio_del_chatbot>
cd RiskTracker.ChatBot```

### Paso 2: Configurar la Red de Conexión

Este servicio necesita saber a qué red de Docker, creada por Kong, debe conectarse.

1.  **Encuentra el nombre de la red de Kong:**
    -   Abre una terminal y ejecuta `docker ps` para encontrar el nombre de tu contenedor de Kong (ej. `risktrackerdocker-kong-gateway-1`).
    -   Luego, ejecuta `docker inspect <nombre_del_contenedor_kong>` y busca en la salida la sección `"Networks"`. El nombre completo de la red estará ahí (ej. `risktrackerdocker_kong-net`).

2.  **Actualiza el archivo `docker-compose.yml`:**
    -   Abre el archivo `docker-compose.yml` de este proyecto.
    -   Busca y reemplaza las dos instancias de `nombre_de_la_red_de_kong` con el nombre real que encontraste.

    ```yaml
    # docker-compose.yml
    services:
      chatbot:
        # ...
        networks:
          # Reemplaza esta línea con el nombre real de la red
          - risktrackerdocker_kong-net

    networks:
      # Y reemplaza esta línea también
      risktrackerdocker_kong-net:
        external: true
    ```

### Paso 3: Construir y Ejecutar el Contenedor

Una vez configurada la red, ejecuta el siguiente comando desde la raíz del proyecto del chatbot. Este comando construirá la imagen de Docker por primera vez y levantará el contenedor.

```bash
docker-compose up --build