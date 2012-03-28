from django.shortcuts import render_to_response

import random
from datetime import datetime
# Create your views here.

# name them year<year> so that the manager can grab them

YOUTUBE_EMBED = """<iframe width="560" height="315" src="http://www.youtube.com/embed/{}?rel=0&autoplay=1" frameborder="0"></iframe>"""

def year2011(request):
    '''April Fools 2011 Random Attack determiner'''
    
    choice = random.choice(range(14)) #makes the last choice more likely :P
    
    if choice == 0:
        #Willy Bum Bum
        q = "MY EYES. MY EARS. MY MOUTH."
        embed = ''' <iframe width="640" height="390"
        src="http://www.youtube.com/embed/qrBj3u5dPgM?rel=0&autoplay=1" frameborder="0"></iframe>'''
    elif choice == 1:
        #Death Metal Friday
        q = "attractive people complaining about stems"
        embed = ''' <iframe width="640" height="390"
        src="http://www.youtube.com/embed/pi00ykRg_5c?rel=0&autoplay=1" frameborder="0"></iframe>'''
    elif choice == 2:
        #Dubstep Badgers
        q = "m2m you are a cruel mistress"
        embed = ''' <iframe width="640" height="390"
        src="http://www.youtube.com/embed/HMtcqfQNd2Y?rel=0&autoplay=1" frameborder="0"></iframe>'''
    elif choice == 3:
        #Dancing Bird Men
        q = "proof of your religion"
        embed = ''' <iframe width="640" height="390"
        src="http://www.youtube.com/embed/uSfGFnqxmVo?rel=0&autoplay=1" frameborder="0"></iframe>'''
    elif choice == 4:
        #Vader vs Hitler
        q = "forced labor, amiright"
        embed = ''' <iframe width="640" height="390"
        src="http://www.youtube.com/embed/AFA-rOls8YA?rel=0&autoplay=1" frameborder="0"></iframe>'''
    elif choice == 5:
        #face monsters
        q = "the song that ends the earth"
        embed = ''' <iframe width="640" height="390"
        src="http://www.youtube.com/embed/dZfmPREbTd8?rel=0&autoplay=1" frameborder="0"></iframe> '''
    elif choice == 6:
        #slow trolololo
        q = "her name was marie-claire"
        embed = ''' <iframe width="640" height="390"
        src="http://www.youtube.com/embed/-8AZyAtP2eo?rel=0&autoplay=1" frameborder="0"></iframe>'''
    elif choice == 7:
        #metal
        q = "define: metal"
        embed = ''' <iframe width="640" height="390"
        src="http://www.youtube.com/embed/BhYT-7bzHis?rel=0&autoplay=1" frameborder="0"></iframe>'''
    elif choice == 8:
        #dubstep santa
        q = "very naughty indeed"
        embed = ''' <iframe width="640" height="390"
        src="http://www.youtube.com/embed/z59gAXZ0ksQ?rel=0&autoplay=1" frameborder="0"></iframe>'''
    elif choice == 9:
        #house trolololo
        q = "how to grow a neard"
        embed = ''' <iframe width="640" height="390"
        src="http://www.youtube.com/embed/Pmjz4YVL46U?rel=0&autoplay=1" frameborder="0"></iframe>'''
    elif choice == 10:
        #will scott
        q = "there is no spoon"
        embed = '''<img src="/media/images/willscott.gif" /> <br /> <br /> IT IS A SPORK '''
    elif choice == 11:
        #hell friday
        q = "the face of god"
        embed =''' <iframe title="YouTube video player" width="640" height="390" src="http://www.youtube.com/embed/Ti1D9t8n0qA?rel=0&autoplay=1" frameborder="0" allowfullscreen></iframe>'''
    else:
        # FBI warning
        q = "fuuuuu"
        embed = '''<div id="FEEB" style="position:fixed;
                                top:0;
                                left:0;
                                width:100%;
                                height:100%;
                                background-color:white;
                                background-image: url(/media/images/fbi.jpg) no-repeat;
                                z-index:100;" align="center"
                                > 
                                <img onclick="$('#FEEB').fadeOut('slow');" src="/media/images/fbi.jpg"></div>'''
        script = '''<script>
                    </script>
                 '''


    # not everything defines a script
    try:
        script
    except:
        script = ""

    return render_to_response('aprilfools/index.html',
                            {
                                'title':"M2M-Search",
                                'q':q,
                                'embed':embed,
                                'script':script,
                            },)

