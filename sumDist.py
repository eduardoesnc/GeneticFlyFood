# [44, 32, 28, 2, 47, 54, 53, 1, 40, 34, 9, 51, 50, 46, 48, 42, 26, 4, 22, 11, 56, 23, 57, 43, 17, 0, 29, 12, 39, 24, 8, 31, 19, 52, 49, 3, 7, 21, 15, 41, 37, 30, 6, 10, 38, 20, 35, 16, 25, 18, 5, 27, 13, 36, 14, 33, 45, 55]
import tsplib95

# carrega a instância do problema do arquivo BRAZIL58.TSP
problem = tsplib95.load("BRAZIL58.TSP")

# obtém a lista de cidades (pontos) do problema
cities = list(problem.get_nodes())

# obtém a ordem em que as cidades devem ser visitadas
tour = [44, 32, 28, 2, 47, 54, 53, 1, 40, 34, 9, 51, 50, 46, 48, 42, 26, 4, 22, 11, 56, 23, 57, 43, 17, 0, 29, 12, 39, 24, 8, 31, 19, 52, 49, 3, 7, 21, 15, 41, 37, 30, 6, 10, 38, 20, 35, 16, 25, 18, 5, 27, 13, 36, 14, 33, 45, 55]
# adiciona a primeira cidade ao final do caminho para fechar o ciclo
tour.append(tour[0])

# calcula a soma das distâncias entre as cidades do caminho
distance_sum = sum(problem.get_weight(tour[i], tour[i+1]) for i in range(len(tour)-1))

print("A soma das distâncias percorridas é:", distance_sum)