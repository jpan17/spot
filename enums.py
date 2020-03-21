# enums.py
# Description: Declarations for enums used throughout the application.

import enum

class PetType(enum.Enum):
    DOG = 'Dog'
    CAT = 'Cat'
    RODENT = 'Rodent'
    FISH = 'Fish'
    BIRD = 'Bird'
    REPTILE = 'Reptile'
    OTHER = 'Other'

class Activity(enum.Enum):
    FEEDING = 'Feeding'
    WALKING = 'Walking'
    PLAYING = 'Playing'
    GROOMING = 'Grooming'
    BATHING = 'Bathing'
    OTHER = 'Other'