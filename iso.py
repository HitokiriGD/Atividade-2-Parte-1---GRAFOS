from itertools import permutations, product
from collections import defaultdict
from typing import List, Tuple, Dict, Optional

class Graph:
    def __init__(self, vertices: List, edges: List[Tuple]):
        self.V = list(vertices)
        self.n = len(self.V)
        self.idx = {v: i for i, v in enumerate(self.V)}
        self.A = [[0]*self.n for _ in range(self.n)]
        for u, v in edges:
            i, j = self.idx[u], self.idx[v]
            self.A[i][j] += 1
            if i != j:
                self.A[j][i] += 1  # não direcional

    def num_vertices(self) -> int:
        return self.n

    def num_edges(self) -> int:
        soma = 0
        for i in range(self.n):
            soma += self.A[i][i]  # laços
            for j in range(i+1, self.n):
                soma += self.A[i][j]
        return soma

    def degrees(self) -> List[int]:
        return [sum(self.A[i]) for i in range(self.n)]


def _compatible_by_degrees(g1: Graph, g2: Graph) -> bool:
    return sorted(g1.degrees()) == sorted(g2.degrees())


def _partition_by_degree(A: Graph) -> Dict[int, List[int]]:
    part = defaultdict(list)
    degs = A.degrees()
    for i, d in enumerate(degs):
        part[d].append(i)
    return dict(part)


def _check_mapping(g1: Graph, g2: Graph, mapping: List[int]) -> bool:
    A1, A2 = g1.A, g2.A
    n = g1.n
    for i in range(n):
        mi = mapping[i]
        row2 = A2[mi]
        for k in range(n):
            if A1[i][k] != row2[mapping[k]]:
                return False
    return True


def are_isomorphic(g1: Graph, g2: Graph) -> Tuple[bool, Optional[Dict]]:
    if g1.num_vertices() != g2.num_vertices():
        return (False, None)
    if g1.num_edges() != g2.num_edges():
        return (False, None)
    if not _compatible_by_degrees(g1, g2):
        return (False, None)

    P1 = _partition_by_degree(g1)
    P2 = _partition_by_degree(g2)

    sizes1 = sorted((d, len(P1[d])) for d in P1)
    sizes2 = sorted((d, len(P2.get(d, []))) for d in P1)
    if sizes1 != sizes2:
        return (False, None)

    per_class_perms = []
    class_pairs = []
    for d, idxs1 in P1.items():
        idxs2 = P2[d]
        per_class_perms.append(permutations(idxs2))
        class_pairs.append(idxs1)

    for choice in product(*per_class_perms):
        mapping = [-1] * g1.n
        ok = True
        for idxs1, perm2 in zip(class_pairs, choice):
            if len(idxs1) != len(perm2):
                ok = False
                break
            for i, j in zip(idxs1, perm2):
                mapping[i] = j
        if not ok:
            continue

        if _check_mapping(g1, g2, mapping):
            inv1 = {i: v for v, i in g1.idx.items()}
            inv2 = {i: v for v, i in g2.idx.items()}
            map_labels = {inv1[i]: inv2[mapping[i]] for i in range(g1.n)}
            return (True, map_labels)

    return (False, None)


# ========================
# TESTES
# ========================
if __name__ == "__main__":
    # Exemplo 1: Ciclo de 4 vértices
    g1 = Graph(
        vertices=["A", "B", "C", "D"],
        edges=[("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")]
    )
    g2 = Graph(
        vertices=["w", "x", "y", "z"],
        edges=[("w", "x"), ("x", "y"), ("y", "z"), ("z", "w")]
    )
    iso, mapping = are_isomorphic(g1, g2)
    print("Exemplo 1 - Isomorfos?", iso)
    if iso:
        print("Mapeamento:", mapping)

    # Exemplo 2: Triângulo + isolado vs caminho de 4
    g3 = Graph(["A", "B", "C", "D"], edges=[("A","B"),("B","C"),("C","A")])
    g4 = Graph(["p", "q", "r", "s"], edges=[("p","q"),("q","r"),("r","s")])
    iso2, mapping2 = are_isomorphic(g3, g4)
    print("Exemplo 2 - Isomorfos?", iso2)

    # Exemplo 3: Multigrafo
    g5 = Graph(["X","Y"], edges=[("X","Y"),("X","Y")])
    g6 = Graph(["u","v"], edges=[("u","v"),("u","v")])
    iso3, mapping3 = are_isomorphic(g5, g6)
    print("Exemplo 3 - Isomorfos (multigrafo)?", iso3, mapping3)
