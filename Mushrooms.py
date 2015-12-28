__author__ = 'gregory'

#create the exe using cx freeze

import pygame
import tmx

class Goody(pygame.sprite.Sprite):
    image = pygame.image.load('Mushroom.png')
    def __init__(self, location, *groups):
        super(Goody, self).__init__(*groups)
        self.rect = pygame.rect.Rect(location, self.image.get_size())

class Player(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load('playernoah.png')
        self.right_image = self.image
        self.left_image = pygame.image.load('playernoahleft.png')
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.resting = False
        self.dy = 0
        self.direction = 1

    def update(self, dt, game):
        last = self.rect.copy()

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x -= 300 * dt
            self.image = self.left_image
            self.direction = -1
        if key[pygame.K_RIGHT]:
            self.rect.x += 300 * dt
            self.image = self.right_image
            self.direction = 1

        if self.resting and key[pygame.K_SPACE]:
            game.bounce.play()
            self.dy = -800

        self.dy = min(400, self.dy + 40)

        self.rect.y += self.dy * dt

        new = self.rect
        self.resting = False
        for cell in game.tilemap.layers['triggers'].collide(new, 'blockers'):
            blockers = cell['blockers']
            if 'l' in blockers and last.right <= cell.left and new.right > cell.left:
                new.right = cell.left
            if 'r' in blockers and last.left >= cell.right and new.left < cell.right:
                new.left = cell.right
            if 't' in blockers and last.bottom <= cell.top and new.bottom > cell.top:
                self.resting = True
                new.bottom = cell.top
                self.dy = 0
            if 'b' in blockers and last.top >= cell.bottom and new.top < cell.bottom:
                new.top = cell.bottom
                self.dy = 0

        if pygame.sprite.spritecollide(self, game.goodies, True):
            game.collect.play()
            pass

        game.tilemap.set_focus(new.x, new.y)

class Game(object):
    def main(self, screen):
        clock = pygame.time.Clock()

        background = pygame.image.load('BG.png')


        self.tilemap = tmx.load("Mushroom Map.tmx", screen.get_size())

        self.sprites = tmx.SpriteLayer()
        start_cell = self.tilemap.layers['triggers'].find('player')[0]
        self.player = Player((start_cell.px, start_cell.py), self.sprites)
        self.tilemap.layers.append(self.sprites)

        self.goodies = tmx.SpriteLayer()
        for goody in self.tilemap.layers['triggers'].find('goody'):
            Goody((goody.px, goody.py), self.goodies)
        self.tilemap.layers.append(self.goodies)

        winner = pygame.image.load('winner.png')

        self.collect = pygame.mixer.Sound('pop2.wav')
        self.bounce = pygame.mixer.Sound('bounce.wav')
        background_music = 'bensound-jazzcomedy.mp3'
        pygame.mixer.music.load(background_music)
        pygame.mixer.music.play(-1,0)

        while 1:
            dt = clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return


            self.tilemap.update(dt / 1000., self)

            screen.blit(background, (0, 0))
            self.tilemap.draw(screen)
            if not self.goodies:
                break
            pygame.display.flip()

        pygame.mixer.music.stop()
        pygame.mixer.music.load('bensound-clapandyell.mp3')
        pygame.mixer.music.play()

        while 1:
            dt = clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return


            self.tilemap.update(dt / 1000., self)

            screen.blit(background, (0, 0))
            self.tilemap.draw(screen)
            screen.blit(winner, (0, 0))
            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1000, 750))
    Game().main(screen)


