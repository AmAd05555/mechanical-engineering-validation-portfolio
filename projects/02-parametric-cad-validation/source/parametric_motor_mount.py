"""Parametric Adjustable Motor Mount benchmark project.
Generated for CAD validation, geometry robustness, configuration testing, and debugging practice.
Units: mm.
"""
import cadquery as cq

DEFAULT = dict(
    base_l=220, base_w=140, base_t=8,
    slot_l=90, slot_w=12, slot_offset=45,
    slider_l=130, slider_w=110, slider_t=10,
    motor_pitch_x=70, motor_pitch_y=50,
    motor_hole_d=8.5, guide_hole_d=10.5,
    pin_d=10, travel=40, edge_fillet=4,
)

def base_plate(p=DEFAULT):
    base = cq.Workplane("XY").rect(p["base_l"],p["base_w"]).extrude(p["base_t"])
    for y in (p["slot_offset"],-p["slot_offset"]):
        slot=(cq.Workplane("XY").center(0,y).slot2D(p["slot_l"],p["slot_w"]).extrude(p["base_t"]+2))
        base=base.cut(slot)
    xh=p["base_l"]/2-20; yh=p["base_w"]/2-15
    base=base.faces(">Z").workplane().pushPoints([(xh,yh),(xh,-yh),(-xh,yh),(-xh,-yh)]).hole(9)
    return base

def slider_plate(p=DEFAULT):
    s=cq.Workplane("XY").rect(p["slider_l"],p["slider_w"]).extrude(p["slider_t"])
    xs=p["motor_pitch_x"]/2; ys=p["motor_pitch_y"]/2
    s=s.faces(">Z").workplane().pushPoints([(xs,ys),(xs,-ys),(-xs,ys),(-xs,-ys)]).hole(p["motor_hole_d"])
    s=s.faces(">Z").workplane().pushPoints([(0,p["slot_offset"]),(0,-p["slot_offset"])]).hole(p["guide_hole_d"])
    return s

def deterministic_checks(p=DEFAULT):
    max_travel=(p["slot_l"]-p["pin_d"])/2
    return {
      "slot_clearance": p["slot_w"] > p["pin_d"],
      "guide_hole_clearance": p["guide_hole_d"] > p["pin_d"],
      "slider_inside_base": p["slider_l"] < p["base_l"] and p["slider_w"] < p["base_w"],
      "travel_valid": p["travel"] <= max_travel,
      "motor_pattern_inside_slider": (p["motor_pitch_x"]/2+p["motor_hole_d"]/2 < p["slider_l"]/2 and p["motor_pitch_y"]/2+p["motor_hole_d"]/2 < p["slider_w"]/2),
    }
