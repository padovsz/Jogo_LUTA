import pygame
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

#cria a janela do jogo
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")

#define a taxa de quadros
clock = pygame.time.Clock()
FPS = 60

#define as cores
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)


#define as variaveis do jogo
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]#player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

#define as variaveis do lutador/jogador
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

#carrega a musica e os sons
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)

#carrega a imagem de fundo
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()
bgS_image = pygame.image.load("assets/images/background/backgroundSobre.jpg").convert_alpha()

#carrega as spritesheets
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

#carrega as imagens de vitoria/qual lutador ganhou
Fight_img = pygame.image.load("assets/images/icons/fight.png").convert_alpha()
Round2_img = pygame.image.load("assets/images/icons/round2.png").convert_alpha()
victoryWizzard_img = pygame.image.load("assets/images/icons/wizzardwin.png").convert_alpha()
victoryWarrior_img = pygame.image.load("assets/images/icons/warriorwin.png").convert_alpha()


#define o numero de etapas em cada animacao
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

#define a fonte
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

#funcao para desenhar texto
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#funcao para desenhar o fundo
def draw_bg():
  scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.blit(scaled_bg, (0, 0))


#funcao para desenhar barras de saude do lutador
def draw_health_bar(health, x, y):
  ratio = health / 100
  pygame.draw.rect(screen, WHITE, pygame.Rect(x - 4, y - 4, 408, 18), 2, 3)
  pygame.draw.rect(screen, BLACK, pygame.Rect(x - 2, y - 2, 404, 14), 2, 3)
  pygame.draw.rect(screen, RED, (x, y, 400, 10))
  pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 10))

def resize_image(image, width, height):
    return pygame.transform.scale(image, (width, height))


#cria duas instancias dos lutadores
fighter_1 = Fighter(1, 200, 369, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 700, 369, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

#game loop
run = True
while run:

  clock.tick(FPS)

  #desenha o fundo/background
  draw_bg()

  #mostra as estatisticas do jogador
  draw_health_bar(fighter_1.health, 20, 40)
  draw_health_bar(fighter_2.health, 580, 40)
  draw_text(str(score[0]), score_font, WHITE, 20, 5)
  draw_text(str(score[1]), score_font, WHITE, 970, 5)
  draw_text("Bozo", score_font, YELLOW, 20, 50)
  draw_text("Naro", score_font, GREEN, 80, 50)
  draw_text("Nove Dedos", score_font, RED, 840, 50)

  #contagem regressiva de atualizacoes
  if intro_count <= 0:
    #movimento dos lutadores
    fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
    fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
  else:
    #temporizador de contagem de exibicao
    draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
    #temporizador de contagem de atualizacoes
    if (pygame.time.get_ticks() - last_count_update) >= 1000:
      intro_count -= 1
      last_count_update = pygame.time.get_ticks()

  #atualiza os lutadores
  fighter_1.update()
  fighter_2.update()

  #desenha os lutadores
  fighter_1.draw(screen)
  fighter_2.draw(screen)

  
  scaled_bgS = pygame.transform.scale(bgS_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.blit(scaled_bgS, (0, 0))

  #verifica a derrota do jogador
  if round_over == False:
    if fighter_1.alive == False:
      score[1] += 1
      round_over = True
      round_over_time = pygame.time.get_ticks()
    elif fighter_2.alive == False:
      score[0] += 1
      round_over = True
      round_over_time = pygame.time.get_ticks()
  else:
    #exibe a imagem da vitoria de acordo com o jogador
    if fighter_1.alive:
        resized_image = resize_image(victoryWarrior_img, SCREEN_WIDTH, SCREEN_HEIGHT)
        screen.blit(resized_image, (0, 0))
    elif fighter_2.alive:
        resized_image = resize_image(victoryWizzard_img, SCREEN_WIDTH, SCREEN_HEIGHT)
        screen.blit(resized_image, (0, 0))
    if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
      round_over = False
      intro_count = 3
      fighter_1 = Fighter(1, 200, 369, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
      fighter_2 = Fighter(2, 700, 369, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

  #manipulador de eventos
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False


  #atualiza a exibicao
  pygame.display.update()

#sair do pygame
pygame.quit()