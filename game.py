#参考www.pygame.org/docs
import pygame,sys,time
from pygame.locals import *
from random import randint

class TankMain():  #坦克大战 主界面 
    width=600
    height=500
    my_tank = None
    my_tank_missile_list = []#我方坦克炮弹列表
    #ene_list = []
    wall=None
    ene_list = pygame.sprite.Group()#敌方坦克的组群
    explode_list = []#爆炸列表
    ene_missile_list=pygame.sprite.Group()#敌方坦克的组群
    
    def startGame(self):#开始游戏的方法
        pygame.init()
        #创建屏幕大小（宽，高），特性(0,R,F),颜色位
        screem = pygame.display.set_mode((TankMain.width,TankMain.height),0,32)
        #标题
        pygame.display.set_caption("坦克大战")
        TankMain.my_tank = My_Tank(screem)#我坦克显示在中下部
        TankMain.wall=Wall(screem,150,150,200,30)#创建墙大小
        for i in range(1,6):#初始化5个敌方坦克
                TankMain.ene_list.add(Ene_Tank(screem))#敌方坦克加入组中
        while True:
            #背景色color RGB
            screem.fill((0,0,0))#背景hei色
            for i,text in enumerate(self.write_text(),0):#显示左上角文字,enumerate()位枚举函数
                screem.blit(text,(2,5+(20*i)))

            if len(TankMain.ene_list) == 0:#如果地方被消灭
                screem.blit(self.write_1(),(100,200)) 
            TankMain.wall.display()#显示游戏中的墙
            TankMain.wall.hit_other()#碰撞检测
            self.get_event(TankMain.my_tank,screem)#获取事件，根据获取处理
            if TankMain.my_tank:
                TankMain.my_tank.hit_ene_missile()#我方坦克与敌方炮弹碰撞检测
            if TankMain.my_tank and TankMain.my_tank.live:
                TankMain.my_tank.display()#显示我方坦克
                TankMain.my_tank.move()#用移动的方法移动坦克
            else:
                TankMain.my_tank = None
                screem.blit(self.write_2(),(150,200)) #显示DEFEAT
               
            for ene in TankMain.ene_list:#显示和移动敌方坦克
                ene.display()
                ene.random_move()
                ene.random_fire()
            for m in TankMain.my_tank_missile_list: # 显示我方发射炮弹
                if m.live:#我方活着才能发射炮弹
                    m.display()
                    m.hit_tank()
                    m.move()
                else:
                   TankMain.my_tank_missile_list.remove(m)
            for m in TankMain.ene_missile_list: # 显示敌方发射炮弹
                if m.live:#活着才能发射炮弹
                    m.display()
                    #m.hit_tank()
                    m.move()
                else:
                   TankMain.ene_missile_list.remove(m)
            
            for explode in TankMain.explode_list:
                explode.display()


            time.sleep(0.05)
            #显示重置
            pygame.display.update()

    def get_event(self,my_tank,screem):#获取事件,键盘鼠标等
        for event in pygame.event.get():
            if event.type == QUIT:
                self.stopGame()#右上角退出
            if event.type == KEYDOWN and (not my_tank) and event.key == K_n:
                TankMain.my_tank = My_Tank(screem)#我方坦克显示
            if event.type == KEYDOWN and my_tank:
                if event.key == K_LEFT:
                    my_tank.direction="L"
                    #my_tank.move()
                    my_tank.stop = False
                if event.key == K_RIGHT:
                    my_tank.direction="R"
                    #my_tank.move()
                    my_tank.stop = False
                if event.key == K_UP:
                    my_tank.direction="U"
                    #my_tank.move()
                    my_tank.stop = False
                if event.key == K_DOWN:
                    my_tank.direction="D"
                    #my_tank.move()
                    my_tank.stop = False
                if event.key == K_ESCAPE:#ESC退出
                    self.stopGame()
                if event.key == K_SPACE:
                    m = my_tank.fire()
                    m.good = True #我方发射的炮弹
                    TankMain.my_tank_missile_list.append(m)
            if event.type == KEYUP and my_tank:
                if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN:
                    my_tank.stop = True
    def write_text(self):
        font = pygame.font.SysFont("隶书",20)
        text_sf1 = font.render("敌方坦克为：%d"%(len(TankMain.ene_list)),True,(255,0,0))
        text_sf2 = font.render("我方子弹为：%d"%(len(TankMain.my_tank_missile_list)),True,(255,0,0))
        return text_sf1,text_sf2
    def write_1(self):
        font = pygame.font.SysFont("隶书",100)
        text_1 = font.render("VICTORY",True,(255,0,0))
        return text_1
    def write_2(self):
        font = pygame.font.SysFont("隶书",100)
        text_2 = font.render("DEFEAT",True,(255,0,0))
        return text_2
    def stopGame(self):#停止游戏
        sys.exit()    

