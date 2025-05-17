#!/usr/bin/env python3

#Basic scripts for general functions

def triple_char(str):
    """When given a string return three of each char in the string."""
    results = ""
    for i in str:
        results += i + i + i
    return results
