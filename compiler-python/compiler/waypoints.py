import os

class WaypointsDatabase:
  waypoints = set()

  def initialize():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, "waypoints.txt"), "r") as f:
      for line in f:
        parts = line.split(",")
        WaypointsDatabase.waypoints.add(parts[0])