import json
import sys
from heapdict import heapdict


class Dijkstra:
    def __init__(self, graph):
        self.start = graph['start-point']
        self.links = graph['links']

        self.ready = {}
        self.distance = {}
        self.previous = {}


    def adjacent(self, point):
        adjacent_links = []

        for link in self.links:
            points = link['points']
            weight = link['weight']
            if points[0] == point and points[1] not in adjacent_links:
                adjacent_links.append({
                    'point': points[1],
                    'weight': weight
                })
            if points[1] == point and points[0] not in adjacent_links:
                adjacent_links.append({
                    'point': points[0],
                    'weight': weight
                })

        return adjacent_links


    def initialize(self):
        for link in self.links:
            points = link['points']
            self.ready[points[0]] = False
            self.distance[points[0]] = float('inf')
            self.ready[points[1]] = False
            self.distance[points[1]] = float('inf')

        self.ready[self.start] = True
        self.distance[self.start] = 0

        self.queue = heapdict()
        for link in self.adjacent(self.start):
            point = link['point']
            weight = link['weight']
            self.previous[point] = self.start
            self.distance[point] = weight
            self.queue[point] = weight


    def main(self):
        self.initialize()

        counter = 0
        while len(self.queue) > 0:
            counter += 1

            point, distance = self.queue.popitem()
            self.ready[point] = True

            for link in self.adjacent(point):
                adjacent_point = link['point']
                weight = link['weight']
                path_weight = self.distance[point] + weight
                if adjacent_point in self.queue and path_weight < self.distance[adjacent_point]:
                    self.previous[adjacent_point] = point
                    self.distance[adjacent_point] = path_weight
                    self.queue[adjacent_point] = path_weight
                elif adjacent_point not in self.queue and not self.ready[adjacent_point]:
                    self.previous[adjacent_point] = point
                    self.distance[adjacent_point] = path_weight
                    self.queue[adjacent_point] = path_weight

            print 'Iteration:', counter
            print [point for point, ready in self.ready.items() if ready]
            print sorted(self.distance.items(), key=lambda pd: pd[1])
            print


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        graph_json = json.load(f)
    DIJKSTRA = Dijkstra(graph_json)
    DIJKSTRA.main()
