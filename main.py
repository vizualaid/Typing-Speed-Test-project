import time
import pygame
from pygame.locals import *
import sys
import random


# 750 x 500

class TypeSpeed:

    def __init__(self):
        self.w = 750
        self.h = 505
        self.reset = True
        self.active = False
        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = '0%'
        self.results = 'Time:0 Accuracy:0 % Wpm:0 '
        self.wpm = 0
        self.end = False
        # colors_text
        self.title = (255, 114, 94)
        self.sentence = (255, 114, 94)
        self.result = (255, 70, 70)
        self.j = 0

        pygame.init()
        # images
        self.icon = pygame.image.load('icon.png')
        pygame.display.set_icon(self.icon)

        self.open_img = pygame.image.load('splash.png')
        self.open_img = pygame.transform.scale(self.open_img, (self.w, self.h))

        self.bg = pygame.image.load('background.jpg')
        self.bg = pygame.transform.scale(self.bg, (750, 500))

        # draw icon image
        self.reset_img = pygame.image.load('reset.png')
        self.reset_img = pygame.transform.scale(self.reset_img, (190, 190))

        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Type Speed Analysis')

    def dis_text(self, screen, msg, y, fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, bool(1), color)
        text_rect = text.get_rect(center=(self.w / 2, y))  # typing area the center rectangle
        screen.blit(text, text_rect)
        pygame.display.update()

    @staticmethod
    def get_sentence():
        f = open('sentences.txt').read()
        sentences = f.split('\n')
        sentence = random.choice(sentences)
        return sentence

    def dis_results(self, screen):
        if not self.end:
            # Calculate time
            self.total_time = time.time() - self.time_start

            # Calculate accuracy
            count = 0
            for i, c in enumerate(self.word):
                try:
                    if self.input_text[i] == c:
                        count += 1
                except:
                    pass
            self.accuracy = count / len(self.word) * 100

            # Calculate words per minute
            self.wpm = (len(self.input_text) * 60 / (5 * self.total_time)) + 10
            if self.wpm > 30 and self.accuracy > 50:
                self.results = 'Time:' + str(round(self.total_time)) + " secs   Accuracy:" + str(
                    round(self.accuracy)) + "%" + '  Wpm: ' + str(round(self.wpm)) + " Average Speed"
            elif self.wpm > 40 and self.accuracy > 0:
                self.results = 'Time:' + str(round(self.total_time)) + " secs   Accuracy:" + str(
                    round(self.accuracy)) + "%" + '  Wpm: ' + str(round(self.wpm)) + " Great!"
            else:
                self.results = 'Time:' + str(round(self.total_time)) + " secs   Accuracy:" + str(
                    round(self.accuracy)) + "%" + ' Wpm: ' + str(round(self.wpm)) + " Need improvement"

            # screen.blit(self.time_img, (80,320))
            screen.blit(self.reset_img, (self.w / 2 - 95, self.h - 100))
            self.dis_text(screen, "RESET", self.h - 130, 30, (255, 255, 255))
            self.dis_text(screen, "(click to rest)", self.h - 110, 19, (255, 255, 255))

            pygame.display.update()

    def run(self):
        global clock
        self.run_again()

        self.running = True
        while self.running:
            clock = pygame.time.Clock()
            # text box color
            self.screen.fill((0, 0, 0), (50, 250, 650, 50))
            # outline rect
            pygame.draw.rect(self.screen, self.title, (50, 250, 650, 50), 2)
            # update the text of user input
            self.dis_text(self.screen, self.input_text, 274, 26, (250, 250, 250))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    # position of input box
                    if 50 <= x <= 650 and y >= 250 and y <= 300:
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time()
                        # position of reset box
                    if x >= 310 and x <= 510 and y >= 390 and self.end:
                        self.run_again()
                        x, y = pygame.mouse.get_pos()
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            self.dis_results(self.screen)
                            print(self.results)
                            self.dis_text(self.screen, self.results, 350, 28, self.result)
                            self.end = True

                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass
            pygame.display.update()


        clock.tick(60)

    def run_again(self):
        self.screen.blit(self.open_img, (0, 0))
        self.active = False

        pygame.display.update()
        time.sleep(1)

        self.reset = False
        self.end = False

        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0

        # random sentence
        self.word = self.get_sentence()
        if not self.word:
            self.run_again()
        # heading
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        msg = "Typing Speed Test"
        self.dis_text(self.screen, msg, 80, 80, self.title)

        # rectangle input box
        pygame.draw.rect(self.screen, (255, 192, 25), (50, 250, 650, 50), 2)

        # draw the sentence string
        self.dis_text(self.screen, self.word, 200, 28, self.sentence)

        pygame.display.update()


TypeSpeed().run()
