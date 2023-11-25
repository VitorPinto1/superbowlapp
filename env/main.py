from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivy.graphics import Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.properties import DictProperty
from kivymd.uix.list import ThreeLineListItem

import mysql.connector

# Design
KV = '''
ScreenManager:
    LoginScreen:
    WelcomeScreen:
    BetDetailScreen:

<LoginScreen>:
    name: 'login'
    
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(20)
        
        MDLabel:
            text: 'Login'
            theme_text_color: 'Primary'
            font_style: 'H4'
            pos_hint: {'center_y':.20}
            halign: 'center'
            
            
            
           
            
        MDTextField:
            id: username_field
            hint_text: 'Email'
            required: True
            size_hint: (1, None)
            
            pos_hint: {"center_x": .5, "center_y": .5}
          
            
        MDTextField:
            id: password_field
            hint_text: 'Mot de passe'
            required: True
            password: True
            size_hint: (1, None)
           
            pos_hint: {"center_x": .5, "center_y": .5}
           

        MDRaisedButton:
            text: 'Se connecter'
            on_release: app.login()
            size_hint_x: 0.5  # Ajusta el ancho del botón
            size_hint_y: None
            height: dp(50)
            pos_hint: {"center_x": .5, "center_y": .5}
           

<WelcomeScreen>:
    name: 'welcome'
    
    BoxLayout:
        orientation: 'vertical'
        size_hint: 1, 1
        spacing: dp(10)
        padding: dp(20)

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(50)  # Altura fija para el encabezado

            MDLabel:
                text: 'Mises:'
                theme_text_color: 'Primary'
                font_style: 'H4'
                halign: 'center'  # Alinea el texto en el centro horizontal
                valign: 'center'  # Alinea el texto en el centro vertical
       
        ScrollView:
            MDList:
                id: bets_list
                
                    

        MDRaisedButton:
            text: 'Retourner au login'
            on_release: app.go_to_login()
            size_hint_x: 0.5
            size_hint_y: None
            height: dp(50)
            pos_hint: {"center_x": .5, "center_y": .5}

<BetDetailScreen>:
    name: 'bet_detail'
    
    BoxLayout:
        orientation: 'vertical'
        size_hint: 1, 1
        padding: dp(10)
        spacing: dp(10)

        MDLabel:
            text: 'Détails du match'
            font_style: 'H5'
            halign: 'center'
            size_hint_y: None
            height: self.texture_size[1]
            padding: dp(20)

        MDLabel:
            id: detail_label  # Asegúrate de que este id esté definido
            text: ''

        

        MDRaisedButton:
            text: 'Retourner'
            on_release: app.go_to_welcome()
            size_hint_x: 0.5
            size_hint_y: None
            height: dp(50)
            pos_hint: {"center_x": .5, "center_y": .5}

        
 
'''

class LoginScreen(Screen):
    pass

