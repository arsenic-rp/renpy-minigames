define config.mouse = {}
define config.mouse['empty'] = [ ( 'images/minigame3/empty_cursor.png', 0,0 ) ]

################################################################################################################################

init python:
    import random
    
    class ThirdMinigame:
    
        background = 'bg_grass'
        bugs = ['bug{}'.format(x) for x in range(1,8)]
        
        # чтобы изображения не накладывались друг надруга, разбиваем поле на ячейки
        grid_x = 20
        grid_y = 20
        
        def __init__(self):
            self.count = 0
            self.score = 0

        def get_data(self): # список элементов (index, img, x, y); считаем, что первый в списке - цель
            num_bugs = 6 + self.count * 2
            targetid = self.count % len(self.bugs)
            
            target = self.bugs[targetid]
            extras = self.bugs[:targetid] + self.bugs[targetid+1:]
            
            bugs_images = [target] + [random.choice(extras) for _ in range(num_bugs-1)] # список изображений
            bugs_sectors = random.sample(range(self.grid_x * self.grid_y), num_bugs) # список уникальных ячеек
            
            # преобразуем в координаты от 0 до 1
            bugs_xs = [ (index  % self.grid_x + random.uniform(-0.5,0.5)) / self.grid_x * 0.9 + 0.05 for index in bugs_sectors]
            bugs_ys = [ (index // self.grid_x + random.uniform(-0.5,0.5)) / self.grid_y * 0.9 + 0.05 for index in bugs_sectors]
            
            return list( zip(range(num_bugs), bugs_images, bugs_xs, bugs_ys) )

        def next(self):
            self.count += 1
        
        def add_score(self, x=0):
            self.score += x * 100
        
        def set_score(self, x):
            self.score = x

        def on_start(self):
            renpy.store.quick_menu = False
            # renpy.music.set_volume(1.0, channel="music")
            # renpy.music.play(audio.minigame3, channel="music", fadein=1.0, fadeout=1.0)
   
        def on_finish(self):
            renpy.store.quick_menu = True
            # renpy.music.set_volume(1.0, channel="music")
            # renpy.music.stop(channel="music", fadeout=3.0)

################################################################################################################################

screen third_minigame_main(minigame=None, exit_action=NullAction()):
    default remaining_time = 120
    
    # key "game_menu" action None
    
    button: # скрываем курсор
        xsize 1.0
        ysize 1.0
        mouse "empty"
        action NullAction()
    
    timer 1.0:
        action SetLocalVariable('remaining_time', remaining_time-1)
        repeat True
    
    if minigame is not None:
        hbox:
            anchor (0.0, 0.5)
            pos (0.7, 0.06)
            text "Очки:":
                size 48
                color "#fff"
                font minigame_font
            text str(minigame.score):
                size 48
                color "#fff"
                font minigame_font
            
    text time_format(remaining_time):
        size 64
        font minigame_font
        bold True
        anchor (0.5, 0.5)
        pos (0.5, 0.06)
        if remaining_time < 30:
            at text_blink(0.5,0.5)
            
    if remaining_time < 0:
        timer 0.1:
            action exit_action
            repeat False
            
################################################################################################################################

screen third_minigame_search(minigame):
    default alpha_mask = Tracer("lens_alpha", anchor=(0.65,0.35), init_xy=(800,600))
    default lens = Tracer("lens", anchor=(0.65,0.35), init_xy=(800,600))
    default bugs_data = minigame.get_data()
    default target = bugs_data[0][1]

    default found_bugs = set() # на случай, если есть >1 возможной цели
    default hovered_bug = None
    
    frame:
        
        background None
        xsize 1.0
        ysize 1.0
        padding (0,0)
        align (0.5,0.5)
        at transform:
            zoom 0.75
        
        fixed: # обычный вид
            for (index,img,x,y) in bugs_data:
                button:
                    mouse "empty"
                    action [SetLocalVariable('found_bugs', found_bugs | {img})]
                    hovered [SetLocalVariable('hovered_bug', index)] # + [SetLocalVariable('found_bugs', found_bugs | {img})] -- если хотим активировать при наведении
                    unhovered SetLocalVariable('hovered_bug', None)
                    xsize 40
                    ysize 40
                    padding (0,0)
                    
                    add img:
                        align (0.5, 0.5)
                        zoom 0.1
                        at transform:
                            matrixcolor BrightnessMatrix(-1.0)
                    
                    pos (x,y)
                    anchor (0.5, 0.5)

        fixed: # вид через линзу
            at zoomtrace(4.0, (0,0), init_xy=(lens.x, lens.y)), apply_mask(alpha_mask)
            add 'bg_grass'

            for (index, img,x,y) in bugs_data:
                add img:
                    pos (x,y)
                    anchor (0.5, 0.5)
                    zoom 0.1
                    if hovered_bug == index:
                        at transform:
                            matrixcolor BrightnessMatrix(0.2) zoom 1.2
        
        add lens
    
    if target not in found_bugs:
        text "НАЙДИ ЭТОГО ЖУКА":
            size 64
            bold True
            font minigame_font
            color "#fff"
            anchor (0.5, 0.5)
            pos (0.5, 0.94)
            at text_blink(1.0,1.0)
        for xx in (0.26,1-0.26):
            add target:
                zoom 0.25
                anchor (0.5, 0.5)
                pos (xx, 0.925)
                at blink_rotation(-10,1.0,10,1.0)
    else:
        text "ЖУК НАЙДЕН":
            size 64
            bold True
            font minigame_font
            color "#0f0"
            anchor (0.5, 0.5)
            pos (0.5, 0.94)
        timer 0.1 repeat False action Function(minigame.add_score, 1)
        timer 1.0 repeat False action Return(target)

        
################################################################################################################################

label minigame3_start:

    $ minigame3 = ThirdMinigame()
    $ minigame3.on_start()
    
    show bg_grass:
        align (0.5, 0.5)
        zoom 0.75

    show screen third_minigame_main(minigame3, exit_action=Jump('minigame3_finish'))
    window hide

    label .cycle:
        call screen third_minigame_search(minigame3)
        # play sound audio.task_done
        show expression _return as bug:
            align (0.5,0.5)
            zoom 2.0
        with {'master' : Dissolve(0.5)}
        $ renpy.pause(1.0, hard=True)
        hide bug
        with {'master' : Dissolve(0.5)}
        $ minigame3.next()
        if minigame3.count < 10: # ограничение на количество раундов
            jump .cycle

label minigame3_finish:

    hide bg_grass
    hide screen third_minigame_main
    hide screen third_minigame_search
    with {'master' : Dissolve(0.5)}
    $ renpy.pause(0.5, hard=True)
    
    window auto
    "Вы поймали [minigame3.count] жуков!"
    
    $ minigame3.on_finish()
    $ del minigame3
    
    return