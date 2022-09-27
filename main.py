import pygame
import random

pygame.init()

GAME_WIDHT = 288
GAME_HEIGHT = 512

screen = pygame.display.set_mode((GAME_WIDHT, GAME_HEIGHT))
clock = pygame.time.Clock()

BG_LIST = []
BG_LIST.append('assets/sprites/background-day.png')
BG_LIST.append('assets/sprites/background-night.png')

PLR_LIST = [
    [
        'assets/sprites/yellowbird-upflap.png',
        'assets/sprites/yellowbird-midflap.png',
        'assets/sprites/yellowbird-downflap.png'
    ],
    [
        'assets/sprites/redbird-upflap.png',
        'assets/sprites/redbird-midflap.png',
        'assets/sprites/redbird-downflap.png'
    ],
    [
        'assets/sprites/bluebird-upflap.png',
        'assets/sprites/bluebird-midflap.png',
        'assets/sprites/bluebird-downflap.png'
    ],
]

PIPES_LIST = [
    'assets/sprites/pipe-green.png',
    'assets/sprites/pipe-red.png'
]

IMAGE = {}
HITMASK = {}
SOUND = {}

def getRandomPipe():
    pipeH = IMAGE['pipe'][0].get_height()
    Y = random.randint(0, 150) + 80
    X = GAME_WIDHT - 10

    return [
        {'x': X, 'y': Y - pipeH},
        {'x': X, 'y': Y + 100}
    ]


def getHitMask(image):
    mask = []
    for x in range(image.get_width()):
        mask.append([])
        for y in range(image.get_height()):
            # print(bool(image.get_at((x, y))[3]))
            mask[x].append(bool(image.get_at((x, y))[3]))
    return mask


def checkCrash(plr, uPipes, lPipes):
    global screen
    # распаковка игрока
    plr['w'] = IMAGE['player'][0].get_width()
    plr['h'] = IMAGE['player'][0].get_height()

    # столкновение с землей
    if plr['y'] + plr['h'] >= int(GAME_HEIGHT * 0.8):
        return [True, True]
    else:
        # столновение с трубами
        plrRect = pygame.Rect(plr['x'], plr['y'], plr['w'], plr['h'])

        # параметры труб
        pipeW = IMAGE['pipe'][0].get_width()
        pipeH = IMAGE['pipe'][0].get_height()

        for upipe, lpipe in zip(uPipes, lPipes):
            uPipeRect = pygame.Rect(upipe['x'], upipe['y'], pipeW, pipeH)
            lPipeRect = pygame.Rect(lpipe['x'], lpipe['y'], pipeW, pipeH)

            plrHM = HITMASK['plr'][0]
            uHM = HITMASK['pipe'][0]
            lHM = HITMASK['pipe'][1]

            # проверяем столкновение
            uColl = pixCollide(plrRect, uPipeRect, plrHM, uHM)
            lColl = pixCollide(plrRect, lPipeRect, plrHM, lHM)

            if uColl or lColl:
                return [True, False]

            # pygame.draw.rect(screen, (0, 255, 255), plrRect, 6)
            # pygame.draw.rect(screen, (0, 255, 255), uPipeRect, 6)
            # pygame.draw.rect(screen, (0, 255, 255), lPipeRect, 6)
            #
            # pygame.display.update()

    return [False, False]


def pixCollide(rect1, rect2, h1, h2):
    rect = rect1.clip(rect2)
    if rect.width == 0 or rect.height == 0:
        return False

    x1 = rect.x - rect1.x
    y1 = rect.y - rect1.y
    x2 = rect.x - rect2.x
    y2 = rect.y - rect2.y

    for x in range(int(rect.width)):
        for y in range(int(rect.height)):
            if h1[x1 + x][y1 + y] and h2[x2 + x][y2 + y]:
                return True

    return False