def results2011():
    '''Evil Results'''
    queries = ["terrible, terrible porn",
               "peeping toms",
               "pantsless master jammers", 
               "the end of all things",
               "her terrible orgasm", 
               "hello, goodbye",
               "you are dead to me", 
               "why won't you ever quit",
               "just give up, you should have searched yesterday",
               "M2M; she does not forgive, and she does not forget",
               "My name is Inigo Montoya",
               "prepare to die",
               "Help! I'm trapped in the machines!"]
    q = random.choice(queries)
    return q   

def year2012(request):
    choice = random.choice(range(14))
    
    q = ""
    script = ""
    
    if choice == 0:
        # elmo+cookie monster, sitting in a tree; f.u.c.k.i.n.g.
        q = 'All your base'
        embed = YOUTUBE_EMBED.format("-_49VS4nuao")
    elif choice == 1:
        # dildo machine
        q = "your life, my rules"
        embed = YOUTUBE_EMBED.format("9hBpF_Zj4OA")
    elif choice == 2:
        # rotate your owl
        q = "PETA's on the way"
        embed = YOUTUBE_EMBED.format("9hBpF_Zj4OA")
    elif choice == 3:
        # stoned with dinosaurs
        q = "Philosoraptor"
        embed = YOUTUBE_EMBED.format("L1SKf9YU4QQ")
    elif choice == 4:
        #stupidfacedd    
        q = "5 - M2M happens while you are asleep"
        embed = YOUTUBE_EMBED.format("5dE-7-kBxXw")
    elif choice == 5:
        #drive recklessly
        q = "You are a cruel mistress, M2M"
        embed = YOUTUBE_EMBED.format("9S75Rfva9O8")
    elif choice == 6:
        #trolololol
        q = "the face of god"
        embed = YOUTUBE_EMBED.format("woySeSNBL3o")
    elif choice == 7:
        #stupid metal
        q = "define: metal"
        embed = YOUTUBE_EMBED.format("XrVPRFTUbRw")
    elif choice == 8:
        # awesome metal
        q = "define: define: metal"
        embed = YOUTUBE_EMBED.format("l_WMHg8c_4I")
    elif choice == 9:
        # gir loves tree
        q = "terrible, terrible porn"
        embed = YOUTUBE_EMBED.format("xYmVE4fASCc")
    elif choice == 10:
        #will scott
        q = "The not-so-fabled godhead"
        embed = '''<img src="/media/images/willscott.gif" /> <br /> <br /> FABLE IV IS SO FABLED'''
    elif choice == 11:
        # penis vegetables song
        q = "pretty bad porn"
        embed = YOUTUBE_EMBED.format("seRxE3b6m_w")
    else:
        # FBI warning
        q = "fuuuuu"
        embed = '''<div id="FEEB" style="position:fixed;
                                top:0;
                                left:0;
                                width:100%;
                                height:100%;
                                background-color:white;
                                background-image: url(/media/images/fbi.jpg) no-repeat;
                                z-index:100;" align="center"
                                > 
                                <img onclick="$('#FEEB').fadeOut('slow');" src="/media/images/fbi.jpg"></div>'''
        script = '''<script>
                    </script>
                 '''
    return render_to_response('aprilfools/index.html',
                            {
                                'title':"M2M-Search",
                                'q':q,
                                'embed':embed,
                                'script':script,
                            },)
def results2012():
    '''Evil Results'''
    queries = ["terrible, terrible porn",
               ]
    q = random.choice(queries)
    return q  

def yearcaller(request):
    ''' Chooses which april fools to display'''
    year = datetime.now().year
    
    # picks the function to be used
    return globals()['year%d'%year](request)

def resultcaller():
    ''' Chooses which april fools queries to make'''
    year = datetime.now().year

    return globals()['results%d'%year]()
