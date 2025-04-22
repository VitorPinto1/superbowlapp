from kivy.uix.screenmanager import Screen

class PariDetailEcran(Screen):
    user_id = None
    def open_notifications(self, *args):
        welcome_screen = self.manager.get_screen('welcome')
        welcome_screen.open_notifications()

    def sync_stats_and_check(self, *args):
        welcome_screen = self.manager.get_screen('welcome')
        welcome_screen.sync_stats_and_check()