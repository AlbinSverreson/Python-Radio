#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import io
import subprocess
import math
import datetime
import curses
from pathlib import Path

def run(stdscr):
  running = False
  selected_index = -1
  cursor_index = 0
  curses.use_default_colors()
  curses.init_pair(1, curses.COLOR_GREEN, -1)
  curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)
  valid = ["KEY_DOWN", "KEY_UP", "q", "Q", repr("\n"), "KEY_RESIZE"]

  f = open(f"{Path.home()}/stations.csv", 'r')
  stations = [l.split(',') for l in f.read().splitlines()]
  f.close()

  textwin = curses.newwin(curses.LINES-1, curses.COLS)
  playwin = curses.newwin(1,curses.COLS, curses.LINES-1, 0)
  textwin.keypad(1)
  textwin.scrollok(True)
  playwin.scrollok(True)
  horiz = "─"
  vert = "│"
  u_l = "┌"
  u_r = "┐"
  l_l = "└"
  l_r = "┘"

  while(True):
    curses.curs_set(0)
    curses.update_lines_cols()
    textwin.resize(curses.LINES-1, curses.COLS)

    playwin.resize(1, curses.COLS)
    playwin.mvwin(curses.LINES-1, 0)

    top_text = "[Radio]"
    if(((curses.COLS-2-len(top_text)) % 2) != 0):
      top_text = top_text + " "
    line = horiz * int((curses.COLS-2-len(top_text))/2)
    textwin.addstr(u_l+line+top_text+line+u_r)

    mid = int((curses.LINES-3)/2)
    stat_range = range(mid-cursor_index, mid+(len(stations)-cursor_index))

    for i in range(curses.LINES-3):
      if(i in stat_range):
        s = stations[stat_range.index(i)][0]
        #if(i==mid-cursor_index+selected_index and selected_index != -1):
        if(i == mid):
          s = "[ " + s + " ]"
        if(((curses.COLS-2-len(s)) % 2) != 0):
          s = s + " "
        spacing = " " * int((curses.COLS-2-len(s))/2)
        if(i == mid-cursor_index+selected_index and selected_index !=-1):
          textwin.addstr(vert)
          textwin.addstr(spacing + s + spacing,  curses.color_pair(1)|curses.A_BOLD)
          textwin.addstr(vert)
        else:
          textwin.addstr(vert+spacing+s+spacing+vert)

      else:
        textwin.addstr(vert+" "*(curses.COLS-2)+vert)

    textwin.insstr(l_l+horiz*(curses.COLS-2)+l_r)

    if (selected_index == -1):
      bottom_text = " Select a channel"
    else:
      bottom_text =  " Now playing: " + stations[selected_index][0]
    spacing = " " *  (curses.COLS - len(bottom_text))
    bottom_text = bottom_text + spacing
    playwin.insstr(bottom_text, curses.color_pair(2))
    textwin.refresh()
    playwin.refresh()

    keypress = textwin.getkey()
    while(not keypress in valid and not repr(keypress) in valid):
      keypress = textwin.getkey()

    if(keypress == "KEY_DOWN" and (cursor_index != len(stations)-1)):
      cursor_index = cursor_index + 1
    elif(keypress == "KEY_UP" and (cursor_index != 0)):
      cursor_index = cursor_index - 1
    elif(keypress == "q" or keypress == "Q"):
      if(running):
        proc.terminate()
      sys.exit(0)
    elif(repr(keypress) == repr("\n")):
      if(not running):
        selected_index = cursor_index
        proc = subprocess.Popen(["ffplay", "-nodisp", stations[selected_index][1]], \
          stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        running = True
      elif(cursor_index == selected_index):
        selected_index = -1
        proc.terminate()
        running = False
      else:
        selected_index = cursor_index
        proc.terminate()
        proc = subprocess.Popen(["ffplay","-nodisp", stations[selected_index][1]], \
          stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

curses.wrapper(run)
