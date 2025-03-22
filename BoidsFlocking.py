import heapq
import numpy as np

class Boid:
    def __init__(self, position, velocity):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)

    def update(self, boids):
        separation = self.calculate_separation(boids)
        alignment = self.calculate_alignment(boids)
        cohesion = self.calculate_cohesion(boids)
        
        self.velocity += separation + alignment + cohesion
        self.position += self.velocity

    def calculate_separation(self, boids):
        separation_vector = np.array([0.0, 0.0])
        for boid in boids:
            if boid is not self:
                diff = self.position - boid.position
                dist = np.linalg.norm(diff)
                if dist < 10:  # Separation threshold
                    separation_vector += diff / (dist + 1e-5)
        return separation_vector * 0.1

    def calculate_alignment(self, boids):
        avg_velocity = np.mean([boid.velocity for boid in boids if boid is not self], axis=0)
        return (avg_velocity - self.velocity) * 0.05

    def calculate_cohesion(self, boids):
        avg_position = np.mean([boid.position for boid in boids if boid is not self], axis=0)
        return (avg_position - self.position) * 0.01

# Example usage
boids = [
    Boid((0, 0), (1, 1)),
    Boid((10, 10), (-1, -1)),
    Boid((5, 5), (0, -1))
]

for _ in range(10):
    for boid in boids:
        boid.update(boids)
    print([boid.position for boid in boids])
