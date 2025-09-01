define minigame_font = "Better VCR 6.1.ttf"

init python:

    def time_format(t):
        m, s = t // 60, t % 60
        mm, ss = str(m), str(s)
        if s < 10: ss = '0' + ss
        if m < 10: mm = '0' + mm
        if m <  0: mm, ss = '00', '00'
        return mm + ':' + ss

transform highlight(z=0.1):
    matrixcolor BrightnessMatrix(z)

transform tint(col):
    matrixcolor TintMatrix(col)

transform text_blink(t1,t2):
    alpha 1.0
    pause t1
    alpha 0.0
    pause t2
    repeat

transform blink_rotation(a1,t1,a2,t2):
    #rotate_pad True
    rotate a1
    pause t1
    rotate a2
    pause t2
    repeat

define e = Character('Эйлин', color="#c8ffc8")


label start:

    scene black

    e "Добро пожаловать"

    jump choose_game


label choose_game:

    menu:
        e "Во что сыграем?"
        
        "3. Поиск жуков":
            call minigame3_start
        
        "Выйти":
            return


    e "Вот и все"
    jump choose_game
