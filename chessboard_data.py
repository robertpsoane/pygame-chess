# -*- coding: utf-8 -*-
"""
Initial Setup of Chess Board
Created on Fri Apr 24 22:53:19 2020

@author: Robert Soane
"""
cb_init = {'A': {'1': 'wr1', '2': 'wp1', '3': 'null', '4': 'null', '5': 'null', '6': 'null', '7': 'bp1', '8': 'br1'}, 'B': {'1': 'wn1', '2': 'wp2', '3': 'null', '4': 'null', '5': 'null', '6': 'null', '7': 'bp2', '8': 'bn1'}, 'C': {'1': 'wb1', '2': 'wp3', '3': 'null', '4': 'null', '5': 'null', '6': 'null', '7': 'bp3', '8': 'bb1'}, 'D': {'1': 'wqu', '2': 'wp4', '3': 'null', '4': 'null', '5': 'null', '6': 'null', '7': 'bp4', '8': 'bqu'}, 'E': {'1': 'wki', '2': 'wp5', '3': 'null', '4': 'null', '5': 'null', '6': 'null', '7': 'bp5', '8': 'bki'}, 'F': {'1': 'wb2', '2': 'wp6', '3': 'null', '4': 'null', '5': 'null', '6': 'null', '7': 'bp6', '8': 'bb2'}, 'G': {'1': 'wn2', '2': 'wp7', '3': 'null', '4': 'null', '5': 'null', '6': 'null', '7': 'bp7', '8': 'bn2'}, 'H': {'1': 'wr2', '2': 'wp8', '3': 'null', '4': 'null', '5': 'null', '6': 'null', '7': 'bp8', '8': 'br2'}}

let2num = {

    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "F": 6,
    "G": 7,
    "H": 8

}

num2let = {

    "1": "A",
    "2": "B",
    "3": "C",
    "4": "D",
    "5": "E",
    "6": "F",
    "7": "G",
    "8": "H"

}

coordconversion = {

            "l2n": let2num,
            "n2l": num2let

        }

wbt = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8']
