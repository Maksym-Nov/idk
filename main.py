import pygame
pygame.init()
import os

def path_file(file_name):
    folder_path = os.path.abspath(__file__ + "/..")
    path = os.path.join(folder_path, file_name)
    return path



WIN_WIDTH = 800
WIN_HEIGHT = 600
FPS = 40 
YELLOW = (255, 255, 0)
GRAY = (80, 80, 80)
DARKER_GREY = (70, 70, 70) 
BLACK = (0, 0, 0)


window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()
fon = pygame.image.load(path_file("fon_for_game_IT.jpg"))
fon = pygame.transform.scale(fon, (WIN_WIDTH, WIN_HEIGHT))

win_picture = pygame.image.load(path_file("WIN_FOTO_FOR_IT_GAME.jpg"))
win_picture = pygame.transform.scale(win_picture,(WIN_WIDTH, WIN_HEIGHT))

pygame.mixer.music.load(path_file("fonovaya-muzyika-quotokonchaniequot-24709.wav"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

music_win = pygame.mixer.Sound(path_file("muzyika-iz-igryi-zelda-23480.wav"))

music_lose = pygame.mixer.Sound(path_file("fonovaya-muzyika-quotproyasneniequot-24769.wav"))
music_lose.set_volume(1)

music_KABOOM = pygame.mixer.Sound(path_file("dinamicheskiy-zvuk-pistoleta-vibriruet-byistro-korotkaya-ruka-video-korotkaya-muzyika-fonovyiy-zvuk-38203.wav"))

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, img):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (width, height))
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def __init__(self, x, y, width, height, img, speed):
        super().__init__(x, y, width, height, img)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIN_WIDTH or self.rect.right < 0:
            self.kill()
        

    




class Enemy(GameSprite):
    def __init__(self, x, y, width, height, img, speed, direction, min_coord, max_coord):
        super().__init__(x, y, width, height, img)
        self.speed = speed
        self.direction = direction 
        self.min_coord = min_coord
        self.max_coord = max_coord

    def update(self):
        if self.direction == "left" or self.direction == "right":
            if self.direction == "left":
                self.rect.x -= self.speed
            if self.direction == "right":
                self.rect.x += self.speed
            
            if self.rect.right >= self.max_coord:
                self.direction = "left"
            if self.rect.left <= self.min_coord:
                self.direction = "right"

        elif self.direction == "up" or self.direction == "down":
            if self.direction == "down":
                self.rect.y += self.speed
            if self.direction == "up":
                self.rect.y -= self.speed

            if self.rect.top <= self.min_coord:
                self.direction = "down"
            if self.rect.bottom >= self.max_coord:
                self.direction = "up"  
         
class Player(GameSprite):
    def __init__(self, x, y, width, height, img):
        super().__init__(x, y, width, height, img)
        self.speed_x = 0
        self.speed_y = 0
        self.direction = "left"
        self.image_l = self.image
        self.image_r = pygame.transform.flip(self.image, True, False)
    
    def update(self):
        if self.speed_x > 0 and self.rect.right < WIN_WIDTH or self.speed_x < 0 and self.rect.left > 0:     
            self.rect.x += self.speed_x
        walls_touched = pygame.sprite.spritecollide(self, walls, False)
        
        if self.speed_x > 0:
            for wall in walls_touched:
                self.rect.right = min(self.rect.right, wall.rect.left)
        elif self.speed_x < 0:
            for wall in walls_touched:
                self.rect.left = max(self.rect.left, wall.rect.right)
        
        if self.speed_y < 0 and self.rect.top > 0 or self.speed_y > 0 and self.rect.bottom < WIN_HEIGHT:
            self.rect.y += self.speed_y
        walls_touched = pygame.sprite.spritecollide(self, walls, False)
        if self.speed_y > 0:
            for wall in walls_touched:
                self.rect.bottom = min(self.rect.bottom, wall.rect.top)
        elif self.speed_y < 0:
            for wall in walls_touched:
                self.rect.top = max(self.rect.top, wall.rect.bottom)

    def shoot(self):
        if self.direction == "right":
            bullet = Bullet(self.rect.right, self.rect.centery, 10, 10, path_file("ammo_for_game_IT.png"), 5)
            bullets.add(bullet)
        if self.direction == "left":
            bullet = Bullet(self.rect.left - 10 ,self.rect.centery, 10, 10, path_file("ammo_for_game_IT.png"), -5)
            bullets.add(bullet)


class Button():
    def __init__(self, color, x, y, height, width, text):
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.font30 = pygame.font.SysFont("arial", 30)
        self.text = self.font30.render(text, True, BLACK)
    
    def button_show(self, px_x, px_y):
        pygame.draw.rect(window, self.color, self.rect)
        window.blit(self.text, (self.rect.x + px_x, self.rect.y + px_y))
    
