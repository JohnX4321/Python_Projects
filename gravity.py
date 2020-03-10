import pygame,os,sys


class Platform(pygame.sprite.Sprite):

    def __init__(self,xloc,yloc,imgw,imgh,img):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(os.path.join('images',img)).convert()
        self.image.convert_alpha()
        self.rect=self.image.get_rect()
        self.rect.y=yloc
        self.rect.x=xloc


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.health = 10
        self.score = 1
        self.images = []
        for i in range(1, 9):
            img = pygame.image.load(os.path.join('images', 'hero' + str(i) + '.png')).convert()
            img.convert_alpha()
            img.set_colorkey(ALPHA)
            self.images.append(img)
            self.image = self.images[0]
            self.rect = self.image.get_rect()

    def gravity(self):
        self.movey+=3.2
        if self.rect.y>worldy and self.movey>=0:
            self.movey=0
            self.rect.y=world-2*ty

    def control(self, x, y):
        '''
        control player movement
        '''
        self.movex += x
        self.movey += y

    def update(self):
        '''
        Update sprite position
        '''

        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey

        # moving left
        if self.movex < 0:
            self.frame += 1
            if self.frame > ani * 3:
                self.frame = 0
            self.image = self.images[self.frame // ani]

        # moving right
        if self.movex > 0:
            self.frame += 1
            if self.frame > ani * 3:
                self.frame = 0
            self.image = self.images[(self.frame // ani) + 4]

        # collisions
        enemy_hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        for enemy in enemy_hit_list:
            self.health -= 1
            print(self.health)

        ground_hit_list = pygame.sprite.spritecollide(self, ground_list, False)
        for g in ground_hit_list:
            self.health -= 1
            print(self.health)


class Enemy(pygame.sprite.Sprite):
    '''
    Spawn an enemy
    '''

    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', img))
        # self.image.convert_alpha()
        # self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.counter = 0

    def move(self):
        '''
        enemy movement
        '''
        distance = 80
        speed = 8

        if self.counter >= 0 and self.counter <= distance:
            self.rect.x += speed
        elif self.counter >= distance and self.counter <= distance * 2:
            self.rect.x -= speed
        else:
            self.counter = 0

        self.counter += 1


class Level():
    def bad(lvl, eloc):
        if lvl == 1:
            enemy = Enemy(eloc[0], eloc[1], 'yeti.png')  # spawn enemy
            enemy_list = pygame.sprite.Group()  # create enemy group
            enemy_list.add(enemy)  # add enemy to group

        if lvl == 2:
            print("Level " + str(lvl))

        return enemy_list

    def loot(lvl, lloc):
        print(lvl)

    def ground(lvl, gloc, tx, ty):
        ground_list = pygame.sprite.Group()
        i = 0
        if lvl == 1:
            while i < len(gloc):
                ground = Platform(gloc[i], worldy - ty, tx, ty, 'ground.png')
                ground_list.add(ground)
                i = i + 1

        if lvl == 2:
            print("Level " + str(lvl))

        return ground_list

    def platform(lvl, tx, ty):
        plat_list = pygame.sprite.Group()
        ploc = []
        i = 0
        if lvl == 1:
            ploc.append((0, worldy - ty - 128, 3))
            ploc.append((300, worldy - ty - 256, 3))
            ploc.append((500, worldy - ty - 128, 4))

            while i < len(ploc):
                j = 0
                while j <= ploc[i][2]:
                    plat = Platform((ploc[i][0] + (j * tx)), ploc[i][1], tx, ty, 'ground.png')
                    plat_list.add(plat)
                    j = j + 1
                print('run' + str(i) + str(ploc[i]))
                i = i + 1

        if lvl == 2:
            print("Level " + str(lvl))

        return plat_list


'''
Setup
'''
worldx = 960
worldy = 720

fps = 40  # frame rate
ani = 4  # animation cycles
clock = pygame.time.Clock()
pygame.init()
main = True

BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)
ALPHA = (0, 255, 0)

world = pygame.display.set_mode([worldx, worldy])
backdrop = pygame.image.load(os.path.join('images', 'stage.png')).convert()
backdropbox = world.get_rect()
player = Player()  # spawn player
player.rect.x = 0
player.rect.y = 0
player_list = pygame.sprite.Group()
player_list.add(player)
steps = 10  # how fast to move

eloc = []
eloc = [200, 20]
gloc = []
# gloc = [0,630,64,630,128,630,192,630,256,630,320,630,384,630]
tx = 64  # tile size
ty = 64  # tile size

i = 0
while i <= (worldx / tx) + tx:
    gloc.append(i * tx)
    i = i + 1

enemy_list = Level.bad(1, eloc)
ground_list = Level.ground(1, gloc, tx, ty)
plat_list = Level.platform(1, tx, ty)

'''
Main loop
'''
while main == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit();
            sys.exit()
            main = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                print("LEFT")
                player.control(-steps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                print("RIGHT")
                player.control(steps, 0)
            if event.key == pygame.K_UP or event.key == ord('w'):
                print('jump')

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(steps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(-steps, 0)
            if event.key == pygame.K_UP or event.key == ord('w'):
                print('jump')

            if event.key == ord('q'):
                pygame.quit()
                sys.exit()
                main = False

    world.blit(backdrop, backdropbox)
    player.gravity()  # check gravity
    player.update()
    player_list.draw(world)
    enemy_list.draw(world)
    ground_list.draw(world)
    plat_list.draw(world)
    for e in enemy_list:
        e.move()
    pygame.display.flip()
    clock.tick(fps)
