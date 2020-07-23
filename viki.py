#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# 5

from resources.lib.gui.hoster import cHosterGui 
from resources.lib.gui.gui import cGui 
from resources.lib.handler.inputParameterHandler import cInputParameterHandler 
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler 
from resources.lib.handler.requestHandler import cRequestHandler 
from resources.lib.parser import cParser 
from resources.lib.comaddon import progress, VSlog, xbmc ,dialog
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.comaddon import dialog
import re


import sys
import os
import time
import urllib
import urllib2
import json
from hashlib import sha1
import hmac
import binascii
import xbmc

import xbmcgui
import xbmcplugin
import xbmcaddon
#

# Support for fan channels
fc='false'

# first langage
se='true'#activation ou non de sous titre autre que anglais si false english sub

#!! request with en give  more result
lang='en'

language = 'English'

#lang='fr'

#language = 'French'

# quality : video quality
# probleme non resolue dash file avec
# quality ='2'
# quality ='3'

# fichier mp4
quality ='4'#

iconimage=None

#Définissez l'ordre des épisodes


MUA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/ 604.1.21 (KHTML, like Gecko) Version/ 12.0 Mobile/17A6278a Safari/602.1.26' 
UA = 'Mozilla/5.0 (Macintosh; MacOS X10_14_3; rv;67.0) Gecko/20100101 Firefox/67.0' 



SITE_IDENTIFIER = 'viki'# 
SITE_NAME = '[COLOR skyblue]A tester viki 001[/COLOR]'
SITE_DESC = ' viki ' 


URL_MAIN= 'https://www.viki.com/'

URLMAIN_API='https://api.viki.io/v4/'
MOVIE_GENRES=(True, 'showMovieGenre')
MOVIE_PAYS = (True, 'showMoviePays')

MOVIE_NEW =    (URLMAIN_API+ 'movies.json?sort=newest_video&page=1&per_page=50&app=100000a&t=', 'showMovies')
MOVIE_RECENT = (URLMAIN_API+ 'movies.json?sort=views_recent&page=1&per_page=50&app=100000a&t=', 'showMovies')
MOVIE_POPULAR =(URLMAIN_API+ 'movies.json?sort=trending&page=1&per_page=50&app=100000a&t=', 'showMovies')
MOVIE_BEST =   (URLMAIN_API+ 'movies.json?sort=views&page=1&per_page=50&app=100000a&t=', 'showMovies')

#tous meme resultats que news
#https://api.viki.io/v4/movies.json?&page=1&per_page=50&app=100000a&t=#



SERIE_GENRES=(True, 'showSerieGenre')
SERIE_PAYS = (True, 'showSeriePays')

SERIE_NEW=  (URLMAIN_API+'series.json?sort=newest_video&page=1&per_page=50&app=100000a&t=', 'showMovies')
SERIE_RECENT=  (URLMAIN_API+'series.json?sort=views_recent&page=1&per_page=50&app=100000a&t=', 'showMovies')
SERIE_POPULAR=  (URLMAIN_API+'series.json?sort=trending&page=1&per_page=50&app=100000a&t=', 'showMovies')
SERIE_BEST=  (URLMAIN_API+'series.json?sort=views&page=1&per_page=50&app=100000a&t=', 'showMovies')

URL_SEARCH = (URLMAIN_API + 'search.json?page=1&per_page=50&app=100000a&term=', 'showMovies')#m000
FUNCTION_SEARCH = 'showMovies'
#MOVIE_NEWS = (URL_MAIN , 'showMovies')

def load(): 
   
    oGui = cGui() 
    
    oOutputParameterHandler = cOutputParameterHandler() #appelle la fonction pour sortir un parametre
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') # sortie du parametres siteUrl n'oubliez pas la Majuscule
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSerie', 'Séries', 'series.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory() 
 
 
def showMenuMovies():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PAYS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_PAYS[1], 'Films (Pays)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEW[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEW[1], 'Films (News)', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_RECENT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_RECENT[1], 'Films (Récents)', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_POPULAR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_POPULAR[1], 'Films (Poulaires)', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BEST[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BEST[1], 'Films (Best)', 'genres.png', oOutputParameterHandler)
    
    
    
    oGui.setEndOfDirectory()
    
def showMenuSerie():
    
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Serie (Genres)', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_PAYS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_PAYS[1], 'Series (Pays)', 'genres.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEW[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEW[1], 'Series (News)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_RECENT[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_RECENT[1], 'Series (Recent)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_POPULAR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_POPULAR[1], 'Series (Populaire)', 'genres.png', oOutputParameterHandler)


    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_BEST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_BEST[1], 'Series (Best)', 'genres.png', oOutputParameterHandler)
    
    
    oGui.setEndOfDirectory()   
    
 
    
