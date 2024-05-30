import telebot 
from telebot.types import ReplyKeyboardMarkup
from datetime import datetime 
import pandas as pd
import openpyxl 
from openpyxl import load_workbook
from Models import DBManager as DB
from Demanda import *


token = '6520917243:AAFkccJ0Pj8mFpNgM0lVZp8T9NkWEdWJlsI'
datos={}
articulo={}
fecha = datetime.now().strftime("%Y-%m-%d")  
horas = datetime.now().strftime("%H:%M:%S")  



                                #LINEA UNO (AVERIGUAR PRECIO PRODUCTO)

#biblioteca de mensajes
bot = telebot.TeleBot(token)
texto_bienvenida= 'Hola. Bienvenido a la empresa Canela y Vainilla, a continuación encontraras una serie de botones para realizar todo el proceso de información o compra, con el fin de mejorar tu experiencia con nosotros '
texto_introduccion='Desea averiguar el precio o comprar un producto?'
valor_camiseta=25000
valor_medias=3000
valor_chompas=75000
valor_boxer=15000
valor_zapatos=105000



##CREAR UN BOTON 
@bot.message_handler(commands=["start"])
def cmd_start(message):
    """da la bienvenida"""
    bot.reply_to(message,texto_bienvenida )
    markup = ReplyKeyboardMarkup(input_field_placeholder="pulsa un botón",resize_keyboard=True)## CREA EL BOTON
    markup.add("Averiguar Precio Producto","Comprar un Prodructo")## MENSAJE DENTRO BOTON
    msg = bot.send_message(message.chat.id, texto_introduccion , reply_markup=markup)## MENSAJE ANTES DEL BOTON

    bot.register_next_step_handler(msg,primera_desicion)

def manejo_de_Data_repetida(message):
    markup = ReplyKeyboardMarkup(input_field_placeholder="pulsa un botón",resize_keyboard=True)
    markup.add("Si","No")
    return bot.send_message(message.chat.id, 'NOS PERMITES EL MANEJO DE DATA?',reply_markup=markup)
def repeticion(message):
    markup = ReplyKeyboardMarkup(input_field_placeholder="pulsa un botón",resize_keyboard=True)
    markup.add("Zapatos","Camiseta","Medias","Chompas","Boxer")
    return bot.send_message(message.chat.id, 'Oprima el botón del producto',reply_markup=markup)

#primer condicional
def primera_desicion(message):
    
    if message.text !="Averiguar Precio Producto" and message.text !="Comprar un Prodructo":
        msg = bot.send_message(message.chat.id, 'Error: respuesta no valida\nPulsa un botón')
        bot.register_next_step_handler(msg,primera_desicion)
    elif message.text == "Averiguar Precio Producto":
        msg = repeticion(message)
        bot.register_next_step_handler(msg,averiguar_precio)
    elif message.text == "Comprar un Prodructo":
        msg = manejo_de_Data_repetida(message)
        bot.register_next_step_handler(msg,condicional_manejo_data)    

def averiguar_precio(message):

    demandas(message)
    if message.text !="Zapatos" and message.text !="Camiseta" and message.text !="Medias"and message.text !="Chompas"and message.text !="Boxer":
        bot.send_message(message.chat.id, 'Error: respuesta no valida\nPulsa un botón')
        adquisicion_producto(message)  
    elif message.text == "Camiseta":
        bot.send_message(message.chat.id, 'El precio es $25.000')
        adquisicion_producto(message)
        ###tiempo: debe ir una varible de tiempo que se almacena en la base de datos 
    elif message.text == "Medias":
        bot.send_message(message.chat.id, 'El precio es $3.000')
        adquisicion_producto(message) 
    elif message.text == "Chompas":
        bot.send_message(message.chat.id, 'El precio es $75.000')
        adquisicion_producto(message)
    elif message.text == "Boxer":
        bot.send_message(message.chat.id, 'El precio es $15.000')
        adquisicion_producto(message) 
    elif message.text == "Zapatos":
        bot.send_message(message.chat.id, 'El precio es $105.000')
        adquisicion_producto(message)
#ACA VA MARCACIÓN REGISTRO DEMANDA EN EXCEL
def adquisicion_producto(message):
    markup = ReplyKeyboardMarkup(input_field_placeholder="pulsa un botón",resize_keyboard=True)
    markup.add("Si","No")
    msg= bot.send_message(message.chat.id, '¿Desea adquirir el producto?',reply_markup=markup)
    bot.register_next_step_handler(msg,condicional_adquisicion_producto) 

def condicional_adquisicion_producto(message):
    if message.text !="Si" and message.text !="No":
        msg = bot.send_message(message.chat.id, 'Error: respuesta no valida\nPulsa un botón')
        bot.register_next_step_handler(msg,condicional_adquisicion_producto)  
    elif message.text == "Si":
        msg = manejo_de_Data_repetida(message)
        bot.register_next_step_handler(msg,condicional_manejo_data)
    elif message.text == "No":
        mensaje_agradecimiento(message)

  
    #LINEA 2 (COMPRAR UN PRODUCTO ) 
def condicional_manejo_data(message):
    if message.text !="Si" and message.text !="No":
        msg = bot.send_message(message.chat.id, 'Error: respuesta no valida\nPulsa un botón')
        bot.register_next_step_handler(msg,condicional_manejo_data)  
    elif message.text == "Si":
        pedir_nombre(message)
    elif message.text == "No":
        mensaje_agradecimiento(message)

#Obtencion de Datos Personales
        
