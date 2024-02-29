from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivy.graphics import Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivy.properties import DictProperty
from kivymd.uix.list import ThreeLineListItem
from kivy.clock import Clock
from dotenv import load_dotenv
from kivymd.uix.dialog import MDDialog

from werkzeug.security import check_password_hash


import os

import mysql.connector

load_dotenv()
db_host = os.environ.get('DB_HOST')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')

Window.size = (360, 640)



# Design
KV = '''

ScreenManager:


    canvas.before:
        Color:
            rgba: 0, 0, 0, 1

        Rectangle:
            pos: self.pos
            size: self.size
   
    LoginScreen:
    WelcomeScreen:
    BetDetailScreen:

    



<LoginScreen>:
    name: 'login'


    FloatLayout:
        Image:
            source: 'env/sources/super_bowl_logo.png'
            size_hint: 1, None
            height: '50dp'
            allow_stretch: False
            keep_ratio: True
            pos_hint: {"top": 0.98}  

    MDCard:
        orientation: 'vertical'
        size_hint: None, None
        size: dp(320), dp(400)
        pos_hint: {"center_x": .5, "center_y": .55}
        elevation: 1
        padding: dp(20)
        spacing: dp(20)
        radius: [25, 25, 25, 25] 
       

        canvas.before:
            Color:
                rgba: 0.435, 0.259, 0.757, 1
            BoxShadow:
                pos: self.pos
                size: self.size
                offset: 0, 0
                spread_radius: -20, -20
                border_radius: 10, 10, 10, 10
                blur_radius: 120
        
        
        MDLabel:
            text: 'Login'
            theme_text_color: 'Primary'
            font_style: 'H4'
            size_hint_y: None
            height: self.texture_size[1]
            pos_hint: {'center_y': .20}
            halign: 'center'
        
        MDTextField:
            id: username_field
            hint_text: 'Email'
            required: True
            size_hint_x: 1
            pos_hint: {"center_x": .5}
            
          
        MDTextField:
            id: password_field
            hint_text: 'Mot de passe'
            required: True
            password: True
            size_hint_x: 1
            pos_hint: {"center_x": .5}
            
        MDRaisedButton:
            text: 'Se connecter'
            on_release: app.login()
            size_hint_x: 0.5
            size_hint_y: None
            height: dp(50)
            pos_hint: {"center_x": .5}
            md_bg_color: 0.435, 0.259, 0.757, 1


<WelcomeScreen>:
    name: 'welcome'

    FloatLayout:
        Image:
            source: 'env/sources/super_bowl_logo.png'
            size_hint: 1, None
            height: '50dp'
            allow_stretch: False
            keep_ratio: True
            pos_hint: {"top": 0.98}  
    
    BoxLayout:
        orientation: 'vertical'
        size_hint: 1, 1
        spacing: dp(10)
        padding: dp(20)

        MDLabel:
            text: 'Mises:'
            theme_text_color: 'Custom'
            text_color: 1, 1, 1, 1
            font_style: 'H4'
            size_hint_y: None
            height: self.texture_size[1]
            halign: 'center'
            padding_y: dp(10)

        MDCard:
            orientation: 'vertical'
            size_hint: 1, None
            height: self.minimum_height
            padding: dp(10)
            spacing: dp(10)
            elevation: 1
            radius: [25, 25, 25, 25]

            canvas.before:
                Color:
                    rgba: 0.435, 0.259, 0.757, 1
                BoxShadow:
                    pos: self.pos
                    size: self.size
                    offset: 0, 0
                    spread_radius: -20, -20
                    border_radius: 10, 10, 10, 10
                    blur_radius: 120
            
            ScrollView:
                size_hint_y: None
                height: dp(400)  # Ajusta este valor según sea necesario

                MDList:
                    id: bets_list
                    
            MDRaisedButton:
                text: 'Retourner au login'
                on_release: app.go_to_login()
                size_hint_x: 0.5
                size_hint_y: None
                height: dp(50)
                pos_hint: {"center_x": .5}
                md_bg_color: 0.435, 0.259, 0.757, 1

<BetDetailScreen>:
    name: 'bet_detail'
    
    FloatLayout:
        Image:
            source: 'env/sources/super_bowl_logo.png'
            size_hint: 1, None
            height: '50dp'
            allow_stretch: False
            keep_ratio: True
            pos_hint: {"top": 0.98}  

        MDLabel:
            text: 'Détails du match'
            theme_text_color: 'Custom'
            text_color: 1, 1, 1, 1
            font_style: 'H4'
            size_hint_y: None
            height: self.texture_size[1]
            halign: 'center'
            padding_y: dp(10)
            pos_hint: {"center_x": 0.5, "top": 0.86}

        MDCard:
            size_hint: None, None
            size: "260dp", "200dp"
            pos_hint: {"center_x": 0.5, "top": 0.7}
            elevation: 1
            padding: "8dp"
            spacing: "10dp"
            radius: [25, 25, 25, 25]
            
            canvas.before:
                Color:
                    rgba: 0.435, 0.259, 0.757, 1
                BoxShadow:
                    pos: self.pos
                    size: self.size
                    offset: 0, 0
                    spread_radius: -20, -20
                    border_radius: 10, 10, 10, 10
                    blur_radius: 120

            MDLabel:
                id: detail_label
                text: ''
                halign: 'center'
                valign: 'top'
                size_hint_y: None
                height: self.texture_size[1]
                pos_hint: {"center_x": 0.5, "top": 0.98}

        MDRaisedButton:
            text: 'Retourner'
            on_release: app.go_to_welcome()
            size_hint: None, None
            size: "200dp", "50dp"
            pos_hint: {"center_x": .5, "top": 0.1}
            md_bg_color: 0.435, 0.259, 0.757, 1


 
'''

