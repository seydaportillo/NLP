print("*****************************************\nThis is a game where you will guess which word the computer thinks of. Every time you make a guess you will recieve a similarity-score, that tells you how similar the meaning of your guess is to the correct word: this score goes from -100 to 100. \n\n- If you want a hint you write HINT with capital letters in the guess-space. There is only one hint per word. \n- If you want to see any of the most similar words to the one you are trying to guess, you write which number in the sequence you're looking for. For example, if you write 2 you get to see the second most similar word, 300 gives you the 300th most similar word and so on. \n- If you want to give up you write GIVE UP with capital letters in the guess-space.\n\n*****************************************")
print("\nThe game is loading. The guess-space will show up when it is ready.")      # printing the game instructions. They come first so that the user can read them while everything loads. 

# importing libraries
import random 
import gensim
from nltk.corpus import wordnet

dsm_file = 'cc.en.300.vec.gz'                                                       # assigning the file cc.en.300.vec.gz to the variable "dsm_file" 
model = gensim.models.KeyedVectors.load_word2vec_format(dsm_file, limit = 50000)    # loading the distributional semantics model, limiting it to 50000 words

def ordinals(x):                                                                            # a function called "ordinals", that takes one argument (a string with a number). This function will return the correct suffix for the specific number to make it into an ordinal number.
    if len(x) >= 2 and x[-2] == "1" and (x[-1] == "1" or x[-1] == "2" or x[-1] == "3"):     # first we make sure 11, 12 and 13 (as well as 111, 112, 211, 213, etc) get the suffix "th", since they are exceptions to the rule
        n = "th"
    elif (int(x)%10) == 1:
        n = "st"                    # if the number ends with a 1 the ordinal suffix is "st"
    elif (int(x)%10) == 2:
        n = "nd"                    # if the number ends with a 2 the ordinal suffix is "nd"
    elif (int(x)%10) == 3:
        n = "rd"                    # if the number ends with a 3 the ordinal suffix is "rd"
    else:
        n = "th"                    # otherwise the ordinal suffix is "th"
    return n                        # the function returns the correct ordinal suffix

def closest(z, y):                                              # a function called "closest", that is used when your guess is close to the correct word. This function takes two arguments, the guess and the list of the correct word's 500 closest neighbours.  
    index = y.index(z)                                          # the position of the guess in the list of the correct word's closest neighbours is assigned to "index"
    if index == 0:                                              # if the index is 0, it means that the guess is the closest neighbour in the list...
        print(f'"{z}" is the closest word! Almost there!')      # ...and we print a statement letting the user know this. This statement is separate from the rest below since we don't say "the 1st closest word", but just "the closest word"
    else:                                                       # if the guess is not the closest neighbour...
        x = index + 1                                           # we add one to the index and assign this value to "x" (since the positions in the list is one less than when counting "3rd closest word, 5th closest word, etc")
        x = str(x)                                              # x is made into a string, since the function "ordinals" only takes strings
        print(f'"{z}" is the {x}{ordinals(x)} closest word!')   # the number x goes into the function ordinals, and we print a statement letting the user know how close their guess is to the correct word.

def number_hint(x, y):                                                              # a function called "number_hint" that is used when the user wants to know which word is at a chosen distance from the correct one. Number_hint takes two arguments: the number chosen by the user, and the list of closest neighbours to the correct word.
    if int(x) > len(y):                                                             # if the number the user chose is bigger than the number of items in the neighbour-list...
        print("This number is too high. Write a number between 1 and", len(y))      #... we let the user know to choose a smaller number
    elif int(x) == 1:                                                               # if the number that the user chose is 1...
        print((f'The closest word is "{y[int(x)-1]}"'))                             # we give them the closest word from the list of neighbours. The position of the item in the list is [x-1] since the (number 1) closest word has position 0, and so on for all the numbers.
    else:                                                                           # if the chosen number is not too big or 1...
        print(f'The {x}{ordinals(x)} closest word is "{y[int(x)-1]}"')              # we print a statement letting them know what the x:th closest word is. We use the function "ordinals" to get the correct ordinal suffix for the number.

