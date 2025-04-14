def trace_to_founders(graph, subject_id, founders, max_depth=20):
    paths = []

    def dfs(node, path, depth):
        if depth > max_depth:
            return
        if node in founders:
            paths.append(path + [node])
            return
        for parent in graph.successors(node):  # child -> parents
            dfs(parent, path + [node], depth + 1)

    dfs(subject_id, [], 0)
    print(f"Finished DFS. Total paths found: {len(paths)}")
    return paths