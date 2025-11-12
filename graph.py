"""
Graph Data Structure
====================
A collection of nodes (vertices) and edges connecting them.

Time Complexity (V = vertices, E = edges):
Adjacency List:
- Space: O(V + E)
- Add vertex: O(1)
- Add edge: O(1)
- Remove vertex: O(V + E)
- Remove edge: O(E)
- Query edge: O(V)

Adjacency Matrix:
- Space: O(V²)
- Add vertex: O(V²)
- Add edge: O(1)
- Remove vertex: O(V²)
- Remove edge: O(1)
- Query edge: O(1)

Use Cases:
- Social networks
- Maps and navigation
- Network routing
- Dependency resolution
- Recommendation systems
"""

from collections import deque, defaultdict
import heapq


class Graph:
    """Graph using adjacency list (supports both directed and undirected)"""
    
    def __init__(self, directed=False):
        self.graph = defaultdict(list)
        self.directed = directed
        self.vertices = set()
    
    def add_vertex(self, vertex):
        """Add a vertex"""
        self.vertices.add(vertex)
        if vertex not in self.graph:
            self.graph[vertex] = []
    
    def add_edge(self, u, v, weight=1):
        """Add an edge"""
        self.vertices.add(u)
        self.vertices.add(v)
        self.graph[u].append((v, weight))
        
        if not self.directed:
            self.graph[v].append((u, weight))
    
    def remove_edge(self, u, v):
        """Remove an edge"""
        self.graph[u] = [(vertex, weight) for vertex, weight in self.graph[u] if vertex != v]
        
        if not self.directed:
            self.graph[v] = [(vertex, weight) for vertex, weight in self.graph[v] if vertex != u]
    
    def remove_vertex(self, vertex):
        """Remove a vertex and all its edges"""
        if vertex in self.vertices:
            self.vertices.remove(vertex)
        
        # Remove all edges to this vertex
        for v in self.graph:
            self.graph[v] = [(neighbor, weight) for neighbor, weight in self.graph[v] 
                           if neighbor != vertex]
        
        # Remove vertex from graph
        if vertex in self.graph:
            del self.graph[vertex]
    
    def get_neighbors(self, vertex):
        """Get all neighbors of a vertex"""
        return self.graph[vertex]
    
    def has_edge(self, u, v):
        """Check if edge exists"""
        return any(vertex == v for vertex, _ in self.graph[u])
    
    def bfs(self, start):
        """Breadth-First Search traversal"""
        visited = set()
        queue = deque([start])
        result = []
        
        visited.add(start)
        
        while queue:
            vertex = queue.popleft()
            result.append(vertex)
            
            for neighbor, _ in self.graph[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return result
    
    def dfs(self, start):
        """Depth-First Search traversal"""
        visited = set()
        result = []
        
        def dfs_recursive(vertex):
            visited.add(vertex)
            result.append(vertex)
            
            for neighbor, _ in self.graph[vertex]:
                if neighbor not in visited:
                    dfs_recursive(neighbor)
        
        dfs_recursive(start)
        return result
    
    def shortest_path_bfs(self, start, end):
        """Find shortest path using BFS (unweighted graph)"""
        if start == end:
            return [start]
        
        visited = {start}
        queue = deque([(start, [start])])
        
        while queue:
            vertex, path = queue.popleft()
            
            for neighbor, _ in self.graph[vertex]:
                if neighbor == end:
                    return path + [neighbor]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def dijkstra(self, start, end=None):
        """Dijkstra's algorithm for shortest path (weighted graph)"""
        distances = {vertex: float('infinity') for vertex in self.vertices}
        distances[start] = 0
        previous = {}
        pq = [(0, start)]
        visited = set()
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            if end and current == end:
                break
            
            for neighbor, weight in self.graph[current]:
                distance = current_dist + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current
                    heapq.heappush(pq, (distance, neighbor))
        
        if end:
            # Reconstruct path
            if distances[end] == float('infinity'):
                return None, float('infinity')
            
            path = []
            current = end
            while current in previous:
                path.append(current)
                current = previous[current]
            path.append(start)
            return path[::-1], distances[end]
        
        return distances
    
    def has_cycle(self):
        """Detect cycle in graph"""
        visited = set()
        rec_stack = set()
        
        def has_cycle_util(vertex, parent=-1):
            visited.add(vertex)
            
            if self.directed:
                rec_stack.add(vertex)
            
            for neighbor, _ in self.graph[vertex]:
                if neighbor not in visited:
                    if has_cycle_util(neighbor, vertex):
                        return True
                elif self.directed:
                    if neighbor in rec_stack:
                        return True
                else:
                    if neighbor != parent:
                        return True
            
            if self.directed:
                rec_stack.remove(vertex)
            
            return False
        
        for vertex in self.vertices:
            if vertex not in visited:
                if has_cycle_util(vertex):
                    return True
        
        return False
    
    def topological_sort(self):
        """Topological sort (only for directed acyclic graphs)"""
        if not self.directed:
            raise ValueError("Topological sort only works for directed graphs")
        
        visited = set()
        stack = []
        
        def dfs(vertex):
            visited.add(vertex)
            
            for neighbor, _ in self.graph[vertex]:
                if neighbor not in visited:
                    dfs(neighbor)
            
            stack.append(vertex)
        
        for vertex in self.vertices:
            if vertex not in visited:
                dfs(vertex)
        
        return stack[::-1]
    
    def is_bipartite(self):
        """Check if graph is bipartite (can be colored with 2 colors)"""
        color = {}
        
        def bfs_check(start):
            queue = deque([start])
            color[start] = 0
            
            while queue:
                vertex = queue.popleft()
                
                for neighbor, _ in self.graph[vertex]:
                    if neighbor not in color:
                        color[neighbor] = 1 - color[vertex]
                        queue.append(neighbor)
                    elif color[neighbor] == color[vertex]:
                        return False
            
            return True
        
        for vertex in self.vertices:
            if vertex not in color:
                if not bfs_check(vertex):
                    return False
        
        return True
    
    def connected_components(self):
        """Find all connected components (for undirected graph)"""
        visited = set()
        components = []
        
        def dfs(vertex, component):
            visited.add(vertex)
            component.append(vertex)
            
            for neighbor, _ in self.graph[vertex]:
                if neighbor not in visited:
                    dfs(neighbor, component)
        
        for vertex in self.vertices:
            if vertex not in visited:
                component = []
                dfs(vertex, component)
                components.append(component)
        
        return components
    
    def __str__(self):
        result = []
        for vertex in sorted(self.vertices):
            neighbors = [(n, w) for n, w in self.graph[vertex]]
            result.append(f"{vertex}: {neighbors}")
        return "\n".join(result)


class WeightedGraph:
    """Weighted graph using adjacency matrix"""
    
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for _ in range(vertices)] for _ in range(vertices)]
    
    def add_edge(self, u, v, weight):
        """Add weighted edge"""
        self.graph[u][v] = weight
        self.graph[v][u] = weight
    
    def prim_mst(self):
        """Prim's algorithm for Minimum Spanning Tree"""
        selected = [False] * self.V
        parent = [-1] * self.V
        key = [float('infinity')] * self.V
        
        key[0] = 0
        mst_edges = []
        
        for _ in range(self.V):
            # Find minimum key vertex not yet included
            min_key = float('infinity')
            u = -1
            
            for v in range(self.V):
                if not selected[v] and key[v] < min_key:
                    min_key = key[v]
                    u = v
            
            selected[u] = True
            
            if parent[u] != -1:
                mst_edges.append((parent[u], u, self.graph[parent[u]][u]))
            
            # Update key values
            for v in range(self.V):
                if (self.graph[u][v] > 0 and not selected[v] and 
                    self.graph[u][v] < key[v]):
                    key[v] = self.graph[u][v]
                    parent[v] = u
        
        return mst_edges