def again():                                                        # a function called "again" that is used when we ask the user if they want to play again.
    again = input("\nPress enter if you wanna play again\n")        # we print instructions on how to play again
    if again == "":                                                 # if the user presses enter...
        print("Let's play again!")                  
        whole_game()                                                # the game starts over by executing the "whole_game" function
    else:                                           
        print("See you next time!")

def guessing(x, y):                                             # a function called "guessing" which is where the biggest part of the game takes place. It takes two arguments, the correct word and the list of closest neighbours to that word.
    guess = input("\nWrite your guess here: ")                  # the "guess-space" is created, where the user writes their guesses or other instructions (requests for the hint or number-hints, demand to give up)
    if guess == "HINT":                                         # if the user writes "HINT"...
        syn = wordnet.synsets(x)[0]                             # ... we define "syn" as the first synset for the correct word in wordnet...
        print("\nThe word is defined as:", syn.definition())    #... and print the definition of this word
        guessing(x, y)                                          # the guessing will then resume and the guess-space shows up again
    elif guess.isdigit():                                       # if the guess is a number...
        number_hint(guess, y)                                   # we know that the user asked for a number hint and we excecute the number_hint function with the guess and the list of closest neighbours as arguments.
        guessing(x, y)                                          # the guessing will then resume and the guess-space shows up again
    elif guess == "GIVE UP":                                    # if the user writes "GIVE UP" in the guess-space...
        print(f'The word is "{x}".')                            # we print the correct word...
        again()                                                 # and run the "again" function so that the player can choose if they want to play another round
    else:                                                       # if the guess is not one of these three special instructions mentioned above...
        if guess in model.key_to_index:                         # we check if the guess is in the dictionary
            similarity = (model.similarity(guess, x))           # if it is, we create a "similarity-score", which is the similarity between the correct word and the guess
            print("Similarity:", round(similarity*100, 2))                  # we print the similarity score - but made clearer for the user (round up to 2 decimals and on a scale from -100 to 100 instead of -1 to 1)
        else:                                                               # if the guess is not in the dictionary...
            print("\nThis word is not in our dictionary. Try a new one")    # we print a statement telling the user this
            guessing(x, y)                                                  # the guessing will then resume and the guess-space shows up again
        if guess == x:                                                      # if the guess is the correct word...
            print(f'"{guess}" is the correct word! Good job!')              # ...we print a statement telling the user that they found the correct word...
            again()                                             #... and run the again-function so that the user can choose to play again
        elif guess in y:                                        # if the guess is in the list of closest neighbours to the correct word...
            closest(guess, y)                                   # we excecute the function "closest" with the guess and the list of neighbours as arguments
            guessing(x, y)                                      # the guessing will then resume and the guess-space shows up again
        else:                                                   # if the guess is not correct and not in the list of neighbours...
            guessing(x, y)                                      # ... the guessing will resume and the guess-space shows up again

def whole_game():                                                                           # a function called "whole_game", which is where the game is started
    chosen = (random.choice(model.index_to_key)).lower()                                    # we take a random word from the dictionary, make it lowercase, and assign it to the variable "chosen"
    if chosen not in model.key_to_index or not wordnet.synsets(chosen) or len(chosen) < 3:  # if the chosen word is not in the dictionary, or is not in the wordnet synsets, or is shorter than 3 tokens...
        whole_game()                                                                        # the whole_game function is excecuted again, and we start over
    neighbours_raw = list(model.most_similar(chosen, topn = 500))                           # a list of the 500 closest neighbours to the chosen word is assigned to the list "neighbours_raw". This list contains pairs of word + similarity score
    neighbours = []                                                                         # a new, empty list called "neighbours" is created
    for i in neighbours_raw:                                                                # for every item in neghbours_raw...
        neighbours.append(i[0])                                                             # ... we add the first part (the word) into the list "neighbours", without the similarity score

    print("\nIn this round, the word that is the closest to the correct one has a similarity score of", round(neighbours_raw[0][1]*100, 2))           # we print the similarity score of the most similar word to give the user some information about what the similarity scores that will show up throughout the game will mean
    print("In this round, the word that is the 500th closest to the correct one has a similarity score of", round(neighbours_raw[499][1]*100, 2))     # we print the similarity score of the 500th most similar word, for the same reason
    guessing(chosen, neighbours)                                # we excecute the guessing-function with the chosen word and the list of neighbours as arguments


whole_game()                                                    # we excecute the function "whole_game"