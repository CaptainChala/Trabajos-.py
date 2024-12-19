import random #Se utiliza para creación de arreglos en los ficheros
import json   #Se utiliza para crear el fichero a utilizar
import time   #Se utiliza para medir los tiempos de ejecución de cada enfoque
from itertools import combinations #permite generar todas las combinaciones posibles de un conjunto de elementos, sin importar el orden, y sin repetir elementos

# Funciones para el Problema del Pintor de Particiones

# Fuerza Bruta
def max_time_for_partition(partition):
    return max(sum(part) for part in partition)

def brute_force_partition(L, k):
    n = len(L)
    if k >= n:
        return max(L)
    
    min_time = float('inf')
    for dividers in combinations(range(1, n), k - 1):
        partition = [L[i:j] for i, j in zip((0,) + dividers, dividers + (n,))]
        min_time = min(min_time, max_time_for_partition(partition))
    return min_time

# Divide y Conquistar 
def is_possible(L, k, max_time):
    painters = 1
    time_spent = 0
    for length in L:
        if time_spent + length > max_time:
            painters += 1
            time_spent = length
            if painters > k:
                return False
        else:
            time_spent += length
    return True

def divide_and_conquer(L, k):
    low, high = max(L), sum(L)
    while low < high:
        mid = (low + high) // 2
        if is_possible(L, k, mid):
            high = mid
        else:
            low = mid + 1
    return low

# Programación Dinámica
def dp_partition(L, k):
    n = len(L)
    if k >= n:
        return max(L)
    
    dp = [[float('inf')] * (k + 1) for _ in range(n + 1)]
    prefix_sum = [0] * (n + 1)

    for i in range(1, n + 1):
        prefix_sum[i] = prefix_sum[i - 1] + L[i - 1]

    for i in range(1, n + 1):
        dp[i][1] = prefix_sum[i]

    for j in range(2, k + 1):
        for i in range(1, n + 1):
            for p in range(1, i):
                dp[i][j] = min(dp[i][j], max(dp[p][j - 1], prefix_sum[i] - prefix_sum[p]))

    return dp[n][k]

# Crear Fichero con arreglos
def generate_test_data(num_arrays=300, min_length=40, max_length=100, max_value=100):
    test_data = []
    for _ in range(num_arrays):
        length = random.randint(min_length, max_length)
        array = [random.randint(1, max_value) for _ in range(length)]
        test_data.append(array)
    
    with open("test_data.json", "w") as f:
        json.dump(test_data, f)
    print("Datos de prueba generados y guardados en 'test_data.json'.")

# Función para medir tiempos de ejecución
def measure_time(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    return end_time - start_time, result

# Función para seleccionar el método de entrada del arreglo
def get_array_input():
    choice = input("¿Deseas cargar datos de prueba o ingresar un arreglo manualmente? (1: Prueba, 2: Manual): ")
    if choice == "1":
        with open("test_data.json", "r") as f:
            test_data = json.load(f)
        return test_data
    elif choice == "2":
        user_input = input("Ingresa el arreglo de longitudes (por ejemplo: 10,20,30): ")
        array = list(map(int, user_input.split(',')))
        return [array]
    else:
        print("Opción inválida.")
        return get_array_input()

# Menú Principal
def main():
    while True:
        print("\n=== Problema del Pintor de Particiones ===")
        print("1. Generar Fichero con datos")
        print("2. Ejecutar los tres métodos")
        print("3. Salir")
        
        choice = input("Selecciona una opción: ")
        
        if choice == "1":
            generate_test_data()
        elif choice == "2":
            k = int(input("Ingresa el número de pintores: "))
            test_data = get_array_input()
            
            for L in test_data:
                # Ejecutar Fuerza Bruta
                time_brute, result_brute = measure_time(brute_force_partition, L, k)
                print(f"\nResultados para Fuerza Bruta: Tiempo mínimo = {result_brute}, Tiempo de ejecución = {time_brute:.4f} segundos")

                # Ejecutar Divide y Conquistar
                time_binary, result_binary = measure_time(divide_and_conquer, L, k)
                print(f"Resultados para Divide y Conquistar: Tiempo mínimo = {result_binary}, Tiempo de ejecución = {time_binary:.4f} segundos")

                # Ejecutar Programación Dinámica
                time_dynamic, result_dynamic = measure_time(dp_partition, L, k)
                print(f"Resultados para Programación Dinámica: Tiempo mínimo = {result_dynamic}, Tiempo de ejecución = {time_dynamic:.4f} segundos")
        elif choice == "3":
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida, por favor selecciona una opción del menú.")

# Ejecutar el menú principal
if __name__ == "__main__":
    main()
