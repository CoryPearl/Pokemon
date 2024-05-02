#colldown working and display
#loading screen when start
#better win screen
#healing heals full thing?????????

import pygame
import requests
import random
import io

pygame.init()
pygame.font.init()

my_font = pygame.font.SysFont('Comic Sans MS', 30)
my_font2 = pygame.font.SysFont('Comic Sans MS', 60)
my_font3 = pygame.font.SysFont('Comic Sans MS', 40)
my_font4 = pygame.font.SysFont('Comic Sans MS', 20)
my_font5 = pygame.font.SysFont('Comic Sans MS', 15)
my_font6 = pygame.font.SysFont('Comic Sans MS', 28)
my_font7 = pygame.font.SysFont('Comic Sans MS', 25)

game_width = 1050
game_height = 640
size = (game_width, game_height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Pokémon')
running = True
first_screen = True
second_screen = False
win_screen = False
current_input = 0
potion_count1 = 3
potion_count2 = 3
can_defend1 = True
can_defend2 = True
winner = ''
clock = pygame.time.Clock()

bg1 = pygame.image.load("bg1.png")
bg1 = pygame.transform.scale(bg1, (1050,640))

bg2 = pygame.image.load("bg2.png")
bg2 = pygame.transform.scale(bg2, (1050,640))

class Pokemon(pygame.sprite.Sprite):
    def __init__(self, name, level, x, y):
        pygame.sprite.Sprite.__init__(self)

        base_url = 'https://pokeapi.co/api/v2'

        req = requests.get(f'{base_url}/pokemon/{name.lower()}')
        self.json = req.json()

        self.name = self.json['name'].capitalize()
        self.level = level

        self.x = x
        self.y = y

        self.coolDown = [0,0,0,0]

        stats = self.json['stats']
        for stat in stats:
            if stat['stat']['name'] == 'hp':
                self.current_hp = stat['base_stat'] + self.level
                self.max_hp = stat['base_stat'] + self.level
            elif stat['stat']['name'] == 'attack':
                self.attack = stat['base_stat']
            elif stat['stat']['name'] == 'defense':
                self.defense = stat['base_stat']
                self.default_defence = stat['base_stat']
            elif stat['stat']['name'] == 'speed':
                self.speed = stat['base_stat']

        types = self.json['types']
        self.type = types[0]['type']['name']

        self.moves = []
        moves = self.json['moves']
        
        for i in range(4):
            move_url = moves[i]['move']['url']
            req2 = requests.get(move_url)
            movesJson = req2.json()
            if movesJson['accuracy'] and movesJson['power'] and movesJson['name']:
                toAppend = [movesJson['accuracy'], movesJson['power'], movesJson['name']]
                toAppend.reverse()
                self.moves.append(toAppend)
            else:
                while not movesJson['accuracy'] or not movesJson['power'] or not movesJson['name']:
                    move_url = moves[i+4]['move']['url']
                    req2 = requests.get(move_url)
                    movesJson = req2.json()
                    toAppend = [movesJson['accuracy'], movesJson['power'], movesJson['name']]
                    toAppend.reverse()
                    self.moves.append(toAppend)

        self.types = [type_data['type']['name'] for type_data in self.json['types']]
        self.size = 500

        self.set_sprite('front_default')

    def set_sprite(self, side):
        image_url = self.json['sprites'][side]
        image_data = requests.get(image_url).content
        image_file = io.BytesIO(image_data)
        self.image = pygame.image.load(image_file).convert_alpha()

        scale = self.size / self.image.get_width()
        new_width = self.image.get_width() * scale
        new_height = self.image.get_height() * scale
        self.image = pygame.transform.scale(self.image, (int(new_width), int(new_height)))

    def draw(self, alpha=255):
        sprite = self.image.copy()
        transparency = (255, 255, 255, alpha)
        screen.fill(transparency, None, pygame.BLEND_RGBA_MULT)
        screen.blit(sprite, (self.x, self.y))

def drawHealthBars():
    global player1,player2
    border1 = pygame.draw.rect(screen, (0, 0, 0),(20,45,312.5,60))
    border2 = pygame.draw.rect(screen, (0, 0, 0),(720,45,312.5,60))
    player1_box = pygame.draw.rect(screen, (255, 0, 0),(25,50,300,50))
    player2_box = pygame.draw.rect(screen, (255, 0, 0),(725,50,300,50))

    player1_name = my_font.render(f'{player1.name}', False, (255, 255, 255))
    screen.blit(player1_name, (25,2.5))

    player2_name = my_font.render(f'{player2.name}', False, (255, 255, 255))
    screen.blit(player2_name, (725,2.5))

    player1_ininterval = 300/player1.max_hp
    length = 0
    while length < player1.current_hp*player1_ininterval:
        length += player1_ininterval
    player1_health = pygame.draw.rect(screen, (0, 255, 0),(25,50,length,50))
    player1_health_text = my_font.render(f'{player1.current_hp}/{player1.max_hp}', False, (255, 255, 255))
    screen.blit(player1_health_text, (240,5))

    player2_ininterval = 300/player2.max_hp
    length = 0
    while length < player2.current_hp*player2_ininterval:
        length += player2_ininterval
    player2_health = pygame.draw.rect(screen, (0, 255, 0),(725,50,length,50))
    player2_health_text = my_font.render(f'{player2.current_hp}/{player2.max_hp}', False, (255, 255, 255))
    screen.blit(player2_health_text, (940,5))

def drawMenu():
    random_border = pygame.draw.rect(screen,(0,0,0),(10,10,325,75))
    random = pygame.draw.rect(screen,(255,255,255),(15,15,315,65))
    random_text = my_font3.render('Random Pokémon',False, (0,0,0))
    screen.blit(random_text, (15,15))

    button_border = pygame.draw.rect(screen,(0,0,0),(game_width/2-155,420,310,75))
    start_button = pygame.draw.rect(screen,(255,255,255),(game_width/2-150,425,300,65))
    start_text = my_font2.render('Start',False, (0,0,0))
    screen.blit(start_text, (game_width/2-77.5,410))

    input2_border = pygame.draw.rect(screen,(0,0,0),(game_width/2-255,325,510,90))
    input2 = pygame.draw.rect(screen,(255,255,255),(game_width/2-250,330,500,80))
    input2_text = my_font3.render('Player 2 enter pokémon',False, (200,200,200))
    if len(input2_charecters) == 0:
        screen.blit(input2_text, (game_width/2-245,337.5))

    input1_border = pygame.draw.rect(screen,(0,0,0),(game_width/2-255,225,510,90))
    input1 = pygame.draw.rect(screen,(255,255,255),(game_width/2-250,230,500,80))
    input1_text = my_font3.render('Player 1 enter pokémon',False, (200,200,200))
    if len(input1_charecters) == 0:
        screen.blit(input1_text, (game_width/2-245,237.5))

def set_players():
    global player1,player2, current_turn, first_player
    level = 10

    player1_choice = ''
    for char in input1_charecters:
        player1_choice += char

    player2_choice  = ''
    for char in input2_charecters:
        player2_choice += char

    player1 = Pokemon(player1_choice, level, 75, 150)
    player2 = Pokemon(player2_choice, level, 450, 20)

    if player2.speed > player1.speed:
        current_turn = 2
        first_player = 2

def set_text():
    to_blit = ''
    for char in input1_charecters:
        to_blit += char
    to_blit_render = my_font3.render(to_blit,False, (0,0,0))
    screen.blit(to_blit_render, (game_width/2-245,237.5))

    to_blit = ''
    for char in input2_charecters:
        to_blit += char
    to_blit_render = my_font3.render(to_blit,False, (0,0,0))
    screen.blit(to_blit_render, (game_width/2-245,337.5))

input1_charecters = []
input2_charecters = []

def draw_button(x,y,width,height,text, fontSize):
    rect_border = pygame.draw.rect(screen, (0,0,0), (x-5,y-5,width+10, height+10))
    rect = pygame.draw.rect(screen, (255,255,255),(x,y,width,height))

    if fontSize == 4:
        label = my_font4.render(text,False, (0,0,0))
        screen.blit(label, (x+2.5,y-5))
    elif fontSize == 3:
        label = my_font3.render(text,False, (0,0,0))
        screen.blit(label, (x+2.5,y-5))
    elif fontSize == 7:
        label = my_font7.render(text,False, (0,0,0))
        screen.blit(label, (x+2.5,y+5))

def draw_move_stats(power, accuracy,x,y):
    to_blit = f'Dmg: {power}   Hitchance: {accuracy}%'
    to_blit_render = my_font5.render(to_blit,False, (0,0,0))
    screen.blit(to_blit_render, (x,y))

active_menu = 0
current_turn = 1
first_player = 1
def draw_options():
    if current_turn == 1:
        turn_name = my_font6.render(f'{player1.name.capitalize()} what will you do?', False,(255,255,255))
        screen.blit(turn_name, (595,425))
        underline = pygame.draw.rect(screen, (255,0,0), (25,140,310,2.5))
    else:
        turn_name = my_font6.render(f'{player2.name.capitalize()} what will you do?', False, (255,255,255))
        screen.blit(turn_name, (595,425))
        underline = pygame.draw.rect(screen, (255,0,0), (725,140,310,2.5))

    if active_menu == 0:
        draw_button(600,475,200,50,'Attack',3)
        draw_button(820,475,200,50,'Defend',3)
        if current_turn == 1:
            draw_button(600,545,200,50,f'Health Potion ({potion_count1})',7)
        elif current_turn == 2:
            draw_button(600,545,200,50,f'Health Potion ({potion_count2})',7)
        draw_button(820,545,200,50,'Run',3)

    elif active_menu == 1:
        new_moves = []
        move_stats = []
        for item in player1.moves:
            toAppend = f'{item[0].capitalize()}'
            new_moves.append(toAppend)
            stats_to_append = []
            stats_to_append.append(item[1])
            stats_to_append.append(item[2])
            move_stats.append(stats_to_append)

        draw_button(820,610,200,20,'Back',4)

        draw_button(600,475,200,50,new_moves[0],4)
        draw_button(820,475,200,50,new_moves[1],4)
        draw_button(600,545,200,50,new_moves[2],4)
        draw_button(820,545,200,50,new_moves[3],4)
        draw_move_stats(move_stats[3][0],move_stats[3][1],822.5,570)
        draw_move_stats(move_stats[2][0],move_stats[2][1],822.5,500)
        draw_move_stats(move_stats[1][0],move_stats[1][1],602.5,570)
        draw_move_stats(move_stats[0][0],move_stats[0][1],602.5,500)
    
    elif active_menu == 2:
        new_moves = []
        move_stats = []
        for item in player2.moves:
            toAppend = f'{item[0].capitalize()}'
            new_moves.append(toAppend)
            stats_to_append = []
            stats_to_append.append(item[1])
            stats_to_append.append(item[2])
            move_stats.append(stats_to_append)

        draw_button(820,610,200,20,'Back',4)

        draw_button(600,475,200,50,new_moves[0],4)
        draw_button(820,475,200,50,new_moves[1],4)
        draw_button(600,545,200,50,new_moves[2],4)
        draw_button(820,545,200,50,new_moves[3],4)
        draw_move_stats(move_stats[3][0],move_stats[3][1],822.5,570)
        draw_move_stats(move_stats[2][0],move_stats[2][1],822.5,500)
        draw_move_stats(move_stats[1][0],move_stats[1][1],602.5,570)
        draw_move_stats(move_stats[0][0],move_stats[0][1],602.5,500)

def updateCooldowns():
    for item in player1.coolDown:
        if item == 1 or item == 2:
            item = item - 1
    
    for item in player2.coolDown:
        if item == 1 or item == 2:
            item = item - 1

def drawCooldowns():
    if current_turn == 1:
        player1_defend = my_font.render(f'Can defend: {str(can_defend1)}', False, (255,255,255))
        screen.blit(player1_defend, (595,595))

    elif current_turn == 2:
        player2_defend = my_font.render(f'Can defend: {str(can_defend2)}', False, (255,255,255))
        screen.blit(player2_defend, (595,595))

def random_players():
    global player1,player2, current_turn, first_player
    with open('pokemon.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        random_pokemon1 = random.choice(lines).strip()
        random_pokemon2 = random.choice(lines).strip()

        level = 10

        player1 = Pokemon(random_pokemon1, level, 75, 150)
        player2 = Pokemon(random_pokemon2, level, 450, 20)

        if player2.speed > player1.speed:
            current_turn = 2
            first_player = 2

def drawWinScreen(txt):
    screen.blit(bg2,(0,0))

    if txt == "Player 1: " + player1.name:
        screen.blit(player1.image, (75,150))
    elif txt == "Player 2: " + player2.name:
        screen.blit(player2.image, (420,20))

    message = my_font2.render(f'Winner is {txt}!', False, (255, 255, 255))
    screen.blit(message, (game_width/2-425, 250))

def drawStats():
    player1_stats = f'Defence: {player1.defense} Speed: {player1.speed}'
    player1_stats_render = my_font6.render(player1_stats, False, (255,255,255))
    screen.blit(player1_stats_render, (25,100))

    player2_stats = f'Defence: {player2.defense} Speed: {player2.speed}'
    player2_stats_render = my_font6.render(player2_stats, False, (255,255,255))
    screen.blit(player2_stats_render, (725,100))

while running:
    for event in pygame.event.get():
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_BACKSPACE:
                if current_input == 1 and len(input1_charecters) > 0:
                    input1_charecters.pop()
                elif current_input == 2 and len(input2_charecters) > 0:
                    input2_charecters.pop()
            else:
                if current_input == 1:
                    if pygame.key.get_mods() & pygame.KMOD_CAPS:
                        input1_charecters.append(event.unicode.upper())
                    else:
                        input1_charecters.append(event.unicode.lower())
                elif current_input == 2:
                    if pygame.key.get_mods() & pygame.KMOD_CAPS:
                        input2_charecters.append(event.unicode.upper())
                    else:
                        input2_charecters.append(event.unicode.lower())

        if event.type == pygame.MOUSEBUTTONDOWN:
            if first_screen == True:
                if game_width/2-155 <= mouse_x <= (game_width/2-155) + 310 and 420 <= mouse_y <= 495:
                    second_screen = True
                    first_screen = False
                    set_players()

                elif 10 <= mouse_x <= 335 and 10 <= mouse_y <= 85:
                    second_screen = True
                    first_screen = False
                    random_players()

                elif game_width/2-255 <= mouse_x <= (game_width/2-255) + 510 and 225 <= mouse_y <= 315:
                    current_input = 1
                
                elif game_width/2-255 <= mouse_x <= (game_width/2-255) + 510 and 325 <= mouse_y <= 415:
                    current_input = 2
            elif first_screen == False:
                if active_menu == 0:
                    if 600 <= mouse_x <= 800 and 475 <= mouse_y <= 525 and current_turn == 1:
                        active_menu = 1

                    elif 600 <= mouse_x <= 800 and 475 <= mouse_y <= 525 and current_turn == 2:
                        active_menu = 2

                    elif 820 <= mouse_x <= 1020 and 545 <= mouse_y <= 595 and current_turn == 2:
                        winner = 'Player 1: ' + player1.name
                        win_screen = True
                        second_screen = False

                    elif 820 <= mouse_x <= 1020 and 545 <= mouse_y <= 595 and current_turn == 1:
                        winner = 'Player 2: ' + player1.name
                        win_screen = True
                        second_screen = False

                    elif 820 <= mouse_x <= 1020 and 475 <= mouse_y <= 525 and current_turn == 1 and can_defend1:
                        player1.defense *= 2

                        can_defend1 =  False
                        player2.defense = player2.default_defence
                        updateCooldowns()
                        current_turn = 2
                        active_menu = 0
                    
                    elif 820 <= mouse_x <= 1020 and 475 <= mouse_y <= 525 and current_turn == 2 and can_defend2:
                        player2.defense *= 2

                        can_defend2 =  False
                        player1.defense = player1.default_defence
                        updateCooldowns()
                        current_turn = 1
                        active_menu = 0

                    elif 600 <= mouse_x <= 800 and 545 <= mouse_y <= 595:
                        if current_turn == 1 and potion_count1 > 0:
                            player1.current_hp = player1.current_hp + (player1.max_hp/2)
                            if (player1.current_hp + (player1.max_hp/2) > player1.max_hp):
                                player1.current_hp = player1.max_hp
                            potion_count1 -= 1

                        elif current_turn == 2 and potion_count2 > 0:
                            player2.current_hp = player1.current_hp + (player2.max_hp/2)
                            if (player2.current_hp + (player2.max_hp/2) > player2.max_hp):
                                player2.current_hp = player2.max_hp
                            potion_count2 -= 1

                elif active_menu == 1:
                    if 820 <= mouse_x <= 1020 and 610 <= mouse_y <= 630:
                        active_menu = 0
                    elif 600 <= mouse_x <= 800 and 475 <= mouse_y <= 525 and player1.coolDown[0] == 0:
                        if random.randint(0,100) <= player1.moves[0][2]:
                            if (player1.moves[0][1] - player2.defense ) > 0:
                                    player2.current_hp -= (player1.moves[0][1] - player2.defense )

                        updateCooldowns()
                        can_defend1 =  True
                        player2.defense = player2.default_defence
                        # player1.coolDown[0] = 2
                        current_turn = 2
                        active_menu = 0

                    elif 600 <= mouse_x <= 800 and 545 <= mouse_y <= 595 and player1.coolDown[1] == 0:
                        if random.randint(0,100) <= player1.moves[1][2]:
                            if (player1.moves[1][1] - player2.defense ) > 0:
                                    player2.current_hp -= (player1.moves[1][1] - player2.defense )
                        
                        updateCooldowns()
                        can_defend1 =  True
                        player2.defense = player2.default_defence
                        # player1.coolDown[1] = 2
                        current_turn = 2
                        active_menu = 0

                    elif 820 <= mouse_x <= 1020 and 475 <= mouse_y <= 525 and player1.coolDown[2] == 0:
                        if random.randint(0,100) <= player1.moves[2][2]:
                            if (player1.moves[2][1] - player2.defense ) > 0:
                                    player2.current_hp -= (player1.moves[2][1] - player2.defense )
                        
                        updateCooldowns()
                        can_defend1 =  True
                        player2.defense = player2.default_defence
                        # player1.coolDown[2] = 2
                        current_turn = 2
                        active_menu = 0

                    elif 820 <= mouse_x <= 1020 and 545 <= mouse_y <= 595 and player1.coolDown[3] == 0:
                        if random.randint(0,100) <= player1.moves[3][2]:
                            if (player1.moves[3][1] - player2.defense ) > 0:
                                    player2.current_hp -= (player1.moves[3][1] - player2.defense )
                        
                        updateCooldowns()
                        can_defend1 =  True
                        player2.defense = player2.default_defence
                        # player1.coolDown[3] = 2
                        current_turn = 2
                        active_menu = 0
                
                elif active_menu == 2:
                    if 820 <= mouse_x <= 1020 and 610 <= mouse_y <= 630:
                        active_menu = 0
                    elif 600 <= mouse_x <= 800 and 475 <= mouse_y <= 525 and player2.coolDown[0] == 0:
                        if random.randint(0,100) <= player2.moves[0][2]:
                            if (player2.moves[0][1] - player1.defense ) > 0:
                                player1.current_hp -= (player2.moves[0][1] - player1.defense )
                        
                        updateCooldowns()
                        can_defend2 =  True
                        player1.defense = player1.default_defence
                        # player2.coolDown[0] = 2
                        current_turn = 1
                        active_menu = 0
                    elif 600 <= mouse_x <= 800 and 545 <= mouse_y <= 595 and player2.coolDown[1] == 0:
                        if random.randint(0,100) <= player2.moves[1][2]:
                            if (player2.moves[1][1] - player1.defense ) > 0:
                                player1.current_hp -= (player2.moves[1][1] - player1.defense )
                        
                        updateCooldowns()
                        can_defend2 =  True
                        player1.defense = player1.default_defence
                        # player2.coolDown[1] = 2
                        current_turn = 1
                        active_menu = 0
                    elif 820 <= mouse_x <= 1020 and 475 <= mouse_y <= 525 and player2.coolDown[2] == 0:
                        if random.randint(0,100) <= player2.moves[2][2]:
                            if (player2.moves[2][1] - player1.defense ) > 0:
                                player1.current_hp -= (player2.moves[2][1] - player1.defense )

                        updateCooldowns()
                        can_defend2 =  True
                        player1.defense = player1.default_defence
                        # player2.coolDown[2] = 2
                        current_turn = 1
                        active_menu = 0
                    elif 820 <= mouse_x <= 1020 and 545 <= mouse_y <= 595 and player2.coolDown[3] == 0:
                        if random.randint(0,100) <= player2.moves[3][2]:
                            if (player2.moves[3][1] - player1.defense ) > 0:
                                player1.current_hp -= (player2.moves[3][1] - player1.defense )

                        updateCooldowns()
                        can_defend2 =  True
                        player1.defense = player1.default_defence
                        # player2.coolDown[3] = 2
                        current_turn = 1
                        active_menu = 0
    
    if second_screen:
        screen.blit(bg1,(0,0))
        player1.draw()
        player2.draw()
        draw_options()
        fight_text = my_font2.render("Fight!",False,(255,255,255))
        screen.blit(fight_text, (game_width/2-75,25))
        drawHealthBars()
        drawStats()
        drawCooldowns()

        if player2.current_hp <= 0:
            winner = 'Player 1: ' + player1.name
            win_screen = True
            second_screen = False

        if player1.current_hp <= 0:
            winner = 'Player 2: ' + player2.name
            win_screen = True
            second_screen = False

    if first_screen:
        screen.blit(bg2,(0,0))
        drawMenu()
        set_text()
        fight_text = my_font2.render("Pokémon Battles!",False,(0,0,0))
        screen.blit(fight_text, (game_width/2-235,140))
    
    if win_screen:
        drawWinScreen(winner)

    pygame.display.flip()

    clock.tick(60)
