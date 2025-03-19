import os
import random
import sys
import pygame as pg


class Ball:
    def __init__(self, surface, colour, x, y, width, height):
        self.surface = surface
        self.colour = colour
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.moveDown, self.moveLeft = True, False
        self.ballXSpeed, self.ballYSpeed = 5, 5
        self.rect = pg.Rect((self.y, self.x), (self.width, self.height))


class Paddle:
    def __init__(self, surface, colour, x, y, width, height):
        self.surface = surface
        self.colour = colour
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.speed = 10
        self.rect = pg.Rect((self.y, self.x), (self.width, self.height))
        self.movingDown, self.movingUp = False, False
        self.score = 0


# def getType():
#     powerType = random.randint(0, 2)
#     if powerType == 0:
#         return "Slow"
#     elif powerType == 1:
#         return "Fast"


class PowerBlock:
    def __init__(self, surface, colour, x, y, width, height):
        self.surface = surface
        self.colour = colour
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.rect = pg.Rect((self.y, self.x), (self.width, self.height))
        self.speed = 1
        # self.powerType = getType()


class Game:
    def __init__(self):
        self.pg = pg.init()
        self.width, self.height = 900, 500
        self.FPS = 60
        self.clock = pg.time.Clock()
        self.window = pg.display.set_mode((self.width, self.height))
        self.display = pg.Surface((self.width, self.height))
        self.running, self.playing, self.menu = True, False, True
        self.font = os.path.join("assets","fonts","digital-7.ttf")
        self.ball = Ball(self.display, (255, 0, 0), self.height/2, self.width/2, 20, 20)
        self.players = [Paddle(self.display, (255, 0, 0), self.height / 2 - 35, 10, 7, 70),
                        Paddle(self.display, (255, 0, 0), self.height / 2, self.width - 20, 7, 70)]

        self.powers = [PowerBlock(self.display, (0, 0, 255), self.height / 2 - 100, self.width / 2, 30, 30),
                       PowerBlock(self.display, (255, 0, 0), self.height / 2 + 100, self.width / 2, 30, 30),
                       PowerBlock(self.display, (255, 0, 255), self.height / 2, self.width / 2, 30, 30)]


    def mainMenu(self):
        self.ballReset(self.width, self.height)
        for player in self.players:
            player.score = 0

        while self.running:
            randColour = (random.randint(100, 255), 0, random.randint(100, 255))
            self.checkMenu()
            self.display.fill((0, 0, 0))
            self.window.blit(self.display, (0, 0))
            self.drawText("Pong", 100, randColour, self.width/2, self.height/2 - 100)
            self.drawText("Press Enter to Start", 50, (255, 0, 255), self.width/2, self.height/2 + 100)
            pg.display.update()
            self.clock.tick(self.FPS)


    def drawText(self, text, size, colour, x, y):
        font = pg.font.Font(self.font, size)
        fontRender = font.render(text, False, colour)
        fontRect = fontRender.get_rect()
        fontRect.center = (x, y)
        self.window.blit(fontRender, fontRect)


    def checkMenu(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if self.menu:
                    if event.key == pg.K_RETURN:
                        self.playing = True
                        self.menu = False
                        self.gameLoop()

                if self.playing:
                    if event.key == pg.K_ESCAPE:
                        self.playing = False
                        self.menu = True
                        self.mainMenu()


    def drawPaddles(self, paddles):
        for paddle in paddles:
            pg.draw.rect(paddle.surface, paddle.colour, paddle)


    def movePaddles(self, keyPressed):
        if keyPressed[pg.K_s] and self.players[0].rect.height + self.players[0].rect.y < self.height:
            self.players[0].rect.y += self.players[0].speed
            self.players[0].movingDown = True
        elif keyPressed[pg.K_w] and self.players[0].rect.y > 0:
            self.players[0].rect.y -= self.players[0].speed
            self.players[0].movingUp = True
        else:
            self.players[0].movingUp = False
            self.players[0].movingDown = False

        if keyPressed[pg.K_DOWN] and self.players[1].rect.height + self.players[1].rect.y < self.height:
            self.players[1].rect.y += self.players[1].speed
            self.players[1].movingDown = True
        elif keyPressed[pg.K_UP] and self.players[1].rect.y > 0:
            self.players[1].rect.y -= self.players[1].speed
            self.players[1].movingUp = True
        else:
            self.players[1].movingUp = False
            self.players[1].movingDown = False

    # def checkPaddleCollision(self):
    #     ball = self.ball.rect
    #     pg.mixer.init()
    #
    #     beepSound = pg.mixer.Sound(os.path.join("src\assets\sounds\SFX_-_beep_08.ogg", "SFX_-_beep_08.ogg"))
    #     beepSound.set_volume(0.3)
    #
    #     if ball.colliderect(self.players[0]) or ball.colliderect(self.players[1]):
    #         beepSound.play()
    #         self.ball.ballXSpeed *= -1
    #         # if ball.y < self.players[0].y + self.players[0].height:
    #         #     self.ball.ballXSpeed *= -1
    #         # elif ball.y + ball.height > self.players[0].y:
    #         #     self.ball.ballXSpeed *= -1
    #

    # def checkPaddleCollision(self):
    #     ball = self.ball.rect
    #     playerOne = self.players[0].rect
    #     playerTwo = self.players[1].rect
    #
    #     beepSound = pg.mixer.Sound(os.path.join("src\assets\sounds\SFX_-_beep_08.ogg", "SFX_-_beep_08.ogg"))
    #     beepSound.set_volume(0.3)
    #
    #     if (ball.x <= playerOne.x + playerOne.width and ball.x + ball.width >= playerOne.x) and \
    #             (ball.y <= playerOne.y + playerOne.height and ball.y + ball.height >= playerOne.y) or \
    #             (ball.x <= playerTwo.x + playerTwo.width and ball.x + ball.width >= playerTwo.x) and \
    #             (ball.y <= playerTwo.y + playerTwo.height and ball.y + ball.height >= playerTwo.y):
    #         beepSound.play()
    #         self.ball.ballXSpeed *= -1


    def ballReset(self, width, height):
        self.ball.rect.x = width/2
        self.ball.rect.y = height/2


    def animateBall(self):
        self.ball.rect.x += self.ball.ballXSpeed
        self.ball.rect.y += self.ball.ballYSpeed

        ball = self.ball.rect

        playerOneRect = self.players[0].rect
        playerTwoRect = self.players[1].rect

        if self.ball.rect.top <= 0 or self.ball.rect.bottom >= self.height:
            self.ball.ballYSpeed *= -1

        beepSound = pg.mixer.Sound(os.path.join("src","assets","sounds", "SFX_-_beep_08.ogg"))
        beepSound.set_volume(0.3)

        if ball.colliderect(playerOneRect):
            beepSound.play()
            self.ball.ballXSpeed *= -1
            self.ball.rect.left = playerOneRect.right

        elif ball.colliderect(playerTwoRect):
            beepSound.play()
            self.ball.ballXSpeed *= -1
            self.ball.rect.right = playerTwoRect.left

        if self.ball.rect.left <= -30 or self.ball.rect.right >= self.width + 30:
            if self.ball.rect.left <= -30:
                self.players[1].score += 1
            else:
                self.players[0].score += 1

            self.ball.ballXSpeed *= -1
            self.ballReset(self.width, self.height)

        pg.draw.ellipse(self.display, (255, 0, 255), self.ball.rect)



    def animatePaddles(self):
        # self.checkPaddleCollision()
        keyPressed = pg.key.get_pressed()
        self.movePaddles(keyPressed)
        self.drawPaddles(self.players)


    def animatePowers(self):
        for power in self.powers:
            if self.ball.rect.colliderect(power.rect):
                 self.ball.ballXSpeed *= -1

            power.rect.y += power.speed
            pg.draw.rect(self.display, power.colour, power.rect)

            if power.rect.bottom >= self.height or power.rect.top <= 0:
                power.speed *= -1


    def updateScore(self):
        self.drawText("Score", 60, (255, 0, 0), self.width / 2, self.height / 2 - 200)
        self.drawText(f"{self.players[0].score}", 70, (255, 0, 255), self.width / 2 - 250, self.height / 2 - 150)
        self.drawText(f"{self.players[1].score}", 70, (255, 0, 255), self.width / 2 + 250, self.height / 2 - 150)


    def gameLoop(self):
        while self.playing:
            self.checkMenu()
            self.display.fill((0, 0, 0))
            self.animateBall()
            self.animatePaddles()
            self.animatePowers()
            self.window.blit(self.display, (0, 0))
            self.updateScore()
            pg.display.update()
            self.clock.tick(self.FPS)


if __name__ == "__main__":
    game = Game()

    while True:
        game.mainMenu()