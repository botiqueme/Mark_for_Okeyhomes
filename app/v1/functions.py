# import phonenumbers
# from phonenumbers import carrier
# from phonenumbers.phonenumberutil import number_type
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import mailsender
# import utils

def take_appointment():
    return
# def take_appointment(phone_number=None):
#     print('funzione take_appointments called')
#     try:
#         phone_number = phonenumbers.parse(phone_number, None)
#     except phonenumbers.NumberParseException:
#         try:
#             phone_number = phonenumbers.parse(phone_number, "IT")
#         except phonenumbers.NumberParseException:
#             return 'Ho bisogno di un numero di telefono per poter ricontattare'
#
#     try:
#         val1 = phonenumbers.is_possible_number(phone_number)
#     except phonenumbers.NumberParseException:
#         val1 = False
#         return 'Il numero di telefono non è valido, numero di cifre non corretto'
#
#     try:
#         val2 = phonenumbers.is_valid_number(phone_number)
#     except phonenumbers.NumberParseException:
#         val2 = False
#         return 'E\' necessario fornire un numero di telefono per poter essere ricontattati'
#
#     if val1 and val2:
#
#         try:
#             appointment_date = utils.get_apointment()
#         except Exception as e:
#             print('Exception in get_apointment: ', e)
#         try:
#             mailsender.send_email(f'Appuntamento telefonico fissato per il giorno {appointment_date.strftime("%d/%m/%Y")} alle ore {appointment_date.strftime("%H:%M")} al numero {phone_number}')
#         except Exception as e:
#             print('Exception in send_email: ', e)
#
#         return f'Grazie. Appuntamento telefonico fissato per il giorno {appointment_date.strftime("%d/%m/%Y")} alle ore {appointment_date.strftime("%H:%M")} al numero {phone_number}'
