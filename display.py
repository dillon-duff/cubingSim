from manim import (
    ThreeDScene,
    Cube,
    Create,
    Rotate,
    DEGREES,
    RIGHT,
    UP,
    OUT,
    VGroup,
    ORIGIN,
    BLACK
)
import os
import numpy as np  # Import numpy for array comparison
from dataclasses import dataclass
from typing import Dict, List, Tuple

# Add FFmpeg to PATH
os.environ["PATH"] += os.pathsep + r"C:\Program Files\ffmpeg-7.1-essentials_build\bin"

@dataclass
class CubieState:
    position: Tuple[int, int, int]
    colors: Dict[str, str]
    mobject: Cube

class RubiksCubeAnimation(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # Initialize cube state
        self.cube_state = {}
        rubiks_cube = self.create_rubiks_cube()
        self.play(Create(rubiks_cube))
        self.wait(1)
        
        # Example sequence of moves
        moves = [
            (RIGHT, 90 * DEGREES, 2),  # R
            (UP, 90 * DEGREES, 0),     # D
            (OUT, 90 * DEGREES, 1),    # E
        ]
        
        for axis, angle, layer in moves:
            self.rotate_layer(rubiks_cube, axis, angle, layer)
            self.wait(1)

    def create_rubiks_cube(self):
        rubiks_cube = VGroup()
        
        # Define colors for each face
        colors = {
            'U': "#FFFFFF",    # Up (white)
            'D': "#FFFF00",    # Down (yellow)
            'F': "#00FF00",    # Front (green)
            'B': "#0000FF",    # Back (blue)
            'L': "#FFA500",    # Left (orange)
            'R': "#FF0000"     # Right (red)
        }

        # Create cubies
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    position = (x - 1, y - 1, z - 1)
                    # Cube vector square order: IN, OUT, LEFT, RIGHT, UP, DOWN (OUT means back, IN means front)
                    cubie = Cube(side_length=0.95)
                    cubie.move_to([x - 1, y - 1, z - 1])
                    
                    # Set all faces to black by default
                    for face in cubie:
                        face.set_fill(BLACK, opacity=1)
                        face.set_stroke(BLACK, width=2, opacity=1)
                    
                    # Only color the outer faces
                    face_config = {}
                    
                    # Check if this cubie is on any outer face
                    is_on_right = x == 2
                    is_on_left = x == 0
                    is_on_up = y == 0
                    is_on_down = y == 2
                    is_on_front = z == 0
                    is_on_back = z == 2
                    
                    # Color the visible faces only
                    if is_on_right:
                        face_config["right"] = colors['R']
                        cubie[3].set_fill(colors['R'], opacity=1)
                    if is_on_left:
                        face_config["left"] = colors['L']
                        cubie[2].set_fill(colors['L'], opacity=1)
                    if is_on_back:
                        face_config["back"] = colors['B']
                        cubie[1].set_fill(colors['B'], opacity=1)
                    if is_on_front:
                        face_config["front"] = colors['F']
                        cubie[0].set_fill(colors['F'], opacity=1)
                    if is_on_down:
                        face_config["down"] = colors['D']
                        cubie[4].set_fill(colors['D'], opacity=1)
                    if is_on_up:
                        face_config["up"] = colors['U']
                        cubie[5].set_fill(colors['U'], opacity=1)
                    
                    # Skip internal pieces (pieces with no colors)
                    if face_config:
                        rubiks_cube.add(cubie)
                        
                        # Store cubie state
                        self.cube_state[position] = CubieState(
                            position=position,
                            colors=face_config,
                            mobject=cubie
                        )
        
        return rubiks_cube

    def rotate_layer(self, rubiks_cube, axis, angle, layer):
        # Select cubies in the specified layer
        selected_cubies = [
            self.cube_state[tuple(map(round, cube.get_center()))]
            for cube in rubiks_cube
            if self.is_in_layer(cube, axis, layer)
        ]
        
        # Create rotation animation
        selected = VGroup(*[cubie.mobject for cubie in selected_cubies])
        rotation = Rotate(selected, angle=angle, axis=axis, about_point=ORIGIN)
        self.play(rotation)
        
        # Update cube state after rotation
        angle_degrees = int(angle / DEGREES)
        rotations = (angle_degrees // 90) % 4
        
        for _ in range(rotations):
            self.update_cube_state(selected_cubies, axis)

    def update_cube_state(self, cubies: List[CubieState], axis):
        # Update positions and face colors based on 90-degree rotation
        for cubie in cubies:
            old_pos = cubie.position
            
            # Calculate new position after rotation
            if np.allclose(axis, RIGHT):  # X-axis rotation
                new_pos = (old_pos[0], -old_pos[2], old_pos[1])
                self.rotate_colors_x(cubie)
            elif np.allclose(axis, UP):   # Y-axis rotation
                new_pos = (old_pos[2], old_pos[1], -old_pos[0])
                self.rotate_colors_y(cubie)
            else:  # Z-axis rotation
                new_pos = (-old_pos[1], old_pos[0], old_pos[2])
                self.rotate_colors_z(cubie)
            
            cubie.position = new_pos
            self.cube_state[new_pos] = cubie

    def rotate_colors_x(self, cubie):
        old_colors = cubie.colors.copy()
        if 'up' in old_colors: cubie.colors['front'] = old_colors['up']
        if 'front' in old_colors: cubie.colors['down'] = old_colors['front']
        if 'down' in old_colors: cubie.colors['back'] = old_colors['down']
        if 'back' in old_colors: cubie.colors['up'] = old_colors['back']

    def rotate_colors_y(self, cubie):
        old_colors = cubie.colors.copy()
        if 'front' in old_colors: cubie.colors['right'] = old_colors['front']
        if 'right' in old_colors: cubie.colors['back'] = old_colors['right']
        if 'back' in old_colors: cubie.colors['left'] = old_colors['back']
        if 'left' in old_colors: cubie.colors['front'] = old_colors['left']

    def rotate_colors_z(self, cubie):
        old_colors = cubie.colors.copy()
        if 'up' in old_colors: cubie.colors['right'] = old_colors['up']
        if 'right' in old_colors: cubie.colors['down'] = old_colors['right']
        if 'down' in old_colors: cubie.colors['left'] = old_colors['down']
        if 'left' in old_colors: cubie.colors['up'] = old_colors['left']

    def is_in_layer(self, cubie, axis, layer):
        """
        Determines if the cubie is in the specified layer based on the axis and layer index.
        """
        pos = cubie.get_center()
        if np.allclose(axis, RIGHT):  # X-axis
            return round(pos[0], 1) == (layer - 1)
        elif np.allclose(axis, UP):  # Y-axis
            return round(pos[1], 1) == (layer - 1)
        elif np.allclose(axis, OUT):  # Z-axis
            return round(pos[2], 1) == (layer - 1)
        return False

    def get_group(self):
        return VGroup()

# Run with: manim -pql display.py RubiksCubeAnimation