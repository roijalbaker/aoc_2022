import re
import numpy as np
from pydantic.dataclasses import dataclass
from numpy.linalg import norm
from typing import List
from scipy import sparse
from collections import OrderedDict


def line_to_path(line: str):
    regex = r"at x=([-]*\d+), y=([-]*\d+): .*x=([-]*\d+), y=([-]*\d+)"
    points = re.findall(regex, line)
    return points


def parse_file(fn):
    paths = []
    with open(fn, "r") as f:
        for line in f.readlines():
            paths.extend(line_to_path(line))
    return paths


@dataclass
class Beacon:
    x: int
    y: int

    @property
    def as_vector(self):
        return np.array([self.x, self.y])


@dataclass
class Sensor(Beacon):
    beacon: Beacon

    @property
    def distance(self) -> int:
        if not hasattr(self, "_distance"):
            self._distance = norm(self.as_vector - self.beacon.as_vector, 1)
        return int(self._distance)

    def inside_range(self, x, y):
        # print("\t", self, x, y, self.distance, norm(self.as_vector - np.array([x, y])) <= self.distance)
        return norm(self.as_vector - np.array([x, y]), 1) <= self.distance


def solve_less_naive(sensors: List[Sensor], y):
    covered_x = set([])
    for s in sensors:
        dist_y = int(s.distance - norm(np.array([s.x, y]) - s.as_vector))
        if dist_y > 0:
            covered_x.update(set(range(s.x-dist_y, s.x+dist_y+1,1)))
    for s in sensors:
        if s.beacon.y == y and s.beacon.x in covered_x:
            covered_x.remove(s.beacon.x)
    print(len(covered_x))


def part2(sensors: List[Sensor], max_size=20):
    # set a default dictionary for all y
    not_covered = OrderedDict([])

    # Initialize all possible x coordinates
    for y in range(max_size + 1):
        beacon_x = set([sensor.beacon.x for sensor in sensors if sensor.beacon.y == y])
        not_covered.update({y: set(range(max_size + 1)).difference(beacon_x)})

    # loop over sensors to remove possible x coordinates   
    for s in sensors:
        for y in range(max_size + 1):
            dist_y = int(s.distance - norm(np.array([s.x, y]) - s.as_vector))
            if dist_y > 0:
                not_covered.update({y: not_covered[y].difference(set(range(s.x-dist_y, s.x+dist_y+1, 1)))})

    y, x = next((key, list(value)[0]) for key, value in not_covered.items() if len(value) > 0)

    print(4000000 * x + y)


def part2_less_naive(sensors: List[Sensor], max_size=20):
    # Create a map in numpy
    layout = np.ones((max_size+1, max_size+1))  # all points are visible

    for sensor in sensors:
        if 0 <= (b := sensor.beacon).x <= max_size and 0 <= b.y <= max_size:
            layout[b.y, b.x] = 0

    # loop over sensors to remove possible x coordinates   
    for s in sensors:
        for i, distance in enumerate(reversed(range(s.distance+1))):
            # print(s.x + distance, -2*i -1, +2*i+1)
            if 0 <= s.x + distance <= max_size:
                layout[
                    max(0, s.y - i):min(max_size + 1, s.y + i + 1),
                    s.x + distance
                ] = 0
            if not distance:
                continue
            if 0 <= s.x - distance <= max_size:
                layout[
                    max(0, s.y - i):min(max_size+1, s.y + i + 1),
                    s.x - distance
                ] = 0
    np.savetxt("part2.txt", layout, fmt="%d")
    print((sol := (sparse.csr_matrix(layout).nonzero())))
    return sol[1][0], sol[0][0]


def solve_naive(sensors: List[Sensor], y, x_min, x_max):
    outside_range = []
    xrange = range(x_min-2, x_max + 2, 1)
    existing_beacons = [s.beacon.x for s in sensors if s.beacon.y == y]
    for x in xrange:
        if x in existing_beacons:
            outside_range.append(True)  # hack to evade beacons
            continue
        # loop over all sensors to figure out whether it is outside all of these ranges
        outside_all_ranges = next((not value for s in sensors if (value := s.inside_range(x, y))), True)
        outside_range.append(outside_all_ranges)
        # print(x,y, outside_range[-1])
    print(sum([not x for x in outside_range]))


if __name__ == "__main__":
    sensors_beacons = parse_file("day15_test1.txt")
    sensors = [Sensor(s_x, s_y, Beacon(b_x, b_y)) for s_x, s_y, b_x, b_y in sensors_beacons]
    x_max = max([max(sensor.x, sensor.beacon.x) for sensor in sensors])
    x_min = min([min(sensor.x, sensor.beacon.x) for sensor in sensors])
    y_max = max([max(sensor.y, sensor.beacon.y) for sensor in sensors])
    y_min = min([min(sensor.y, sensor.beacon.y) for sensor in sensors])
    print(x_min, x_max, y_min, y_max)
    # solve_naive(sensors, 10, x_min, x_max)  # takes ages
    solve_less_naive(sensors, 2000000)
    x, y = part2_less_naive(sensors, 20)
    print(4000000 * x + y)