def showSearch(): 
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()       
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText  
        showMovies(sUrl)                    
        oGui.setEndOfDirectory()
        return


def showMovies(sSearch=''):       
    
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    if sSearch:
        sUrl = sSearch
        
    url=sUrl
    VSlog('showMovies ')
    timestamp = str(int(time.time()))
    
    if not 'search.json' in url:
        url=url+timestamp

    VSlog('showMovies ')
    VSlog('# request = ' +url)
    
    if(True) :
        
        oRequestHandler = cRequestHandler(url)
        oRequestHandler.addHeaderEntry('User-Agent',UA)
        oRequestHandler.addHeaderEntry('Accept-Language', '')  #result en anglais par default 
        sJsonContent = oRequestHandler.request()
        jsonrsp  = json.loads(sJsonContent)
    
    else :
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        opener = urllib2.build_opener()
        f = opener.open(req)
        jsonrsp = json.loads(f.read())
    
    
    for movie in range(0, len(jsonrsp['response'])): # change 
        try:
            if (jsonrsp['response'][movie]['flags']['licensed'] == True ):   
                if jsonrsp['response'][movie]['type'] == 'series': 
                    
                    #sTitle=str(jsonrsp['response'][movie]['titles']['fr'].encode('utf-8', 'ignore'))
                    #sTitle=str(jsonrsp['response'][movie]['titles']['en'].encode('utf-8', 'ignore'))
                    sTitle=jsonrsp['response'][movie]['titles']['en']
                    #sTitle=jsonrsp['response'][movie]['titles']['fr']
                    
                    sThumb=jsonrsp['response'][movie]['images']['poster']['url']#120ko
                    #sThumb=jsonrsp['response'][movie]['images']['atv_cover']['url'] #with tag 800 ko
                    
                    #link to saison
                    sUrl2='https://api.viki.io/v4/series/'+ jsonrsp['response'][movie]['id'] + '/episodes.json?page=1&per_page=50&app=100000a&t=' +str(timestamp)
                    
                    #serie movie with descriptions
                    sDesc=jsonrsp['response'][movie]['descriptions']['fr'].encode('utf-8', 'ignore')
                    #sDesc=jsonrsp['response'][movie]['descriptions']['en'].encode('utf-8', 'ignore')
                    
                    sDisplayTitle=sTitle
                    #addDir(jsonrsp['response'][movie]['titles']['en'].encode('utf-8', 'ignore'),'https://api.viki.io/v4/series/'+jsonrsp['response'][movie]['id']+'/episodes.json?page=1&per_page=50&app=100000a&t='+timestamp,jsonrsp['response'][movie]['descriptions']['en'].encode('utf-8', 'ignore'),2,jsonrsp['response'][movie]['images']['poster']['url'])
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oOutputParameterHandler.addParameter('sDesc', sDesc)
                    oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
                
                
                else: 
                    # 
                    if (jsonrsp['response'][movie]['blocked'] == False ): 
                       
                        try:    # 
                            subtitle_completion1 = '0'
                            subtitle_completion1 = str(jsonrsp['response'][movie]['subtitle_completions']['fr'])
                        except:
                            pass
                        try: 
                            subtitle_completion2 = '0'
                            subtitle_completion2 = str(jsonrsp['response'][movie]['subtitle_completions']['en'])
                        except:
                            pass
                        try: 
                            dur = ''
                            dur = str(jsonrsp['response'][movie]['duration'])
                        except:
                            pass
                        try: #Résolution flag hd  yes or no
                            hd = 'False'
                            hd = str(jsonrsp['response'][movie]['flags']['hd'])
                        except:
                            pass
                        try: #pas de description trouvé pour les movies on utilise le titres
                            mt = ''
                            mt = jsonrsp['response'][movie]['titles']['fr'] # 
                        except:
                            pass
                        try: 
                            at = ''
                            at = jsonrsp['response'][movie]['author']
                        except:
                            pass
                        try: 
                            rating = 'G'
                            rating = jsonrsp['response'][movie]['rating']
                        except:
                            pass
                        try: 
                            ar = '0'
                            ar = str(jsonrsp['response'][movie]['container']['review_stats']['average_rating'])
                        except:
                            pass
                        
                        try: # lien web link pour verifier
                            sUrlweb = 'weblink'
                            #VSlog('url web=' +sUrlweb)
                            sUrlweb= str(jsonrsp['response'][movie]['container']['url']['web'])
                        except:
                            pass
                        
        
                        VSlog('')
                        VSlog(sUrlweb)#real link
                        VSlog('title  ' +jsonrsp['response'][movie]['titles']['en'])
                        VSlog('link url  '+jsonrsp['response'][movie]['id']+'@'+jsonrsp['response'][movie]['images']['poster']['url']+'@'+subtitle_completion1+'@'+subtitle_completion2+'@'+mt)
                        VSlog('desc'+ ' duration=' +dur + ' HD ? ='+ hd + ' description ='+ mt +' author='+ at +' rating='+rating +' evaluation='+ar)
                        
                        sTitle=str(jsonrsp['response'][movie]['titles']['en'].encode('utf-8', 'ignore'))
                        sThumb=str(jsonrsp['response'][movie]['images']['poster']['url'])
                        sUrlapi=str(jsonrsp['response'][movie]['id']+'@'+jsonrsp['response'][movie]['images']['poster']['url']+'@'+subtitle_completion1+'@'+subtitle_completion2+'@'+mt)
                        
                        sDesc=str(mt)
                        
                        VSlog(' ' )
                        VSlog('title  ' +sTitle )
                        VSlog('sThumb=  ' +sThumb )
                        VSlog('link urlapi=  ' +sUrlapi )
                        VSlog('link urlweb=  ' +sUrlweb )
                        VSlog('sdesc=  ' +str(mt))
                        
                        
                        sDisplayTitle=sTitle
                        #infos 
                        #jsonrsp['response'][movie]['titles']['en'],
                        #jsonrsp['response'][movie]['id']+'@'+jsonrsp['response'][movie]['images']['poster']['url']+'@'+subtitle_completion1+'@'+subtitle_completion2+'@'+mt
                        #,dur,hd,mt,at,rating,ar,4,jsonrsp['response'][movie]['images']['poster']['url'])
                        
                        
                        oOutputParameterHandler = cOutputParameterHandler()
                        oOutputParameterHandler.addParameter('siteUrl', sUrlapi)
                        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                        oOutputParameterHandler.addParameter('sThumb', sThumb)
                        oOutputParameterHandler.addParameter('sDesc', sDesc)
                        
                        
                        oGui.addMovie(SITE_IDENTIFIER, 'Showlinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)   
                        #addLink(jsonrsp['response'][movie]['titles']['en'],jsonrsp['response'][movie]['id']+'@'+jsonrsp['response'][movie]['images']['poster']['url']+'@'+subtitle_completion1+'@'+subtitle_completion2+'@'+mt,dur,hd,mt,at,rating,ar,4,jsonrsp['response'][movie]['images']['poster']['url'])
                        
                        
                        ##addLink(jsonrsp['response'][movie]['titles']['en'],jsonrsp['response'][movie]['id']+'@'+jsonrsp['response'][movie]['images']['poster']['url']+'@'+subtitle_completion1+'@'+subtitle_completion2,jsonrsp['response'][movie]['duration'],hd,mt,at,rating,ar,4,jsonrsp['response'][movie]['images']['poster']['url'])
        
        
        except:
            pass
   
    
    
    if jsonrsp['more'] == True:
        getpage=re.compile('(.+?)&page=(.+?)&per_page=(.+?)&t=').findall(url)
        for fronturl,page, backurl in getpage:
            newpage = int(page)+1
            url = fronturl + '&page=' + str(newpage) + '&per_page=' + backurl + '&t='
            #print 'URL OF THE NEXT PAGE IS' + url
            #addDir('Next page >>',url,'',1,md+'DefaultFolder.png')
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', url)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:  # Le moteur de recherche du site est correct, laisser le nextPage même en globalSearch
        oGui.setEndOfDirectory()



def showSaisons(): 
        
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    
     
    url=sUrl 
    #url=url+ '&direction=desc'
    url=url+ '&direction=asc'
    timestamp = str(int(time.time()))

    VSlog('showSaisons()')
    VSlog('# request = '+url)
    #req = urllib2.Request('https://api.viki.io/v4/series/36557c/episodes.json?page=1&per_page=50&app=100000a&t=1594571874&direction=desc')
    
    if True :
        oRequestHandler = cRequestHandler(url)
        oRequestHandler.addHeaderEntry('User-Agent',UA)
        oRequestHandler.addHeaderEntry('Accept-Language', '')
        sJsonContent = oRequestHandler.request()
        jsonrsp  = json.loads(sJsonContent)
    else:
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        opener = urllib2.build_opener()
        f = opener.open(req)
        jsonrsp = json.loads(f.read())

    #infos
    #jsonrsp['response'][0]['number']
    #jsonrsp['response'][episode]['rating']
    #jsonrsp['response'][episode]['author']
    #jsonrsp['response'][episode]['titles']['en']
    #jsonrsp['response'][episode]['container']['review_stats']['average_rating']
    
    #VSlog(len(jsonrsp['response']))
    
    for episode in range(0, len(jsonrsp['response'])):
        VSlog('passed1')
        try:
            VSlog('passed2')
            if (jsonrsp['response'][episode]['blocked'] == False ):
                
                VSlog('blocked falsed')
                try: # sub 1 : select  'lang' subtitles
                    subtitle_completion1 = '0'
                    subtitle_completion1 = str(jsonrsp['response'][episode]['subtitle_completions']['fr'])
                except:
                    pass
                try: # sub 2 :English subtitles
                    subtitle_completion2 = '0'
                    subtitle_completion2 = str(jsonrsp['response'][episode]['subtitle_completions']['en'])
                except:
                    pass
                try: #  sbool: video resolution is hd ?
                    hd = 'False'
                    hd = str(jsonrsp['response'][episode]['flags']['hd'])
                except:
                    pass
                try: #c
                    et = ''
                    et = jsonrsp['response'][episode]['titles']['en']
                except:
                    pass
                try: 
                    at = ''
                    at = jsonrsp['response'][episode]['author']
                except:
                    pass
                try: 
                    rating = 'G'
                    rating = jsonrsp['response'][episode]['rating']
                except:
                    pass
                
                sTitle=jsonrsp['response'][episode]['container']['titles']['en']+' Episode '+str(jsonrsp['response'][episode]['number']) 
                sUrl=str(jsonrsp['response'][episode]['id']+'@'+jsonrsp['response'][episode]['images']['poster']['url']+'@'+subtitle_completion1+'@'+subtitle_completion2+'@'+et)
               
                #VSlog('sTitle='+'sTitle')
                #VSlog('sUrl='+sUrl)
                
                
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oGui.addEpisode(SITE_IDENTIFIER, 'Showlinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
                #infos :
                #jsonrsp['response'][episode]['container']['titles']['en'].encode('utf-8', 'ignore')+' Episode '+str(jsonrsp['response'][episode]['number']),
                #jsonrsp['response'][episode]['id']+'@'+jsonrsp['response'][episode]['images']['poster']['url']+'@'+subtitle_completion1+'@'+subtitle_completion2+'@'+et,
                #jsonrsp['response'][episode]['duration'],hd,et,at,rating,str(jsonrsp['response'][episode]['container']['review_stats']['average_rating']),
                #jsonrsp['response'][episode]['images']['poster']['url'])
        
            else:
                VSlog('block =true')
                
        except:
            VSlog('excepted ')
            pass
    
    if len(jsonrsp['response'])==0:
        VSlog('There are no episodes ')
    
    
    if jsonrsp['more'] == True:
        getpage=re.compile('(.+?)page=(.+?)&per_page').findall(url)
        for fronturl,page in getpage:
            newpage = int(page)+1
            url = fronturl + 'page=' + str(newpage) + '&per_page=50&app=100000a&t=' + timestamp
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', url)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page >>>[/COLOR]', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieGenre():
    oGui = cGui()
    
    
    showgenre='movies'
    url='https://api.viki.io/v4/videos/genres.json?app=100000a'
    
    VSlog('def GENRE')
    VSlog('GENRE = '+ showgenre)
    VSlog('# request url = '+ url) #def GENRE url = movies
    
    
    
    
    if True :
        oRequestHandler = cRequestHandler(url)
        oRequestHandler.addHeaderEntry('User-Agent',UA)
        oRequestHandler.addHeaderEntry('Accept-Language', '')
        sJsonContent = oRequestHandler.request()
        jsonrsp  = json.loads(sJsonContent)
    else:
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        opener = urllib2.build_opener()
        f = opener.open(req)
        jsonrsp = json.loads(f.read())
    
    for genre in range(0, len(jsonrsp)):
        
        typegenre=jsonrsp[genre]['name']['fr']  # or jsonrsp[genre]['name']['en']
        urlgenre='https://api.viki.io/v4/'+showgenre+'.json?sort=newest_video&page=1&per_page=50&app=100000a&genre='+jsonrsp[genre]['id']+'&t='
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', urlgenre)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', typegenre.capitalize(), 'genres.png', oOutputParameterHandler)
        VSlog(str(genre))
        VSlog(jsonrsp[genre]['name']['fr'])
        VSlog('https://api.viki.io/v4/'+showgenre+'.json?sort=newest_video&page=1&per_page=50&app=100000a&genre='+jsonrsp[genre]['id']+'&t=')
    
    oGui.setEndOfDirectory()


def showSerieGenre():
    oGui = cGui()
    
    showgenre='series'
    url='https://api.viki.io/v4/videos/genres.json?app=100000a'
    
    VSlog('def GENRE')
    VSlog('GENRE = '+ showgenre)
    VSlog('# request url = '+ url) #def GENRE url = movies
    
    if True :
        oRequestHandler = cRequestHandler(url)
        oRequestHandler.addHeaderEntry('User-Agent',UA)
        oRequestHandler.addHeaderEntry('Accept-Language', '')
        sJsonContent = oRequestHandler.request()
        jsonrsp  = json.loads(sJsonContent)
    else :
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        opener = urllib2.build_opener()
        f = opener.open(req)
        jsonrsp = json.loads(f.read())
    
    for genre in range(0, len(jsonrsp)):
       
        urlgenre='https://api.viki.io/v4/'+showgenre+'.json?sort=newest_video&page=1&per_page=50&app=100000a&genre='+jsonrsp[genre]['id']+'&t='
        typegenre=jsonrsp[genre]['name']['fr']
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', urlgenre )
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', typegenre.capitalize(), 'genres.png', oOutputParameterHandler)
        
        VSlog(jsonrsp[genre]['name']['fr'])
        VSlog('https://api.viki.io/v4/'+showgenre+'.json?sort=newest_video&page=1&per_page=50&app=100000a&genre='+jsonrsp[genre]['id']+'&t=')
    
    oGui.setEndOfDirectory()


def showMoviePays():
    showPays('movies')


def showSeriePays():
    showPays('series')


def showPays(genre):
    
    
    oGui = cGui()
    url='https://api.viki.io/v4/videos/countries.json?app=100000a'
    VSlog('showPays')
    VSlog('GENRE = '+ genre)
    VSlog('# request url = '+ url) #def GENRE url = movies
    
    bAciveBlackList=True
    
    
    if True :
        oRequestHandler = cRequestHandler(url)
        oRequestHandler.addHeaderEntry('User-Agent',UA)
        oRequestHandler.addHeaderEntry('Accept-Language', '')
        sJsonContent = oRequestHandler.request()
        jsonrsp  = json.loads(sJsonContent)
    else :
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        opener = urllib2.build_opener()
        f = opener.open(req)
        jsonrsp = json.loads(f.read())
   
    #site ou il n'y a jamais rien
    
    sBlaccountryList = ['none']
    if genre == 'movies': #
        sBlaccountryList = ['tw' , 'ca', 'us','gb' , 'th', 'ph','es']
    
        
    #if genre=='series': ## repertoire non vide
        #sBlaccountryList = ['gounlimited' , 'upstream', 'ddownload.com']
    
    
    
    #for country, subdict in jsonrsp.iteritems(): #  ok for generator methode on python2.7 but with  python3 ?!
    for country, subdict in jsonrsp.items():      #  so use a simple list of tuple items methode for compatible features     
            
            if ( bAciveBlackList) and (country in sBlaccountryList):
                VSlog(True)
                continue
            
                urlcountry='https://api.viki.io/v4/'+genre+'.json?sort=newest_video&page=1&per_page=50&app=100000a&origin_country='+country+'&t='
                #testecountry(urlcountry)
                country=jsonrsp[country]['name']['en']
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', urlcountry)
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', country.capitalize(), 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


#only for blacklist
def testecountry(url):
    VSlog('')
    VSlog('teste pays')
   
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent',UA)
    oRequestHandler.addHeaderEntry('Accept-Language', '')  #result en anglais par default 
    sJsonContent = oRequestHandler.request()
    jsonrsp  = json.loads(sJsonContent)
   
    #for urlcountry
    var1,var2,var3,var4,country,var6=url.split('&')
    
    VSlog(url)
    VSlog(country)
    for movie in range(0, len(jsonrsp['response'])): # change 
        nb=len(jsonrsp['response'])
        if nb >= 0 :
            VSlog('Find element '+ str(nb))
            return
    VSlog('no Find element')
    return 
    
#Signature des demandes au nom de Flash player
def SIGN(url,pth):
    
    #timestamp = str(int(time.time()))
    #key = '-$iJ}@p7!G@SyU/je1bEyWg}upLu-6V6-Lg9VD(]siH,r.,m-r|ulZ,U4LC/SeR)'
    #rawtxt = '/v4/videos/'+url+pth+'?app=65535a&t='+timestamp+'&site=www.viki.com'
    #hashed = hmac.new(key, rawtxt, sha1)
    #fullurl = 'https://api.viki.io' + rawtxt+'&sig='+binascii.hexlify(hashed.digest())
    #return fullurl
    
    timestamp = str(int(time.time()))
    key = 'MM_d*yP@`&1@]@!AVrXf_o-HVEnoTnm$O-ti4[G~$JDI/Dc-&piU&z&5.;:}95=Iad'
    rawtxt = '/v4/videos/'+url+pth+'?app=100005a&t='+timestamp+'&site=www.viki.com'
    hashed = hmac.new(key, rawtxt, sha1)
    fullurl = 'https://api.viki.io' + rawtxt+'&sig='+binascii.hexlify(hashed.digest())
    return fullurl    
    
    

def GET_SUBTILES(url,subtitle_completion1,subtitle_completion2):
        
    try:                                           
        srtsubs_path1 = xbmc.translatePath('special://temp/vstream.viki.French.srt')
        srtsubs_path2 = xbmc.translatePath('special://temp/vstream.viki.English.srt')
        if (int(subtitle_completion1)>79 and se=='true'): 
            urlreq=SIGN(url,'/subtitles/fr.srt')
            
            req = urllib2.Request(urlreq)
            
            req.add_header('User-Agent', UA)
            response = urllib2.urlopen(req)
            data=response.read()
            response.close()
            
            with open(srtsubs_path1, "w") as subfile:
                subfile.write(data)
                sub = 'true'                                

        if (int(subtitle_completion2)>0 and se=='true'):  
            urlreq=SIGN(url,'/subtitles/en.srt')
            req = urllib2.Request(urlreq)
            
            req.add_header('User-Agent', UA)
            response = urllib2.urlopen(req)
            data=response.read()
            response.close()
            
            with open(srtsubs_path2, "w") as subfile:
                subfile.write(data)
                sub = 'true'
        else:
            sub = 'false' 
            #xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('VIKI®','Subtitles not available or disabled', 4000, md+'DefaultAddonSubtitles.png'))
            VSlog('no subtitles availables')
    except:
        pass
    
    
    return srtsubs_path1,srtsubs_path2 
   
  
def GET_URLS_STREAM(url):

    qlist=['480p','360p','240p','mpd']
    #
    streamUrllist=[]
    validq=[]
    #voir pour le debug
    debug='false'
    if (debug == 'false'):     
        urlreq=SIGN(url,'/streams.json')
        #VSlog('request for streams url =' + urlreq )
        req = urllib2.Request(urlreq)
        
        req.add_header('User-Agent', UA)
        opener = urllib2.build_opener()
        f = opener.open(req)
        jsonrsp = json.loads(f.read())
        
        #  extract url for each q
        for qual in qlist :
            basehttp='https'
            if qual in jsonrsp :   
                if qual=='mpd': # pfou... ne marche pas
                    basehttp='http'    
                streamUrllist.append(jsonrsp[qual][basehttp]['url'] )
                validq.append(qual)
        
    #
    else:
        pass
        #xbmc.executebuiltin("Notification(VIKI®,Debug mode is no longer supported <!>,8000)")
        #VSlog('Debug mode is no supported ')
    
    
    return validq,streamUrllist

    
    

def GET_INFO_PLAY(name,url,iconimage):
    
    #name='Romantic Warriors'
    #url='1164653v'
    
    url, thumbnail, subtitle_completion1, subtitle_completion2, plot = url.split("@")#url, thumbnail, subtitle_completion1, subtitle_completion2 = url.split("@")
   
    try:                                            #Si nous avons traduit plus de 79% des sous-titres dans notre langue
        srtsubs_path1 = xbmc.translatePath('special://temp/vstream.viki.French.srt')
        srtsubs_path2 = xbmc.translatePath('special://temp/vstream.viki.English.srt')
        
        if (int(subtitle_completion1)>79 and se=='true'): #Ако имаме преведени над 79% субтитри на нашия език
            
            #use elif srtsubs_path
            srtsubs_path = xbmc.translatePath('special://temp/vstream.viki.French.fr')
            
            
            #xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('VIKI®',language+' subtitles at '+subtitle_completion1+'%', 4000, md+'DefaultAddonSubtitles.png')) 
            
            #req = urllib2.Request(SIGN(url,'/subtitles/'+lang+'.srt'))
            
            #urlreq=SIGN(url,'/subtitles/'+lang+'.srt')
            urlreq=SIGN(url,'/subtitles/fr.srt')
            
            req = urllib2.Request(urlreq)
            
            req.add_header('User-Agent', UA)
            response = urllib2.urlopen(req)
            data=response.read()
            response.close()
            
            with open(srtsubs_path1, "w") as subfile:
                subfile.write(data)
                sub = 'true'                                #Nous passons aux sous-titres anglais
        #elif (int(subtitle_completion2)>0 and se=='true'): #Превключваме към английски субтитри
        if (int(subtitle_completion2)>0 and se=='true'):  
            
            #use elif srtsubs_path
            #srtsubs_path = xbmc.translatePath('special://temp/vstream.vikir.English.srt')
            
           
            #xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('TESTER VIKI®','English subtitles at '+subtitle_completion2+'%', 4000, md+'DefaultAddonSubtitles.png'))
            
            #req = urllib2.Request(SIGN(url,'/subtitles/en.srt'))
            urlreq=SIGN(url,'/subtitles/en.srt')
            req = urllib2.Request(urlreq)
            
            req.add_header('User-Agent', UA)
            response = urllib2.urlopen(req)
            data=response.read()
            response.close()
            
            with open(srtsubs_path2, "w") as subfile:
                subfile.write(data)
                sub = 'true'
        else:
            sub = 'false' #Ако няма налични субтитри  #Si aucun sous-titre n'est disponible #
            #xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('VIKI®','Subtitles not available or disabled', 4000, md+'DefaultAddonSubtitles.png'))
            VSlog('Subtitles not available or disabled')
    except:
        pass
    
    rapi = 'true'
    
    # qualité existantes normalement dans le resultat de la requete streams.json
    qlist=['480p','360p','240p','mpd']
    #
    streamUrllist=[]
    validq=[]
    #if (debug == 'false' and rapi == 'true'):  
    VSlog('quality select = ' +str(quality))
    VSlog(' rapi == true')
    if (rapi == 'true'):     
        
        #req = urllib2.Request(SIGN(url,'/streams.json'))
        urlreq=SIGN(url,'/streams.json')
        #VSlog('request for streams url =' + urlreq )
        req = urllib2.Request(urlreq)
        
        req.add_header('User-Agent', UA)
        opener = urllib2.build_opener()
        f = opener.open(req)
        jsonrsp = json.loads(f.read())
        
        #  extract url for each q
        for qual in qlist :
            basehttp='https'
            if qual in jsonrsp :   
                if qual=='mpd': # pfou... ne marche pas
                    basehttp='http'    
                streamUrllist.append(jsonrsp[qual][basehttp]['url'] )
                validq.append(qual)
        
        #verifie list url
        #for urlstream in  streamlist:
            #VSlog('############'+urlstream)
        
        
        
        if '360p' in jsonrsp:
            if (quality == '3' or quality == '2'): #MPEG-DASH DYNAMIC MOBILE
                stream = jsonrsp['mpd']['http']['url'] #.replace('https','http')
                xbmc.executebuiltin("Notification(VIKI®,Dynamic Mobile Streaming: MPEG-DASH,2000)")
            #elif quality == '2': #MPEG-DASH 480p
                #stream = jsonrsp['480p']['https']['url'].replace('https','http').replace('v4.viki.io','http')
                #xbmc.executebuiltin("Notification(VIKI®,DASH Streaming: 480p,2000)")
            #elif quality == '1': #Direct MP4 360p
                #domain = re.search('//(.+?)/', jsonrsp['360p']['https']['url']).group(1)
                #stream = jsonrsp['360p']['https']['url'].replace(domain,'content.viki.com').replace('https','http')
                #xbmc.executebuiltin("Notification(VIKI®,MP4 Progressive Download,2000)")
            else: #Direct MP4 480p
                #domain = re.search('//(.+?)/', jsonrsp['480p']['https']['url']).group(1)
                stream = jsonrsp['480p']['https']['url'] #.replace(domain,'content.viki.com') #.replace('https','http')
                #stream = jsonrsp['360p']['https']['url']
                #stream = jsonrsp['240p']['https']['url']
                
                #xbmc.executebuiltin("Notification(VIKI®,MP4 Progressive Download,2000)")
                VSlog(' Link to copy')
                VSlog('stream'+str(stream))
                
        else:
            xbmc.executebuiltin("Notification(VIKI®,The addon needs rewriting!!!,2000)")
            VSlog('(VIKI®,The addon needs rewriting!!!,2000)')

    #Ако е разрешен дебъга Si le débogage est autorisé
    else:
        xbmc.executebuiltin("Notification(VIKI®,Debug mode is no longer supported <!>,8000)")
        VSlog('VIKI®,Debug mode is no longer supported <!>,8000)')
    
    srtsubs_path=srtsubs_path
    return validq,streamUrllist,str(stream),srtsubs_path1,srtsubs_path2 
    
    
    
    
    #xbmc.executebuiltin("Notification(VIKI®,setResolvedUrl")
    try:
        if 'dash' not in stream:
            stream = stream+'|verifypeer=false&User-Agent='+urllib.quote_plus(MUA)+'&Referer=https://www.viki.com'
        if 'dash' in stream:
            li.setMimeType('application/xml+dash')
            li.setContentLookup(False)
            li.setProperty('inputstreamaddon', 'inputstream.adaptive')
            li.setProperty('inputstream.adaptive.manifest_type', 'mpd')
            li.setProperty('inputstream.adaptive.stream_headers', 'verifypeer=false&User-Agent='+urllib.quote_plus(UA)+'&Referer=https://www.viki.com')
        #print stream
        li = xbmcgui.ListItem(iconImage=thumbnail, thumbnailImage=thumbnail, path=stream)
        li.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot } )
        
        
        #Задаване на субтитри, ако има такива или изключването им
        if sub=='true':
            li.setSubtitles([srtsubs_path])
            #while not xbmc.Player().isPlaying():
            #    xbmc.sleep(1000) #wait until video is being played
            #    xbmc.Player().setSubtitles(srtsubs_path)
        else:
            xbmc.Player().showSubtitles(False)

        sPluginHandle = cPluginHandler().getPluginHandle()
        xbmcplugin.setResolvedUrl(sPluginHandle, True, li)
        #xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
        
    except:
        xbmc.executebuiltin("Notification(VIKI®,Addon cannot play this Video <R>,2000)")
    
    return str(stream),srtsubs_path,srtsubs_path
         

