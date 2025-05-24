# Security Policy

## Versiones Soportadas

Actualmente se proporcionan actualizaciones de seguridad para estas versiones:

| Versión | Soporte de Seguridad |
| ------- | -------------------- |
| 2.0.x   | ✅ Completo          |
| < 2.0   | ❌ No soportado      |

## Reportar Vulnerabilidades

Si descubres una vulnerabilidad de seguridad, por favor NO uses issues públicos.

### Proceso de Reporte

1. **Contacto Directo**: Envía un email privado a [tu-email@example.com]
2. **Información Requerida**:
   - Descripción detallada de la vulnerabilidad
   - Pasos para reproducirla
   - Versión afectada
   - Impacto potencial

3. **Tiempo de Respuesta**:
   - Confirmación: 48 horas
   - Evaluación inicial: 7 días
   - Resolución: 30 días (dependiendo de la severidad)

### Qué NO reportar como vulnerabilidad

- Configuraciones incorrectas del usuario
- Problemas con versiones no soportadas
- Ataques que requieren acceso físico a la máquina

### Proceso de Resolución

1. **Confirmación**: Verificamos y confirmamos la vulnerabilidad
2. **Desarrollo**: Creamos un fix en privado
3. **Testing**: Probamos exhaustivamente la solución
4. **Release**: Publicamos una versión corregida
5. **Disclosure**: Anunciamos la corrección (sin detalles del exploit)

## Buenas Prácticas de Seguridad

### Para Usuarios
- ✅ Mantén actualizadas las dependencias
- ✅ Usa contraseñas fuertes para MySQL
- ✅ Limita el acceso de red a tu servidor MySQL
- ✅ Revisa regularmente los logs de conexión
- ❌ No compartas credenciales en repositorios públicos
- ❌ No uses credenciales por defecto en producción

### Para Desarrolladores
- Revisión de código obligatoria para cambios de seguridad
- Uso de herramientas automáticas de análisis de seguridad
- Testing de penetración antes de releases mayores

## Agradecimientos

Agradecemos a todos los investigadores de seguridad que reportan vulnerabilidades de manera responsable.

---

**Última actualización**: Diciembre 2024
