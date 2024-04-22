# Importación de todas las librerías
from flet import *; import requests as api; import local_propierties as LOCAL; import time as t

# Todos los colores utilizados en el proyecto
colores = {
    "window_bg" : "#60a85f", #? Fondo de pantalla
    "AppBar_bg" : '#88e23b', #? Fondo de la AppBar
    "AppBar_fg" : '#035AA6', #? Fuente de la AppBar
    "Name_fg": "#7CB0FF", #? Fuente del nombre del personaje
    "Card_bg": "#bbffff", #? Fondo de las cartas
    "Card_fg" : "#444444", #? Fuente de las cartas
}


def obtener_datos_de_pagina():
        url_api = f"https://rickandmortyapi.com/api/character?page={LOCAL.page}"
        respuesta = api.get(url_api)
        if respuesta.status_code == 200:
            return respuesta.json()
        else:
            return "Error"


async def main(page : Page):
    #Vamos a obtener los datos por lotes de 20
    LOCAL.dt_pg_actual = obtener_datos_de_pagina()
    LOCAL.dt_pg_actual = LOCAL.dt_pg_actual['results']
    #? Propiedades de la pantalla:
    page.window_height = 550  #Alto
    page.window_width = 840 #Ancho
    page.title = "Rick and Morty API" #Titulo
    page.bgcolor = colores["window_bg"] #Color de fondo

    # Función que hace visible la información de las tarjetas
    def cargar():
        #Con la función cargar, hacemos visibles todos los elementos
        Boton_Anterior.visible = True #* Boton anterior
        Contenedor_Botones.alignment = MainAxisAlignment.SPACE_BETWEEN
        Contenedor_Central.controls[1].content.controls[0].visible = False #* Rick GIF
        Contenedor_Central.controls[1].content.controls[1].visible = True #* Name
        Contenedor_Central.controls[1].content.controls[2].visible = True #* ID
        Contenedor_Central.controls[1].content.controls[3].visible = True #* Specie
        Contenedor_Central.controls[1].content.controls[4].visible = True #* Status 
        Contenedor_Central.controls[1].content.controls[5].visible = True #* Location
        Contenedor_Central.controls[0].content = Contenedor_Imagen #Cambiamos el GIF de la pantalla, por la img del personaje
        page.update()

    # Función que cambia al siguiente elemento
    async def siguiente_elemento(e):
        # Llamamos a la función cargar
        cargar() 
        
        # Si el ID del personaje accede al ultimo elemento de la página(19)
        # Debemos aumentar la página actual y reiniciar el elemento que visitamos( a 0)
        if LOCAL.id_personaje == 19:
            # Cambiamos a la siguiente página
            LOCAL.page += 1
            # Volvemos a comenzar en el elemento 0
            LOCAL.id_personaje = 0
            LOCAL.dt_pg_actual = obtener_datos_de_pagina()
            LOCAL.dt_pg_actual = LOCAL.dt_pg_actual['results']

        # Caso contrario a estar en el ultimo elemento
        else:
            # Simplemente aumentaremos un elemento( 0, 1, 2, 3, ...)
            LOCAL.id_personaje += 1

        # Rick_and_morty es la función que accede a la API, obtiene la información
        # Y la coloca en pantalla, la llamamos y esperamos a que todo se actualice
        await rick_and_morty(LOCAL.dt_pg_actual)
    
    # Función que cambia al elemento anterior
    async def elemento_anterior(e):
        # Llamamos a la función cargar
        cargar()

        # Si estamos en el primer elemento de la página(0)
        # Debemos ir al ultimo elemento(19) de la página anterior
        if LOCAL.id_personaje == 0:
            # Cambiamos a la página anterior
            LOCAL.page -= 1
            # Vamos al ultimo elemento
            LOCAL.id_personaje = 19
            LOCAL.dt_pg_actual = obtener_datos_de_pagina()
            LOCAL.dt_pg_actual = LOCAL.dt_pg_actual['results']
        # Si no estamos en el primer elemento, volvemos atrás
        else: 
            LOCAL.id_personaje -= 1

        await rick_and_morty(LOCAL.dt_pg_actual)

    # Función que hace la llamada a la API
    async def rick_and_morty(datos):
        datos_personaje = datos[LOCAL.id_personaje]

        #Nombre:
        Contenedor_Central.controls[1].content.controls[1].value = f"Name: {datos_personaje['name']}"
        #ID:
        Contenedor_Central.controls[1].content.controls[2].value = f"ID: {datos_personaje['id']}"
        #Especie
        Contenedor_Central.controls[1].content.controls[3].value = f"Specie: {datos_personaje['species']}"                   
        #Estado(vivo/muerto)
        Contenedor_Central.controls[1].content.controls[4].value = f"Status: {datos_personaje['status']}"
        #Ubicación
        Contenedor_Central.controls[1].content.controls[5].value = f"Location: {datos_personaje['location']['name']}"
        #Foto
        Contenedor_Imagen.content = Image(src=f"https://rickandmortyapi.com/api/character/avatar/{datos_personaje['id']}.jpeg", width=300, height=300)
        page.update()


    #Elementos
    Boton_Anterior = ElevatedButton(text= "<<", on_click= elemento_anterior)
    Boton_Siguiente = ElevatedButton(text=">>", on_click= siguiente_elemento)
    Contenedor_Botones = Row([Boton_Anterior, Boton_Siguiente], alignment= MainAxisAlignment.END, vertical_alignment= CrossAxisAlignment.END)
    Contenedor_Imagen = AnimatedSwitcher(Image(
                src= "https://www.google.com/url?sa=i&url=https%3A%2F%2Far.pinterest.com%2Fpin%2F704180091723575473%2F&psig=AOvVaw1vorMHIK2eZLlTKamxUOpS&ust=1713746845231000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCPD_9OWJ0oUDFQAAAAAdAAAAABAE",
                width= 300,
                height= 300,
                border_radius= BorderRadius(14, 14, 14, 14),), 
                #transition= AnimatedSwitcherTransition.FADE,
            )

    #Contenedores  
    Contenedor_Superior = AppBar(
        leading= Image(
            src="https://upload.wikimedia.org/wikipedia/commons/b/b1/Rick_and_Morty.svg",
            width= 400,
            height= 120,
            fit= ImageFit.NONE
            ),
        leading_width= 1000,
        toolbar_height= 100,
        bgcolor = colores["AppBar_bg"],
        adaptive = True,
        
        

    )
    Contenedor_Central = Row([
        Container(
            content= Lottie(
                        src='https://lottie.host/d2b97621-26e3-470f-a622-3a09513dadce/yJgjTM9DE4.json',
                        repeat=True,
                        animate=True,
                        height= 160,
                        width= 160,
                        visible= True
                    ),
            margin=10,
            padding=10,
            alignment=alignment.center,
            bgcolor= colores["Card_bg"] ,
            width=200,
            height=200,
            border_radius=10,
            ),
            
        Container(
            content=Column([
                Lottie(
                    src='https://lottie.host/822d0417-f3e5-4d82-b933-86d0358d74e5/nsKIK4rQxv.json',
                    repeat=True,
                    animate=True,
                    height= 260,
                    width= 260,
                    visible= True
                ),
                Text(
                    visible= False,
                    value= "Name: ¿¿??",
                    color= colores["Card_fg"],
                    style= TextStyle(size= 26, weight= FontWeight.BOLD),
                    text_align= MainAxisAlignment.START
                ),
                Text(
                    visible= False,
                    value= "Id: ¿¿??",
                    color= colores["Card_fg"],
                    style= TextStyle(size= 26, weight= FontWeight.BOLD),
                ),
                Text(
                    visible = False,
                    value= "Specie: ¿¿??",
                    color= colores["Card_fg"],
                    style= TextStyle(size= 26, weight= FontWeight.BOLD),
                ),
                Text(
                    visible = False,
                    color= colores["Card_fg"],
                    value= "Status: ¿¿??",
                    style= TextStyle(size= 26, weight= FontWeight.BOLD),
                ),
                Text(
                    visible = False,
                    color= colores["Card_fg"],
                    value= "Location: ¿¿??",
                    style= TextStyle(size= 26, weight= FontWeight.BOLD),
                ),
            ],
            expand= True,
            alignment= MainAxisAlignment.SPACE_AROUND
            ), 
            margin=10,
            padding=10,
            alignment=alignment.center,
            bgcolor= colores["Card_bg"] ,
            width=540,
            height=320,
            border_radius=10,
            ),
        ],

    )
    Contenedor_Inferior = BottomAppBar(Contenedor_Botones, bgcolor="#02afc5", height= 60)

    # Al iniciar la app no quiero que se muestre el Boton_anterior
    if LOCAL.id_personaje == -1:
        Boton_Anterior.visible = False

    page.add(Contenedor_Superior, Contenedor_Central, Contenedor_Inferior)
    page.update()


if __name__ == '__main__':
    app(target=main)
