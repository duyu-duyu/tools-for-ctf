#!/usr/bin/env python3

import re
from pathlib import Path
from argparse import ArgumentParser
from PIL import Image, ImageDraw

DT=0.25
MARGIN=20

DIR_RE = re.compile(r'\(x=(?P<x>[\-]?\d+(\.\d+)?),y=(?P<y>[\-]?\d+(\.\d+)?),z=(?P<z>[\-]?\d+(\.\d+)?)\)')
ACCEL_RE = re.compile(r'(?P<accel>[\-]?\d+(\.\d+)?)')

def info(msg):
    print(f"[drone-trajectory]> {msg}")

def parse_sensors_data(sensors_logfile):
    accel = None
    direction = None
    sensors_data = []
    with sensors_logfile.open() as fp:
        for line in fp:
            line = line.split(':')[-1].strip()
            match = ACCEL_RE.match(line)
            if match:
                accel = float(match.group('accel'))
            match = DIR_RE.match(line)
            if match:
                direction = (float(match.group('x')), float(match.group('y')), float(match.group('z')))
                if not accel:
                    RuntimeError("log parsing failed.")
                sensors_data.append((accel, direction))
                accel = None
    return sensors_data

def compute_trajectory(sensors_data):
    pos = (0, 0, 0)
    speed = 0
    trajectory = []
    for accel, direction in sensors_data:
        speed += DT * accel
        trajectory.append(pos)
        pos = (
            pos[0] + speed * direction[0],
            pos[1] + speed * direction[1],
            pos[2] + speed * direction[2],
        )
    trajectory.append(pos)
    return trajectory

def bounding_rect(trajectory):
    min_x, max_x = 0, 0
    min_y, max_y = 0, 0
    for point in trajectory:
        min_x = min(min_x, point[0])
        max_x = max(max_x, point[0])
        min_y = min(min_y, point[1])
        max_y = max(max_y, point[1])
    w = int(max_x - min_x)
    h = int(max_y - min_y)
    return w, h

def draw_trajectory(trajectory, output_image):
    w, h = bounding_rect(trajectory)
    img = Image.new('RGB', (w+2*MARGIN, h+2*MARGIN), color='white')
    drawer = ImageDraw.Draw(img, 'RGB')
    for point in trajectory:
        drawer.point((point[0]+MARGIN, -point[1]+h+MARGIN), fill='black')
    img.save(output_image)

def parse_args():
    p = ArgumentParser(description="")
    p.add_argument('sensors_logfile', type=Path, help="")
    p.add_argument('output_image', type=Path, help="")
    return p.parse_args()

def app():
    args = parse_args()
    info('parsing sensors data...')
    sensors_data = parse_sensors_data(args.sensors_logfile)
    info('computing trajectory...')
    trajectory = compute_trajectory(sensors_data)
    info('drawing trajectory...')
    draw_trajectory(trajectory, args.output_image)

if __name__ == '__main__':
    app()