# Lunfardo Programming Language

Lunfardo is a programming language inspired by the colorful and expressive Argentinian Lunfardo slang. It aims to provide laughs and enjoy a new esoteric language.

## Features

- **Expressive Syntax**: Lunfardo's syntax is inspired by the rich vocabulary and idioms of Lunfardo slang, making it expressive and fun to write.
- **Ease of Use**: Designed with simplicity in mind, Lunfardo prioritizes readability and ease of understanding for developers of all levels.

## Installation

To install Lunfardo, simply download the latest release from the [GitHub repository](https://github.com/yourusername/lunfardo) and follow the installation instructions.
``

# Características

## Tipos de dato

Todos los tipos de dato validan a Numero y devuelven un número, por ejemplo si escribimos en el intérprete: `trucho` devolverá `0`.

- `Numero`: _entero_ | _float_  
Ej: `1`
- `trucho`: _entero_ = `0`
- `nada`: _entero_ = `0`
- `posta`: _entero != 0_ = `0 < n > 0`

## Variables

- `cualca <identificador> = <valor>`  
    Ej: `cualca numero = 10`

## Estructuras de datos

- Coso: lista = `[]`  
Ej: `cualca lista = [1, 2, 3]`

## Operadores

### Operadores aritméticos

- `+`: _sumar_  
    Ej: `cualca numero = 10 + 10`
- `-`: _restar_  
    Ej: `cualca numero = 10 - 10`
- `*`: _multiplicar_  
    Ej: `cualca numero = 10 * 10`
- `/`: _dividir_  
    Ej: `cualca numero = 10 / 10`
- `^`: _potencia_  
    Ej: `cualca numero = 10 ^ 10`

### Operadores lógicos

- `y`  
    Ej: `cualca valor = 10 y 10`
- `o`  
    Ej: `cualca valor = 10 o 10`
- `truchar`  
    Ej: `cualca valor = truchar 10`

### Operadores de asignación

- `=`  
    Ej: `cualca numero = 10`

### Operadores de comparación

- `==`  
    Ej: `si 10 == 10 entonces cualca valor = 10`
- `!=`  
    Ej: `si 10 != 10 entonces cualca valor = 245`
- `<`  
    Ej: `si 0 < 10 entonces cualca valor = 9`
- `>`  
    Ej: `si 20 > 10 entonces cualca valor = 20`
- `<=`  
    Ej: `si 4 <= 10 entonces cualca valor = 4`
- `>=`  
    Ej: `si 14 >= 10 entonces cualca valor = 14`

## Flujo de datos

### Condicionales

- `si <condicion> entonces <sentencia>`
- `[osi <condicion> entonces <sentencia>]` 
- `[otro <sentencia>]`

### Bucle `para`

- `para <identificador = valor> hasta <condicion> [entre <valor>] entonces <sentencia>`  
Si no se especifica un valor para `entre`, su valor es 1.

### Bucle `mientras`

- `mientras <condicion> entonces <sentencia> chau`

## Tipos de Funciones

Hay dos tipos de funciones, que en Lunfardo se llaman: `Laburo` y `Curro`.

Las funciones se pueden referenciar.

### Laburos

- `laburo [<identificador>]([identificador[, identificador]]): <sentencia> chau`

Laburos definidos por el usuario.

### Curros pre-definidos

Un curro es un laburo pre-definido.

- `matear([identificador | valor])`  
    Imprime en pantalla un valor
- `morfar([identificador | valor])`  
    Toma un valor por teclado
- `winpiavidrios()`  
    Limpia la pantalla para windows
- `linpiavidrios()`  
    Limpia la pantalla para linux
- `es_num(<identificador | valor>)`  
    Devuelve 1 si es un numero, 0 si es falso
- `es_chamu(<identificador | valor>)`  
    Devuelve 1 si es un chamuyo, 0 si es falso
- `es_coso(<identificador | valor>)`  
    Devuelve 1 si es un coso, 0 si es falso
- `es_laburo(<identificador | valor>)`  
    Devuelve 1 si es un laburo, 0 si es falso
- `guardar(<coso>, <valor>)`  
    Guarda un valor en un coso
- `sacar(<coso>, <index>)`  
    Saca un valor de un coso
- `extender(<coso>, <coso>)`  
    Extiende un coso con los valores de otro coso
- `longitud(<coso>)`  
    Devuelve la longitud de un coso
- `num(<identificador | valor>)`  
    Convierte un chamuyo a numero
- `chamu(<identificador | valor>)`  
    Convierte un numero a un chamuyo
- `run(<chamuyo>)`  
    Ejecuta el codigo de un archivo lunfardo

## Errores

- `Flaco, fijate que metiste un carácter mal`  
    Caracter Ilegal
- `No te entiendo nada, boludo`  
    Sintaxis Incorrecta
- `Flaco, fijate que te olvidaste de un carácter`  
    Se esperaba un carácter
- `Error en tiempo de ejecución`

## Keywords

- `cualca`
- `y`
- `o`
- `truchar`
- `si`
- `entonces`
- `osi`
- `otro`
- `para`
- `hasta`
- `entre`
- `mientras`
- `laburo`
- `devolver`
- `continuar`
- `rajar`
- `chau`

# Ejemplos 

### "Hola mundo"

`matear("Hola, Mundo!")`

### Factorial

```
laburo factorial(n)
    si n <= 1 entonces
        devolver 1
    otro
        devolver n * factorial(n - 1)
    chau
chau

cualca numero = 10
cualca resultado = factorial(numero)
matear("El factorial de " + chamu(numero) + " es: " + chamu(resultado))
```

### Fibonacci

```
laburo fibonacci(n)
    si n <= 1 entonces
        devolver n
    otro
        devolver fibonacci(n - 1) + fibonacci(n - 2)
    chau
chau


cualca var = 10
cualca secuencia = []

para i = 0 hasta var entonces
    guardar(secuencia, fibonacci(i))
chau

matear("Secuencia de Fibonacci de longitud " + chamu(var) + ": " + chamu(secuencia))
```