# Example usage
if __name__ == "__main__":
    print("=== Undirected Graph ===")
    g = Graph(directed=False)
    
    # Add edges
    g.add_edge('A', 'B', 1)
    g.add_edge('A', 'C', 2)
    g.add_edge('B', 'D', 3)
    g.add_edge('C', 'D', 1)
    g.add_edge('D', 'E', 2)
    
    print("Graph:")
    print(g)
    
    print(f"\nBFS from A: {g.bfs('A')}")
    print(f"DFS from A: {g.dfs('A')}")
    
    print(f"\nShortest path A to E: {g.shortest_path_bfs('A', 'E')}")
    
    path, distance = g.dijkstra('A', 'E')
    print(f"Dijkstra A to E: {path} (distance: {distance})")
    
    print(f"\nHas cycle: {g.has_cycle()}")
    print(f"Is bipartite: {g.is_bipartite()}")
    print(f"Connected components: {g.connected_components()}")
    
    print("\n=== Directed Graph ===")
    dg = Graph(directed=True)
    
    # DAG for topological sort
    dg.add_edge('A', 'C')
    dg.add_edge('B', 'C')
    dg.add_edge('B', 'D')
    dg.add_edge('C', 'E')
    dg.add_edge('D', 'F')
    dg.add_edge('E', 'F')
    
    print("Directed Graph:")
    print(dg)
    
    print(f"\nTopological Sort: {dg.topological_sort()}")
    print(f"Has cycle: {dg.has_cycle()}")
    
    print("\n=== Minimum Spanning Tree (Prim's) ===")
    wg = WeightedGraph(5)
    wg.add_edge(0, 1, 2)
    wg.add_edge(0, 3, 6)
    wg.add_edge(1, 2, 3)
    wg.add_edge(1, 3, 8)
    wg.add_edge(1, 4, 5)
    wg.add_edge(2, 4, 7)
    wg.add_edge(3, 4, 9)
    
    mst = wg.prim_mst()
    print(f"MST edges (u, v, weight):")
    total_weight = 0
    for u, v, w in mst:
        print(f"  {u} - {v}: {w}")
        total_weight += w
    print(f"Total MST weight: {total_weight}")
