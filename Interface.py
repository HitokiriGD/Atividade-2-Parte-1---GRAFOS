from abc import ABC, abstractmethod

# =============================
# Interface Grafo
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
# Grafo Denso (Matriz de Adjacência)
# =============================
class GrafoDenso(Grafo):
    def __init__(self, rotulos):
        """
        Grafo denso não direcionado e não ponderado (matriz de adjacência).
        Não permite múltiplas arestas entre dois vértices.
        """
        self.rotulos = rotulos
        self.n = len(rotulos)
        self.matriz = [[0 for _ in range(self.n)] for _ in range(self.n)]
        self.arestas = 0

    def numero_de_vertices(self):
        return self.n

    def numero_de_arestas(self):
        return self.arestas

    def sequencia_de_graus(self):
        return [sum(self.matriz[i]) for i in range(self.n)]

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
# Grafo Esparso (Lista de Adjacência)
# =============================
class GrafoEsparso(Grafo):
    def __init__(self, rotulos):
        """
        Grafo esparso não direcionado e não ponderado (lista de adjacências).
        Permite múltiplas arestas entre dois vértices.
        """
        self.rotulos = rotulos
        self.n = len(rotulos)
        self.adj = {rotulo: [] for rotulo in rotulos}
        self.arestas = 0

    def numero_de_vertices(self):
        return self.n

    def numero_de_arestas(self):
        return self.arestas

    def sequencia_de_graus(self):
        return [len(self.adj[v]) for v in self.rotulos]

    def adicionar_aresta(self, u, v):
        if u in self.adj and v in self.adj:
            self.adj[u].append(v)
            self.adj[v].append(u)
            self.arestas += 1

    def remover_aresta(self, u, v):
        if u in self.adj and v in self.adj:
            if v in self.adj[u]:
                self.adj[u].remove(v)   # remove apenas uma ocorrência
                self.adj[v].remove(u)
                self.arestas -= 1

    def imprimir(self):
        print("Lista de Adjacência:")
        for v in self.rotulos:
            print(f"{v}: {self.adj[v]}")


# =============================
# Testes das duas implementações
# =============================
if __name__ == "__main__":
    V = ["A", "B", "C", "D", "E"]

    print("===== TESTE GRAFO DENSO =====")
    grafo_denso = GrafoDenso(V)
    arestas = [("A","B"), ("A","C"), ("C","D"), ("C","E"), ("B","D")]
    for (u, v) in arestas:
        grafo_denso.adicionar_aresta(u, v)

    grafo_denso.imprimir()
    print("Número de vértices:", grafo_denso.numero_de_vertices())
    print("Número de arestas:", grafo_denso.numero_de_arestas())
    print("Sequência de graus:", grafo_denso.sequencia_de_graus())

    print("\nRemovendo aresta (A, C)...\n")
    grafo_denso.remover_aresta("A", "C")
    grafo_denso.imprimir()
    print("Número de vértices:", grafo_denso.numero_de_vertices())
    print("Número de arestas:", grafo_denso.numero_de_arestas())
    print("Sequência de graus:", grafo_denso.sequencia_de_graus())


    print("\n===== TESTE GRAFO ESPARSO =====")
    grafo_esparso = GrafoEsparso(V)
    for (u, v) in arestas:
        grafo_esparso.adicionar_aresta(u, v)

    # Adicionando múltiplas arestas (A-B 2x)
    grafo_esparso.adicionar_aresta("A", "B")
    grafo_esparso.adicionar_aresta("A", "B")

    grafo_esparso.imprimir()
    print("Número de vértices:", grafo_esparso.numero_de_vertices())
    print("Número de arestas:", grafo_esparso.numero_de_arestas())
    print("Sequência de graus:", grafo_esparso.sequencia_de_graus())

    print("\nRemovendo apenas UMA aresta (A, B)...\n")
    grafo_esparso.remover_aresta("A", "B")
    grafo_esparso.imprimir()
    print("Número de vértices:", grafo_esparso.numero_de_vertices())
    print("Número de arestas:", grafo_esparso.numero_de_arestas())
    print("Sequência de graus:", grafo_esparso.sequencia_de_graus())
