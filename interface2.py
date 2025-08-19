from abc import ABC, abstractmethod

# ==========================
# INTERFACE
# ==========================
class Grafo(ABC):
    @abstractmethod
    def adicionar_aresta(self, u, v): pass
    
    @abstractmethod
    def remover_aresta(self, u, v): pass
    
    @abstractmethod
    def mostrar(self): pass
    
    @abstractmethod
    def numero_vertices(self): pass
    
    @abstractmethod
    def numero_arestas(self): pass
    
    @abstractmethod
    def sequencia_graus(self): pass

    # Novos métodos
    @abstractmethod
    def is_simples(self): pass

    @abstractmethod
    def is_nulo(self): pass

    @abstractmethod
    def is_completo(self): pass


# ==========================
# GRAFO DENSO (MATRIZ)
# ==========================
class GrafoDenso(Grafo):
    def __init__(self, vertices):
        self.vertices = vertices
        self.n = len(vertices)
        self.matriz = [[0] * self.n for _ in range(self.n)]

    def adicionar_aresta(self, u, v):
        i, j = self.vertices.index(u), self.vertices.index(v)
        self.matriz[i][j] += 1
        self.matriz[j][i] += 1

    def remover_aresta(self, u, v):
        i, j = self.vertices.index(u), self.vertices.index(v)
        if self.matriz[i][j] > 0:
            self.matriz[i][j] -= 1
            self.matriz[j][i] -= 1

    def mostrar(self):
        print("Matriz de Adjacência:")
        print("   ", " ".join(self.vertices))
        for i in range(self.n):
            print(self.vertices[i] + ":", " ".join(map(str, self.matriz[i])))

    def numero_vertices(self):
        return self.n

    def numero_arestas(self):
        return sum(sum(linha) for linha in self.matriz) // 2

    def sequencia_graus(self):
        return [sum(linha) for linha in self.matriz]

    # Métodos da Atividade 1
    def is_simples(self):
        # Não pode ter laço ou múltiplas arestas
        for i in range(self.n):
            if self.matriz[i][i] > 0:
                return False
        for i in range(self.n):
            for j in range(i+1, self.n):
                if self.matriz[i][j] > 1:
                    return False
        return True

    def is_nulo(self):
        return self.numero_arestas() == 0

    def is_completo(self):
        return self.numero_arestas() == self.n * (self.n - 1) // 2


# ==========================
# GRAFO ESPARSO (LISTA)
# ==========================
class GrafoEsparso(Grafo):
    def __init__(self, vertices):
        self.vertices = vertices
        self.lista_adj = {v: [] for v in vertices}

    def adicionar_aresta(self, u, v):
        self.lista_adj[u].append(v)
        self.lista_adj[v].append(u)

    def remover_aresta(self, u, v):
        if v in self.lista_adj[u]:
            self.lista_adj[u].remove(v)
        if u in self.lista_adj[v]:
            self.lista_adj[v].remove(u)

    def mostrar(self):
        print("Lista de Adjacência:")
        for v in self.lista_adj:
            print(v, ":", self.lista_adj[v])

    def numero_vertices(self):
        return len(self.vertices)

    def numero_arestas(self):
        return sum(len(adj) for adj in self.lista_adj.values()) // 2

    def sequencia_graus(self):
        return [len(self.lista_adj[v]) for v in self.vertices]

    # Métodos da Atividade 1
    def is_simples(self):
        # Não pode ter laço ou múltiplas arestas
        for v in self.lista_adj:
            if v in self.lista_adj[v]:
                return False
            vizinhos = self.lista_adj[v]
            if len(vizinhos) != len(set(vizinhos)):
                return False
        return True

    def is_nulo(self):
        return self.numero_arestas() == 0

    def is_completo(self):
        n = len(self.vertices)
        for v in self.lista_adj:
            if len(set(self.lista_adj[v])) != n - 1:
                return False
        return True


# ==========================
# TESTES
# ==========================
if __name__ == "__main__":
    print("===== TESTE GRAFO DENSO =====")
    vertices = ["A", "B", "C"]
    g1 = GrafoDenso(vertices)
    g1.adicionar_aresta("A", "B")
    g1.adicionar_aresta("B", "C")
    g1.adicionar_aresta("A", "C")
    g1.mostrar()
    print("É simples?", g1.is_simples())
    print("É nulo?", g1.is_nulo())
    print("É completo?", g1.is_completo())

    print("\n===== TESTE GRAFO ESPARSO =====")
    g2 = GrafoEsparso(vertices)
    g2.adicionar_aresta("A", "B")
    g2.adicionar_aresta("B", "C")
    g2.adicionar_aresta("A", "C")
    g2.mostrar()
    print("É simples?", g2.is_simples())
    print("É nulo?", g2.is_nulo())
    print("É completo?", g2.is_completo())
