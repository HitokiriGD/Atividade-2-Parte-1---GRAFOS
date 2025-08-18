from abc import ABC, abstractmethod

# =============================
# Parte 1 - Interface Grafo
# =============================
class Grafo(ABC):
    @abstractmethod
    def numero_de_vertices(self):
        pass

    @abstractmethod
    def numero_de_arestas(self):
        pass

    @abstractmethod
    def sequencia_de_graus(self):
        pass

    @abstractmethod
    def adicionar_aresta(self, u, v):
        pass

    @abstractmethod
    def remover_aresta(self, u, v):
        pass

    @abstractmethod
    def imprimir(self):
        pass


# =============================
# Parte 2 - Classe GrafoDenso
# =============================
class GrafoDenso(Grafo):
    def __init__(self, rotulos):
        """
        Cria um grafo denso não direcionado e não ponderado.
        :param rotulos: lista de rótulos dos vértices (ex: ["A","B","C"])
        """
        self.rotulos = rotulos
        self.n = len(rotulos)
        # inicializa matriz de adjacência com zeros
        self.matriz = [[0 for _ in range(self.n)] for _ in range(self.n)]
        self.arestas = 0

    # =============================
    # Parte 3 - Métodos básicos
    # =============================
    def numero_de_vertices(self):
        return self.n

    def numero_de_arestas(self):
        return self.arestas

    def sequencia_de_graus(self):
        graus = []
        for i in range(self.n):
            graus.append(sum(self.matriz[i]))
        return graus

    # =============================
    # Parte 4 - Adicionar, remover e imprimir
    # =============================
    def adicionar_aresta(self, u, v):
        i, j = self.rotulos.index(u), self.rotulos.index(v)
        if self.matriz[i][j] == 0:   # evita aresta duplicada
            self.matriz[i][j] = 1
            self.matriz[j][i] = 1
            self.arestas += 1

    def remover_aresta(self, u, v):
        i, j = self.rotulos.index(u), self.rotulos.index(v)
        if self.matriz[i][j] == 1:
            self.matriz[i][j] = 0
            self.matriz[j][i] = 0
            self.arestas -= 1

    def imprimir(self):
        print("Matriz de Adjacência:")
        print("   " + " ".join(self.rotulos))
        for i in range(self.n):
            linha = " ".join(str(x) for x in self.matriz[i])
            print(f"{self.rotulos[i]}: {linha}")


# =============================
# Parte 5 - Teste
# =============================
if __name__ == "__main__":
    V = ["A", "B", "C", "D", "E"]
    grafo = GrafoDenso(V)

    # Adicionar arestas
    arestas = [("A","B"), ("A","C"), ("C","D"), ("C","E"), ("B","D")]
    for (u, v) in arestas:
        grafo.adicionar_aresta(u, v)

    # Imprimir antes
    grafo.imprimir()
    print("Número de vértices:", grafo.numero_de_vertices())
    print("Número de arestas:", grafo.numero_de_arestas())
    print("Sequência de graus:", grafo.sequencia_de_graus())

    # Remover aresta (A, C)
    print("\nRemovendo aresta (A, C)...\n")
    grafo.remover_aresta("A", "C")

    # Imprimir depois
    grafo.imprimir()
    print("Número de vértices:", grafo.numero_de_vertices())
    print("Número de arestas:", grafo.numero_de_arestas())
    print("Sequência de graus:", grafo.sequencia_de_graus())
