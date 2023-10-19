from pygame import *
init()
font.init()
from random import randint
from time import sleep

# окно

window = display.set_mode((1280,720))

display.set_caption('Ping-pong 1.1')

background = transform.scale(image.load('background.png'), (1280,720))

player1_count = 0
player2_count = 0

music_count = 1

settings_flag = 0

# классы

class gameSprite():

    def __init__(self, img, x, y, speed, w= 100, h = 200):

        self.img = img
       
        self.speed = speed

        self.img = transform.scale(image.load(self.img), (w, h))

        self.rect = self.img.get_rect()

        self.rect.x = x
        self.rect.y = y 

    def showSprite(self):

        window.blit(self.img,(self.rect.x, self.rect.y))

class Player(gameSprite):

    def __init__(self, img, x, y, speed, w = 15, h = 200):

        super().__init__(img, x, y, speed, w, h)

    def r_update(self):

        keys_pressed = key.get_pressed()

        if keys_pressed[K_w] and self.rect.y > 0:

            self.rect.y -= self.speed

        if keys_pressed[K_s] and self.rect.y < 520:

            self.rect.y += self.speed

    def l_update(self):

        keys_pressed = key.get_pressed()

        if keys_pressed[K_UP] and self.rect.y > 0:

            self.rect.y -= self.speed

        if keys_pressed[K_DOWN] and self.rect.y < 520:

            self.rect.y += self.speed

class Ball(gameSprite):

    def __init__(self, img, x, y, speed, w = 50, h = 50):

        super().__init__(img, x, y, speed, w, h)

        global choise
        
        choise = randint(1,2)
        print(choise)

        self.x_speed = self.speed
        self.y_speed = 10

        if choise == 1:

            self.x_speed *= -1

    def update(self):

        self.rect.x += self.x_speed

        self.rect.y += self.y_speed

        if self.rect.y < 100 or self.rect.y > 620:

            punch.play()

            self.y_speed *= -1

            self.rect.y += self.y_speed

class SB(gameSprite):

    def __init__(self, img, x, y, speed, w = 50, h = 50):

        super().__init__(img, x, y, speed, w, h)

# звуки

mixer.init()

mixer.music.load('background_music.ogg')

for i in range(music_count):

    mixer.music.play()

plus_ball = mixer.Sound('ball.ogg')
punch = mixer.Sound('punch.ogg')
win_sound = mixer.Sound('win.ogg')

# спрайты

settings = SB('settings.png',0,0,0,1280,720 )

player1 = Player('player1.png', 140, 360, 20)
player2 = Player('player2.png', 1080, 360, 20)

ball = Ball('ball.png', 615, 335, 20)

font = font.SysFont('Arial', 40)

# фпс

clock = time.Clock()

FPS = 60

# игровой цикл

game = True
while game:

    window.blit(background,(0,0))

    keys_pressed = key.get_pressed()

    for e in event.get():

        if e.type == KEYDOWN:

            if e.key == K_ESCAPE:

                settings_flag = False

                print(1)

    if settings_flag:

        mixer.music.pause()

        settings.showSprite()

        display.update()

    else:

        music_count += 1

        player1.showSprite()
        player2.showSprite()

        ball.showSprite()

        player1.r_update()
        player2.l_update()

        ball.update()

        player1_counts = font.render('Первый игрок:'+str(player1_count), True, (255, 255, 255))
        player2_counts = font.render('Второй игрок:'+str(player2_count), True, (255, 255, 255))

        window.blit(player1_counts, (20, 20))
        window.blit(player2_counts, (620, 20))

        keys_pressed = key.get_pressed()

        for e in event.get(): 

            if keys_pressed[K_F1]:

                mixer.music.pause()

            if keys_pressed[K_F2]:

                mixer.music.play()  

                for e in event.get():

                    if e.type == KEYDOWN:

                        if e.key == K_ESCAPE:

                            settings_flag = False

                            print(1)

                            settings_flag = 1
                
            if e.type == QUIT:

                game = False

        if sprite.collide_rect(ball, player1):

            punch.play()

            ball.x_speed *= -1

            ball.x_speed += -1
            ball.y_speed += -1

        if sprite.collide_rect(ball, player2):

            punch.play()

            ball.x_speed *= -1

            ball.x_speed += -1
            ball.y_speed += -1


        if ball.rect.x < 100:

            plus_ball.play()

            player2_count += 1

            print('player2:',player2_count)

            ball.rect.y = 335
            ball.rect.x = 615

            ball.y_speed *= -1

        if ball.rect.x > 1180:

            plus_ball.play()

            player1_count += 1

            print('player1:',player1_count)

            ball.rect.y = 335
            ball.rect.x = 615

            ball.y_speed *= -1

        if player1_count > 10:

            win_sound.play()

            lose_game1 = font.render('Первый игрок победил!', True, (50, 255, 50))

            window.blit(lose_game1, (200, 200))

            display.update()

            next_game1 = font.render('Загрузка следующего матча...', True, (150, 255, 150))

            window.blit(next_game1, (615, 315))

            display.update()

            sleep(10)

            player1_count = 0
            player2_count = 0

            ball.rect.y = 335
            ball.rect.x = 615

            player1.rect.y = 360
            player1.rect.x = 140
            player2.rect.y = 360
            player2.rect.x = 1080

            choise = randint(1,2)
            print(choise)

            ball.x_speed = ball.speed
            ball.y_speed = 10

            if choise == 1:

                ball.x_speed *= -1

            display.update()

        if player2_count > 10:

            win_sound.play()

            lose_game2 = font.render('Второй игрок победил!', True, (50, 255, 50))

            window.blit(lose_game2, (200, 200))

            display.update()

            next_game2 = font.render('Загрузка следующего матча...', True, (150, 255, 150))

            window.blit(next_game2, (615, 315))

            display.update()

            sleep(10)

            player1_count = 0
            player2_count = 0

            ball.rect.y = 335
            ball.rect.x = 615

            player1.rect.y = 360
            player1.rect.x = 140
            player2.rect.y = 360
            player2.rect.x = 1080

            choise = randint(1,2)
            print(choise)

            ball.x_speed = ball.speed
            ball.y_speed = 10

            if choise == 1:

                ball.x_speed *= -1

            display.update()

    clock.tick(FPS)

    display.update()