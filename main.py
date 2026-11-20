"""LuxShare application entry point.

The UI and networking modules are kept separate so they can be added under
screens/ and core/ without changing this entry point.
"""
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, NoTransition

from config import APP_NAME, COLORS, WINDOW_TITLE


class LuxShareApp(App):
    title = WINDOW_TITLE

    def build(self):
        Window.clearcolor = COLORS["background"]
        self.manager = ScreenManager(transition=NoTransition())

        # Import screens only when the app starts. This gives clear errors if
        # a screen module has not yet been added to the repository.
        try:
            from screens.home import HomeScreen
            from screens.send import SendScreen
            from screens.receive import ReceiveScreen
            from screens.settings import SettingsScreen
        except ImportError as exc:
            from kivy.uix.boxlayout import BoxLayout
            from kivy.uix.label import Label
            from kivy.uix.button import Button

            fallback = BoxLayout(orientation="vertical", padding=24, spacing=16)
            fallback.add_widget(Label(
                text=f"{APP_NAME}\nProject setup is incomplete.\nMissing module: {exc}",
                halign="center",
                valign="middle",
            ))
            fallback.add_widget(Button(
                text="Close",
                size_hint_y=None,
                height=52,
                on_release=lambda *_: self.stop(),
            ))
            return fallback

        self.manager.add_widget(HomeScreen(name="home"))
        self.manager.add_widget(SendScreen(name="send"))
        self.manager.add_widget(ReceiveScreen(name="receive"))
        self.manager.add_widget(SettingsScreen(name="settings"))
        return self.manager


if __name__ == "__main__":
    LuxShareApp().run()
