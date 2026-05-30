# People Analytics — Evaluación Inteligente de Proveedores de Capacitación PCI DSS
**Resumen del proyecto · Mayo 2025**
*Autores: Osvaldo Ceballos O. · Yerko Fuentes · Paloma San Martin*

---

## 1. Contexto del Proyecto

La empresa tiene la **obligación regulatoria** de certificar al 100% de sus colaboradores en el estándar **PCI DSS** (Payment Card Industry Data Security Standard). Para los cursos básicos de cumplimiento, coexisten **tres proveedores de capacitación online** que deben ser evaluados analíticamente.

El objetivo del proyecto es generar un **criterio basado en datos** para seleccionar al proveedor más efectivo, superando la métrica tradicional de porcentaje de cobertura.

---

## 2. Situación Actual

### Operación hoy
- Los **tres proveedores coexisten simultáneamente**.
- La asignación de colaboradores a cada proveedor **no responde a efectividad**, sino a disponibilidad de **cupos (capacity) por área funcional**.
- El éxito se mide por **% de cobertura** (colaboradores que completaron el curso), práctica estándar en L&D.

### Por qué la métrica de cobertura no sirve en este contexto

| # | Problema | Detalle |
|---|---|---|
| 01 | **Cobertura 100% es obligatoria** | Si alguien reprueba, debe repetir el curso. La métrica no discrimina entre proveedores: todos deben llegar al 100% de todas formas. |
| 02 | **Vacaciones y ausencias se reagendan** | Quien esté fuera del ciclo activo se reprograma en el siguiente. El % puntual genera una falsa imagen de avance. |
| 03 | **No mide lo que importa** | Completar un curso ≠ aprender. No captura si el colaborador adquirió el conocimiento que reduce el riesgo normativo real. |

> **Conclusión:** Medir con % de cobertura en un contexto de certificación obligatoria al 100% no diferencia proveedores. Se necesitan métricas que capturen ROI normativo y efectividad real de aprendizaje.

---

## 3. Las 2 Dimensiones de Evaluación

### Dimensión 1 — ROI Normativo
- **Qué mide:** Costo del proveedor versus su impacto en evitar multas y riesgo normativo.
- **Lógica:** ¿Cuánto cuesta cada proveedor en relación a la exposición regulatoria que ayuda a cubrir?

### Dimensión 2 — Conocimiento
- **Qué mide:** Puntaje en evaluaciones post-curso.
- **Lógica:** ¿Los colaboradores realmente aprendieron? ¿Qué proveedor genera mayor retención del contenido PCI DSS?

---

## 4. Caso de Negocio

### Supuestos del modelo
- **Colaboradores:** 5.000
- **Tarifa incremental:** 0,1 UF por colaborador
- **Tasa de re-evaluación:** 5% (vacaciones, licencias, reprobaciones)
- **Horizonte:** 3 años
- **Tasa de descuento:** 15% anual (costo de oportunidad)

### Costos anuales por proveedor

| Proveedor | Base | Colaboradores (×0,1 UF) | Re-evaluaciones (5%) | **Total anual** |
|---|---|---|---|---|
| Proveedor A | 100 UF | 500 UF | 25 UF | **625 UF** |
| Proveedor B | 80 UF | 500 UF | 25 UF | **605 UF** |
| Proveedor C | 70 UF | 500 UF | 25 UF | **595 UF** |

### Exposición al Riesgo Normativo

| Concepto | Valor |
|---|---|
| Multa regulatoria PCI DSS | 10.000 UF |
| Impacto reputacional estimado | 20.000 UF |
| **Exposición total** | **30.000 UF** |
| Probabilidad de multa | < 0,05% |
| Pérdida esperada anual | ~15 UF / año |

### VPN a 3 años (tasa descuento 15%)
> Factor de anualidad = 1/1,15 + 1/1,15² + 1/1,15³ = **2,2832**

| Concepto | Valor VPN |
|---|---|
| VPN Costo · Proveedor A | 1.427 UF |
| VPN Costo · Proveedor B | 1.381 UF |
| **VPN Costo · Proveedor C** | **1.359 UF** |
| VPN beneficio (multa evitada, worst-case año 1) | 26.087 UF |
| VPN pérdida esperada evitada (prob. ponderada) | ~34 UF |
| **Diferencia VPN entre proveedor más caro y más barato** | **Solo 68 UF** |

### Aclaración importante: VPN del beneficio vs. ROI esperado

El **VPN del beneficio (26.087 UF)** representa el valor presente de evitar la multa en el **peor escenario posible** (que ocurra en el año 1). Es un valor máximo teórico, **no ponderado por probabilidad**.

El **ROI esperado real** pondera por la probabilidad del evento:
- Pérdida esperada: 30.000 UF × 0,05% = **15 UF/año** → VPN a 3 años ≈ **34 UF**
- Frente a un costo de inversión VPN de 1.359 UF (Proveedor C), el ROI esperado es ~2,5% — financieramente negativo en términos puros.

**¿Por qué se justifica igual la inversión?**
1. **Obligación regulatoria no negociable** — el 100% debe certificarse independientemente del cálculo actuarial.
2. **Asimetría del riesgo** — aunque la probabilidad es baja (<0,05%), la pérdida de 30.000 UF es potencialmente catastrófica. El costo de cobertura (595–625 UF/año) es mínimo frente a la exposición máxima.

> **Hipótesis central:** El precio no distingue a los proveedores (diferencia VPN de solo 68 UF en 3 años). **La clave es el conocimiento que genera cada proveedor.**

---

## 5. Propuesta Metodológica: A/B Testing con Grupos Homogéneos vía Machine Learning

### Paso 01 — Recolección de Datos
Variables a utilizar:
- Datos demográficos de colaboradores
- Historial de capacitación previo
- Nivel de cargo y área funcional
- Antigüedad en la organización

### Paso 02 — Clustering de Colaboradores (K-Means / DBSCAN)
- Algoritmos de ML agrupan colaboradores en **clusters homogéneos**.
- Cada grupo tiene un perfil similar, **eliminando sesgos de selección**.
- Se garantiza que la comparación entre proveedores sea justa y estadísticamente válida.

### Paso 03 — A/B Testing Controlado
- Sub-grupos de cada cluster son **asignados aleatoriamente a distintos proveedores**.
- El diseño garantiza **comparabilidad estadística** entre grupos.
- Se controla por variables confundentes (área, cargo, antigüedad).

### Paso 04 — Análisis de Resultados
- Se comparan **ROI** (costo vs. multas evitadas) y **conocimiento** (score post-test) por proveedor.
- Se aplican **pruebas estadísticas de significancia** (t-test, ANOVA, o equivalentes no paramétricos).
- Se genera un **Score de Efectividad** compuesto por ambas dimensiones.

### Output esperado
- 📊 Ranking de proveedores por efectividad
- 🖥️ Dashboard interactivo de seguimiento
- 📋 Recomendación de contratación basada en datos

---

## 6. Entregable

**Presentación PowerPoint:** `people_analytics_capacitacion.pptx`

| Slide | Contenido |
|---|---|
| 1 | Portada |
| 2 | Contexto y Problema |
| 3 | Propuesta Metodológica |
| 4 | Situación Actual |
| 5 | Caso de Negocio (con VPN 3 años, tasa 15%) |

---


*Documento generado como resumen del proceso del trabajo. Todos los datos y supuestos del caso de negocio son simulados y no representan la realidad de ninguna empresa en particular.*
