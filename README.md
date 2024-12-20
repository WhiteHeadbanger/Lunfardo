![Logo de Lunfardo mostrando un mate argentino](https://i.ibb.co/cQZhPMf/lunfardo-logo-small.png)

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

Nota: los `[]` significa que es un parámetro opcional.

## Tipos de dato

- `Numero`: _entero_ | _float_  
  Ej: `1`, `1.5`
- `Chamuyo`: _string_  
  Ej: `"Hola Argentina!"`
- `Boloodean`: _bool_ = `posta` | `trucho`
- `Nada`: _null_ = `nada`

## Variables

- `poneleque <identificador> = <expresión> | <valor>`  
   Ej: `poneleque numero = 10`, `poneleque variable = (10 + 10) y trucho`

## Estructuras de datos

- `Coso`: _lista_ = `[]`  
  Ej: `poneleque lista = [1, 2, 3]`
- `Mataburros`: _dict_ = `{}`  
  Ej: `poneleque dict = {"1": 1, 2: "dos", var: otra_var}`

## Operadores

### Operadores aritméticos

- `+`: _sumar_  
   Ej: `poneleque numero = 10 + 10`
- `-`: _restar_  
   Ej: `poneleque numero = 10 - 10`
- `*`: _multiplicar_  
   Ej: `poneleque numero = 10 * 10`
- `/`: _dividir_  
   Ej: `poneleque numero = 10 / 10`
- `^`: _potencia_  
   Ej: `poneleque numero = 10 ^ 10`

### Operadores lógicos

- `y`  
   Ej: `poneleque valor = 10 y 10` -> retorna: `posta`
- `o`  
   Ej: `poneleque valor = 10 o 10` -> retorna: `posta`
- `truchar`  
   Ej: `poneleque valor = truchar 10 == 10` -> retorna: `trucho` porque `10 == 10` es `posta`.

### Operadores de asignación

- `=`  
   Ej: `poneleque numero = 10`

### Operadores de comparación

- `==`  
   Ej: `si 10 == 10 entonces poneleque valor = 10`
- `!=`  
   Ej: `si 10 != 10 entonces poneleque valor = 245`
- `<`  
   Ej: `si 0 < 10 entonces poneleque valor = 9`
- `>`  
   Ej: `si 20 > 10 entonces poneleque valor = 20`
- `<=`  
   Ej: `si 4 <= 10 entonces poneleque valor = 4`
- `>=`  
   Ej: `si 14 >= 10 entonces poneleque valor = 14`

## Flujo de datos

### Condicionales

```
si <condicion> entonces
    <sentencia>
[osi <condicion> entonces
    <sentencia>]
[sino
    <sentencia>]
chau
```

```
si a > b entonces
    matear("a es mayor a b")
osi a < b entonces
    matear("a es menor a b")
sino
    matear("a es igual a b")
chau
```

### Bucle `para`

```
para <identificador> = <Numero> hasta <Numero> [entre <Numero>] entonces
    <sentencia>
chau
```

```
para i = 0 hasta 10 entre 2 entonces
    matear(i) # imprime: 0, 2, 4, 6, 8
chau
```

Si no se especifica un valor para `entre`, su valor es 1.

### Bucle `mientras`

```
mientras <condicion> entonces
    <sentencia>
chau
```

```
poneleque i = 0
mientras i < 10 entonces
    # imprime 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
    matear(i)
    poneleque i = i + 1
chau
```

## Tipos de Funciones

Hay dos tipos de funciones, que en Lunfardo se llaman: `Laburo` y `Curro`.

### Laburos

Laburos definidos por el usuario. Pueden tener o no valores por default.

```
laburo <identificador>([identificador[=valor][, identificador[=valor]]])
    <sentencia>
chau
```

```
laburo saludar()
    matear("Hola, Lunfardo!")
chau

saludar() # imprime: "Hola, Mundo!"
```

```
laburo saludar_con_nombre(nombre)
    matear("Hola, " + nombre + "!")
chau

saludar_con_nombre("Lunfardo") # imprime: "Hola, Lunfardo!"
```

```
laburo saludar_con_nombre_opcional(nombre = "Camila")
    matear("Hola, " + nombre + "!")
chau

saludar_con_nombre_opcional() # imprime: "Hola, Camila!"
saludar_con_nombre_opcional("Lunfardo") # imprime: "Hola, Lunfardo!"
```

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
   Devuelve `posta` si es un numero, `trucho` si no lo es.
- `es_chamu(<identificador | valor>)`  
   Devuelve `posta` si es un chamuyo, `trucho` si no lo es.
- `es_coso(<identificador | valor>)`  
   Devuelve `posta` si es un coso, `trucho` si no lo es.
- `es_mataburros(<identificador | valor>)`  
   Devuelve `posta` si es un mataburros, `trucho` si no lo es.
- `es_laburo(<identificador | valor>)`  
   Devuelve `posta` si es un laburo, `trucho` si no lo es.
- `guardar(<coso>, <valor>)`  
   Guarda un valor en un coso
- `sacar(<coso>, <indice>)`  
   Saca un valor de un coso en el índice especificado
- `extender(<coso>, <coso>)`  
   Extiende un coso con los valores de sino coso
- `cambiaso(<coso>, <indice>, <valor>)`  
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
   Devuelve `posta` si la clave existe en el mataburros, `trucho` si no.
- `num(<identificador | valor>)`  
   Convierte un chamuyo a numero
- `chamu(<identificador | valor>)`  
   Convierte un numero a un chamuyo
- `ejecutar(<chamuyo>)`  
   Ejecuta el codigo de un archivo Lunfardo
- `renuncio()`  
   Termina la ejecución del intérprete de Lunfardo.

## Clases

En Lunfardo, las clases se denominan `Chetos`.
Para declarar un nuevo `Cheto` se utiliza la palabra reservada `cheto`.

Los métodos de un `Cheto` se definen con la palabra reservada `laburo`, como si se definiese un `laburo` normal.

### Instanciación de un Cheto

Para instanciar un `Cheto` se utiliza la palabra reservada `nuevo` seguida del nombre del `Cheto`. No son necesarios los paréntesis.
En un `Cheto` se puede definir un método llamado `arranque` que se ejecuta cuando se instancia el `Cheto`. Este método es el método constructor del cheto y va a definir las variables de instancia del mismo (si así se desea). En este caso, son necesarios los paréntesis para instanciar el cheto.

Para acceder a un método de un `Cheto` se utiliza la notación `cheto.nombre_del_metodo()`, donde `cheto` es la instancia del cheto y `nombre_del_metodo` es el nombre del método.

### Ejemplo

```
# Declaración de un Cheto
cheto Persona
    # Declaración del método de arranque (constructor)
    laburo arranque(mi, nombre, edad)
        # Declaración de variables de instancia.
        poneleque mi.nombre = nombre
        poneleque mi.edad = edad
    chau
    # El método saludar accede a las variables de instancia
    laburo saludar(mi)
        matear("Hola, mi nombre es " + mi.nombre)
        matear("Tengo " + chamu(mi.edad) + " anos")
    chau
chau

# Instanciación de un Cheto
poneleque chaboncito = nuevo Persona("Juan", 25)
chaboncito.saludar()

# Modificación de una variable de instancia
poneleque chaboncito.nombre = "Pedro"
chaboncito.saludar()
```

Output:

```
Hola, mi nombre es Juan
Tengo 25 anos
Hola, mi nombre es Pedro
Tengo 25 anos
```

### Herencia

Un `Cheto` puede heredar de otro `Cheto`, para ello se utilizan los paréntesis al momento de la declaración, y entre ellos, el nombre del `Cheto` padre.
Cuando esto sucede, en Lunfardo decimos que el cheto hijo nació en cuna de oro del cheto padre.

```
# Cheto padre
cheto Animal
    laburo arranque(mi, nombre)
        poneleque mi.nombre = nombre
    chau
    laburo saludar(mi)
        matear("Soy " + mi.nombre)
    chau
chau

# Cheto hijo (hereda de Animal)
cheto Perro(Animal)
    laburo ladrar(mi, cantidad)
        matear("Guau! " * cantidad)
    chau
chau

poneleque rocco = nuevo Perro("Rocco")
rocco.saludar()
rocco.ladrar(5)
```

Output:

```
Soy Rocco
Guau! Guau! Guau! Guau! Guau!
```

## Importar archivos

Para importar un archivo se utiliza la palabra reservada `importar`, seguido del nombre del archivo, el cual debe ser un `Chamuyo`.
Nota: Por el momento, solo se pueden importar archivos que estén dentro de la carpeta `examples`.

`/examples/animal.lunf`

```
# Cheto padre
cheto Animal
    laburo arranque(mi, nombre)
        poneleque mi.nombre = nombre
    chau
    laburo saludar(mi)
        matear("Soy " + mi.nombre)
    chau
chau
```

`/examples/perro.lunf`

```
importar "animal.lunf"

# Cheto hijo (hereda de Animal)
cheto Perro(Animal)
    laburo ladrar(mi, cantidad)
        matear("Guau! " * cantidad)
    chau
chau

poneleque rocco = nuevo Perro("Rocco")
rocco.saludar()
rocco.ladrar(5)
```

Output:

```
Soy Rocco
Guau! Guau! Guau! Guau! Guau!
```

## Errores

- `Flaco, fijate que metiste un carácter mal`  
   Caracter Ilegal
- `No te entiendo nada, boludo`  
   Sintaxis Incorrecta
- `Flaco, fijate que te olvidaste de un carácter`  
   Se esperaba un carácter
- `Error en tiempo de ejecución`

## Keywords

- `poneleque`
- `y`
- `o`
- `truchar`
- `si`
- `entonces`
- `osi`
- `sino`
- `para`
- `hasta`
- `entre`
- `mientras`
- `laburo`
- `cheto`
- `nuevo`
- `devolver`
- `continuar`
- `rajar`
- `chau`
- `importar`

## Comentarios

- `#`  
  Ej: `# Esto es un comentario, y esta línea va a ser ignorada por el intérprete`

# Ejemplos

## "Hola mundo"

`matear("Hola, Mundo!")`

## Factorial

```
laburo factorial(n)
    si n <= 1 entonces
        devolver 1
    sino
        devolver n * factorial(n - 1)
    chau
chau

poneleque numero = 10
poneleque resultado = factorial(numero)
matear("El factorial de " + chamu(numero) + " es: " + chamu(resultado))
```

## Fibonacci

```
laburo fibonacci(n)
    si n <= 1 entonces
        devolver n
    sino
        devolver fibonacci(n - 1) + fibonacci(n - 2)
    chau
chau


poneleque var = 10
poneleque secuencia = []

para i = 0 hasta var entonces
    guardar(secuencia, fibonacci(i))
chau

matear("Secuencia de Fibonacci de longitud " + chamu(var) + ": " + chamu(secuencia))
```

## Sistema bancario

```
laburo crear_cuenta(cuentas, nombre, balance_inicial)
    metele_en(cuentas, nombre, balance_inicial)
    matear("Cuenta creada satisfactoriamente!")
chau

laburo deposito(cuentas, nombre, cantidad)
    si existe_clave(cuentas, nombre) entonces
        si cantidad > 0 entonces
            poneleque balance_actual = agarra_de(cuentas, nombre)
            poneleque nuevo_balance = balance_actual + cantidad
            metele_en(cuentas, nombre, nuevo_balance)
            matear("Deposito realizado. Nuevo balance: " + chamu(nuevo_balance))
        sino
            matear("No se puede depositar una cantidad negativa")
        chau
    sino
        matear("La cuenta no existe")
    chau
chau

laburo retiro(cuentas, nombre, cantidad)
    si existe_clave(cuentas, nombre) entonces
        si (cantidad >= 0) y (cantidad <= agarra_de(cuentas, nombre)) entonces
            poneleque balance_actual = agarra_de(cuentas, nombre)
            poneleque nuevo_balance = balance_actual - cantidad
            metele_en(cuentas, nombre, nuevo_balance)
            matear("Retiro realizado. Nuevo balance: " + chamu(nuevo_balance))
        sino
            matear("No se puede retirar una cantidad negativa o mayor al balance")
        chau
    sino
        matear("La cuenta no existe")
    chau
chau

laburo balance(cuentas, nombre)
    si existe_clave(cuentas, nombre) entonces
        matear("Balance: " + chamu(agarra_de(cuentas, nombre)))
    sino
        matear("La cuenta no existe")
    chau
chau

poneleque cuentas_db = {}

mientras posta entonces
    matear("1. Crear cuenta")
    matear("2. Deposito")
    matear("3. Retiro")
    matear("4. Balance")
    matear("5. Salir")

    poneleque opcion = num(morfar("Seleccione una opcion: "))

    si opcion == 1 entonces
        poneleque nombre = morfar("Nombre de la cuenta: ")
        poneleque balance_inicial = num(morfar("Balance inicial: "))
        crear_cuenta(cuentas_db, nombre, balance_inicial)
    osi opcion == 2 entonces
        poneleque nombre = morfar("Nombre de la cuenta: ")
        poneleque cantidad = num(morfar("Cantidad a depositar: "))
        deposito(cuentas_db, nombre, cantidad)
    osi opcion == 3 entonces
        poneleque nombre = morfar("Nombre de la cuenta: ")
        poneleque cantidad = num(morfar("Cantidad a retirar: "))
        retiro(cuentas_db, nombre, cantidad)
    osi opcion == 4 entonces
        poneleque nombre = morfar("Nombre de la cuenta: ")
        balance(cuentas_db, nombre)
    osi opcion == 5 entonces
        matear("Gracias por confiar en nuestro banco.")
        rajar
    sino
        matear("Opcion invalida")
    chau
chau
```

# Quiero contribuir!

Se acepta todo tipo de sugerencias y pull requests. Si tenés alguna idea, o si lo probaste y te encontraste con [muchos bugs](https://www.youtube.com/watch?v=SiMHTK15Pik):

1. Forkeá el proyecto
2. Codeá tu código lindis
3. Hacé un pull request

Si tenés alguna idea pero no tenés código, o por la razón que sea no podés contribuir de esa manera, podés abrir un Issue.

También recibo mensajes de correo electrónico en: sebastianper2018@gmail.com con ideas, sugerencias y preguntas.

# Siguientes pasos

- [x] Importar archivos de código.
- [ ] Más tipos de errores.
- [x] Clases
  - [x] Herencia
