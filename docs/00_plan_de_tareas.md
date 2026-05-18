---
Ruta: /docs/00_plan_de_tareas.md
Nivel de Abstracción: N/A (Planificación del Proyecto)
Reglas Aplicadas: M-01
Version: 1.0.0
---

# 📋 Plan de Tareas — Fase 5: Validación Integral y Sustentación

> **Curso:** Estructuras de Datos — UNAD  
> **Estudiante:** Santiago Villa  
> **Fecha:** 18 de mayo de 2026  

---

## 🎯 Objetivo General

Integrar las tres aplicaciones desarrolladas individualmente en las Fases 2, 3 y 4 en una **única solución unificada** llamada **"Evaluación Final"**, con un sistema de login centralizado y un menú principal que permita acceder a cada aplicación. Adicionalmente, generar el documento académico final con normas APA.

---

## 📦 Inventario de Aplicaciones Existentes

| Fase | Nombre de la Aplicación | Tecnología | Estructura de Datos |
|------|-------------------------|------------|---------------------|
| **Fase 2** | Sistema de Nómina — Constructora Mejor | Python + Tkinter (Arquitectura Hexagonal) | Clases y Objetos (POO, Abstracción, Encapsulamiento) |
| **Fase 3** | Control de Afiliados — Compensándote | Python + Tkinter (3 Capas / MVC simplificado) | Pila, Cola y Lista |
| **Fase 4** | Árbol Binario de Búsqueda | Python + Tkinter (MVC) | Árbol Binario de Búsqueda (BST) |

---

## 🗂️ Estructura de Tareas

### ETAPA 1: Preparación del Proyecto Unificado

#### Tarea 1.1 — Crear la estructura del proyecto "Evaluación Final"
- [ ] Crear el directorio raíz del proyecto dentro del workspace de Fase 5
- [ ] Definir la estructura de carpetas del proyecto integrador
- [ ] Configurar el entorno virtual de Python (`.venv`)
- [ ] Crear el archivo `requirements.txt` con las dependencias necesarias (`tkcalendar`, etc.)
- [ ] Crear el `main.py` como punto de entrada principal

> **Estructura propuesta:**
> ```
> evaluacion_final/
> ├── main.py                  ← Punto de entrada principal
> ├── requirements.txt
> ├── login_window.py          ← Ventana de login centralizado
> ├── menu_principal.py        ← Menú con las 4 opciones
> ├── fase2_nomina/            ← Copia adaptada de Fase 2
> ├── fase3_afiliados/         ← Copia adaptada de Fase 3
> └── fase4_arbol/             ← Copia adaptada de Fase 4
> ```

**Criterio de Aceptación:** El proyecto se crea limpiamente, se puede activar el entorno virtual y las dependencias se instalan sin errores.

---

### ETAPA 2: Desarrollo de la Interfaz de Login Centralizada

#### Tarea 2.1 — Implementar la ventana de Login
- [ ] Crear `login_window.py` con interfaz gráfica Tkinter
- [ ] Mostrar el nombre de la aplicación: **"Evaluación Final"**
- [ ] Mostrar el nombre del estudiante: **Santiago Villa**
- [ ] Incluir una caja de texto para la contraseña de acceso
- [ ] La contraseña genérica válida es: **`8246`**
- [ ] Si la contraseña es correcta → abrir el menú principal
- [ ] Si la contraseña es incorrecta → mostrar mensaje de error y limpiar el campo
- [ ] Diseño profesional con paleta de colores coherente

**Criterio de Aceptación:** Al ejecutar `main.py`, se muestra la ventana de login. Solo con la contraseña `8246` se accede al menú principal.

---

### ETAPA 3: Desarrollo del Menú Principal

#### Tarea 3.1 — Implementar la ventana del Menú Principal
- [ ] Crear `menu_principal.py` con las 4 opciones del menú
- [ ] **Opción 1:** "Aplicación Fase 2 — Nómina Constructora Mejor" → Lanza la app de Fase 2
- [ ] **Opción 2:** "Aplicación Fase 3 — Control de Afiliados Compensándote" → Lanza la app de Fase 3
- [ ] **Opción 3:** "Aplicación Fase 4 — Árbol Binario de Búsqueda" → Lanza la app de Fase 4
- [ ] **Opción 4:** "Salir de la aplicación" → Cierra la aplicación completa
- [ ] Diseño visual con botones claros, descripción de cada opción e iconos representativos
- [ ] Cada opción debe abrir la aplicación correspondiente **sin solicitar contraseña adicional**

**Criterio de Aceptación:** Al seleccionar cualquier opción del menú, la aplicación correspondiente se abre directamente (sin login individual). Al cerrar la sub-aplicación, se regresa al menú principal.

---

### ETAPA 4: Integración de las Aplicaciones

#### Tarea 4.1 — Integrar la Fase 2 (Nómina — Constructora Mejor)
- [ ] Copiar los módulos de la Fase 2 al directorio `fase2_nomina/`
- [ ] Refactorizar para eliminar cualquier login o autenticación propia
- [ ] Adaptar los imports y rutas relativas para funcionar dentro del proyecto integrador
- [ ] Crear un punto de entrada `lanzar()` que pueda ser invocado desde el menú principal
- [ ] Verificar que al cerrar la ventana de la Fase 2 se regrese al menú principal

**Criterio de Aceptación:** La app de Nómina se ejecuta correctamente desde el menú, con todas sus funcionalidades (Calcular Pago, Guardar, Reporte), sin pedir contraseña.

