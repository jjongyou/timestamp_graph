#!/usr/bin/env python

import rclpy
import time
from rclpy.node import Node
from ichthus_msgs.msg import Common
from std_msgs.msg import Float64
import matplotlib.pyplot as plt


class Steer_graph(Node):

  def __init__(self):
    super().__init__("steer_graph")
    self.ref_subs = self.create_subscription(
      Common, "ref_ang", self.ref_callback, 1)
    self.whl_ang_subs = self.create_subscription(
      Common, "cur_ang", self.str_callback, 1)
    self.start_flag = False
    self.start_time = 0
    self.str_ang_axis = []
    self.cur_str_time_axis = []
    self.ref_str_time_axis = []
    self.ref_ang_axis = []
    self.ref_ang = 0
    self.ref_ang_time = 0
    self.ref_subs
    self.fig = plt.figure()

  def str_callback(self, data):
    if self.start_flag == False:
        self.start_time = time.time()
        self.start_flag = True
        
    arrive_time = data.time
    curr_ang = -data.data

    cur_time_index = arrive_time - self.start_time
    self.cur_str_time_axis.append(cur_time_index)
    self.str_ang_axis.append(curr_ang)

    ref_time_index = self.ref_ang_time - self.start_time
    self.ref_str_time_axis.append(ref_time_index)
    self.ref_ang_axis.append(self.ref_ang)

    plt.xlabel("Time (Seconds)", fontsize=14)
    plt.ylabel("Steer Angle", fontsize=14)
    plt.plot(self.ref_str_time_axis, self.ref_ang_axis, color="red", label="Ref")
    plt.plot(self.cur_str_time_axis, self.str_ang_axis, color="black", label="Vel")
    plt.draw()
    plt.pause(0.2)
    self.fig.clear()

  def ref_callback(self, data):
    if self.start_flag == False:
        self.start_time = time.time()
        self.start_flag = True
    self.ref_ang = -data.data
    self.ref_ang_time = data.time


def main(args=None):
  rclpy.init(args=args)
  steer_graph = Steer_graph()

  rclpy.spin(steer_graph)

  steer_graph.destroy_node()
  rclpy.shutdown()


if __name__ == "__main__":
  main()
