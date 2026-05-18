---
trigger: always_on
---



### Reglas Generales del Método ADD (Contexto del Sistema)

*   **Regla de Enfoque:** El sistema debe diseñarse iterativamente aplicando la filosofía de "divide y vencerás", descomponiendo elementos de manera recursiva.
*   **Regla de Responsabilidad (Participante):** Las decisiones de este método recaen y son ejecutadas únicamente por el "Arquitecto".
*   **Regla de Entrada:** El proceso siempre debe ser alimentado por los *drivers* arquitectónicos (una lista que incluye requerimientos funcionales primarios, escenarios de atributos de calidad y restricciones).
*   **Regla de Salida:** El resultado tangible que debe generar el sistema al aplicar el método son "esbozos de vistas" (modelos, diagramas y descripciones de responsabilidades).
*   **Regla de Terminación:** Las iteraciones de diseño se detienen únicamente cuando se han tomado suficientes decisiones para satisfacer todos los *drivers* o requerimientos.

### Reglas de Ejecución (El flujo de trabajo de 8 pasos)

El workspace debe seguir este ciclo recursivo para diseñar la arquitectura:

1.  **Regla de Confirmación:** Antes de iniciar, asegurar que se cuenta con información suficiente, clara y priorizada sobre los *drivers* arquitectónicos del sistema.
2.  **Regla de Selección de Elemento:** Elegir un elemento para descomponer. Si es el inicio del proyecto, el elemento es el "sistema completo". En ciclos posteriores, será un sub-elemento resultante de una iteración previa.
3.  **Regla de Asociación de *Drivers*:** Filtrar e identificar qué *drivers* del conjunto inicial están directamente relacionados con el elemento específico que se va a descomponer en esta iteración.
4.  **Regla de Aplicación de Conceptos:** Elegir un concepto de diseño general que satisfaga los *drivers* del elemento. Es obligatoria la selección y aplicación de **patrones de diseño** (para la estructura) y **tácticas** (para controlar las métricas de calidad).
5.  **Regla de Instanciación:** Crear las instancias de los nuevos sub-elementos derivados de aplicar los patrones elegidos y documentar formalmente las responsabilidades de cada uno.
6.  **Regla de Definición de Interfaces:** Identificar las propiedades de los nuevos elementos creados y establecer las interfaces (los contratos o formas de comunicación) entre ellos.
7.  **Regla de Verificación y Restricción:** Revisar si los *drivers* asociados al elemento se han satisfecho. Si es así, transformar estos *drivers* en nuevas "restricciones" técnicas para los sub-elementos recién creados.
8.  **Regla de Recursividad:** Evaluar si los elementos instanciados necesitan más detalle. Si es así, repetir el flujo desde el paso 2 con cada sub-elemento, hasta que la mayoría de los *drivers* globales se hayan cubierto.