@bot.message_handler(func=lambda message:True)        
def pedir_nombre(message):
    
    msg = bot.send_message(message.chat.id, 'Por favor ingresa tu nombre completo')
    bot.register_next_step_handler(msg,pedir_cedula) 
    
def pedir_cedula(message):
    datos[str(message.chat.id)]={}
    datos[str(message.chat.id)]["nombre"]=message.text
    msg = bot.send_message(message.chat.id, 'Por favor ingresa el número de cedula')
    print("pasó por pedir nombre: "+message.text)
    bot.register_next_step_handler(msg,pedir_celular)

def pedir_celular(message):
    datos[str(message.chat.id)]["cedula"]=message.text
    msg = bot.send_message(message.chat.id, 'Por favor ingresa el numero de tu celular')
    print("pasó por pedir cedula: "+message.text)
    bot.register_next_step_handler(msg,pedir_direccion)

def pedir_direccion(message):
    datos[str(message.chat.id)]["celular"]=message.text
    print("pasó por pedir celular: "+message.text)

    msg = bot.send_message(message.chat.id, 'Por favor ingresa la dirección de tu residencia')
    bot.register_next_step_handler(msg,pedir_correo)

def pedir_correo(message):
    datos[str(message.chat.id)]["direccion"]=message.text
    print("pasó por pedir direccion: "+message.text)


    msg = bot.send_message(message.chat.id, 'Por favor ingresa la dirección del correo')
    bot.register_next_step_handler(msg,obtener_producto)

def creacion_diccionario_productos(message):
    datos[str(message.chat.id)]["producto"]={}
    articulo[str(message.chat.id)]={}    
    
    

def obtener_producto(message):
    datos[str(message.chat.id)]["correo"]=message.text
    print("pasó por pedir correo: "+message.text)
    creacion_diccionario_productos(message)
    print("pasó por pedir creacion diccionario"+message.text)

    msg = repeticion(message)
    bot.register_next_step_handler(msg,eleccion_cantidad)

def obtener_otro_producto(message):
    print("pasó por obtener otro producto: "+message.text)
    msg = repeticion(message)
    bot.register_next_step_handler(msg,eleccion_cantidad)

def eleccion_cantidad(message):
    
    articulo[str(message.chat.id)]["producto"]=message.text
    msg = bot.send_message(message.chat.id, 'Por favor ingresa la cantidad')
    print("pasó por pedir producto: "+message.text)

    bot.register_next_step_handler(msg,condicional_adquisicion_otro_producto)

def condicional_adquisicion_otro_producto(message):
    datos[str(message.chat.id)]["producto"][articulo[str(message.chat.id)]["producto"]]=message.text
    markup = ReplyKeyboardMarkup(input_field_placeholder="pulsa un botón",resize_keyboard=True)
    markup.add("Si","No")
    msg= bot.send_message(message.chat.id, '¿Desea adquirir otro producto?',reply_markup=markup)
    bot.register_next_step_handler(msg,comprar_producto)
    

    
def comprar_producto(message):
    print("este es el mensaje del condicional_adquis: "+message.text)
    if message.text !="Si" and message.text !="No":
        msg = bot.send_message(message.chat.id, 'Error: respuesta no valida\nPulsa un botón')
        bot.register_next_step_handler(msg,condicional_adquisicion_otro_producto)  
    elif message.text == "Si":
        print("pasó por el condicional si: "+message.text)
        obtener_otro_producto(message)
    elif message.text == "No":
        importacion_data(message)

def importacion_data(message):    
    if str(message.chat.id) in datos:
        moneda = datos[str(message.chat.id)]
        total=0
        mensaje_recibo='El valor de su pedido es: \n'
        print(f"Información del cliente {str(message.chat.id)}:")
        for producto, cantidad in moneda['producto'].items():
            # si se quiere agregar el id del chat se pone en el constructor del objeto
            cliente = DB.DBManager(moneda['nombre'],moneda['cedula'],moneda['celular'],moneda['direccion'],moneda['correo'],producto,cantidad)
            print(f"Nombre: {moneda['nombre']}")
            print(f"Cédula: {moneda['cedula']}")
            print(f"Dirección: {moneda['direccion']}")
            print(f"Correo: {moneda['correo']}")
            print(f"  - Producto: {producto}")
            print(f"    Cantidad: {cantidad}")
            print("_"*20)
            if producto == "Camiseta":
                var=valor_camiseta
            elif producto == "Medias":
                var=valor_medias
            elif producto == "Chompas":
                var=valor_chompas
            elif producto == "Boxer":
                var=valor_boxer
            elif producto == "Zapatos":
                var=valor_zapatos
            mensaje_recibo += f'{producto}: ${int(cantidad)*var}\n'
            total=int(cantidad)*var+total
            
            cliente.AlmacenarNombre()
            cliente.Write()
    else:
        print(f"No se encontraron datos para la clave {message.chat.id}.")
    print(mensaje_recibo)
    mensaje_recibo += f'{"_"*15}\n'
    mensaje_recibo += f'Total: ${total}\n'
    bot.send_message(message.chat.id, text=mensaje_recibo)
    mensaje_agradecimiento(message)
    
#----------------------------------------------------------------------------------------------------------
                                          ##FIN DEL CODIGO    
def mensaje_agradecimiento(message):
    bot.send_message(message.chat.id, 'Gracias por visitar nuestra tienda, a la orden en cualquier otro momento')
    if str(message.chat.id) in datos:   
        datos.pop(str(message.chat.id))
    if str(message.chat.id) in articulo: 
        articulo.pop(str(message.chat.id))

if __name__=='__main__':
    print('Iniciandiando el bot')
    bot.infinity_polling()
    print("Fin")