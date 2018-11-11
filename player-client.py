import Pyro4, pygame
import string

#  (parametros)
altura = 550 # ALTURA DA WINDOW
largura = 800  # LARGURA DA WINDOW
rows = 2 # ALTURA DA GRID
cols = 13 # LARGURA DA GRID
MARGIN = 1 # MARGEM DOS BLOCOS DA GRID
WIDTH = 60.5 # LARGURA DOS BLOCOS DA DA GRID
HEIGHT = 60.5 # ALTURA DOS BLOCOS DA DA GRID

pygame.init()
WINDOW_SIZE = [largura, altura]
pygame.display.set_caption('GAME FORCA')
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

remote_object = Pyro4.Proxy("PYRONAME:game_forca")  # use name server object lookup uri shortcut

name = input("What is your name? ").strip()
remote_object.set_players_online()
remote_object.set_name(name)

# (functions)
def background_color(color):
    background_color = {}
    background_color['black'] = (0, 0, 0)
    background_color['white'] = (255, 255, 255)
    background_color['blue'] = (0, 0, 255)
    background_color['red'] = (255, 0, 0)
    background_color['green'] = (0, 255, 0)
    background_color['yellow'] = (255, 255, 0)
    background_color['marrom'] = (92, 51, 23)
    return background_color[color]
# end method background_color

def quit_game():
    pygame.display.quit()
# end method quit_game

def status_bar(chances, name):
    pygame.draw.rect(screen, background_color('black'), [0, 520, 800, 550])
    font = pygame.font.SysFont(None, 25)
    text = font.render('Chances: {} restantes'.format(chances), True, background_color('white'))
    screen.blit(text, [3, 527])
    text = font.render('Player: {}'.format(name), True, background_color('white'))
    screen.blit(text, [300, 527])
    text = font.render('Online: {}'.format(remote_object.get_players_online()), True, background_color('white'))
    screen.blit(text, [600, 527])
# end method status_bar

def draw_alphabet():
    font = pygame.font.SysFont(None, 40)
    lettrs_alphabet = list(string.ascii_uppercase)
    letter = None
    # print(letters_tried)
    letters_grid = remote_object.get_grid()
    pos = remote_object.get_pos_letter()

    for i in range(rows):
        for j in range(cols):
            color = background_color('black')
            try:
                if letters_grid[i][j] == 1:
                    color = background_color('red')
                    if pos != None:
                        x, y = pos
                        if letters_grid[x][y] == 1:
                            if x == 0:
                                letter = lettrs_alphabet[(x + y)]
                            else:
                                letter = lettrs_alphabet[(y + 13)]
            except:
                pass
            if i == 0:
                letters = font.render(lettrs_alphabet[(i + j)], True, background_color('white'))
            else:
                letters = font.render(lettrs_alphabet[(j + 13)], True, background_color('white'))
            pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * j + MARGIN,
                                             (MARGIN + HEIGHT) * i + MARGIN,
                                             WIDTH, HEIGHT])
            screen.blit(letters, [(MARGIN + WIDTH) * j + 20, (MARGIN + HEIGHT) * i + 20])
    return letter
# end method draw_alphabet

def draw_word_field():
    word = remote_object.get_word()
    letter = remote_object.get_letters_tried()
    font = pygame.font.SysFont(None, 40)
    tam = largura / len(word)
    for i in range(len(word)):
        color = background_color('black')
        pygame.draw.rect(screen, color, [i * tam, altura-altura*0.15-20,
                                         tam-MARGIN, 30])
        if letter != None:
            for k in letter:
                text = font.render(word[k], True, background_color('white'))
                screen.blit(text, [k * tam, altura-altura*0.15-20])
# end method draw_word_field

def winner(screen, remote_object):
    done = False
    while not done:
        screen.fill(background_color('white'))
        pygame.draw.rect(screen, background_color('green'),
                         [largura * (1 / 3)-60, altura * (1 / 2) - 50, largura * (1 / 3)+120, 30])
        font = pygame.font.SysFont(None, 40)
        text = font.render('Player {} ganhou!'.format(remote_object.get_name()), True, background_color('white'))
        screen.blit(text, [largura * (1 / 3)-60, altura * (1 / 2) - 50])

        pygame.draw.rect(screen, background_color('blue'),
                         [largura * (1 / 3) - 20, altura * (1 / 2) - 10, largura * (1 / 3) / 2, 30])
        font = pygame.font.SysFont(None, 30)
        text = font.render('Recomeçar', True, background_color('white'))
        screen.blit(text, [largura * (1 / 3) - 20, altura * (1 / 2) - 10])

        pygame.draw.rect(screen, background_color('red'),
                         [largura * (1 / 3) + largura * (1 / 3) / 2 + 20,
                          altura * (1 / 2) - 10, largura * (1 / 3) / 2, 30])
        # font = pygame.font.SysFont(None, 30)
        text = font.render('Sair', True, background_color('white'))
        screen.blit(text, [largura * (1 / 3) + largura * (1 / 3) / 2 + 20, altura * (1 / 2) - 10])

        for event in pygame.event.get():  # User did something
            try:
                if event.type == pygame.QUIT:  # If user clicked close
                    quit_game()
                    return 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if x >= largura * (1 / 3) - 20 and y >= altura * (1 / 2) - 10 and x <= largura * (
                        1 / 3) - 20 + largura * (1 / 3) / 2 and y <= altura * (1 / 2) - 10 + 30:
                        remote_object = Pyro4.Proxy("PYRONAME:game_forca")  # use name server object lookup uri shortcut

                        name = 'Léo'  # input("What is your name? ").strip()
                        remote_object.set_name(name)
                        return 1
                    if x >= largura * (1 / 3) + largura * (1 / 3) / 2 + 20 and y >= altura * (
                        1 / 2) - 10 and x <= largura * (1 / 3) + largura * (1 / 3) / 2 + 20 + largura * (
                        1 / 3) / 2 and y <= altura * (1 / 2) - 10 + 30:
                        quit_game()
                        return 0

            except:
                pass

        clock.tick(30)  # Limit to 30 frames per second
        try:
            pygame.display.update()  # Go ahead and update the screen with what we've drawn.
        except:
            break

