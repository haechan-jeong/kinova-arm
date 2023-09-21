"""
basictest3.py
Description:
    Trying to support the basic meshcat visualizer from within a Drake container.
"""

import importlib
import sys
from urllib.request import urlretrieve

# Start a single meshcat server instance to use for the remainder of this notebook.
server_args = []
# from pydrake import *
# from meshcat.servers.zmqserver import start_zmq_server_as_subprocess
# proc, zmq_url, web_url = start_zmq_server_as_subprocess(server_args=server_args)

# from manipulation import running_as_notebook

# Imports
import numpy as np
import pydot
from ipywidgets import Dropdown, Layout
from IPython.display import display, HTML, SVG

# from pydrake.multibody.plant import AddMultibodyPlantSceneGraph

# from pydrake.systems.meshcat_visualizer import (
#     ConnectMeshcatVisualizer
# )

from pydrake.all import (
    AddMultibodyPlantSceneGraph,
    ConnectMeshcatVisualizer, DiagramBuilder, 
    FindResourceOrThrow, GenerateHtml, InverseDynamicsController, 
    MultibodyPlant, Parser, Simulator)
#from pydrake.multibody.jupyter_widgets import MakeJointSlidersThatPublishOnCallback

# Building Diagram

builder = DiagramBuilder()

plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=1e-4)
Parser(plant, scene_graph).AddModelFromFile(FindResourceOrThrow("drake/manipulation/models/iiwa_description/iiwa7/iiwa7_no_collision.sdf"))
plant.WeldFrames(plant.world_frame(), plant.GetFrameByName("iiwa_link_0"))
plant.Finalize()

meshcat = ConnectMeshcatVisualizer(builder, scene_graph, zmq_url=None)
diagram = builder.Build()

context = diagram.CreateDefaultContext()
meshcat.load()
diagram.Publish(context)

while True:
    1