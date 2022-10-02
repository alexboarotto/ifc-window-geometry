import numpy
from modules.ifc_window_type_partitioning_enum import IfcWindowTypePartitioningEnum
from modules.get_props import get_props as props
from modules.generate_geometry import generate_geometry as geo

def print_heading(text):
  print("============================================")
  print(text)
  print("============================================")

def create_geometry(window_type = IfcWindowTypePartitioningEnum.NOTDEFINED, OHeight = 500, OWidth = 500):
  if window_type not in [wType.name for wType in list(IfcWindowTypePartitioningEnum)]:
    raise Exception("Window Type not valid.")

  if window_type == IfcWindowTypePartitioningEnum(1).name:
    print_heading(window_type)
    create_double_panel_horizontal(OHeight, OWidth)
  elif window_type == IfcWindowTypePartitioningEnum(2).name:
    print_heading(window_type)
    create_double_panel_vertical(OHeight, OWidth)
  elif window_type == IfcWindowTypePartitioningEnum(3).name:
    print_heading(window_type)
    create_single_panel(OHeight, OWidth)
  elif window_type == IfcWindowTypePartitioningEnum(4).name:
    print_heading(window_type)
    create_triple_panel_bottom(OHeight, OWidth)
  elif window_type == IfcWindowTypePartitioningEnum(5).name:
    print_heading(window_type)
    create_triple_panel_horizontal(OHeight, OWidth)
  elif window_type == IfcWindowTypePartitioningEnum(6).name:
    print_heading(window_type)
    create_triple_panel_left(OHeight, OWidth)
  elif window_type == IfcWindowTypePartitioningEnum(7).name:
    print_heading(window_type)
    create_triple_panel_right(OHeight, OWidth)
  elif window_type == IfcWindowTypePartitioningEnum(8).name:
    print_heading(window_type)
    create_triple_panel_top(OHeight, OWidth)
  elif window_type == IfcWindowTypePartitioningEnum(9).name:
    print_heading(window_type)
    create_triple_panel_vertical(OHeight, OWidth)
  elif window_type == IfcWindowTypePartitioningEnum(10).name:
    print_heading(window_type)
    create_userdefined(OHeight, OWidth)
  elif window_type == IfcWindowTypePartitioningEnum(11).name:
    print_heading(window_type)
    create_undefined(OHeight, OWidth)

def create_single_panel(OHeight, OWidth):
  print("Lining Thickness> ", end="")
  LiningThickness = int(input())

  print("Lining To Panel Offset X> ", end="")
  LiningToPanelOffsetX = int(input())

  print("Frame Thickness> ", end="")
  FrameThickness = int(input())

  print(format(geo.single_panel(OverallHeight=OHeight,
                   OverallWidth=OWidth,
                   LiningProps=props.get_lining_props(LiningThickness=LiningThickness, LiningToPanelOffsetX=LiningToPanelOffsetX), 
                   PanelProps=props.get_panel_props(FrameThickness=FrameThickness)
                  )   
  )) 

# ===================================================
# TODO: create functions for remaining window types
# ===================================================
def create_double_panel_horizontal():
  pass

def create_double_panel_vertical():
  pass

def create_triple_panel_bottom():
  pass

def create_triple_panel_horizontal():
  pass

def create_triple_panel_left():
  pass

def create_triple_panel_right():
  pass

def create_triple_panel_top():
  pass

def create_triple_panel_vertical():
  pass

def create_userdefined():
  pass

def create_undefined():
  pass


def main():
  print("Input Overall Height> ", end="")
  OHeight = int(input())
  print("Input Overall Width> ", end="")
  OWidth = int(input())

  print("Input Window Type> ", end="")
  create_geometry(str(input()), OHeight=OHeight, OWidth=OWidth)
  

if __name__ == '__main__':
  main()