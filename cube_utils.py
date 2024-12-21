import magiccube

cube = magiccube.Cube(3,"YYYYYYYYYRRRRRRRRRGGGGGGGGGOOOOOOOOOBBBBBBBBBWWWWWWWWW")

def get_cube_state(cube):
    cube_str = str(cube)
    first_face = "".join(cube_str.split("\n")[:3]).replace(" ","")
    second_face = "".join([s.replace(" ","")[:3] for s in cube_str.split("\n")[3:6]])
    third_face = "".join([s.replace(" ","")[3:6] for s in cube_str.split("\n")[3:6]])
    fourth_face = "".join([s.replace(" ","")[6:9] for s in cube_str.split("\n")[3:6]])
    fifth_face = "".join([s.replace(" ","")[9:12] for s in cube_str.split("\n")[3:6]])
    sixth_face = "".join(cube_str.split("\n")[6:]).replace(" ","")
    return first_face + second_face + third_face + fourth_face + fifth_face + sixth_face
