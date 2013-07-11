#!/usr/bin/python2
# -*- coding: utf-8 -*-

import pygame
import sys
import math
import random
#from pygame.locals import *

debug = True


def debug(message):
    if debug is True:
        print message

# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
grey = (100, 100, 100)
green = (0, 255, 0)
red = (255, 0, 0)


# TODO: Make ship and planet inherit Object
class Gravity_Object:
    def __init(self, radius, x, y, color):
        self.radius = radius
        self.x = x
        self.y = y

    def move(self, x, y):
        """
        Move a certain distance in a direction
        >>> print x, y
        10, 30
        >>> move(10, 20)
        >>> print x, y
        20, 50
        """
        self.x += x
        self.y += y

    def draw(self):
        pygame.draw.circle(pygame.display.get_surface(),
                           red,
                           (self.x, self.y),
                           self.radius)


class Ship(Gravity_Object):
    def __init__(self, radius, x, y):
        self.radius = radius
        self.x = x
        self.y = y
        self.speed_x = 0
        self.speed_y = 0

    def draw(self):
        pygame.draw.circle(pygame.display.get_surface(),
                           red,
                           (self.x, self.y),
                           self.radius)


class Planet(Gravity_Object):
    def __init__(self, min_size, max_size, x, y):
        self.min_size = min_size
        self.max_size = max_size
        self.radius = random.randint(self.min_size, self.max_size)
        self.x = x
        self.y = y
        self.centerpoint = (self.x, self.y)
        self.density = 2643  # kg/m^3
        self.mass = self.density * (self.radius * 2)
        self.speed_x = random.randint(-1, 1)
        self.speed_y = random.randint(-1, 1)
        self.gravity = (0.000000000006674 * self.mass) * 100

    def draw(self):
        pygame.draw.circle(pygame.display.get_surface(),
                           grey,
                           (self.x, self.y),
                           self.radius)


class Untitled:
    def __init__(self):
        self._display_surf = None
        self.size = self.width, self.height = 800, 600
        self.MAX_FPS = 60
        self.entities = []

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size,
                                                     pygame.HWSURFACE
                                                     | pygame.DOUBLEBUF)
        self._clock = pygame.time.Clock()
        self._running = True

        # Planets
        self.earth = Planet(50, 60, 400, 90)
        self.mars = Planet(40, 45, 400, 322)
        self.moon = Planet(20, 30, 530, 422)
        self.venus = Planet(30, 50, 500, 522)

        # Ships
        self.ship = Ship(10, self.width / 2, self.height / 2)

        # Containers
        self.ships = [self.ship]
        self.planets = [self.earth, self.mars, self.moon, self.venus]

        # Meta-Containers
        self.entities = [self.planets, self.ships]

    def on_event(self, event):
        if event.type == pygame.QUIT:
            debug("Good bye.")
            self._running = False

        if event.type == pygame.KEYDOWN:
            debug("You pressed a key.")
            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.key == pygame.K_LEFT:
                self.ship.speed_x += -1
            if event.key == pygame.K_RIGHT:
                self.ship.speed_x += 1
            if event.key == pygame.K_UP:
                self.ship.speed_y += -1
            if event.key == pygame.K_DOWN:
                self.ship.speed_y += 1
            # Shift is sorta brakes.
            # TODO: Better Brakes
            if event.key == pygame.K_LSHIFT:
                if self.ship.speed_x > 0:
                    self.ship.speed_x += -1
                if self.ship.speed_y > 0:
                    self.ship.speed_y += -1
            # Stop the ship in its tracks.
            # TODO Decide if debug functionality.
            if event.key == pygame.K_SPACE:
                self.ship.speed_x = 0
                self.ship.speed_y = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            debug("Ow!")

    def on_loop(self):
        self.collision_detection()
        debug("%s and %s" % (self.ship.speed_x, self.ship.speed_y))
        for things in self.entities:
            for thing in things:
                thing.move(thing.speed_x, thing.speed_y)

    def on_render(self):
        self._display_surf.fill(white)
        for planet in self.planets:
            planet.draw()
        for ship in self.ships:
            ship.draw()

        # Actually show them what we rendered
        pygame.display.flip()

    def on_cleanup(self):
        debug("Pygame cleanup")
        pygame.quit()
        debug("Bye!")
        sys.exit()

    def collision_detection(self):
        for things in self.entities:
            for i, thing in enumerate(things):
                # If thing is further to the right than the left of the screen
                if thing.x > self.width - thing.radius:
                    # Switch directions of it is hitting the edge
                    thing.speed_x *= -1
                # Same stuff again
                if thing.x < thing.radius:
                    thing.speed_x *= -1
                if thing.y > self.height - thing.radius:
                    thing.speed_y *= -1
                if thing.y < thing.radius:
                    thing.speed_y *= -1

                for thing2 in things:
                    # Yes.
                    if thing != thing2:
                        # Distance = sqrt((x_1 - x_2)^2 + (y_1 - y_2)^2)
                        # Pythag!
                        distance = math.sqrt(((thing.x - thing2.x) ** 2)
                                             + ((thing.y - thing2.y) ** 2))
                        if distance < (thing.radius + thing2.radius):
                            if debug:
                                debug("%r & %r: Collision!" % (thing, thing2))
                            # The slower thing gets popped
                            if abs(thing.speed_x) + abs(thing.speed_y) \
                               <= thing2.speed_x + thing2.speed_y:
                                if thing.speed_x + thing.speed_y \
                                   == thing2.speed_x + thing2.speed_y:
                                    things.pop(i)
                                else:
                                    things.pop(i)

                            else:
                                things.pop(i)

    def main_loop(self):
        while (self._running):
            # Handle events
            for event in pygame.event.get():
                self.on_event(event)

            # Handle Computations
            self.on_loop()

            # Handle the rendering
            self.on_render()
            # Make sure we don't go above our fps limit
            self._clock.tick(self.MAX_FPS)

    def on_execute(self):
        if self.on_init() is False:
            self._running = False

        self.main_loop()
        self.on_cleanup()

if __name__ == "__main__":
    untitled = Untitled()
    untitled.on_execute()
