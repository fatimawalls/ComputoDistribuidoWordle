# ComputoDistribuidoWordle
2p_proyecto_2oParcial
The proyect we are creating is based off a game called "wordle"
This is how the logic works:
The user is supossed to guess a 5 letter word. They are supossed to do it by filling up letters, if they are marked in yellow it means that the letter is part of the word to guess but it is not in the right order. If it turns red it means that the letter is not part of the word and if it turns green it means that the position of the letter is perfect.

The server is programmed using the C language and the client program is being developed using Python.


comando para correrlo:
gcc server_wordle.c palabras_random.c helpers_json.c -o serverW
