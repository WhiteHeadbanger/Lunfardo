# Lunfardo: el lenguaje de programación basado en el lunfardo argentino

## Sobre Lunfardo

Lunfardo está fuertemente basado (por el momento) en: [Juro que no es Rick Roll](https://www.youtube.com/watch?v=Eythq9848Fg&list=PLZQftyCk7_SdoVexSmwy_tBgs7P0b97yD)

Es un [esolang](https://github.com/angrykoala/awesome-esolangs) interpretado escrito en Python 3, por ende si Python es lento, Lunfardo es dos veces más lento, ó tres, ó mas ya que todavía no hay una función que mida el tiempo.
La idea del lenguaje es divertirse!

## Instalación

- Requerimiento: tener instalado Python 3
- Clonar el repositorio

## Empezar a usar

- `cd src`
- `python3 run.py`

Inmediatamente se puede empezar a usar el intérprete, pero también podemos escribir nuevos archivos.  

Para ejecutar archivos

- `ejecutar(<nombre_del_archivo_en_strings>)`  
Ej: `ejecutar("factorial.lunf")`

Nota: el archivo debe estar dentro de la carpeta `src/examples` por el momento.  
Si querés cambiar esto, al final del archivo `src/lunfardo_types/laburo.py` podés encontrar  
el método `exec_ejecutar()` en donde se comprueba esta ruta. 

# Características

## Tipos de dato

Todos los tipos de dato validan a Numero y devuelven un número, por ejemplo si escribimos en el intérprete: `trucho` devolverá `0`.

- `Numero`: _entero_ | _float_  
Ej: `1`, `1.5`
- `trucho`: _entero_ = `0`
- `nada`: _entero_ = `0`
- `posta`: _entero != 0_ = `n > 0`

## Variables

- `cualca <identificador> = <valor>`  
    Ej: `cualca numero = 10`

## Estructuras de datos

- `Coso`: _lista_ = `[]`  
Ej: `cualca lista = [1, 2, 3]`
- `Mataburros`: _dict_ = `{}`  
Ej: `cualca dict = {"1": 1, 2: "dos", var: otra_var}`

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

- `para <identificador = valor> hasta <condicion> [entre <valor>] entonces <sentencia> chau`  
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
- `es_mataburros(<identificador | valor>)`  
    Devuelve 1 si es un mataburros, 0 si es falso
- `es_laburo(<identificador | valor>)`  
    Devuelve 1 si es un laburo, 0 si es falso
- `guardar(<coso>, <valor>)`  
    Guarda un valor en un coso
- `sacar(<coso>, <indice>)`  
    Saca un valor de un coso en el índice especificado
- `extender(<coso>, <coso>)`  
    Extiende un coso con los valores de otro coso
- `reemplazar(<coso>, <indice>, <valor>)`  
    Reemplaza un valor en un coso en el índice especificado
- `insertar(<coso>, <indice>, <valor>)`  
    Inserta un valor en un coso en el índice especificado
- `longitud(<coso | chamuyo | mataburros>)`  
    Devuelve la longitud de un coso | chamuyo | mataburros
- `metele_en(<mataburros>, <clave>, <valor>)`  
    Guarda un valor en la clave especificada de un mataburros.  
    Si la clave no está presente, se crea.
- `agarra_de(<mataburros>, <clave>)`  
    Devuelve el valor de una clave de un mataburros.
- `borra_de(<mataburros>, <clave>)`  
    Borra una clave de un mataburros.
- `existe_clave(<mataburros>, <clave>)`  
    Devuelve 1 si la clave existe en el mataburros, 0 si no.
- `num(<identificador | valor>)`  
    Convierte un chamuyo a numero
- `chamu(<identificador | valor>)`  
    Convierte un numero a un chamuyo
- `ejecutar(<chamuyo>)`  
    Ejecuta el codigo de un archivo Lunfardo
- `renuncio()`  
    Termina la ejecución del intérprete de Lunfardo.

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

## Comentarios
- `#`  
Ej: `# Esto es un comentario, y esta línea va a ser ignorada por el intérprete`  


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

### Sistema bancario

```
laburo crear_cuenta(cuentas, nombre, balance_inicial)
    metele_en(cuentas, nombre, balance_inicial)
    matear("Cuenta creada satisfactoriamente!")
chau

laburo deposito(cuentas, nombre, cantidad)
    si existe_clave(cuentas, nombre) entonces
        si cantidad > 0 entonces
            cualca balance_actual = agarra_de(cuentas, nombre)
            cualca nuevo_balance = balance_actual + cantidad
            metele_en(cuentas, nombre, nuevo_balance)
            matear("Deposito realizado. Nuevo balance: " + chamu(nuevo_balance))
        otro
            matear("No se puede depositar una cantidad negativa")
        chau
    otro
        matear("La cuenta no existe")
    chau
chau

laburo retiro(cuentas, nombre, cantidad)
    si existe_clave(cuentas, nombre) entonces
        si (cantidad >= 0) y (cantidad <= agarra_de(cuentas, nombre)) entonces
            cualca balance_actual = agarra_de(cuentas, nombre)
            cualca nuevo_balance = balance_actual - cantidad
            metele_en(cuentas, nombre, nuevo_balance)
            matear("Retiro realizado. Nuevo balance: " + chamu(nuevo_balance))
        otro
            matear("No se puede retirar una cantidad negativa o mayor al balance")
        chau
    otro
        matear("La cuenta no existe")
    chau
chau

laburo balance(cuentas, nombre)
    si existe_clave(cuentas, nombre) entonces
        matear("Balance: " + chamu(agarra_de(cuentas, nombre)))
    otro
        matear("La cuenta no existe")
    chau
chau

cualca cuentas_db = {}

mientras posta entonces
    matear("1. Crear cuenta")
    matear("2. Deposito")
    matear("3. Retiro")
    matear("4. Balance")
    matear("5. Salir")

    cualca opcion = num(morfar("Seleccione una opcion: "))

    si opcion == 1 entonces
        cualca nombre = morfar("Nombre de la cuenta: ")
        cualca balance_inicial = num(morfar("Balance inicial: "))
        crear_cuenta(cuentas_db, nombre, balance_inicial)
    osi opcion == 2 entonces
        cualca nombre = morfar("Nombre de la cuenta: ")
        cualca cantidad = num(morfar("Cantidad a depositar: "))
        deposito(cuentas_db, nombre, cantidad)
    osi opcion == 3 entonces
        cualca nombre = morfar("Nombre de la cuenta: ")
        cualca cantidad = num(morfar("Cantidad a retirar: "))
        retiro(cuentas_db, nombre, cantidad)
    osi opcion == 4 entonces
        cualca nombre = morfar("Nombre de la cuenta: ")
        balance(cuentas_db, nombre)
    osi opcion == 5 entonces
        matear("Gracias por confiar en nuestro banco.")
        rajar
    otro
        matear("Opcion invalida")
    chau
chau
```

# Siguientes pasos

- Importar archivos de código.
- Más tipos de errores, como errores que comprueben tipos de dato.
- OOP, herencia.
- Que el lenguaje valide a `Numero` hace que programar sea más complicado. El tipo de dato `nada` debería ser un dato a parte, en lugar de ser `0`. Lo mismo con `posta` y `trucho`.