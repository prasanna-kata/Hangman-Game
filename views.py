from django.shortcuts import render, redirect
import random

words = ['python', 'django', 'hangman', 'code', 'programming']

def home(request):
    request.session.flush()  
    return render(request, 'hangman/home.html')

def play(request):
    if 'word' not in request.session:
        request.session['word'] = random.choice(words)
        request.session['guessed_letters'] = []
        request.session['attempts'] = 6
    
    game_over = request.session.get('game_over', False)  # Defaults to False
    win = request.session.get('win', False) 
    if request.method == 'POST' and not game_over:
        letter = request.POST.get('letter').lower()
        if letter and letter not in request.session['guessed_letters']:
            request.session['guessed_letters'].append(letter)
            if letter not in request.session['word']:
                request.session['attempts'] -= 1

        request.session.modified = True

        if all(letter in request.session['guessed_letters'] for letter in request.session['word']):
            request.session['win'] = True
            request.session['game_over'] = True

        if request.session['attempts'] <= 0:
            request.session['game_over'] = True

    display_word =''.join([letter if letter in request.session['guessed_letters'] else '_' for letter in request.session['word']])   
    
    context = {
        'word': request.session['word'],
        'guessed_letters': request.session['guessed_letters'],
        'attempts': request.session['attempts'],
        'display_word': display_word,
        'game_over': request.session.get('game_over', False),
        'win': request.session.get('win', False)
    }

    return render(request, 'hangman/play.html', context)