class BaseItem(pygame.sprite.Sprite):
    def __init__(self,screem):
        pygame.sprite.Sprite.__init__(self)
        #所有对象共享的功能属性
        self.screem=screem#坦克使用游戏屏幕窗口
    def display(self):
        if self.live:
            self.image=self.images[self.direction]
            self.screem.blit(self.image,self.rect)#使用边界画出坦克
        
class Tank(BaseItem): 
    #定义类属性宽和高
    width=50
    height=50
    def __init__(self,screem,left,top):
        super().__init__(screem)
        self.direction="U"#坦克默认方向
        self.speed=5#tank移动速度
        self.stop = False
        self.images={}#坦克所有图片
        self.images["L"]=pygame.image.load("images/tankL.gif")
        self.images["R"]=pygame.image.load("images/tankR.gif")
        self.images["U"]=pygame.image.load("images/tankU.gif")
        self.images["D"]=pygame.image.load("images/tankD.gif")
        self.image=self.images[self.direction]#坦克图片由方向决定
        self.rect=self.image.get_rect()#图片边界（坦克）
        self.rect.left=left
        #self.rect.right=right
        self.rect.top=top
        #self.rect.bottom=bottom
        self.live=True#坦克状态是否活着
        self.oldtop=self.rect.top
        self.oldleft=self.rect.left
    def stay(self):
        self.rect.top=self.oldtop
        self.rect.left=self.oldleft
    def display(self):#吧坦克显示在游戏窗口上
        self.image=self.images[self.direction]
        self.screem.blit(self.image,self.rect)#使用边界画出坦克
    def move(self):#移动我方坦克的方法
        if not self.stop:#如果不是停止状态
            self.oldleft=self.rect.left
            self.oldtop=self.rect.top
            if self.direction=="L":#如果方向向左，只需要left减小，移动
                if self.rect.left>0:
                    self.rect.left-=self.speed
                else:
                    self.rect.left=0
            elif self.direction=="R":
                if self.rect.right < TankMain.width:
                    self.rect.right+=self.speed
                else:
                    self.rect.right=TankMain.width
            elif self.direction=="U":
                if self.rect.top>0:
                    self.rect.top-=self.speed
                else:
                    self.rect.top=0
            elif self.direction=="D":
                if self.rect.bottom < TankMain.height:
                    self.rect.bottom+=self.speed
                else:
                    self.rect.bottom=TankMain.height
    def fire(self):
        m = Missile(self.screem,self)
        return m

class My_Tank(Tank):#我方坦克类，继承坦克
    def __init__(self,screem):
        super().__init__(screem,275,450)#我坦克显示在中下部
        self.stop = True#默认坦克静止
        self.live = True
    def hit_ene_missile(self):#用我方坦克检测炮弹碰撞
        hit_list = pygame.sprite.spritecollide(self,TankMain.ene_missile_list,False)
        for m in hit_list:#我方坦克中弹
            m.live = False
            TankMain.ene_missile_list.remove(m)
            self.live = False
            explode = Explode(self.screem,self.rect)
            TankMain.explode_list.append(explode)


class Ene_Tank(Tank):#敌方坦克类，继承坦克
    def __init__(self,screem):
        super().__init__(screem,randint(1,5)*100,0)#敌方坦克显示在上部
        self.speed=4
        self.step=20
        self.get_random_direction()
    def get_random_direction(self):
        r = randint(1,5)
        if  r == 4:
            self.direction="L"
            self.stop =False
        elif r == 1:
            self.direction="R"
            self.stop =False
        elif r == 2:
            self.direction="U"
            self.stop =False
        elif r == 3:
            self.direction="D"
            self.stop =False
    def random_move(self):
        if self.live:
            if self.step==0:
                self.get_random_direction()
                self.step=20#移动20步才能改变方法
            else:
                self.move()
                self.step -= 1
    def random_fire(self):
        r = randint(0,50)
        if r>45:#地方发射炮弹几率
            m = self.fire()
            TankMain.ene_missile_list.add(m)


