import pygame
import random

def lerp(a, b, t):
    return a + (b-a) * t

def map(val, old_min, old_max, new_min, new_max):
    return ((val-old_min)/(old_max-old_min)) * (new_max + new_min)

def clamp(val, min, max):
    if val < min: return min
    elif val > max: return max
    else: return val

class Snake:
    def __init__(self, screen):
        self.screen = screen
        
        self.unit_size = 10
        self.color = (45, 45, 45)
        self.move_speed = 100
        
        self.body = [[120, 0],[120, 0],[120, 0]]
        self.dir = [1, 0]
        self.last_move = 0
        self.smooth_movement = False

        self.food = [0, 0]
        self.spawn_food()
        self.food_color = (100, 0, 0)
    
    def show_body(self):    
        
        if not self.smooth_movement:
            #render body as it is (snappy movement)
            for i in range(0, len(self.body)):
                pygame.draw.rect(self.screen, self.color, [self.body[i][0], self.body[i][1], self.unit_size, self.unit_size])

        else:
            #render rest of body as usual except for head and tail
            for i in range(2, len(self.body)-1):
                pygame.draw.rect(self.screen, self.color, [self.body[i][0], self.body[i][1], self.unit_size, self.unit_size])
            
            # interpolation offset
            offset = clamp(map(pygame.time.get_ticks() - (self.last_move), 0, self.move_speed, 0, 1), 0, 1)
            head_x = lerp(self.body[2][0], self.body[0][0], offset)
            head_y = lerp(self.body[2][1], self.body[0][1], offset)
            pygame.draw.rect(self.screen, self.color, [head_x, head_y, self.unit_size, self.unit_size])

            # to avoid error when snake len < 2            
            try:
                tail_x = lerp(self.body[-1][0], self.body[-2][0], offset)
                tail_y = lerp(self.body[-1][1], self.body[-2][1], offset)
                pygame.draw.rect(self.screen, self.color, [tail_x, tail_y, self.unit_size, self.unit_size])
            except:
                pass
        

    def show_food(self):
        pygame.draw.rect(self.screen, self.food_color, [self.food[0], self.food[1], self.unit_size, self.unit_size])

    def show_ui(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(str(self.get_score()), True, self.color)
        self.screen.blit(text, (self.screen.get_size()[0]/2, 16))

    def show_grid(self):
        for x in range(400):
            pygame.draw.rect(self.screen, (0, 0, 0), [x * self.unit_size, 0, 0.1*self.unit_size, self.screen.get_size()[1]])
        for y in range(400):
            pygame.draw.rect(self.screen, (0, 0, 0), [0, y * self.unit_size, self.screen.get_size()[0], 0.1*self.unit_size])

    def show_all(self):
        #self.show_grid()
        self.show_food()
        self.show_body()
        self.show_ui()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.dir = [-1, 0]
        elif keys[pygame.K_UP]:
            self.dir = [0, -1]
        elif keys[pygame.K_RIGHT]:
            self.dir = [1, 0]
        elif keys[pygame.K_DOWN]:
            self.dir = [0, 1]

        if keys[pygame.K_SPACE]:
            self.grow()

    def move(self):
        if pygame.time.get_ticks() > self.last_move + self.move_speed:
            # move head/start of body
            self.body[0][0] += self.dir[0] * self.unit_size
            self.body[0][1] += self.dir[1] * self.unit_size

            # move rest of body
            for i in range(len(self.body)-1, 0, -1):
                self.body[i][0] = self.body[i-1][0]
                self.body[i][1] = self.body[i-1][1]

            self.last_move = pygame.time.get_ticks()

    def grow(self): 
        self.body.append([self.body[-1][0], self.body[-1][1]])

    def spawn_food(self):
        self.food[0] = random.randint(1, (self.screen.get_size()[0]/self.unit_size)-1) * self.unit_size
        self.food[1] = random.randint(1, (self.screen.get_size()[1]/self.unit_size)-1) * self.unit_size
        if self.is_on_body(self.food[0], self.food[1]):
            self.spawn_food()

    def is_on_food(self):
        if self.body[0] == self.food:
            return True
        return False

    def is_on_body(self, x, y):
        for i in range(2, len(self.body)):
            if x == self.body[i][0] and y == self.body[i][1]:
                return True
        return False

    def get_score(self):
        return len(self.body) - 1

    def update(self):
        self.show_all()
        self.handle_input()
        self.move()
        
        if self.is_on_food():
            self.spawn_food()
            self.grow()
        
        if self.is_on_body(self.body[0][0], self.body[0][1]):
            print("game over")
        

class Game:
    def __init__(self):
        # initiate pygame stuff
        pygame.init()
        pygame.display.set_caption("Snake")
        self.screen = pygame.display.set_mode((400, 400))
        self.clock = pygame.time.Clock()

        # app to be run
        self.snake = Snake(self.screen)

    def update(self):

        self.screen.fill((200,200,200))
        self.snake.update()

        pygame.display.flip()  
        self.clock.tick(30)
    
    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
        
            self.update()


if __name__ == "__main__":
    game = Game()
    game.loop()
            


 