def game_over(screen, remote_object):
    remote_object.set_players_offline()
    done = False
    while not done:
        screen.fill(background_color('white'))
        pygame.draw.rect(screen, background_color('black'),
                         [largura * (1 / 3), altura * (1 / 2) - 50, largura * (1 / 3), 30])
        font = pygame.font.SysFont(None, 49)
        text = font.render('Game Over', True, background_color('white'))
        screen.blit(text, [largura * (1 / 3) + 40, altura * (1 / 2) - 50])

        pygame.draw.rect(screen, background_color('blue'),
                         [largura * (1 / 3) - 20, altura * (1 / 2) - 10, largura * (1 / 3) / 2, 30])
        font = pygame.font.SysFont(None, 30)
        text = font.render('Recomeçar', True, background_color('white'))
        screen.blit(text, [largura * (1 / 3) - 20, altura * (1 / 2) - 10])

        pygame.draw.rect(screen, background_color('red'),
                         [largura * (1 / 3) + largura * (1 / 3) / 2 + 20,
                          altura * (1 / 2) - 10, largura * (1 / 3) / 2, 30])
        # font = pygame.font.SysFont(None, 30)
        text = font.render('Sair', True, background_color('white'))
        screen.blit(text, [largura * (1 / 3) + largura * (1 / 3) / 2 + 20, altura * (1 / 2) - 10])

        for event in pygame.event.get():  # User did something
            try:
                if event.type == pygame.QUIT:  # If user clicked close
                    quit_game()
                    return 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if x >= largura*(1/3)-20 and  y >= altura*(1/2)-10 and x <= largura*(1/3)-20+largura*(1/3)/2 and y <= altura*(1/2)-10+30:
                        remote_object = Pyro4.Proxy("PYRONAME:game_forca")  # use name server object lookup uri shortcut

                        name = 'Léo'  # input("What is your name? ").strip()
                        remote_object.set_name(name)
                        return 1
                    if x >= largura*(1/3)+largura*(1/3)/2+20 and y >= altura*(1/2)-10 and x <= largura*(1/3)+largura*(1/3)/2+20+largura*(1/3)/2 and y <= altura*(1/2)-10+30:
                        quit_game()
                        return 0

            except:
                pass

        clock.tick(30)  # Limit to 30 frames per second
        try:
            pygame.display.update()  # Go ahead and update the screen with what we've drawn.
        except:
            break
# end method game_over

def start_game():
    letters_grid = remote_object.get_grid()
    qtd_chances = remote_object.get_chance()
    # Variável para controlar o jogo
    done = False
    while not done:
        screen.fill(background_color('white'))
        draw_alphabet()
        for event in pygame.event.get():  # User did something
            try:
                if event.type == pygame.QUIT:  # If user clicked close
                    quit_game()
                    return 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    ROW = y // (HEIGHT + MARGIN)
                    COL = x // (WIDTH + MARGIN)
                    if COL >= 0 and ROW >= 0:
                        if not letters_grid[int(ROW)][int(COL)] == 1:
                            letters_grid[int(ROW)][int(COL)] = 1
                            remote_object.set_pos_letter(int(ROW), int(COL))
                            remote_object.set_grid(remote_object.get_pos_letter())
                            letter = draw_alphabet()
                            aux = remote_object.try_find_letter(letter)
                            if aux == 1:
                                qtd_chances -= 1
            except:
                pass

        draw_word_field()
        if len(remote_object.get_letters_tried()) == len(remote_object.get_word()):
            winner(screen, remote_object)
            return 0

        status_bar(qtd_chances, name)
        # Update screen ever 30 frames per second
        clock.tick(30)  # Limit to 30 frames per second
        try:
            pygame.display.update()  # Go ahead and update the screen with what we've drawn.
            if qtd_chances <= 0:
                aux = game_over(screen, remote_object)
                if aux == 0:
                    break
                else:
                    pass
        except:
            break

start_game()