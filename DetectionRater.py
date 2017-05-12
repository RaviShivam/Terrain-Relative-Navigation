import Image
import ImageDraw

from src import EllipseFitter

draw = ImageDraw.Draw(Image.open("data/TRN/Scene1.ppm"))
image = Image.open("data/TRN/Scene1.ppm")
file = open("Scene1.txt")
positions = []
for line in file:
    positions.append(line.split())
    image = EllipseFitter.draw_thick_point(image, map(float, line.split()))

image.show()


