import magiccube

cube = magiccube.Cube(3,"YYYYYYYYYRRRRRRRRRGGGGGGGGGOOOOOOOOOBBBBBBBBBWWWWWWWWW")

def get_cube_state(cube):
    first_face = "".join(str(cube).split("\n")[:3]).replace(" ","")
    second_face = "".join([s.replace(" ","")[:3] for s in str(cube).split("\n")[3:6]])
    third_face = "".join([s.replace(" ","")[3:6] for s in str(cube).split("\n")[3:6]])
    fourth_face = "".join([s.replace(" ","")[6:9] for s in str(cube).split("\n")[3:6]])
    fifth_face = "".join([s.replace(" ","")[9:12] for s in str(cube).split("\n")[3:6]])
    sixth_face = "".join(str(cube).split("\n")[6:]).replace(" ","")
    return first_face + second_face + third_face + fourth_face + fifth_face + sixth_face


cube.rotate("M2 E2 S2")

checkered_cube = magiccube.Cube(3, get_cube_state(cube))

print(checkered_cube)
print(cube)

import pdb; pdb.set_trace()