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

    # Atividade 3
    @abstractmethod
    def get_vertices(self): pass

    @abstractmethod
    def get_arestas(self): pass

    @abstractmethod
    def is_subgrafo(self, outro_grafo): pass

    @abstractmethod
    def is_subgrafo_gerador(self, outro_grafo): pass

    @abstractmethod
    def is_subgrafo_induzido(self, outro_grafo): pass


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

    # Métodos da Atividade 3
    def get_vertices(self):
        return self.vertices

    def get_arestas(self):
        arestas = []
        for i in range(self.n):
            for j in range(i+1, self.n):
                if self.matriz[i][j] > 0:
                    arestas.append((self.vertices[i], self.vertices[j]))
        return arestas

    def is_subgrafo(self, outro_grafo):
        return (set(self.get_vertices()).issubset(set(outro_grafo.get_vertices())) and
                set(self.get_arestas()).issubset(set(outro_grafo.get_arestas())))

    def is_subgrafo_gerador(self, outro_grafo):
        return (set(self.get_vertices()) == set(outro_grafo.get_vertices()) and
                set(self.get_arestas()).issubset(set(outro_grafo.get_arestas())))

    def is_subgrafo_induzido(self, outro_grafo):
        if not set(self.get_vertices()).issubset(set(outro_grafo.get_vertices())):
            return False
        arestas_outro = set(outro_grafo.get_arestas())
        arestas_induzidas = set()
        for u in self.get_vertices():
            for v in self.get_vertices():
                if u != v and (u, v) in arestas_outro or (v, u) in arestas_outro:
                    arestas_induzidas.add(tuple(sorted((u, v))))
        return set(self.get_arestas()) == arestas_induzidas


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

    # Métodos da Atividade 3
    def get_vertices(self):
        return self.vertices

    def get_arestas(self):
        arestas = set()
        for u in self.lista_adj:
            for v in self.lista_adj[u]:
                arestas.add(tuple(sorted((u, v))))
        return list(arestas)

    def is_subgrafo(self, outro_grafo):
        return (set(self.get_vertices()).issubset(set(outro_grafo.get_vertices())) and
                set(self.get_arestas()).issubset(set(outro_grafo.get_arestas())))

    def is_subgrafo_gerador(self, outro_grafo):
        return (set(self.get_vertices()) == set(outro_grafo.get_vertices()) and
                set(self.get_arestas()).issubset(set(outro_grafo.get_arestas())))

    def is_subgrafo_induzido(self, outro_grafo):
        if not set(self.get_vertices()).issubset(set(outro_grafo.get_vertices())):
            return False
        arestas_outro = set(outro_grafo.get_arestas())
        arestas_induzidas = set()
        for u in self.get_vertices():
            for v in self.get_vertices():
                if u != v and (tuple(sorted((u, v))) in arestas_outro):
                    arestas_induzidas.add(tuple(sorted((u, v))))
        return set(self.get_arestas()) == arestas_induzidas


# ==========================
# TESTES
# ==========================
if __name__ == "__main__":
    print("===== TESTE GRAFO DENSO =====")
    vertices = ["A", "B", "C"]
    g1 = GrafoDenso(vertices)
    g1.adicionar_aresta("A", "B")
    g1.adicionar_aresta("B", "C")
    g1.mostrar()
    print("Vértices:", g1.get_vertices())
    print("Arestas:", g1.get_arestas())
    print("É simples?", g1.is_simples())
    print("É subgrafo de si mesmo?", g1.is_subgrafo(g1))

    print("\n===== TESTE GRAFO ESPARSO =====")
    g2 = GrafoEsparso(vertices)
    g2.adicionar_aresta("A", "B")
    g2.adicionar_aresta("B", "C")
    g2.mostrar()
    print("Vértices:", g2.get_vertices())
    print("Arestas:", g2.get_arestas())
    print("É simples?", g2.is_simples())
    print("É subgrafo de si mesmo?", g2.is_subgrafo(g2))
