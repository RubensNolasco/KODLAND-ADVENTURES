import pgzrun
from pgzero.actor import Actor
from pgzero.rect import Rect

WIDTH, HEIGHT, TILE_SIZE = 800, 600, 32

state = "menu"
sound_on = True
confirm_exit = False
music_playing = False
paused = False
show_debug = False
show_game_over = False
show_win = False
show_tutorial = False


# Entities
class Hero(Actor):
    def __init__(self, image="idle_breathing (1)", pos=(100, 400)):
        super().__init__(image, pos)
        # movement
        self.frame_index = 0
        self.frame_timer = 0
        self.vel_y = 0
        self.on_ground = True
        self.direction = "right"
        # damage and health
        self.hp = 5
        self.invulnerable = False
        self.invulnerable_timer = 0.0
        self.damage_frame_index = 0
        self.damage_frame_timer = 0

    def reset(self, pos=(100, 400)):
        self.image = "idle_breathing (1)"
        self.pos = pos
        self.frame_index = 0
        self.frame_timer = 0
        self.vel_y = 0
        self.on_ground = True
        self.direction = "right"
        self.hp = 5
        self.invulnerable = False
        self.invulnerable_timer = 0.0
        self.damage_frame_index = 0
        self.damage_frame_timer = 0

    def update(self, tiles):
        # damage animation/invulnerability
        if self.invulnerable:
            self.invulnerable_timer -= 1 / 60
            self.damage_frame_timer += 1
            if self.damage_frame_timer >= 6:
                self.damage_frame_timer = 0
                self.damage_frame_index = (self.damage_frame_index + 1) % len(sprites_damage)
                set_hero_image(sprites_damage[self.damage_frame_index])
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
                self.visible = True
                self.frame_index = 0
                set_hero_image(sprites_idle[self.frame_index])

        # movement and collision
        old_x = self.x
        moved = False
        if keyboard.left:
            self.x -= VEL_ANDAR
            self.direction = "left"
            self.direcao = "left"
            moved = True
        elif keyboard.right:
            self.x += VEL_ANDAR
            self.direction = "right"
            self.direcao = "right"
            moved = True

        if moved:
            for bloco in tiles:
                if self.colliderect(bloco) and self.on_ground:
                    self.x = old_x
                    break

        self.x = max(self.width // 2, min(WIDTH - self.width // 2, self.x))

        # gravity
        self.vel_y += GRAVIDADE
        self.y += self.vel_y
        self.on_ground = False
        if self.vel_y >= 0:
            for bloco in tiles:
                if self.colliderect(bloco) and self.bottom - self.vel_y <= bloco.top + 2:
                    self.bottom = bloco.top
                    self.vel_y = 0
                    self.on_ground = True
                    break

        # jump input
        if keyboard.space and self.on_ground:
            self.vel_y = VEL_PULO

        # animations hero
        if self.on_ground and (keyboard.left or keyboard.right):
            self.frame_timer += 1
            if self.frame_timer >= 6:
                self.frame_timer = 0
                self.frame_index = (self.frame_index + 1) % len(sprites_left)
                set_hero_image(sprites_left[self.frame_index] if self.direction == "left" else sprites_right[self.frame_index])
            return

        if not self.on_ground:
            self.frame_timer += 1
            if self.frame_timer >= 6:
                self.frame_timer = 0
                self.frame_index = min(self.frame_index + 1, len(sprites_jump_right) - 1)
                set_hero_image((sprites_jump_right if self.direction == "right" else sprites_jump_left)[self.frame_index])
            return

        self.frame_timer += 1
        if self.frame_timer >= 12:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(sprites_idle)
            set_hero_image(sprites_idle[self.frame_index])


class Enemy(Actor):
    def __init__(self, image, pos, root_x):
        super().__init__(image, pos)
        self.root_x = root_x
        self.direction = "right"
        self.direcao = self.direction
        self.frame_index = 0
        self.frame_timer = 0
        self.atacando = False
        self.dying = False
        self.death_frame_index = 0
        self.death_frame_timer = 0
        self.blink_timer = 0
        self.blink_tick = 0

    def update(self, hero):
        # death 
        if self.dying:
            self.death_frame_timer += 1
            if self.death_frame_timer >= 6:
                self.death_frame_timer = 0
                self.death_frame_index += 1
                if self.death_frame_index < 8:
                    self.image = f"coisa_death ({self.death_frame_index + 1})"
                else:
                    return True
            return False

        # attacking
        if self.atacando:
            if not hero.colliderect(self):
                self.atacando = False
                self.frame_index = 0
                self.frame_timer = 0
                return False

            self.frame_timer += 1
            if self.frame_timer >= 6:
                self.frame_timer = 0
                self.frame_index = (self.frame_index + 1) % 10
                self.image = f"coisa_attacking ({self.frame_index + 1})"

            if hero.colliderect(self):
                if hero.vel_y > 0 and hero.bottom - hero.vel_y <= self.top + 5:
                    self.dying = True
                    self.death_frame_index = 0
                    self.death_frame_timer = 0
                    self.image = "coisa_death (1)"
                    hero.vel_y = VEL_PULO / 1.5
                else:
                    take_damage()
            return False

        # patrol m
        self.x += 1 if getattr(self, "direcao", self.direction) == "right" else -1
        if self.x >= self.root_x + TILE_SIZE:
            self.direcao = "left"
            self.direction = "left"
        elif self.x <= self.root_x:
            self.direcao = "right"
            self.direction = "right"

        self.frame_timer += 1
        if self.frame_timer >= 6:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % 6
            self.image = (
                f"coisa_walking_right ({self.frame_index + 1})"
                if self.direcao == "right"
                else f"coisa_walking_left ({self.frame_index + 1})"
            )

        if hero.colliderect(self):
            if hero.vel_y > 0 and hero.bottom - hero.vel_y <= self.top + 5:
                self.dying = True
                self.death_frame_index = 0
                self.death_frame_timer = 0
                self.image = "coisa_death (1)"
                hero.vel_y = VEL_PULO / 1.5
            else:
                self.atacando = True
                self.frame_index = self.frame_timer = 0
                take_damage()

        return False


# phisics
GRAVIDADE = 0.8
VEL_PULO = -12
VEL_ANDAR = 3

# player
hero = Hero()
INV_TIME = 1.5

# sprites
sprites_left = [f"left_walk ({i})" for i in range(1, 7)]
sprites_right = [f"right_walk ({i})" for i in range(1, 7)]
sprites_idle = [f"idle_breathing ({i})" for i in range(1, 5)]
sprites_jump_right = [f"jumping_animation_right ({i})" for i in range(1, 9)]
sprites_jump_left = [f"jumping_animation_left ({i})" for i in range(1, 9)]
sprites_damage = [f"taking_damage ({i})" for i in range(1, 7)]


# UI
config_button = Actor("config_button", (WIDTH - 40, 40))
btn_start = Actor("btn_start", (WIDTH // 2 - 100, HEIGHT // 2 + 175))
btn_exit_game = Actor("btn_exit_game", (WIDTH // 2 + 100, HEIGHT // 2 + 175))
btn_som_on = Actor("processed_som_on", (40, 40))
btn_som_off = Actor("processed_som_off", (40, 40))
title_logo = Actor("title_kodland", (WIDTH // 2, HEIGHT // 2 - 100))
background_menu = Actor("background_menu", (WIDTH // 2, HEIGHT // 2))
exit_game = Actor("exit_game", (WIDTH // 2, HEIGHT // 2 + 50))
return_title = Actor("return_title", (WIDTH // 2, HEIGHT // 2 - 50))
resume_exit = Actor("btn_exit", (WIDTH - 285, 185))
game_over_img = Actor("game_over", (WIDTH // 2, HEIGHT // 2 - 50))
restart_button = Actor("restart_button", (WIDTH // 2, HEIGHT // 2 + 100))
win_tela = Actor("win_tela", (WIDTH // 2, HEIGHT // 2 - 50))
hearts = [Actor("heart_life", (20 + i * 36, 40)) for i in range(5)]
tutorial_screen = Actor("tutorial_screen", (WIDTH // 2, HEIGHT // 2))
confirm_button = Actor("confirm_button", (WIDTH - 400, HEIGHT - 80))

# map
tilemap = [
    "...........................",
    "..*....*..E..*..E..*.......",
    "#####..##############......",
    "#####...#############..**..",
    ".......................##..",
    ".....*...*.E..*...*.E.*##..",
    "....##..#######..#######...",
    "...###..#######..#######...",
    "**.........................",
    "##.........................",
    "##.*..E..*...*.E.*.........",
    "###########..######........",
    "###########..######.*.....",
    "..................###......",
    "..................####.**..",
    ".......................##..",
    ".....*....*.E.......E..##..",
    "###########################",
]

solid_tiles = [
    Rect((c * TILE_SIZE, l * TILE_SIZE), (TILE_SIZE, TILE_SIZE))
    for l in range(len(tilemap))
    for c in range(len(tilemap[l]))
    if tilemap[l][c] == "#"
]

# kodcoins
coins = []
coin_count = 0
coin_anim_index = 0
coin_anim_timer = 0
COIN_FRAMES = 4

def generate_coins_from_map():
    coins.clear()
    for l, linha in enumerate(tilemap):
        for c, ch in enumerate(linha):
            if ch == "*":
                x = c * TILE_SIZE + TILE_SIZE // 2
                y = l * TILE_SIZE + TILE_SIZE // 2
                coins.append(Actor("coin_1", (x, y)))

# enemies
enemies = []

def generate_enemies_from_map():
    enemies.clear()
    for l, linha in enumerate(tilemap):
        for c, ch in enumerate(linha):
            if ch == "E":
                x = c * TILE_SIZE + TILE_SIZE // 2
                y = l * TILE_SIZE + TILE_SIZE // 2
                enemy = Enemy("coisa_walking_right (1)", (x, y), x)
                enemy.direcao = "right"
                enemy.direction = "right"
                enemy.frame_index = 0
                enemy.frame_timer = 0
                enemy.atacando = False
                enemy.dying = False
                enemy.death_frame_index = 0
                enemy.death_frame_timer = 0
                enemy.blink_timer = 0
                enemy.blink_tick = 0
                enemies.append(enemy)
                
def set_hero_image(img):
    old_bottom = hero.bottom
    hero.image = img
    hero.bottom = old_bottom

# reset game

def reset_game():
    global hero, paused, confirm_exit, coin_count, show_win
    hero = Hero()
    hero.reset((100, 400))
    paused = confirm_exit = False
    coin_count = 0
    show_win = False
    generate_coins_from_map()
    generate_enemies_from_map()

def draw():
    screen.clear()

    if state == "menu":
        screen.fill((0, 0, 30))
        title_logo.draw()
        btn_start.draw()
        btn_exit_game.draw()
        config_button.draw()

    elif state == "jogo":
        screen.blit("first_map", (0, 0))
        for coin in coins: coin.draw()
        for enemy in enemies: enemy.draw()
        hero.draw()
        config_button.draw()
        if show_debug:
            for bloco in solid_tiles:
                screen.draw.filled_rect(bloco, (100, 100, 100))

        hp = max(0, min(5, hero.hp))
        for i in range(hp):
            hearts[i].draw()

        screen.draw.text(f"Kodcoins: {coin_count}", center=(WIDTH // 2, 24), fontsize=36, color="yellow")
        if show_tutorial:
            tutorial_screen.draw()
            confirm_button.draw()
        
    if confirm_exit:
        background_menu.draw()
        exit_game.draw()
        return_title.draw()
        resume_exit.draw()
        (btn_som_on if sound_on else btn_som_off).draw()

    # game over screen
    if show_game_over:
        game_over_img.draw()
        restart_button.draw()
        return

    # win screen
    if show_win:
        win_tela.draw()
        restart_button.draw()
        return

def take_damage():
    global show_game_over, paused
    if hero.invulnerable:
        return
    hero.hp -= 1
    hero.hp = max(0, hero.hp)
    hero.invulnerable = True
    hero.invulnerable_timer = INV_TIME
    hero.damage_frame_index = 0
    hero.damage_frame_timer = 0
    set_hero_image(sprites_damage[hero.damage_frame_index])
    if hero.hp <= 0:
        show_game_over = True
        paused = True

generate_coins_from_map()
generate_enemies_from_map()

def update():
    global coin_anim_timer, coin_anim_index, coin_count
    global show_win, paused

    if paused:
        return
    if hero.invulnerable:
        hero.invulnerable_timer -= 1 / 60
        hero.damage_frame_timer += 1
        if hero.damage_frame_timer >= 6:
            hero.damage_frame_timer = 0
            hero.damage_frame_index = (hero.damage_frame_index + 1) % len(sprites_damage)
            set_hero_image(sprites_damage[hero.damage_frame_index])
        if hero.invulnerable_timer <= 0:
            hero.invulnerable = False
            hero.visible = True
            hero.frame_index = 0
            set_hero_image(sprites_idle[hero.frame_index])
            
    hero.update(solid_tiles)

    coin_anim_timer += 1
    if coin_anim_timer >= 8:
        coin_anim_timer = 0
        coin_anim_index = (coin_anim_index + 1) % COIN_FRAMES
        for coin in coins:
            coin.image = f"coin_{coin_anim_index + 1}"

    for coin in coins[:]:
        if hero.colliderect(coin):
            coins.remove(coin)
            coin_count += 1
            if sound_on and hasattr(sounds, "coin_sound"):
                sounds.coin_sound.play()

    # victory condition
    if coin_count >= 22 and not show_win:
        show_win = True
        paused = True

    for e in enemies[:]:
        remove = e.update(hero)
        if remove:
            if e in enemies:
                enemies.remove(e)

def on_key_down(key):
    global frame_index, frame_timer, confirm_exit, paused, show_debug

    if key == keys.ESCAPE:
        confirm_exit = not confirm_exit
        paused = confirm_exit
        if sound_on and hasattr(sounds, "click"):
            sounds.click.play()
        return

    if key == keys.F3:
        show_debug = not show_debug
        return

def on_mouse_down(pos):
    global state, sound_on, confirm_exit, paused, show_game_over, music_playing, show_win, show_tutorial

    if show_win and restart_button.collidepoint(pos):
        if sound_on and hasattr(sounds, "click"):
            sounds.click.play()
        show_win = False
        paused = False
        reset_game()
        return

    if show_game_over and restart_button.collidepoint(pos):
        if sound_on and hasattr(sounds, "click"):
            sounds.click.play()
        show_game_over = False
        paused = False
        reset_game()
        return

    if state == "menu" and btn_start.collidepoint(pos):
        if sound_on and hasattr(sounds, "click"):
            sounds.click.play()
        state = "jogo"
        reset_game()
        # tutorial overlay
        paused = True
        show_tutorial = True
        if sound_on and not music_playing and hasattr(sounds, "music_background"):
            sounds.music_background.play(-1)
            music_playing = True
        return
    
    if state == "jogo" and show_tutorial and confirm_button.collidepoint(pos):
        if sound_on and hasattr(sounds, "click"):
            sounds.click.play()
        show_tutorial = False
        paused = False
        return

    if state == "menu" and btn_exit_game.collidepoint(pos):
        if sound_on and hasattr(sounds, "click"):
            sounds.click.play()
        if hasattr(sounds, "music_background"):
            sounds.music_background.stop()
        import sys
        sys.exit()

    if config_button.collidepoint(pos):
        if sound_on and hasattr(sounds, "click"):
            sounds.click.play()
        confirm_exit = True
        paused = True
        return
    
    if confirm_exit:
        if resume_exit.collidepoint(pos):
            if sound_on and hasattr(sounds, "click"):
                sounds.click.play()
            confirm_exit = False
            paused = False
            return

        if exit_game.collidepoint(pos):
            if sound_on and hasattr(sounds, "click"):
                sounds.click.play()
            if hasattr(sounds, "music_background"):
                sounds.music_background.stop()
            import sys
            sys.exit()

        if return_title.collidepoint(pos):
            if sound_on and hasattr(sounds, "click"):
                sounds.click.play()
            state = "menu"
            confirm_exit = False
            paused = False
            reset_game()
            return

        if sound_on and btn_som_on.collidepoint(pos):
            if sound_on and hasattr(sounds, "click"):
                sounds.click.play()
            sound_on = False
            if hasattr(sounds, "music_background"):
                sounds.music_background.stop()
            music_playing = False
            return
        elif not sound_on and btn_som_off.collidepoint(pos):
            if hasattr(sounds, "click"):
                sounds.click.play()
            sound_on = True
            if not music_playing and hasattr(sounds, "music_background"):
                sounds.music_background.play(-1)
                music_playing = True
            return

if sound_on and not music_playing and hasattr(sounds, "music_background"):
    sounds.music_background.stop()
    music_playing = False

pgzrun.go()
