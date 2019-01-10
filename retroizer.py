#!/bin/python3
import pygame
import pygame.camera
import argparse
import sys
pygame.init()
pygame.camera.init()

parser = argparse.ArgumentParser()
parser.add_argument('file', help='The file to be retroized. Use "webcam" for a live stream.')
parser.add_argument('-x', type=int, default=0, help='Starting x for rendering.')
parser.add_argument('-y', type=int, default=0, help='Starting y for rendering.')
parser.add_argument('-w', '--width', type=int, default=-1, help='Screen width. Use -1 for autmatic sizing.')
parser.add_argument('--height', type=int, default=-1, help='Screen height. Use -1 for autmatic sizing.')
parser.add_argument('-s', '--size', type=int, default=10, help='Set the size of the pixels.')
parser.add_argument('-v', '--verbose', action='store_true', help='Toggle verbose output.')
parser.add_argument('--flip', action='store_true', help='Toggle horizontal flipping.')
parser.add_argument('-o', '--output', default='', help='Output file.')
args = parser.parse_args()

webcam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
webcam.start()

if args.file == 'webcam':
    if args.width == -1:
        width = webcam.get_image().get_size()[0]
    else:
        width = args.width
    if args.height == -1:
        height = webcam.get_image().get_size()[1]
    else:
        height = args.height
else:
    image = pygame.image.load(args.file)
    if args.width == -1:
        width = image.get_size()[0]
    else:
        width = args.width
    if args.height == -1:
        height = image.get_size()[1]
    else:
        height = args.height
pixel_width, pixel_height = args.size, args.size
screen = pygame.display.set_mode((width, height), 0, 32)

while True:
    screen.fill((0, 0, 0))
    if args.file == 'webcam':
        image = webcam.get_image()
    if args.flip:
        image = pygame.transform.flip(image, (True, False))
    pixels = pygame.PixelArray(image)
    for y in range(args.y, height, pixel_height):
        for x in range(args.x, width, pixel_width):
            pixel = pixels[x, y]
            pygame.draw.rect(screen, pixel, (x, y, pixel_width, pixel_height))
    if args.output != '':
        try:
            pygame.image.save(screen, args.output)
        except:
            f = open(args.output, 'wb')
            f.close()
            pygame.image.save(screen, args.output)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    pygame.display.flip()
