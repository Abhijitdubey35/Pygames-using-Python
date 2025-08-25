import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.acceleration = 0.1
        self.max_speed = 8
        self.turn_speed = 3
        self.friction = 0.02
        self.width = 40
        self.height = 20
        
        # Create car surface with better graphics
        self.car_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # Car body
        pygame.draw.rect(self.car_surface, RED, (0, 0, self.width, self.height))
        # Windows
        pygame.draw.rect(self.car_surface, BLUE, (5, 2, 15, 8))
        # Wheels
        pygame.draw.rect(self.car_surface, BLACK, (0, 0, 5, self.height))
        pygame.draw.rect(self.car_surface, BLACK, (self.width-5, 0, 5, self.height))
        
    def move(self):
        # Update position based on angle and speed
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y -= math.sin(math.radians(self.angle)) * self.speed
        
        # Apply friction
        if self.speed > 0:
            self.speed = max(0, self.speed - self.friction)
        elif self.speed < 0:
            self.speed = min(0, self.speed + self.friction)
            
    def rotate(self, surface):
        # Rotate the car surface
        rotated_surface = pygame.transform.rotate(surface, self.angle)
        new_rect = rotated_surface.get_rect(center=(self.x, self.y))
        return rotated_surface, new_rect
    
    def get_rect(self):
        # Get the car's hitbox
        rotated_surface, rect = self.rotate(self.car_surface)
        return rect

class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GRAY

class Track:
    def __init__(self):
        self.outer_boundary = [
            (100, 100), (900, 100), (900, 600), (700, 600),
            (700, 400), (500, 400), (500, 600), (300, 600),
            (300, 400), (100, 400)
        ]
        self.inner_boundary = [
            (200, 200), (800, 200), (800, 500), (600, 500),
            (600, 300), (400, 300), (400, 500), (200, 500)
        ]
        self.obstacles = []
        self.create_obstacles()
        
    def create_obstacles(self):
        # Create some random obstacles on the track
        for _ in range(5):
            x = random.randint(200, 800)
            y = random.randint(200, 500)
            width = random.randint(30, 60)
            height = random.randint(30, 60)
            self.obstacles.append(Obstacle(x, y, width, height))
    
    def draw(self, screen):
        # Draw track boundaries
        pygame.draw.polygon(screen, GRAY, self.outer_boundary, 2)
        pygame.draw.polygon(screen, GRAY, self.inner_boundary, 2)
        
        # Draw obstacles
        for obstacle in self.obstacles:
            pygame.draw.rect(screen, obstacle.color, obstacle.rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("F1 Racer")
        self.clock = pygame.time.Clock()
        self.car = Car(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.track = Track()
        self.running = True
        self.start_time = pygame.time.get_ticks()
        self.best_time = float('inf')
        self.font = pygame.font.Font(None, 36)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
        # Handle continuous key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.car.speed = min(self.car.speed + self.car.acceleration, self.car.max_speed)
        if keys[pygame.K_DOWN]:
            self.car.speed = max(self.car.speed - self.car.acceleration, -self.car.max_speed/2)
        if keys[pygame.K_LEFT]:
            self.car.angle += self.car.turn_speed
        if keys[pygame.K_RIGHT]:
            self.car.angle -= self.car.turn_speed
            
    def check_collision(self):
        car_rect = self.car.get_rect()
        
        # Check collision with obstacles
        for obstacle in self.track.obstacles:
            if car_rect.colliderect(obstacle.rect):
                return True
                
        # Check if car is within track boundaries
        car_point = (self.car.x, self.car.y)
        if not self.is_point_in_polygon(car_point, self.track.outer_boundary) or \
           self.is_point_in_polygon(car_point, self.track.inner_boundary):
            return True
            
        return False
    
    def is_point_in_polygon(self, point, polygon):
        x, y = point
        n = len(polygon)
        inside = False
        p1x, p1y = polygon[0]
        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside
            
    def update(self):
        self.car.move()
        
        # Check for collisions
        if self.check_collision():
            self.car.x = WINDOW_WIDTH // 2
            self.car.y = WINDOW_HEIGHT // 2
            self.car.speed = 0
            self.car.angle = 0
            self.start_time = pygame.time.get_ticks()
        
    def draw(self):
        self.screen.fill(WHITE)
        
        # Draw track
        self.track.draw(self.screen)
        
        # Draw the car
        rotated_car, car_rect = self.car.rotate(self.car.car_surface)
        self.screen.blit(rotated_car, car_rect)
        
        # Draw timer
        current_time = (pygame.time.get_ticks() - self.start_time) / 1000
        time_text = self.font.render(f"Time: {current_time:.2f}s", True, BLACK)
        self.screen.blit(time_text, (10, 10))
        
        if self.best_time != float('inf'):
            best_time_text = self.font.render(f"Best: {self.best_time:.2f}s", True, BLACK)
            self.screen.blit(best_time_text, (10, 50))
        
        pygame.display.flip()
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