button_start = Button(GRAY, 250, 150, 150, 50, "start")
button_exit = Button(GRAY, 250, 350, 150, 80, "exit")



player = Player(50, 50, 50, 80, path_file("charter_for_game_IT-removebg-preview.png"))

goal = GameSprite(700, 500, 50, 80, path_file("goal_for_game_IT-removebg-preview.png"))

bullets = pygame.sprite.Group()


enemies = pygame.sprite.Group()
evil_charter1 = Enemy(700, 100, 50, 80, path_file("evil_charter_for_GAME_IT-removebg-preview.png"), 4, "up", 0, 200)
enemies.add(evil_charter1)
evil_charter2= Enemy(200, 200, 50, 80, path_file("evil_charter_for_GAME_IT-removebg-preview.png"), 4, "down", 400, 600)
enemies.add(evil_charter2)
evil_charter3 = Enemy(200, 100, 50, 80, path_file("evil_charter_for_GAME_IT-removebg-preview.png"), 4, "up", 100, 300)
enemies.add(evil_charter3)
evil_charter4 = Enemy(500, 200, 50, 80, path_file("evil_charter_for_GAME_IT-removebg-preview.png"), 4, "up", 0, 200)
enemies.add(evil_charter4)


walls = pygame.sprite.Group()
wall_1 = GameSprite(0, 300, 150, 50, path_file("wall_for_IT_game.jfif"))
walls.add(wall_1)
wall_3 = GameSprite(300, 100, 150, 50, path_file("wall_for_IT_game.jfif"))
walls.add(wall_3)
wall_5 = GameSprite(300, 300, 150, 50, path_file("wall_for_IT_game.jfif"))
walls.add(wall_5)
wall_7 = GameSprite(450, 300, 150, 50, path_file("wall_for_IT_game.jfif"))
walls.add(wall_7)
wall_9 = GameSprite(0, 300, 150, 50, path_file("wall_for_IT_game.jfif"))
walls.add(wall_9)


wall_2 = GameSprite(250, 0, 50, 150, path_file("wall_for_IT_game.jfif"))
walls.add(wall_2)
wall_4 = GameSprite(250, 300, 50, 150, path_file("wall_for_IT_game.jfif"))
walls.add(wall_4)
wall_6 = GameSprite(600, 450, 50, 150, path_file("wall_for_IT_game.jfif"))
walls.add(wall_6)
wall_8 = GameSprite(600, 350, 50, 150, path_file("wall_for_IT_game.jfif"))
walls.add(wall_8)
wall_10 = GameSprite(600, 250, 50, 150, path_file("wall_for_IT_game.jfif"))
walls.add(wall_10)
wall_12 = GameSprite(600, 150, 50, 150, path_file("wall_for_IT_game.jfif"))
walls.add(wall_12)


level = 0

game = True
play = True
while game == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        if level == 0:
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if button_start.rect.collidepoint(x, y):
                    button_start.color = GRAY
                elif button_exit.rect.collidepoint(x, y):
                    button_exit.color = GRAY
                else:
                    button_start.color = GRAY
                    button_exit.color = GRAY
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if button_start.rect.collidepoint(x, y):
                    level = 1
                elif button_exit.rect.collidepoint(x, y):
                    game = False
        elif level == 1:

        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.speed_x = 5
                    player.direction = "right"
                    player.image = player.image_r
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.speed_x = -5
                    player.direction = "left"
                    player.image = player.image_l
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.speed_y = -5
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.speed_y = 5
                if event.key == pygame.K_SPACE:
                    music_KABOOM.play()
                    player.shoot()
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.speed_x = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.speed_x = 0
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.speed_y = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.speed_y = 0

    if level == 0:
        window.fill(YELLOW)
        button_start.button_show(17, 17)
        button_exit.button_show(17, 17)
    elif level == 1:


        if play == True:
            window.blit(fon, (0, 0))

            print(bullets.sprites())

            player.reset()
            player.update()

            enemies.draw(window)
            enemies.update()

            goal.reset()

            

            bullets.draw(window)
            bullets.update()

            walls.draw(window)

            if pygame.sprite.collide_rect(player, goal):
                play = False
                window.blit(win_picture, (0, 0))
                pygame.mixer.music.stop()
                music_win.play()
            
            if pygame.sprite.spritecollide(player, enemies, False):
                play = False
                window.blit(win_picture, (0, 0))
                pygame.mixer.music.stop()
                music_lose.play()

            pygame.sprite.groupcollide(bullets, walls, True, False)
            pygame.sprite.groupcollide(bullets, enemies, True, True)
            

    clock.tick(FPS)
    pygame.display.update()