def Showlinks():
    
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    
   
    namevik=None
    iconimagevik=None
    modevik=None
    
    namevik='Romantic Warriors'
    urlvik= '1164653v@https://6.vikiplatform.com/image/94c1b82232b94a6e95b5331458fa138a.jpg?x=b&a=0x0@100@100@Romantic Warriors'
    
    Datalist=[]
    #streamurlList=[]
    #qualityList=[]
    url, thumbnail, sub_pourcent1, sub_pourcent2, stitle = sUrl.split("@")
    ## teste
    #sSubPathFr2,sSubPathEn2 =GET_SUBTILES(sMovieTitle,sUrl,iconimagevik)
    if True:
        sSubPathFr2,sSubPathEn2 =GET_SUBTILES(url,sub_pourcent1,sub_pourcent2)
        qualityList2,streamList2=GET_URLS_STREAM(url)
        
        Datalist.append(sSubPathFr2)
        Datalist.append(sSubPathEn2)
        
        for item in  qualityList2:
            Datalist.append(item)  
        
        for item in  streamList2:
            Datalist.append(item)
            
    
        for objects in  Datalist:
            VSlog('Datalist teste 2'+ str(objects))
        
        
        oHoster = cHosterGui().checkHoster('viki')
        #oHoster = cHosterGui().checkHoster(sUrlparam)
        if (oHoster != False):
            
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            #cHosterGui().showHoster(oGui, oHoster, sUrlparam, sThumb)
            cHosterGui().showHoster(oGui, oHoster,Datalist, sThumb)
        else :
            VSlog('hoster failed')
        
        
        oGui.setEndOfDirectory() 
        
        
        return
        
    ##
    
    qualityList,streamList,sUrlrequestHost , sSubPathFr,sSubPathEn = GET_INFO_PLAY(sMovieTitle,sUrl,iconimagevik)
    sUrlrequestHost=streamList[0]
    VSlog('')
    VSlog('sUrlrequestHost =' + sUrlrequestHost)
    
    Datalist.append(sSubPathFr)
    Datalist.append(sSubPathEn)
    for item in  qualityList:
        Datalist.append(item)  
    
    for item in  streamList:
        Datalist.append(item)
        

    for objects in  Datalist:
        VSlog('Datalist '+ str(objects))
    

    sUrlparam=sUrlrequestHost + ';' + str(sSubPathFr) # + ';' + str(qualityList) + ';' + str(streamList)
   
    #
    oHoster = cHosterGui().checkHoster('viki')
    #oHoster = cHosterGui().checkHoster(sUrlparam)
    if (oHoster != False):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        #cHosterGui().showHoster(oGui, oHoster, sUrlparam, sThumb)
        cHosterGui().showHoster(oGui, oHoster,Datalist, sThumb)
    else :
        VSlog('hoster failed')
    
    
    oGui.setEndOfDirectory() 
    
    
    #oviki= viki(sUrlrequestHost,sSubPathFr,qualityList, streamurlList)
    #VSlog(str(oviki))
    #VSlog(oviki.sub)
    #for q in  oviki.qualitylist:
        #VSlog('oviki.qualitylist '+ q)

    #VSlog('##########api_call'+ api_call)
    
class viki:

    def __init__(self, sUrl,sSub,lQuality,lUrlstream):
        self.url =sUrl
        self.sub= sSub
        self.qualitylist =lQuality
        self.urlstreamlist =lUrlstream
    
        

#Voila c'est un peux brouillon mais ça devrait aider un peu, n'hesitez pas a poser vos questions et meme a partager vos sources.