def showWellcom():
    msgX = GAME_WIDHT * 0.2
    msgY = GAME_HEIGHT * 0.2

    baseX = 0
    baseY = int(GAME_HEIGHT * 0.8)

    plrX = int(GAME_WIDHT * 0.2)
    plrY = int(GAME_HEIGHT * 0.55)
    plrY2 = 0
    plrDir = 1
    plrIndx = 0

    loop = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE):
                return {
                    'plrY': plrY + plrY2,
                    'baseX': baseX,
                    'plrIndx': plrIndx
                }

        # перемещение птицы
        if plrDir == 1:
            plrY2 += 1
            if plrY2 == 8:
                plrDir = 0

        if plrDir == 0:
            plrY2 -= 1
            if plrY2 == -8:
                plrDir = 1

        # крылья анимация
        loop += 1
        if loop % 6 == 0:
            if plrIndx != 2:
                plrIndx += 1
            else:
                plrIndx = 0

        # анимация земли
        baseX -= 4
        if baseX == -48:
            baseX = 0

        screen.blit(IMAGE['bg'], (0, 0))
        screen.blit(IMAGE['message'], (msgX, msgY))
        screen.blit(IMAGE['base'], (baseX, baseY))
        screen.blit(IMAGE['player'][plrIndx], (plrX, plrY + plrY2))

        pygame.display.update()
        clock.tick(20)


def main():
    global screen, clock
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((GAME_WIDHT, GAME_HEIGHT))
    pygame.display.set_caption('my game')

    SOUND['die'] = pygame.mixer.Sound('assets/audio/die.wav').set_volume(0.2)
    SOUND['hit'] = pygame.mixer.Sound('assets/audio/hit.wav').set_volume(0.2)
    SOUND['point'] = pygame.mixer.Sound('assets/audio/point.wav').set_volume(0.2)
    SOUND['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh.wav').set_volume(0.2)
    SOUND['wing'] = pygame.mixer.Sound('assets/audio/wing.wav').set_volume(0.2)

    IMAGE['numbs'] = [
        pygame.image.load('assets/sprites/0.png').convert_alpha(),
        pygame.image.load('assets/sprites/1.png').convert_alpha(),
        pygame.image.load('assets/sprites/2.png').convert_alpha(),
        pygame.image.load('assets/sprites/3.png').convert_alpha(),
        pygame.image.load('assets/sprites/4.png').convert_alpha(),
        pygame.image.load('assets/sprites/5.png').convert_alpha(),
        pygame.image.load('assets/sprites/6.png').convert_alpha(),
        pygame.image.load('assets/sprites/7.png').convert_alpha(),
        pygame.image.load('assets/sprites/8.png').convert_alpha(),
        pygame.image.load('assets/sprites/9.png').convert_alpha()
    ]
    while True:
        randBg = random.randint(0, 1)

        # задний фон
        IMAGE['bg'] = pygame.image.load(BG_LIST[randBg]).convert()

        # земля
        IMAGE['base'] = pygame.image.load('assets/sprites/base.png').convert_alpha()

        # главный экран
        IMAGE['message'] = pygame.image.load('assets/sprites/message.png').convert_alpha()

        randPlr = random.randint(0, 2)

        # птичка
        IMAGE['player'] = (
            pygame.image.load(PLR_LIST[randPlr][0]).convert_alpha(),
            pygame.image.load(PLR_LIST[randPlr][1]).convert_alpha(),
            pygame.image.load(PLR_LIST[randPlr][2]).convert_alpha()
        )

        # рандомные трубы
        randPipe = random.randint(0, 1)
        IMAGE['pipe'] = (
            pygame.transform.flip(pygame.image.load(PIPES_LIST[randPipe]).convert_alpha(), False, True),
            pygame.image.load(PIPES_LIST[randPipe]).convert_alpha()
        )

        # hitbox птицы
        HITMASK['plr'] = (
            getHitMask(IMAGE['player'][0]),
            getHitMask(IMAGE['player'][1]),
            getHitMask(IMAGE['player'][2])
        )

        # hitbox Pipes
        HITMASK['pipe'] = (
            getHitMask(IMAGE['pipe'][0]),
            getHitMask(IMAGE['pipe'][1]),
        )

        playMoment = showWellcom()
        gameMain(playMoment)