#### Tarea 4.2 — Integrar la Fase 3 (Afiliados — Compensándote)
- [ ] Copiar los módulos de la Fase 3 al directorio `fase3_afiliados/`
- [ ] **Eliminar** la pantalla de login (`LoginApp`) de la Fase 3 (contraseña actual: `"Caja"`)
- [ ] Adaptar `FormularioPrincipal` para que pueda ser lanzado directamente
- [ ] Adaptar los imports y rutas relativas
- [ ] Crear un punto de entrada `lanzar()` invocable desde el menú principal
- [ ] Verificar que Pila, Cola y Lista funcionan correctamente (registrar, eliminar, reportes)

**Criterio de Aceptación:** La app de Afiliados se abre directamente al formulario principal, sin login, con todas las funcionalidades de Pila/Cola/Lista operativas.

#### Tarea 4.3 — Integrar la Fase 4 (Árbol Binario de Búsqueda)
- [ ] Copiar los módulos de la Fase 4 al directorio `fase4_arbol/`
- [ ] **Eliminar** la pantalla de login (`LoginWindow`) de la Fase 4
- [ ] Adaptar `MainWindow` para que se lance directamente con el `Controlador`
- [ ] Adaptar los imports y rutas relativas
- [ ] Crear un punto de entrada `lanzar()` invocable desde el menú principal
- [ ] Verificar que el árbol binario funciona: inserción, eliminación, recorridos (Inorden, Preorden, Postorden), y visualización gráfica

**Criterio de Aceptación:** La app del Árbol Binario se abre directamente a la ventana principal, sin login, con la funcionalidad completa de BST y visualización gráfica.

---

### ETAPA 5: Pruebas de Integración

#### Tarea 5.1 — Validación completa del flujo integrado
- [ ] Ejecutar `main.py` y verificar el flujo completo: Login → Menú → App → Menú
- [ ] Verificar que la contraseña `8246` funciona y cualquier otra es rechazada
- [ ] Probar Opción 1 (Fase 2): registrar empleado, calcular pago, generar reporte
- [ ] Probar Opción 2 (Fase 3): registrar afiliados en Pila, Cola y Lista; eliminar; generar reportes
- [ ] Probar Opción 3 (Fase 4): insertar nodos, recorrer el árbol, visualizar gráficamente
- [ ] Probar Opción 4: la aplicación se cierra completamente
- [ ] Verificar que cerrar una sub-app retorna al menú sin errores
- [ ] Verificar que no hay conflictos de instancias Tk (solo un `mainloop` activo)

**Criterio de Aceptación:** El flujo completo funciona sin errores, crasheos ni conflictos de ventanas Tkinter.

---

### ETAPA 6: Documento Académico Final

#### Tarea 6.1 — Generar el documento "Fase5Santiago_Villa"
- [ ] **Página 1 — Portada APA:**
  - Título del trabajo
  - Nombre del estudiante: Santiago Villa
  - Nombre del curso: Estructuras de Datos
  - Universidad: UNAD
  - Fecha de entrega
- [ ] **Página 2 — Introduction (en inglés):**
  - Contextualizar el propósito de la actividad integradora
  - Describir las tres fases y sus estructuras de datos
  - Explicar el objetivo de la integración
- [ ] **Página 3 — Objectives (en inglés):**
  - Objetivo general de la validación integral
  - Objetivos específicos alineados con RAC 1, RAC 2 y RAC 3
- [ ] **Página 4 — Conclusions (en inglés):**
  - Reflexión sobre los aprendizajes del curso
  - Conexión entre POO y estructuras de datos
  - Valor de la integración como demostración de competencias
- [ ] **Página 5 — Bibliographic References (APA 7ª edición):**
  - Fuentes bibliográficas del curso
  - Documentación oficial de Python y Tkinter

**Criterio de Aceptación:** El documento cumple con la estructura solicitada, las secciones en inglés están correctamente redactadas, y las referencias siguen APA 7ª edición.

---

## 📊 Resumen de Tareas

| # | Tarea | Etapa | Estado |
|---|-------|-------|--------|
| 1.1 | Crear estructura del proyecto | Preparación | ⬜ Pendiente |
| 2.1 | Implementar ventana de Login | Login | ⬜ Pendiente |
| 3.1 | Implementar menú principal | Menú | ⬜ Pendiente |
| 4.1 | Integrar Fase 2 (Nómina) | Integración | ⬜ Pendiente |
| 4.2 | Integrar Fase 3 (Afiliados) | Integración | ⬜ Pendiente |
| 4.3 | Integrar Fase 4 (Árbol Binario) | Integración | ⬜ Pendiente |
| 5.1 | Pruebas de integración | Pruebas | ⬜ Pendiente |
| 6.1 | Documento académico final | Documentación | ⬜ Pendiente |

---

## ⚠️ Consideraciones Técnicas Importantes

1. **Un solo `Tk()` root:** Tkinter solo permite una instancia principal `Tk()`. Las sub-aplicaciones deben abrirse como `Toplevel` o destruir/recrear ventanas cuidadosamente para evitar conflictos.
2. **Contraseña centralizada:** Solo el login principal valida con `8246`. Las apps individuales deben eliminar sus propios mecanismos de autenticación.
3. **Independencia de imports:** Al mover código a subdirectorios, se deben agregar `__init__.py` y adaptar `sys.path` para que los imports funcionen correctamente.
4. **Dependencia externa:** La Fase 3 usa `tkcalendar` (DateEntry), que debe incluirse en los requisitos del proyecto unificado.