class LoginScreen(Screen):
    pass

class WelcomeScreen(Screen):
    user_id = None  # Asumiremos que este valor se establece en alguna parte antes de entrar a la pantalla

    def on_pre_enter(self, *args):
        # Programar la actualización cada 30 segundos
        self.update_bets()
        Clock.schedule_interval(lambda dt: self.update_bets(), 30)

    def update_bets(self):
        # Limpiar la lista cada vez que se entra a la pantalla para evitar duplicados
        self.ids.bets_list.clear_widgets()
        
        # Intenta conectarte a la base de datos y obtener las apuestas del usuario
        try:
            # Establecer conexión a la base de datos MySQL
            conn = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name
            )
            cursor = conn.cursor()
            # Asegúrate de que 'user_id' está definido y no es None
            if self.user_id is not None:
                # Utiliza parámetros seguros para prevenir la inyección de SQL
                cursor.execute("""
                    SELECT matchs.id, matchs.equipe1, matchs.equipe2, matchs.jour, matchs.debut, 
                    matchs.fin, matchs.score, matchs.statut, mises.mise1, mises.mise2, mises.resultat1, mises.resultat2, mises.equipe1, mises.equipe2, matchs.vainqueur, matchs.commentaires
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
                'vainqueur': bet[14],
                'score': bet[6],
                'commentaires' : bet[15]
            }

            line_one = f"{bet[1]} vs {bet[2]}"
            line_two = f"Date: {bet[3]}, Debut: {bet[4]}, Fin: {bet[5]}"
            line_three = f"Score: {bet[6] if bet[6] is not None else '-'} , Statut: {bet[7]}, Vainqueur: {bet[14]}"

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
            
            print("actualisation")
            self.ids.bets_list.add_widget(list_item)

    def open_bet_details(self, bet_info):
    # This function opens the bet details screen with the provided bet information.
    # If a bet_info value is None, it will not be displayed.
        bet_detail_screen = self.manager.get_screen('bet_detail')
        bet_detail_screen.bet_data = bet_info

         # Determinar el color para 'resultat1' y 'resultat2' en base a 'vainqueur'
        couleur_resultat1 = '33ff33' if bet_info.get('vainqueur') == bet_info.get('equipemise1') else 'ff3333'
        couleur_resultat2 = '33ff33' if bet_info.get('vainqueur') == bet_info.get('equipemise2') else 'ff3333'
    
    # Creating a list of strings for each bet detail
        details = [
            f"{bet_info['equipe1']} VS {bet_info['equipe2']}",
            f"Debut: {bet_info['debut']}",
            f"Fin: {bet_info['fin']}",
            f"Mise {bet_info['equipemise1']}: {str(int(bet_info['mise1']))}" if bet_info['mise1'] is not None else "",
            f"Mise {bet_info['equipemise2']}: {str(int(bet_info['mise2']))}" if bet_info['mise2'] is not None else "",
            f"[color={couleur_resultat1}]Resultat : {str(int(bet_info['mise1'])) if couleur_resultat1 == 'ff3333' else str(bet_info['resultat1'])}[/color]" if bet_info.get('resultat1') is not None and bet_info.get('vainqueur') != '-' else "",
            f"[color={couleur_resultat2}]Resultat : {str(int(bet_info['mise2'])) if couleur_resultat1 == 'ff3333' else str(bet_info['resultat2'])}[/color]" if bet_info.get('resultat2') is not None and bet_info.get('vainqueur') != '-' else "",
            f"Score: {bet_info['score']}" if bet_info['score'] is not None else "",
            f"Commentaires: {bet_info['commentaires']}" if bet_info['commentaires'] != ' - ' else "",
            f"Vainqueur: {bet_info['vainqueur']}" if bet_info['vainqueur'] != '-' else ""
        ]
    
        # Joining the details and filtering out empty strings
        detail_text = "\n".join(filter(None, details))

        bet_detail_screen.ids.detail_label.markup = True
        # Setting the label text to the joined details
        bet_detail_screen.ids.detail_label.text = detail_text

        # Changing the current screen to the bet detail screen
        self.manager.current = 'bet_detail'

    def on_leave(self, *args):
        Clock.unschedule(self.update_bets)


class MyApp(MDApp):
    def build(self):
        self.screen_manager = Builder.load_string(KV)
        return self.screen_manager

  
    
    def on_start(self):
    
        Window.orientation = 'portrait'
    
   
    def login(self):
        login_screen = self.screen_manager.get_screen('login')
        username = login_screen.ids.username_field.text
        password = login_screen.ids.password_field.text

        if not username or not password:
            self.show_error_dialog("Por favor, introduce tanto el correo electrónico como la contraseña.")
            self.screen_manager.current = 'login'
            return

        try:
            
            conn = mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_name)
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()

            if user:

                stored_password_hash = user[4]
                

         
                if check_password_hash(stored_password_hash, password):
                  
                    welcome_screen = self.screen_manager.get_screen('welcome')
                    welcome_screen.user_id = user[0]
                    self.screen_manager.current = 'welcome'
                else:
                    # Falla de autenticación
                     self.show_error_dialog("La contraseña es incorrecta.")
            else:
                # Usuario no encontrado
                 self.show_error_dialog("El usuario no fue encontrado.")

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            self.show_error_dialog("Error al conectarse a la base de datos.")
        
    def go_to_login(self):
        self.screen_manager.current = 'login'
    
    def go_to_welcome(self):
        # Cambia la pantalla actual a 'welcome'
        self.screen_manager.current = 'welcome'

    def show_error_dialog(self, message):
        # Define el botón del diálogo aquí para asegurarte de que se recrea cada vez
        ok_button = MDFlatButton(
            text="OK",
            theme_text_color="Custom",
            text_color=self.theme_cls.primary_color,
            on_release=lambda instance: self.dialog.dismiss()
        )

        # Si el diálogo ya existe, simplemente actualizamos el texto y los botones
        if hasattr(self, 'dialog'):
            self.dialog.text = message
            self.dialog.buttons = [ok_button]
        else:
            # Crear el diálogo si no existe
            self.dialog = MDDialog(
                text=message,
                buttons=[ok_button]
            )

        self.dialog.open()

    def close_dialog(self, instance_button):
        # Desvincular el evento para evitar referencias circulares y luego cerrar el diálogo
        instance_button.unbind(on_release=self.close_dialog)
        self.dialog.dismiss()



class BetDetailScreen(Screen):
    pass
if __name__ == '__main__':
    MyApp().run()