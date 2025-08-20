![Logo de Lunfardo mostrando un mate argentino](https://i.ibb.co/cQZhPMf/lunfardo-logo-small.png)

# Lunfardo: el lenguaje de programación basado en el lunfardo argentino

## Sobre Lunfardo

Lunfardo está fuertemente basado (por el momento) en: [Juro que no es Rick Roll](https://www.youtube.com/watch?v=Eythq9848Fg&list=PLZQftyCk7_SdoVexSmwy_tBgs7P0b97yD)

Es un [esolang](https://github.com/angrykoala/awesome-esolangs) escrito en Python 3.
El lenguaje, naturalmente, no tiene un propósito serio, pero aún así se puede crear software.

## Instalación y uso

> [!NOTE]
> Para información más detallada [click acá](https://github.com/WhiteHeadbanger/Lunfardo/wiki/02.-Instalación-y-Configuración)

### Requisitos

- Python 3 instalado en el sistema.

### Instalación

```sh
# Clonar el repositorio
git clone https://github.com/WhiteHeadbanger/Lunfardo.git
```

### Ejecución

```sh
python3 src/run.py
```

Esto iniciará el intérprete interactivo de Lunfardo.

### Ejecutar un archivo

```sh
python3 src/run.py <ruta_del_archivo.lunf>
```

#### Ejemplo

```sh
python3 src/run.py src/examples/banco_oop.lunf
```

## Características

- Sintaxis inspirada en el lunfardo argentino.
- Lenguaje interpretado.
- Tipado dinámico. (Sujeto a cambios a medida que evolucione)
- No es orientado a objetos, pero tiene soporte para clases y herencia. (Sujeto a cambios a medida que evolucione)

## Ejemplo

```text
laburo factorial(n)
    si n <= 1 entonces
        devolver 1
    sino
        devolver n * factorial(n - 1)
    chau
chau

poneleque numero = 5
matear("El factorial de " + chamu(numero) + " es " + chamu(factorial(numero)))
```

## Quiero contribuir!

Se aceptan sugerencias y pull requests. Si encontrás un [bug](https://www.youtube.com/watch?v=SiMHTK15Pik) o querés proponer una mejora:

1. Hacé un fork del repositorio.
2. Implementá tu cambio.
3. Enviá un pull request.

También podés abrir un Issue o enviar un correo con tus ideas y sugerencias a: <sebastianper2018@gmail.com>.
