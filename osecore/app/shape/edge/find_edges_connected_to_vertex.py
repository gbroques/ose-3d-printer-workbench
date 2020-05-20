def find_edges_connected_to_vertex(vertex, edges):
    vertex_edges = []
    for e in edges:
        for v in e.Vertexes:
            if v.isSame(vertex):
                vertex_edges.append(e)
    return vertex_edges
