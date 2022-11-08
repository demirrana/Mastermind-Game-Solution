import random
import numpy as np

colors = ["Blue" , "Pink" , "Green" , "Purple" , "Yellow" , "Red" , "White" , "Black"]
color = 8

#6 renkli denemeler icin renk seti
#colors = ["Blue" , "Pink" , "Green" , "Purple" , "Yellow" , "Red"]
#color = 6

#10 renkli denemeler icin renk seti
#colors = ["Blue" , "Pink" , "Green" , "Purple" , "Yellow" , "Red" , "White" , "Black" , "Orange" , "Cyan"]
#color = 10

#Tum olasi dizilimleri D yapisina (possibilities) koyar
def create_possibilities(possibilities , color):
    i = 0
    while i < color:
        j = 0
        while j < color:
            k = 0
            while k < color:
                l = 0
                while l < color:
                    possibilities.append([colors[i] , colors[j] , colors[k] , colors[l]])
                    l = l + 1
                k = k + 1
            j = j + 1
        i = i + 1
    
#Tahmin edilmesi gereken orijinal dizilim
def create_sequence(colors):
    sequence = []
    i = 0
    while (i < 4):
        sequence.append(colors[random.randint(0 , 5)])
        i = i + 1
    return sequence

#Ilk tahmini yapar (A,A,B,B seklinde 2 renk olacak bicimde secer)
def first_prediction(prediction):
    first_color = colors[random.randint(0 , 5)]
    second_color = colors[random.randint(0 , 5)]
    while (second_color == first_color):
        second_color = colors[random.randint(0 , 5)]
    prediction.append(first_color)
    prediction.append(first_color)
    prediction.append(second_color)
    prediction.append(second_color)

#Olabilecek tum dizilimlerden birini rastgele secer
def predict(possibilities):
    prediction = possibilities[random.randint(0 , len(possibilities) - 1)]
    return prediction

#Tahminin orijinal dizilime gore gostergelerini bulur
def compute_signs(prediction , sequence , signs):
    white = 0
    red = 0

    used_index_prediction = []
    used_index_sequence = []

    i = 0
    while (i < 4):
        if (prediction[i] == sequence[i]):
            red = red + 1
            used_index_prediction.append(i)
            used_index_sequence.append(i)
        i = i + 1
    
    i = 0
    while i < 4:
        if (i in used_index_prediction):
            i = i + 1
            continue
        j = 0
        while j < 4:
            if (j in used_index_sequence):
                j = j + 1
                continue
            
            if (i == j and prediction[i] == sequence[j]):
                red = red + 1
                break
            elif (prediction[i] == sequence[j]):
                white = white + 1
                used_index_sequence.append(j)
                break
            j = j + 1
        i = i + 1
        
    signs.append(red)
    signs.append(white)
    signs.append(red + white)

#Amac testi
def prediction_accuracy(signs):
    if (signs[0] == 4):
        return True
    return False

#Her tahmin sonrasi cikan gostergelere gore tum olasiliklari iceren yapiyi guncelliyorum
def update_possibilities(prediction , signs , possibilities):
    i = 0
    while (i < len(possibilities)):
        current_signs = []
        compute_signs(possibilities[i] , prediction , current_signs)
        if (current_signs[0] != signs[0] or current_signs[1] != signs[1]): #i. seti siliyorum
            possibilities.pop(i)
        else:
            i = i + 1

#Asil oyunun oldugu fonksiyon
def game(possibilities , color_number):
    possibilities = []
    create_possibilities(possibilities , color_number)

    sequence = []
    sequence = create_sequence(colors)
    print("Sequence: " , sequence)
    print("---------------------------------------------")

    rounds = 0

    prediction = []
    first_prediction(prediction)

    signs = []
    compute_signs(prediction , sequence , signs)
    print("Prediction: " , prediction , "         " , "R:" , signs[0] , " , W:" , signs[1])
    rounds = rounds + 1

    while (prediction_accuracy(signs) != True):
        update_possibilities(prediction , signs , possibilities)
            
        prediction = predict(possibilities)
        signs = []
        compute_signs(prediction , sequence , signs)
        print("Prediction: " , prediction , "         " , "R:" , signs[0] , " , W:" , signs[1])
            
        rounds = rounds + 1

    print(rounds)
    if (rounds <= 10):
        print("Win!")
    else:
        print("Lose")

#game fonksiyonunun yalnizca round sayisini donen versiyonu. Birden fazla kez calistirmak icin bunu kullaniyorum.
def game_only_rounds(possibilities , color_number):
    all_possibilities = possibilities.copy()

    sequence = []
    sequence = create_sequence(colors)

    rounds = 0

    prediction = []
    prediction = predict(possibilities)
    #first_prediction(prediction)

    signs = []
    compute_signs(prediction , sequence , signs)
    rounds = rounds + 1

    while (prediction_accuracy(signs) != True):
        update_possibilities(prediction , signs , all_possibilities)
            
        prediction = predict(all_possibilities)
        signs = []
        compute_signs(prediction , sequence , signs)
            
        rounds = rounds + 1

    return rounds

def execute(color_number , repetition):
    total = 0
    j = 0
    possibilities = []
    create_possibilities(possibilities , color_number)
    while (j < repetition):
        total = total + game_only_rounds(possibilities , color_number)
        j = j + 1
    print(total/repetition)

#6,8 ve 10 renkli mastermind icin denemeler fakat genelde 500 ve 1000 uzun zaman aliyor
#7-9 arasindaki satirlardaki commentler kaldirilarak 6 renkli denemeler gerceklestirilebilir.
#11-13 arasindaki satirlardaki commentler kaldirilarak 10 renkli denemeler gerceklestirilebilir.
#execute(8 , 20)
#execute(8 , 50)
#execute(8 , 100)
#execute(8 , 500)
#execute(8 , 1000)

game([] , 8)