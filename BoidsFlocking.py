'''
	BoidsFlocking.py

	Copyright (c) PAUL MICKY D COSTA
	Licensed under the MIT license: https://opensource.org/license/mit
'''
import pygame
import random
import math

# Define the Boid class
class Boid:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acceleration = pygame.Vector2(0, 0)
        self.max_speed = 4
        self.max_force = 0.1

    def apply_force(self, force):
        self.acceleration += force

    def align(self, boids):
        steer = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            if boid != self and self.position.distance_to(boid.position) < 50:
                steer += boid.velocity
                total += 1
        if total > 0:
            steer /= total
            steer = steer.normalize() * self.max_speed
            steer -= self.velocity
            steer = self.limit(steer, self.max_force)
        return steer

    def cohesion(self, boids):
        steer = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            if boid != self and self.position.distance_to(boid.position) < 50:
                steer += boid.position
                total += 1
        if total > 0:
            steer /= total
            steer -= self.position
            steer = steer.normalize() * self.max_speed
            steer -= self.velocity
            steer = self.limit(steer, self.max_force)
        return steer

    def separation(self, boids):
        steer = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            distance = self.position.distance_to(boid.position)
            if boid != self and distance < 25:
                diff = self.position - boid.position
                diff /= distance
                steer += diff
                total += 1
        if total > 0:
            steer /= total
        if steer.length() > 0:
            steer = steer.normalize() * self.max_speed
            steer -= self.velocity
            steer = self.limit(steer, self.max_force)
        return steer

    def limit(self, vector, max_value):
        if vector.length() > max_value:
            vector = vector.normalize() * max_value
        return vector

    def update(self):
        self.velocity += self.acceleration
        self.velocity = self.limit(self.velocity, self.max_speed)
        self.position += self.velocity
        self.acceleration *= 0

    def edges(self, width, height):
        if self.position.x < 0:
            self.position.x = width
        if self.position.x > width:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = height
        if self.position.y > height:
            self.position.y = 0

    def flock(self, boids):
        separation = self.separation(boids)
        alignment = self.align(boids)
        cohesion = self.cohesion(boids)

        self.apply_force(separation)
        self.apply_force(alignment)
        self.apply_force(cohesion)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), 3)


# Main function to initialize the simulation
def main():
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Boids Flocking Simulation")

    boids = [Boid(random.randint(0, width), random.randint(0, height)) for _ in range(100)]
    clock = pygame.time.Clock()

    run = True
    while run:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for boid in boids:
            boid.flock(boids)
            boid.update()
            boid.edges(width, height)
            boid.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
