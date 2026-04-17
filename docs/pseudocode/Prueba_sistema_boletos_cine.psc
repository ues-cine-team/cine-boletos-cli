Algoritmo SistemaCineLogicaprogramacion
    // Definimos las dimensiones de la sala
    Definir filas, columnas Como Entero
    filas <- 5
    columnas <- 5
    
    // Matriz de asientos (0 = Libre, 1 = Ocupado)
    Definir sala1, sala2 Como Entero
    Dimension sala1[filas, columnas], sala2[filas, columnas]
    
    // Inicializar salas como vacías
    InicializarSala(sala1, filas, columnas)
    InicializarSala(sala2, filas, columnas)
    
    Definir opcion, f_idx, f_coord, c_coord Como Entero
    Definir continuar Como Logico
    continuar <- Verdadero
    
    Mientras continuar Hacer
        Limpiar Pantalla
        Escribir "=== SISTEMA DE BOLETOS DE CINE ==="
        Escribir "1. Ver Cartelera y Funciones"
        Escribir "2. Comprar Boletos"
        Escribir "3. Salir"
        Leer opcion
        
        Segun opcion Hacer
            1:
                Escribir "1. Logica de programacion - Horario: 14:00"
                Escribir "2. Logica de programacion 2 - Horario: 18:00"
                Escribir "Presione una tecla para continuar..."
                Esperar Tecla
            2:
                Escribir "Seleccione la función (1 o 2):"
                Escribir "1. Logica de programacion (14:00)"
                Escribir "2. Logica de programacion 2 (18:00)"
                Leer f_idx
                
                Si f_idx = 1 o f_idx = 2 Entonces
                    // Mostrar mapa según la sala elegida
                    Si f_idx = 1 Entonces
                        MostrarMapa(sala1, filas, columnas, "Logica de programacion", "14:00")
                    Sino
                        MostrarMapa(sala2, filas, columnas, "Logica de programacion 2", "18:00")
                    FinSi
                    
                    Escribir "Ingrese Fila (1 a ", filas, "):"
                    Leer f_coord
                    Escribir "Ingrese Columna (1 a ", columnas, "):"
                    Leer c_coord
                    
                    // Intentar comprar
                    Si f_idx = 1 Entonces
                        ComprarBoleto(sala1, filas, columnas, f_coord, c_coord)
                    Sino
                        ComprarBoleto(sala2, filas, columnas, f_coord, c_coord)
                    FinSi
                Sino
                    Escribir "Función no válida."
                FinSi
                Escribir "Presione una tecla para continuar..."
                Esperar Tecla
            3:
                Escribir "Cerrando sistema..."
                continuar <- Falso
            De Otro Modo:
                Escribir "Opción no válida."
                Esperar Tecla
        FinSegun
    FinMientras
FinAlgoritmo

SubProceso InicializarSala(matriz, f, c)
    Definir i, j Como Entero
    Para i <- 1 Hasta f Hacer
        Para j <- 1 Hasta c Hacer
            matriz[i, j] <- 0 // 0 significa LIBRE
        FinPara
    FinPara
FinSubProceso

SubProceso MostrarMapa(matriz, f, c, titulo, horario)
    Definir i, j Como Entero
    Definir libres Como Entero
    libres <- 0
    Escribir "--- Sala: ", titulo, " (", horario, ") ---"
    
    // Escribir cabecera de columnas
    Escribir "    C1 C2 C3 C4 C5" 
    
    Para i <- 1 Hasta f Hacer
        Escribir Sin Saltar "F", i, "  "
        Para j <- 1 Hasta c Hacer
            Si matriz[i, j] = 0 Entonces
                Escribir Sin Saltar "[ ]"
                libres <- libres + 1
            Sino
                Escribir Sin Saltar "[X]"
            FinSi
        FinPara
        Escribir "" // Salto de línea
    FinPara
    Escribir "Asientos disponibles: ", libres
FinSubProceso

SubProceso ComprarBoleto(matriz, f, c, fila, col)
    // Validar rango
    Si fila >= 1 y fila <= f y col >= 1 y col <= c Entonces
        // Validar si está ocupado
        Si matriz[fila, col] = 1 Entonces
            Escribir "Error: El asiento ya está ocupado. Elige otro."
        Sino
            matriz[fila, col] <- 1
            Escribir "¡Éxito! Has comprado el asiento F", fila, "-C", col
        FinSi
    Sino
        Escribir "Error: Esa coordenada de asiento no existe."
    FinSi
FinSubProceso