class WelcomeScreen(Screen):
    user_id = None  # Asumiremos que este valor se establece en alguna parte antes de entrar a la pantalla

    def on_pre_enter(self, *args):
        # Limpiar la lista cada vez que se entra a la pantalla para evitar duplicados
        self.ids.bets_list.clear_widgets()
        
        # Intenta conectarte a la base de datos y obtener las apuestas del usuario
        try:
            # Establecer conexión a la base de datos MySQL
            conn = mysql.connector.connect(
                host='localhost',
                user='PEPE',
                password='PEPE',
                database='bdsuperbowl'
            )
            cursor = conn.cursor()
            # Asegúrate de que 'user_id' está definido y no es None
            if self.user_id is not None:
                # Utiliza parámetros seguros para prevenir la inyección de SQL
                cursor.execute("""
                    SELECT matchs.id, matchs.equipe1, matchs.equipe2, matchs.jour, matchs.debut, 
                    matchs.fin, matchs.score, matchs.statut, mises.mise1, mises.mise2, mises.resultat1, mises.resultat2, mises.equipe1, mises.equipe2, matchs.vainqueur
                    FROM mises
                    JOIN matchs ON mises.id_match = matchs.id
                    WHERE mises.id_utilisateur = %s
                """, (self.user_id,))
                self.user_bets = cursor.fetchall()
            else:
                # Manejar caso en el que 'user_id' no está definido (por ejemplo, mostrar un mensaje de error)
                self.user_bets = []

            # Cerrar la conexión a la base de datos
            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.user_bets = []  # Resetear la lista de apuestas en caso de error

        for bet in self.user_bets:
            # Formatear la información de la apuesta para mostrarla en tres líneas
            bet_info = {
                'equipe1': bet[1],
                'equipe2': bet[2],
                'debut': bet[4],
                'fin': bet[5],
                'mise1': bet[8],
                'mise2': bet[9],
                'resultat1': bet[10],
                'resultat2': bet[11],
                'equipemise1': bet[12],
                'equipemise2': bet[13],
                'vainqueur': bet[14]
            }

            line_one = f"{bet[1]} vs {bet[2]}"
            line_two = f"Date: {bet[3]}, Debut: {bet[4]}, Fin: {bet[5]}"
            line_three = f"Resultat: {bet[6]}, Statut: {bet[7]}, 'Vainqueur': {bet[14]}"
            if bet[7] == "En cours":
                list_item = ThreeLineListItem(text=line_one,
                                            secondary_text=line_two,
                                            tertiary_text=line_three,
                                            on_release=lambda x, bet_info=bet_info: self.open_bet_details(bet_info))
                                       
            else:
                list_item = ThreeLineListItem(text=line_one,
                                            secondary_text=line_two,
                                            tertiary_text=line_three,
                                            theme_text_color='Secondary',
                                            on_release=lambda x, bet_info=bet_info: self.open_bet_details(bet_info))
                
            self.ids.bets_list.add_widget(list_item)

    def open_bet_details(self, bet_info):
    # This function opens the bet details screen with the provided bet information.
    # If a bet_info value is None, it will not be displayed.
        bet_detail_screen = self.manager.get_screen('bet_detail')
        bet_detail_screen.bet_data = bet_info
    
    # Creating a list of strings for each bet detail
        details = [
            f"Equipo 1: {bet_info['equipe1']}",
            f"Equipo 2: {bet_info['equipe2']}",
            f"Fecha de inicio: {bet_info['debut']}",
            f"Fecha de fin: {bet_info['fin']}",
            f"Apuesta en equipo 1: {bet_info['mise1']}" if bet_info['mise1'] is not None else "",
            f"Apuesta en equipo 2: {bet_info['mise2']}" if bet_info['mise2'] is not None else "",
            f"Resultado equipo 1: {bet_info['resultat1']}" if bet_info['resultat1'] is not None else "",
            f"Resultado equipo 2: {bet_info['resultat2']}" if bet_info['resultat2'] is not None else "",
            f"Equipo ganador: {bet_info['vainqueur']}" if bet_info['vainqueur'] != '-' else ""
        ]
    
        # Joining the details and filtering out empty strings
        detail_text = "\n".join(filter(None, details))
    
        # Setting the label text to the joined details
        bet_detail_screen.ids.detail_label.text = detail_text

        # Changing the current screen to the bet detail screen
        self.manager.current = 'bet_detail'

 


class MyApp(MDApp):
    def build(self):
        self.screen_manager = Builder.load_string(KV)

        with self.screen_manager.canvas.before:
            self.bg = Rectangle(source='/Users/vitorpinto/Documents/ECF/AppPython/env/imagesite1.png', pos=self.screen_manager.pos, size=Window.size)

        Window.bind(size=self.on_window_size_change)
        return self.screen_manager

    
    def on_start(self):
    
        Window.size = (360, 640) 
        Window.orientation = 'portrait'
        self.on_window_size_change(Window, Window.size)
    
    def on_window_size_change(self, instance, value):
        self.bg.size = value

    
    def login(self):
        login_screen = self.screen_manager.get_screen('login')
        username = login_screen.ids.username_field.text
        password = login_screen.ids.password_field.text
        
        try:
            # Establecer conexión a la base de datos MySQL
            conn = mysql.connector.connect(
                host='localhost',
                user='PEPE',
                password='PEPE',
                database='bdsuperbowl'
            )
            
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE email = %s AND mot_de_passe = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            
            if user:
                welcome_screen = self.screen_manager.get_screen('welcome')
                welcome_screen.user_id = user[0]
                self.screen_manager.current = 'welcome'
            else:
                self.screen_manager.current = 'login'
            
            cursor.close()
            conn.close()
            
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def go_to_login(self):
        self.screen_manager.current = 'login'
    
    def go_to_welcome(self):
        # Cambia la pantalla actual a 'welcome'
        self.screen_manager.current = 'welcome'


class BetDetailScreen(Screen):
    pass
if __name__ == '__main__':
    MyApp().run()