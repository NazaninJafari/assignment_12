import random
from turtle import speed
import arcade
import time
import math

from requests import delete

Screen_w = 800
Screen_h = 600

class  Aireplane(arcade.Sprite):
    def __init__(self):
        super().__init__(":resources:images/space_shooter/playerShip2_orange.png")
        self.width = 48
        self.height = 48
        self.score = 0
        self.center_x = Screen_w // 2
        self.center_y = 32
        self.angle = 0
        self.change_angle = 0
        self.speed = 6
        self.change_x = 0
        self.change_y = 0
        self.bullet_list = []

    def fire(self):
        self.bullet_list.append(Bullet(self))

    def rotate(self):
        self.angle += self.speed * self.change_angle        

    def move(self):
        self.center_x += self.speed * self.change_x
        self.center_y += self.speed * self.change_y

class Enemy(arcade.Sprite):
    def __init__(self , sp):
        super().__init__(":resources:images/space_shooter/playerShip1_blue.png")
        self.width = 48
        self.height = 48
        self.center_x = random.randint(self.width , Screen_w - self.width) 
        self.center_y = Screen_h + 24
        self.speed = sp

    def move(self):
        self.center_y -= self.speed

class Bullet(arcade.Sprite):
    def __init__(self, host):
        super().__init__(':resources:images/space_shooter/laserRed01.png')
        self.center_x = host.center_x
        self.center_y = host.center_y
        self.angle = host.angle
        self.speed = 6
    
    def move(self):
        a = math.radians(self.angle)
        self.center_x -= self.speed * math.sin(a)
        self.center_y += self.speed * math.cos(a)

class BigEnemy(arcade.Sprite):
    def __init__(self):
        super().__init__(':resources:images/topdown_tanks/tank_red.png')
        self.width = 60
        self.height = 50
        self.center_x = random.randint(self.width , Screen_w - self.width) 
        self.center_y = Screen_h - 55
        self.speed = 2


#safe bazi
class Game(arcade.Window):
    def __init__(self):
        super().__init__(Screen_w, Screen_h,'shooting Enemy')
        arcade.set_background_color(arcade.color.BLACK)
        self.bg_image = arcade.load_texture(":resources:images/backgrounds/stars.png")
        self.music = arcade.load_sound('explosion1.wav')
        self.fire_music = arcade.load_sound('laser1.mp3')
        self.image = arcade.load_texture('1.png')  
        self.me = Aireplane()
        self.sp = 4
        self.enemy_list = []
        self.start_time = time.time()
        self.count1 = 3
        self.bigenemy = BigEnemy()
        self.count2 = 5
        self.rect = arcade.load_texture('rectangle.png')
        self.flag = 0
    
    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0 , 0, Screen_w, Screen_h, self.bg_image)
        arcade.draw_text('score: '+str(self.me.score), 40 , 40 , arcade.color.WHITE, 12, font_name='arial')
        self.me.draw()

        #show heart
        for i in range (self.count1):
            arcade.draw_lrwh_rectangle_textured((i*10)+700 + i*10 , 40, 20, 20 , self.image)
        
        if self.count1 <= 0:
            arcade.set_background_color(arcade.color.BLACK)
            arcade.draw_text('GAME OVER', 250, 300, arcade.color.RED, 50)
            arcade.exit()
        
        if self.me.score < 10 :
            for i in range(len(self.enemy_list)):
                self.enemy_list[i].draw()

        for b in self.me.bullet_list:
            b.draw()
        
        if self.me.score >= 10 :
            self.bigenemy.draw()
            self.flag = 1
            for i in range(self.count2):
               arcade.draw_lrwh_rectangle_textured((i*10)+700 + i*10 , Screen_h - 40, 20, 20 , self.rect)
            
            if self.count2 == 0:
                arcade.draw_text('You Win', 250, 300, arcade.color.RED, 50)
                arcade.exit()
    
    def on_update(self, delta_time: float):

        self.me.rotate()
        self.me.move()
        
        if self.flag == 0: 
            self.end_time = time.time()
            t = random.randint(3,6)
            if self.end_time - self.start_time > t :
                self.enemy_list.append(Enemy(self.sp))
                self.sp += 0.1
                self.start_time = time.time()
 
            for b in self.me.bullet_list:
                b.move() 
            
            for enemy in self.enemy_list:
                enemy.move()
        
            for enemy in self.enemy_list:
                if enemy.center_y < 0 :
                    self.enemy_list.remove(enemy)
                    self.count1 -= 1
        
            for i in self.enemy_list :
                for j in self.me.bullet_list :
                    if arcade.check_for_collision(i , j):
                        arcade.play_sound(self.music)
                        self.enemy_list.remove(i)
                        self.me.bullet_list.remove(j)
                        self.me.score += 1
        
        if self.flag== 1:

            for b in self.me.bullet_list:
                b.move()    
        
            for b in self.me.bullet_list:
                if b.center_x < 0 or b.center_x > Screen_w or b.center_y > Screen_h or b.center_y < 0 :
                    self.me.bullet_list.remove(b)
            
            for b in self.me.bullet_list:
                if arcade.check_for_collision(self.bigenemy , b):
                    self.me.bullet_list.remove(b)
                    self.count2 -= 1
    
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            arcade.play_sound(self.fire_music)
            self.me.fire()        

        elif symbol == arcade.key.LEFT:
            self.me.change_angle = 1
    
        elif symbol == arcade.key.RIGHT:
            self.me.change_angle = -1

        elif symbol == arcade.key.UP:
            self.me.change_x = 0
            self.me.change_y = 1    
    
        elif symbol == arcade.key.DOWN:
            self.me.change_x = 0
            self.me.change_y = -1
    
        elif symbol == arcade.key.A:
            self.me.change_x = -1
            self.me.change_y = 0
    
        elif symbol == arcade.key.D:
            self.me.change_x = 1
            self.me.change_y = 0

    def on_key_release(self, key, modifiers):
        self.me.change_angle = 0
        self.me.change_x = 0
        self.me.change_y = 0

game = Game()
arcade.run()