def showScore(score):
    scores = []
    for x in str(score):
        scores.append(int(x))

    totalW =0
    for n in scores:
        totalW = totalW + IMAGE['numbs'][n].get_width()

    X = (GAME_WIDHT - totalW) / 2

    for n in scores:
        screen.blit(IMAGE['numbs'][n], (X, 50))
        X = X + IMAGE['numbs'][n].get_width()
def gameMain(playMoment):
    getHitMask(IMAGE['player'][0])

    # игрок
    plrY, plrX = playMoment['plrY'], GAME_WIDHT * 0.2
    plrIndx = playMoment['plrIndx']
    plrVelY = -6  # скорость по Y
    plrMaxVelY = 6
    plrFlapp = False  # True - взлет
    plrRot = 45  # угол поворта

    # земля
    baseX = playMoment['baseX']
    baseY = int(GAME_HEIGHT * 0.8)

    pipe1 = getRandomPipe()
    pipe2 = getRandomPipe()

    upperPipes = [
        {'x': pipe1[0]['x'], 'y': pipe1[0]['y']},
        {'x': pipe2[0]['x'] + 144, 'y': pipe2[0]['y']}
    ]

    lowerPipes = [
        {'x': pipe1[1]['x'], 'y': pipe1[1]['y']},
        {'x': pipe2[1]['x'] + 144, 'y': pipe2[1]['y']}
    ]

    loop = 0
    pipeVelX = -4

    score = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                SOUND['wing'].play()
                if plrY > IMAGE['player'][0].get_height() * -2:
                    plrVelY = -9
                    plrFlapp = True
                    SOUND['wing'].play()


        #счет
        plrCenter = plrX + IMAGE['player'][0].get_width() / 2
        for pipe in upperPipes:
            pipeCenter = pipe['x'] + IMAGE['pipe'][0].get_width() / 2
            if pipeCenter <= plrCenter < pipeCenter + 4:
                score += 1
                SOUND['point'].play()

        print(score)
        # крылья анимация
        loop += 1
        if loop % 6 == 0:
            if plrIndx != 2:
                plrIndx += 1
            else:
                plrIndx = 0

        if plrVelY < plrMaxVelY and not plrFlapp:
            plrVelY += 1

        # взмах-падение
        if plrFlapp:
            plrFlapp = False
            plrRot = 45

        plrH = IMAGE['player'][0].get_height()
        plrY += min(plrVelY, baseY - plrY - plrH)

        # анимация земли
        baseX -= 4
        if baseX == -48:
            baseX = 0

        if plrRot >= -45:
            plrRot -= 3


        # движение труб
        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            uPipe['x'] += pipeVelX
            lPipe['x'] += pipeVelX

        # удаляем трубы за экраном
        if len(upperPipes) > 0 and upperPipes[0]['x'] < -52:
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # спаун труб
        if 3 > len(upperPipes) > 0 and 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        crashInfo = checkCrash({'x': plrX, 'y': plrY}, upperPipes, lowerPipes)
        if crashInfo[0]:
            return {
                'y': plrY,
                'groundCrash': crashInfo[1],
                'baseX': baseX,
                'uPipes': upperPipes,
                'lPipes': lowerPipes,
                'plrVelY': plrVelY,
                'plrRot': plrRot
        }

        plrSurface = pygame.transform.rotate(IMAGE['player'][plrIndx], plrRot)

        screen.blit(IMAGE['bg'], (0, 0))

        screen.blit(plrSurface, (plrX, plrY))

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            screen.blit(IMAGE['pipe'][0], (uPipe['x'], uPipe['y']))
            screen.blit(IMAGE['pipe'][1], (lPipe['x'], lPipe['y']))

        screen.blit(IMAGE['base'], (baseX, baseY))
        showScore(score)
        pygame.display.update()
        clock.tick(40)


if __name__ == '__main__':
    main()