class Missile(BaseItem):
    width=12
    height=12
    def __init__(self,screem,tank):
        super().__init__(screem)
        self.tank=tank
        self.direction=tank.direction#炮弹方向和坦克方向一样
        self.speed=15#tank移动速度
        self.stop = False
        self.images={}#坦克所有图片
        self.images["L"]=pygame.image.load("images/missileL.gif")
        self.images["R"]=pygame.image.load("images/missileR.gif")
        self.images["U"]=pygame.image.load("images/missileU.gif")
        self.images["D"]=pygame.image.load("images/missileD.gif")
        self.image=self.images[self.direction]#炮弹图片由方向决定
        self.rect=self.image.get_rect()#图片边界（坦克）
        self.rect.left=tank.rect.left+(tank.width-self.width)/2
        #self.rect.right=right
        self.rect.top=tank.rect.top+(tank.height-self.height)/2
        #self.rect.bottom=bottom
        self.live=True#炮弹状态活着
    def move(self):#移动炮弹的方法
        if not self.stop:#如果不是停止状态
            if self.direction=="L":#如果方向向左，只需要left减小，移动
                if self.rect.left>0:#判断是否在屏幕左边界
                    self.rect.left-=self.speed
                else:
                    self.live=False
            elif self.direction=="R":#如果方向向右，right增加
                if self.rect.right < TankMain.width:
                    self.rect.right+=self.speed
                else:
                    self.live=False
            elif self.direction=="U":
                if self.rect.top>0:
                    self.rect.top-=self.speed
                else:
                    self.live=False
            elif self.direction=="D":
                if self.rect.bottom < TankMain.height:
                    self.rect.bottom+=self.speed
                else:
                    self.live=False
    def hit_tank(self):#炮弹击中tank，1.我方击中敌方，2.敌方击中我方
        if self.good:
            hit_list = pygame.sprite.spritecollide(self, TankMain.ene_list, False)
            for e in hit_list:
                e.live =False
                TankMain.ene_list.remove(e)
                self.live = False
                explode = Explode(self.screem,e.rect)
                TankMain.explode_list.append(explode)

class Explode(BaseItem):#爆炸类
    def __init__(self,screem,rect):
        super().__init__(screem)
        self.live = True
        self.images=[pygame.image.load("images/5.gif"),\
                    pygame.image.load("images/6.gif"),\
                    pygame.image.load("images/7.gif"),\
                    pygame.image.load("images/8.gif"),\
                    pygame.image.load("images/9.gif"),
                    pygame.image.load("images/10.gif"),]
        self.step=0
        self.rect=rect#爆炸位置和被击中坦克的位置一样
    def display(self):#display游戏中循环调用。每0.05s点用一次
        if self.live:
            if self.step == len(self.images):#最后一张图片已经显示
                self.live = False
            else:
                self.image = self.images[self.step]
                self.screem.blit(self.image,self.rect)#使用边界画出爆炸
                self.step+=1
        else:
            return

class Wall(BaseItem):
    def __init__(self,screem,left,top,width,height):
        super().__init__(screem)
        self.rect = Rect(left,top,width,height)
        self.color=(255,255,255)
    def display(self):
        self.screem.fill(self.color,self.rect)
    def hit_other(self):#墙与其他对象碰撞检测
        if TankMain.my_tank:
            is_hit=pygame.sprite.collide_rect(self,TankMain.my_tank)
            if is_hit:
                TankMain.my_tank.stop = True#如果碰撞停止移动
                TankMain.my_tank.stay()
        if len(TankMain.ene_list)!=0:
            hit_list = pygame.sprite.spritecollide(self,TankMain.ene_list,False)
            for e in hit_list:
                e.stop=True
                e.stay()
        if len(TankMain.ene_missile_list)!=0:
            hit_list = pygame.sprite.spritecollide(self,TankMain.ene_missile_list,False)
            for f in hit_list:
                f.live=False
        if len(TankMain.my_tank_missile_list)!=0:
            hit_list = pygame.sprite.spritecollide(self,TankMain.my_tank_missile_list,False)
            for g in hit_list:
                g.live=False



game = TankMain()
game.startGame()