import re
import numpy as np
from pydantic.dataclasses import dataclass
from numpy.linalg import norm


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
    def distance(self):
        if not hasattr(self, "_distance"):
            self._distance = norm(self.as_vector - self.beacon.as_vector, 1)
        return self._distance

    def inside_range(self, x, y):
        # print("\t", self, x, y, self.distance, norm(self.as_vector - np.array([x, y])) <= self.distance)
        return norm(self.as_vector - np.array([x, y]), 1) <= self.distance


if __name__ == "__main__":
    sensors_beacons = parse_file("day15_test1.txt")
    sensors = [Sensor(s_x, s_y, Beacon(b_x, b_y)) for s_x, s_y, b_x, b_y in sensors_beacons]
    x_max = max([max(sensor.x, sensor.beacon.x) for sensor in sensors])
    x_min = min([min(sensor.x, sensor.beacon.x) for sensor in sensors])
    y_max = max([max(sensor.y, sensor.beacon.y) for sensor in sensors])
    y_min = min([min(sensor.y, sensor.beacon.y) for sensor in sensors])

    y = 10
    outside_range = []
    xrange = range(x_min-2, x_max + 2, 1)
    existing_beacons = [s.beacon for s in sensors if s.beacon.y == y]
    for x in xrange:
        if x in [b.x for b in existing_beacons]:
            outside_range.append(True)  # hack to evade beacons
            continue    
        # loop over all sensors to figure out whether it is outside all of these ranges
        outside_all_ranges = next((not value for s in sensors if (value := s.inside_range(x, y))), True)
        outside_range.append(outside_all_ranges)
        # print(x,y, outside_range[-1])
    print(list(zip(xrange, outside_range)))
    print(sum([not x for x in outside_range]))

