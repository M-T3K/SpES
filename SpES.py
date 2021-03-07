# This is a web scrapping tool to obtain information for the spanish MAEC
# (Ministerio de Asuntos Exteriores, Unión Europea, y Cooperación)
# In particular, the task is to obtain the emails of every embassy
# List of full consulates & embassies is available at
# http://www.exteriores.gob.es/Portal/es/ServiciosAlCiudadano/Documents/Registromatricula.pdf

# Format of embassy websites with contact is:
# http://www.exteriores.gob.es/Embajadas/{CITY_NAME}/es/Embajada/Paginas/Directorio.aspx

import requests
from time import sleep
from  urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import time
from bs4 import BeautifulSoup

# List of all embassies and consulates of Spain in other nations
embs = [
        'kabul',
        'tirana',
        'berlin',
        'andorra',
        'riadh',
        'argel',
        'oran', 
        'bahiablanca',
        'buenosaires',
        'cordoba',
        'mendoza',
        'rosario',
        'canberra',
        'melbourne',
        'sydney',
        'viena',
        'dhaka',
        'bruselas',
        'lapaz',
        'santacruzdelasierra',
        'sarajevo',
        'brasilia',
        'portoalegre',
        'riodejaneiro',
        'salvadorbahia',
        'saopaulo',
        'sofia',
        'praia',
        'yaunde',
        'montreal',
        'otawa',
        'toronto',
        'santiagodechile',
        'canton',
        'hongkong',
        'pekin',
        'shanghai',
        'nicosia',
        'bogota',
        'seul',
        'abidjan',
        'sanjosedecostarica',
        'zagreb',
        'lahabana',
        'copenhague',
        'quito',
        'guayaquil',
        'elcairo',
        'sansalvador',
        'abudhabi',
        'liubliana',
        'boston',
        'chicago',
        'houston',
        'losangeles',
        'miami',
        'nuevayork',
        'sanfrancisco',
        'washington',
        'tallin',
        'addisabeba',
        'manila',
        'helsinki',
        'bayona',
        'burdeos',
        'estrasburgo',
        'lyon',
        'marsella',
        'montpellier',
        'paris',
        'pau',
        'perpinan',
        'toulouse',
        'libreville',
        'accra',
        'atenas',
        'guatemala',
        'conakry',
        'bissau',
        'bata',
        'malabo',
        'puertoprincipe',
        'tegucigalpa',
        'budapest',
        'nuevadelhi',
        'mumbay',
        'yakarta',
        'teheran',
        'bagdad',
        'dublin',
        'telaviv',
        'milan',
        'napoles',
        'roma',
        'kingston',
        'tokio',
        'jerusalen',
        'amman',
        'astana',
        'nairobi',
        'kuwait',
        'riga',
        'beirut',
        'tripoli',
        'vilnius',
        'luxemburgo',
        'skopjie',
        'kualalumpur',
        'bamako',
        'lavaleta',
        'agadir',
        'casablanca',
        'larache',
        'nador',
        'rabat',
        'tanger',
        'tetuan',
        'nouadhibu',
        'nouakchott',
        'guadalajara',
        'mexico',
        'monterrey',
        'maputo',
        'windhoek',
        'managua',
        'niamey',
        'abuja',
        'lagos',
        'oslo',
        'wellington',
        'mascate',
        'amsterdam',
        'islamabad',
        'panama',
        'asuncion',
        'lima',
        'varsovia',
        'lisboa',
        'oporto',
        'sanjuandepuertorico',
        'doha',
        'edimburgo',
        'londres',
        'praga',
        'kinshasa',
        # 'santodomingo',
        'bratislava',
        'bucarest',
        'moscu',
        'sanpetersburgo',
        'dakar',
        'belgrado',
        'singapur',
        'damasco',
        'ciudaddelcabo',
        'pretoria',
        'jartum',
        'estocolmo',
        'berna',
        'ginebra',
        'zurich',
        'bangkok',
        'daressalaam',
        'puertoespana',
        'tunez',
        'ankara',
        'estambul',
        'kiev',
        'montevideo',
        'caracas',
        'hanoi',
        'harare'
        ]


urls = [
        "http://www.exteriores.gob.es/Embajadas/{CITY_NAME}/es/Embajada/Paginas/HorariosLocalizacionContacto.aspx",
        "http://www.exteriores.gob.es/Embajadas/{CITY_NAME}/es/Embajada/Paginas/Directorio.aspx",
        "http://www.exteriores.gob.es/Consulados/{CITY_NAME}/es/Consulado/Paginas/Localizaci%C3%B3n.aspx",
        "http://www.exteriores.gob.es/Consulados/{CITY_NAME}/es/Consulado/Paginas/LocalizacionContacto.aspx"
]

# @info This is necessary to avoid 403 forbidden error, it is the latest chrome agent
# @info Obtained from http://www.useragentstring.com/index.php?id=19919
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36' }
mail_list = []
# test_exit = 1
for emb in embs:
        print("####################### %s #######################" % emb)
        for url in urls:
                url_new = url.format(CITY_NAME = emb)
                pred_complete = True
                pred_useful = True
                print(url_new)
                req = Request(url=url_new, headers=headers)
                try:
                        with urlopen(req) as res:
                                html_bytes = res.read()
                                html = html_bytes.decode("utf-8")
                                soup = BeautifulSoup(html, features="html.parser")
                                mails = soup.select('a[href^=mailto]')
                                for m in mails:
                                        data=m['href']
                                        try:
                                                useless, mail = data.split(':')
                                        except ValueError:
                                                break
                                        # END
                                        # Mails dont start with '.' so if that's the case, it is possibly incomplete
                                        if mail[0] == '.':
                                                print("Possibly incomplete email address. Attempting reconstruction.")
                                                # It is probably incomplete, we attempt to find new text
                                                fix = soup.body.findAll(text="emb.{CITY_NAME}".format(CITY_NAME=emb))
                                                for f in fix:
                                                        print("Attemted mail reconstruction: %s -> %s%s" % (mail, f, mail))
                                                        mail = "{0}{1}".format(f, mail)
                                                        break # Doing this more times is redundant, although we could be missing email addresses
                                                # END
                                                pred_complete = False
                                        # Diplomatic emails will generally use the city's name in their emails.
                                        if not emb in mail:
                                                pred_useful = False
                                        print(mail)
                                        # Comma Separated Values
                                        info = "{emb}, {mail}, {url}, {complete}, {useful}".format(emb=emb, mail=mail, url=url_new, complete=pred_complete, useful=pred_useful)
                                        mail_list.append(info)
                                # END
                        # END
                except URLError as e:
                        print("ERROR: ", e.reason)
                # END
                sleep(1) # We sleep for a second to avoid getting flagged
        # END
        # @debug
        # test_exit -= 1
        # if test_exit <= 0:
        #         break
        # END
        # @debug end
# END

# Remove Duplicates
final = set()
result_list = []
for i in mail_list:
        if i not in final:
                final.add(i)
                result_list.append(i)
        # END
# END

with open("results.csv", 'w') as results_file:
        results_file.writelines(["%s\n" % ln for ln in result_list])
# END 