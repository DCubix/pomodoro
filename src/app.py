import flet
from flet import app, NavigationBar, NavigationDestination, Page, RouteChangeEvent, View, icons

from main_page import MainPage

def main(page: Page):
  page.title = 'Pomodoro Clock!'
  page.vertical_alignment = 'center'
  page.horizontal_alignment = 'center'
  page.window_resizable = False
  page.window_maximizable = False
  page.window_width = 480
  page.window_height = 512

  page.add(MainPage())


app(target=main, assets_dir='../assets')
