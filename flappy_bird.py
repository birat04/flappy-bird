import pygame
import sys
import random


pygame.init()


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 50


GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_GAP = 150
PIPE_WIDTH = 70
PIPE_SPEED = 3


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")


clock = pygame.time.Clock()


font = pygame.font.Font(None, 36)


background_image = pygame.image.load("background.png").convert()
bird_image = pygame.image.load("bird.png").convert_alpha()
bird_image = pygame.transform.scale(bird_image, (40, 30))  
sun_image = pygame.image.load("sun.png").convert_alpha()
sun_image = pygame.transform.scale(sun_image, (50, 50))  


class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.width = 40
        self.height = 30

    def draw(self):
        screen.blit(bird_image, (self.x, self.y))

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def flap(self):
        self.velocity = FLAP_STRENGTH


class Pipe:
    def __init__(self, x):
        self.x = x
        self.top_height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
        self.bottom_height = SCREEN_HEIGHT - self.top_height - PIPE_GAP

    def draw(self):
        pygame.draw.rect(screen, (0, 200, 0), (self.x, 0, PIPE_WIDTH, self.top_height))
        pygame.draw.rect(screen, (0, 200, 0), (self.x, SCREEN_HEIGHT - self.bottom_height, PIPE_WIDTH, self.bottom_height))

    def update(self):
        self.x -= PIPE_SPEED

    def is_off_screen(self):
        return self.x + PIPE_WIDTH < 0

    def collides_with(self, bird):
        bird_rect = pygame.Rect(bird.x, bird.y, bird.width, bird.height)
        top_pipe_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.top_height)
        bottom_pipe_rect = pygame.Rect(self.x, SCREEN_HEIGHT - self.bottom_height, PIPE_WIDTH, self.bottom_height)
        return bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect)


def main():
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH)]
    score = 0
    sun_x = 10
    sun_y = 50
    running = True

    while running:
        screen.blit(background_image, (0, 0))  

       
        sun_x += 0.5
        if sun_x > SCREEN_WIDTH:
            sun_x = -50
        screen.blit(sun_image, (sun_x, sun_y))  

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.flap()

        
        bird.update()

       
        if pipes[-1].x < SCREEN_WIDTH // 2:
            pipes.append(Pipe(SCREEN_WIDTH))

        
        for pipe in pipes:
            pipe.update()

        
        pipes = [pipe for pipe in pipes if not pipe.is_off_screen()]

        
        for pipe in pipes:
            if pipe.collides_with(bird):
                running = False

        
        if bird.y + bird.height > SCREEN_HEIGHT or bird.y < 0:
            running = False

        
        for pipe in pipes:
            if pipe.x + PIPE_WIDTH < bird.x and not hasattr(pipe, "scored"):
                score += 1
                pipe.scored = True

        
        bird.draw()
        for pipe in pipes:
            pipe.draw()

        
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

   
    game_over_text = font.render("Game Over! Press R to Restart", True, (255, 255, 255))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
    pygame.display.flip()

    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                main()


if __name__ == "__main__":
    main()
