import flet as ft
import math
from flet import UserControl, Column, ElevatedButton, Text, TextThemeStyle, Image, Container, icons
from threading import Timer
from dataclasses import dataclass

TIMER_STEP = 0.25

@dataclass
class TimerEntry:
  duration: int # secs
  description: str


class MainPage(UserControl):
  def build(self):
    self.clockText = Text('00:00', style=TextThemeStyle.DISPLAY_LARGE)
    self.descriptionText = Text('Idling...', style=TextThemeStyle.TITLE_SMALL)
    self.startStopButton = ElevatedButton('Start', icon=icons.PLAY_ARROW, on_click=self.on_start_stop)
    self.tomato = Image(
      src='/tomato.png',
      width=120,
      fit=ft.ImageFit.CONTAIN,
      animate_scale=ft.animation.Animation(400, ft.AnimationCurve.EASE_OUT_QUAD),
      scale=ft.transform.Scale(scale=1.0)
    )

    self.running = False
    self.timer = None
    self.elapsedTime = 0
    self.currentIndex = 0

    self.pomodoroSequence = [
      TimerEntry(25, 'Work!'),
      TimerEntry(5, 'Take a break...'),
      TimerEntry(25, 'Work!'),
      TimerEntry(5, 'Take a break...'),
      TimerEntry(25, 'Work!'),
      TimerEntry(5, 'Take a break...'),
      TimerEntry(25, 'Work!'),
      TimerEntry(15, 'Take a long break...')
    ]

    return Column(
      spacing=6,
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        self.tomato,
        self.clockText,
        self.descriptionText,
        Container(height=16),
        self.startStopButton
      ]
    )

  def next(self, inc=1):
    self.currentIndex += inc
    currentEntry = self.pomodoroSequence[self.currentIndex % len(self.pomodoroSequence)]
    self.descriptionText.value = f'({currentEntry.description})'
    self.descriptionText.update()
    self.elapsedTime = currentEntry.duration * 60

  def on_start_stop(self, ev):
    def timer_tick():
      ss = math.floor(self.elapsedTime) % 60
      mm = math.floor(self.elapsedTime) // 60
      self.elapsedTime -= TIMER_STEP

      sx = 1.1 if (self.elapsedTime / TIMER_STEP) % 2 == 0 else 0.9
      self.tomato.scale = sx
      self.tomato.update()

      self.clockText.value = f'{mm:02d}:{ss:02d}'
      self.clockText.update()

      if self.running:
        self.startStopButton.text = 'Stop'
        self.startStopButton.icon = icons.STOP
      else:
        self.startStopButton.text = 'Start'
        self.startStopButton.icon = icons.PLAY_ARROW
      self.startStopButton.update()

      if self.elapsedTime <= 0:
        self.next()

      if not self.running:
        return

      self.timer = Timer(TIMER_STEP, timer_tick)
      self.timer.start()

    if self.running:
      self.running = False
      self.timer.cancel()

      self.startStopButton.text = 'Start'
      self.startStopButton.icon = icons.PLAY_ARROW
      self.startStopButton.update()

      self.descriptionText.value = 'Idling...'
      self.descriptionText.update()

      self.clockText.value = '00:00'
      self.clockText.update()

      self.tomato.scale = 1
      self.tomato.update()
    else:
      self.running = True
      self.next(inc=0)
      timer_tick()
