from manim import *
from heapq import heappop, heappush

class DijkstraScene(Scene):
    def construct(self):
        self.title()
        graph, edge_labels, neighbors = self.create_graph()
        self.play(Create(graph), *[Write(label) for label in edge_labels.values()])
        self.wait(1)
        self.run_dijkstra(graph, edge_labels, neighbors, start='A', end='F')

    def title(self):
        title = Text("Dijkstra's Shortest Path Algorithm", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

    def create_graph(self):
        vertices = ['A', 'B', 'C', 'D', 'E', 'F']
        edges = [
            ('A', 'B'), ('A', 'C'), ('B', 'D'),
            ('C', 'D'), ('C', 'E'), ('D', 'F'),
            ('E', 'F')
        ]
        weights = {
            ('A', 'B'): 2,
            ('A', 'C'): 4,
            ('B', 'D'): 7,
            ('C', 'D'): 1,
            ('C', 'E'): 3,
            ('D', 'F'): 1,
            ('E', 'F'): 5
        }
        positions = {
            'A': LEFT * 4 + UP * 2,
            'B': LEFT * 2 + UP * 1,
            'C': LEFT * 2 + DOWN * 1,
            'D': ORIGIN,
            'E': RIGHT * 2 + DOWN,
            'F': RIGHT * 4
        }

        graph = Graph(
            vertices,
            edges,
            layout=positions,
            labels=True,
            edge_config={"stroke_width": 4}
        )

        edge_labels = {}
        for (u, v), weight in weights.items():
            edge_center = (graph[u].get_center() + graph[v].get_center()) / 2
            label = Text(str(weight), font_size=30).move_to(edge_center + 0.3 * UP)
            edge_labels[(u, v)] = label
            self.add(label)

        neighbors = {v: [] for v in vertices}
        for u, v in edges:
            neighbors[u].append(v)
            neighbors[v].append(u)

        return graph, edge_labels, neighbors

    def run_dijkstra(self, graph, edge_labels, neighbors, start='A', end='F'):
        weights = {
            ('A', 'B'): 2, ('A', 'C'): 4,
            ('B', 'D'): 7, ('C', 'D'): 1,
            ('C', 'E'): 3, ('D', 'F'): 1,
            ('E', 'F'): 5
        }

        vertices = list(graph.vertices)
        dist = {v: float('inf') for v in vertices}
        prev = {v: None for v in vertices}
        dist[start] = 0
        queue = [(0, start)]

        # Distance labels
        dist_labels = {}
        for v in vertices:
            label = always_redraw(lambda v=v: Text(
                f"{dist[v] if dist[v] != float('inf') else '∞'}", font_size=24
            ).next_to(graph[v], UP))
            dist_labels[v] = label
            self.add(label)

        visited = set()
        distance_text = Text(f"Start: {start}, Distance: {dist[start]}", font_size=24).to_edge(UP)
        self.play(Write(distance_text))

        while queue:
            current_dist, u = heappop(queue)
            if u in visited:
                continue
            visited.add(u)

            self.play(graph[u].animate.set_fill(GREEN, opacity=0.6), run_time=0.5)
            distance_text.become(Text(f"Current Node: {u}, Distance: {dist[u]}", font_size=24).to_edge(UP))

            for v in neighbors[u]:
                edge = (u, v) if (u, v) in weights else (v, u)
                alt = dist[u] + weights[edge]

                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    heappush(queue, (alt, v))

                    label_key = edge if edge in edge_labels else (edge[1], edge[0])
                    self.play(
                        edge_labels[label_key].animate.set_color(YELLOW),
                        graph[v].animate.set_color(BLUE),
                        run_time=0.5
                    )

            self.wait(0.5)

        # Trace back the shortest path
        path_edges = []
        path_nodes = [end]
        u = end
        while prev[u] is not None:
            path_edges.append((prev[u], u))
            path_nodes.append(prev[u])
            u = prev[u]
        path_edges.reverse()
        path_nodes.reverse()

        # Visualize shortest path
        lines = []
        for u, v in path_edges:
            edge = (u, v) if (u, v) in graph.edges else (v, u)
            line = graph.edges[edge]
            lines.append(line)

        self.play(*[line.animate.set_color(RED).set_stroke(width=8) for line in lines])
        self.wait(1)

        # Display shortest path text
        path_text = " → ".join(path_nodes)
        final_text = Text(f"Shortest Path: {path_text}", font_size=36).to_edge(DOWN)
        self.play(Write(final_text))
        self.wait(2)
