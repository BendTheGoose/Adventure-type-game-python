import pygame
import random
import math

SZEL = 800
MAG = 600
MERET = 40
FPS = 30

FEKETE = (0, 0, 0)
FEHER = (255, 255, 255)
PIROS = (200, 0, 0)
SARGA = (255, 255, 0)
LILA = (150, 0, 255)

pygame.init()
ablak = pygame.display.set_mode((SZEL, MAG))
pygame.display.set_caption("Adventure type 1.1")
ora = pygame.time.Clock()

betu = pygame.font.SysFont(None, 36)
kicsi_betu = pygame.font.SysFont(None, 24)
halal_betu = pygame.font.SysFont(None, 120) 

def vilag_krealas(szint, max_erme):
    vilag = {}
    
    for rx in range(3):
        for ry in range(3):
            falak = []
            
            for x in range(MERET, SZEL - MERET, MERET):
                for y in range(MERET, MAG - MERET, MERET):
                    if rx == 1 and ry == 1 and (SZEL//2 - 80 < x < SZEL//2 + 80) and (MAG//2 - 80 < y < MAG//2 + 80):
                        continue
                        
                    if random.random() < 0.12:
                        falak.append(pygame.Rect(x, y, MERET, MERET))
                        
            vilag[(rx, ry)] = {'falak': falak, 'ermek': [], 'botok': []}

    ermek_lerakva = 0
    while ermek_lerakva < max_erme:
        rx = random.randint(0, 2)
        ry = random.randint(0, 2)
        
        x = random.randint(MERET, SZEL - MERET - 10)
        y = random.randint(MERET, MAG - MERET - 10)
        rect = pygame.Rect(x, y, 10, 10)
        
        utkozik = False
        for f in vilag[(rx, ry)]['falak']:
            if rect.colliderect(f):
                utkozik = True
                break
                
        if not utkozik:
            vilag[(rx, ry)]['ermek'].append(rect)
            ermek_lerakva += 1

    bot_szam = szint * 2
    botok_lerakva = 0
    while botok_lerakva < bot_szam:
        rx = random.randint(0, 2)
        ry = random.randint(0, 2)
        
        if rx == 1 and ry == 1:
            continue
            
        x = random.randint(MERET, SZEL - MERET - 20)
        y = random.randint(MERET, MAG - MERET - 20)

        bot_rect = pygame.Rect(x, y, 20, 20)
        vilag[(rx, ry)]['botok'].append(bot_rect)
        botok_lerakva += 1

    return vilag


def main():
    szint = 1
    max_erme = 50
    score = 0
    
    szoba_x, szoba_y = 1, 1
    jatekos = pygame.Rect(SZEL//2, MAG//2 + 50, 20, 20)
    vilag = vilag_krealas(szint, max_erme)
    finish_rect = pygame.Rect(SZEL//2 - 25, MAG//2 - 25, 50, 50)
    
    fut = True
    halott = False 

    while fut:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fut = False

        gombok = pygame.key.get_pressed()

        if halott:
            if gombok[pygame.K_SPACE]:
                vilag = vilag_krealas(szint, max_erme)
                score = 0
                szoba_x, szoba_y = 1, 1
                jatekos.center = (SZEL//2, MAG//2 + 50)
                halott = False
        
        else:
            dx, dy = 0, 0
            sebesseg = 6
            
            if gombok[pygame.K_LEFT] or gombok[pygame.K_a]: dx = -sebesseg
            if gombok[pygame.K_RIGHT] or gombok[pygame.K_d]: dx = sebesseg
            if gombok[pygame.K_UP] or gombok[pygame.K_w]: dy = -sebesseg
            if gombok[pygame.K_DOWN] or gombok[pygame.K_s]: dy = sebesseg

            aktualis_szoba = vilag[(szoba_x, szoba_y)]
            falak = aktualis_szoba['falak']
            
            jatekos.x += dx
            for f in falak:
                if jatekos.colliderect(f):
                    if dx > 0: jatekos.right = f.left
                    if dx < 0: jatekos.left = f.right

            jatekos.y += dy
            for f in falak:
                if jatekos.colliderect(f):
                    if dy > 0: jatekos.bottom = f.top
                    if dy < 0: jatekos.top = f.bottom

            if jatekos.left < 0:
                if szoba_x > 0:
                    szoba_x -= 1
                    jatekos.right = SZEL - 5
                else: jatekos.left = 0
            elif jatekos.right > SZEL:
                if szoba_x < 2:
                    szoba_x += 1
                    jatekos.left = 5
                else: jatekos.right = SZEL
            if jatekos.top < 0:
                if szoba_y > 0:
                    szoba_y -= 1
                    jatekos.bottom = MAG - 5
                else: jatekos.top = 0
            elif jatekos.bottom > MAG:
                if szoba_y < 2:
                    szoba_y += 1
                    jatekos.top = 5
                else: jatekos.bottom = MAG

            ermek = aktualis_szoba['ermek']
            for p in ermek[:]:
                if jatekos.colliderect(p):
                    ermek.remove(p)
                    score += 1

            bot_sebesseg = 2 + (szint * 0.5)
            for bot in aktualis_szoba['botok']:
                if bot.x < jatekos.x: bot.x += bot_sebesseg
                if bot.x > jatekos.x: bot.x -= bot_sebesseg
                if bot.y < jatekos.y: bot.y += bot_sebesseg
                if bot.y > jatekos.y: bot.y -= bot_sebesseg
                
                if jatekos.colliderect(bot):
                    halott = True

            if szoba_x == 1 and szoba_y == 1:
                if jatekos.colliderect(finish_rect) and score >= max_erme:
                    szint += 1
                    max_erme += 10
                    score = 0
                    szoba_x, szoba_y = 1, 1
                    jatekos.center = (SZEL//2, MAG//2 + 50)
                    vilag = vilag_krealas(szint, max_erme)

        ablak.fill(FEKETE)
        
        if not halott:
            for f in vilag[(szoba_x, szoba_y)]['falak']: pygame.draw.rect(ablak, PIROS, f)
            for p in vilag[(szoba_x, szoba_y)]['ermek']: pygame.draw.circle(ablak, SARGA, p.center, 5)
            for bot in vilag[(szoba_x, szoba_y)]['botok']: pygame.draw.rect(ablak, LILA, bot)

            if szoba_x == 1 and szoba_y == 1:
                ido = pygame.time.get_ticks()
                r = int((math.sin(ido * 0.005) + 1) * 127)
                g = int((math.sin(ido * 0.003) + 1) * 127)
                b = int((math.sin(ido * 0.007) + 1) * 127)
                pygame.draw.rect(ablak, (r, g, b), finish_rect)
                finish_szoveg = kicsi_betu.render("FINISH", True, FEHER)
                ablak.blit(finish_szoveg, (finish_rect.x, finish_rect.y - 20))

            pygame.draw.rect(ablak, FEHER, jatekos)

            szint_szoveg = betu.render(f"Level {szint}", True, FEHER)
            pont_szoveg = betu.render(f"Points: {score} / {max_erme}", True, SARGA)
            terkep_szoveg = kicsi_betu.render(f"Room: ({szoba_x}, {szoba_y})", True, (150, 150, 150))
            
            ablak.blit(szint_szoveg, (10, 10))
            ablak.blit(pont_szoveg, (10, 40))
            ablak.blit(terkep_szoveg, (SZEL - 120, 10))

        else:
            halal_szoveg = halal_betu.render("YOU DIED", True, PIROS)
            info_szoveg = betu.render("Press space to continue", True, FEHER)
            
            ablak.blit(halal_szoveg, (SZEL//2 - halal_szoveg.get_width()//2, MAG//2 - 50))
            ablak.blit(info_szoveg, (SZEL//2 - info_szoveg.get_width()//2, MAG//2 + 50))

        pygame.display.flip()
        ora.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()