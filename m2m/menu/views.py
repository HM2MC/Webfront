from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page
# Create your views here.

from BeautifulSoup import BeautifulSoup, Tag, NavigableString
from datetime import datetime
import urllib2
import requests
import re


def classless(tag):
    try:
        return tag.attrMap['class'] == None
    except:
        return True

def has_class(tag, classname):
    try:
        return tag.attrMap['class'] == classname
    except:
        return False
    
def has_day_class(tag):
    dayclasses = ['mon','tue','wed','thu','fri','sat','sun']
    for c in dayclasses:
        if has_class(tag,c):
            return True
        
    return False

def strip_tags(html, invalid_tags):
    soup = BeautifulSoup(html)
    for tag in soup.findAll(True):
        if tag.name in invalid_tags:
            s = ""
            for c in tag.contents:
                if not isinstance(c, NavigableString):
                    c = strip_tags(c, invalid_tags)
                s += unicode(c)
            tag.replaceWith(s)
    return soup

def reset_attrs(tag, excluding=[], recurse=True):
    if not hasattr(tag, 'attrs'):
        return
    #print tag, tag.attrs
    for attr in tag.attrs:
        print attr, excluding
        if attr[0] in excluding:
            print "excluding"
            continue
        del(tag[attr[0]])
    if recurse and hasattr(tag, 'contents') and len(tag.contents) > 0:
        reset_attrs(tag.contents[0], excluding=excluding)
        

def get_pitzer_menu(today):
    pz_url = "http://www.cafebonappetit.com/menu/your-cafe/pitzer/cafes/details/219/mcconnell-bistro"
    pz_resp = requests.get(pz_url)
    pz_soup = BeautifulSoup(pz_resp.content)
    pzhead = BeautifulSoup("<thead><tr><td colspan=3>McConnell</td></tr></thead>")
    try:
        pz_table = pz_soup('a',{'name':'time_{}_{:02d}'.format(today.now().day, today.month)})[0].parent.findNextSibling('table')
        for row in pz_table('tr',{'class':'always-show-me'}):
            for tag in row.findAll(True):
                if tag.name in ['div', 'p', 'strong']:
                    tag.replaceWith(tag.renderContents())
            reset_attrs(row)
            row['class'] = 'mealtime'
        for row in pz_table('td',{'class':'border-candidate'}):
            for tag in row.findAll(True):
                if tag.name in ['div', 'p', 'strong']:
                    tag.replaceWith(tag.renderContents())
            reset_attrs(row, ['rowspan'])
            row['class'] = 'mealstation'
        reset_attrs(pz_table, recurse=False)
        pz_table['class'] = 'mealtable'
        
        pz_table.insert(0,pzhead)
        
        pz_table = pz_table.prettify()
    except Exception, e:
        pz_table = e
    
    
    return pz_table        

def get_hm_menu(today):
    # The Hoch's dining calendars start on fridays. why? Fuck if I know.
    week = today.isocalendar()[1]
    if today.month < 7: # also, they're ordered by WEEKS OF THE SEMESTER. what. the. fuck.
        week = week - 2
        if today.isocalendar()[2] in range(5,7):
            week = week + 1
    elif today.month > 8:
        pass
        
    hm_url = "http://www.hmcdining.com/dining/menus/week_{}.html".format(week) # get the current week number
    print hm_url
    hm_soup = BeautifulSoup(requests.get(hm_url).content)
    hmhead = BeautifulSoup("<thead><tr><td colspan=3>Hoch-Shanahan</td></tr></thead>")
    #try:
    hm_table = hm_soup('table',{'id':'table'})[0]
    day_map = {'5':1,
               '6':2,
               '7':3,
               '1':4,
               '2':5,
               '3':6,
               '4':7}
    target_column = day_map[str(today.isocalendar()[2])] # exploit mod to wrap around, and adjust for stupid calendar
    if target_column == 0:
        target_column = 1
    print "target column:", target_column
    
    final_table = BeautifulSoup()
    table = Tag(final_table, 'table')
    final_table.insert(0, table)
    table.insert(0,hmhead)
    table['class']='mealtable'
    
    for image in hm_table.findAll('img'):
        src = image['src'].split('/')[-1]
        image['src'] = "http://www.hmcdining.com/images/{}".format(src)
        
    for row in hm_table.findAll(name=lambda tag: (tag.name=='tr') and (not has_class(tag,'divider_row'))):
        # set the meal heading, i guess.        
        meal = row.findAll('td')[target_column]
        if meal['class'] == 'divider_row':
            continue
        
        place = row.find('td')
        reset_attrs(place)
        place['class'] = 'mealstation'
        
        place.extract()
        meal.extract()
        #data += [place.attrs]
        
        for find in meal.findAll('p'):
            reset_attrs(find, recurse=False)
        for find in meal.findAll('div'):
            reset_attrs(find,recurse=False)
        
        tr = Tag(final_table, 'tr')
        table.insert(len(table.contents)-1,tr) # this is dumb, but can't figure out another way to un-reverse
        tr.insert(0,meal)
        if meal['class'] == 'meal_row':
            reset_attrs(meal)
            meal['class'] = 'mealtime'
            meal['colspan'] = 2
            #tr.insert(, Tag(final_table, 'td'))
        else:
            reset_attrs(meal, ['src'])
            tr.insert(0, place)

    return final_table.prettify()

def get_cm_menu(today):
    cm_url = "http://www.cafebonappetit.com/menu/your-cafe/collins-cmc/cafes/details/50/collins-"
    cm_resp = requests.get(cm_url)
    cm_soup = BeautifulSoup(cm_resp.content)
    cm_head = BeautifulSoup("<thead><tr><td colspan=3>Collins</td></tr></thead>")
    try:
        cm_table = cm_soup('a',{'name':'time_{}_{:02d}'.format(today.now().day, today.month)})[0].parent.findNextSibling('table')
        for row in cm_table('tr',{'class':'always-show-me'}):
            for tag in row.findAll(True):
                if tag.name in ['div', 'p', 'strong']:
                    tag.replaceWith(tag.renderContents())
            reset_attrs(row)
            row['class'] = 'mealtime'
        for row in cm_table('td',{'class':'border-candidate'}):
            for tag in row.findAll(True):
                if tag.name in ['div', 'p', 'strong']:
                    tag.replaceWith(tag.renderContents())
            reset_attrs(row, ['rowspan'])
            row['class'] = 'mealstation'
        reset_attrs(cm_table, recurse=False)
        cm_table['class'] = 'mealtable'
        
        cm_table.insert(0,cm_head)
        
        cm_table = cm_table.prettify()
    except Exception, e:
        cm_table = e
    
    
    return cm_table

def get_frank_menu(today):
    data = []
    fr_url = "http://www.pomona.edu/administration/dining/menus/frank.aspx"
    fr_resp = requests.get(fr_url)
    fr_soup = BeautifulSoup(fr_resp.content)
    fr_head = BeautifulSoup("<thead><tr><td colspan=3>Frank</td></tr></thead>")
    #try:
    
    target_day = today.strftime("%A")
    
    day_div = fr_soup.find('div', text=target_day.upper())
    if day_div == None:
        raise Exception('No menu available for today')
    
    table = fr_soup.findAll('table', {'class':'menu'})[today.isoweekday()-1] # find the right menu
    table.extract()
    
    table['class'] = 'mealtable'
    
    stations = []
    for td in table.findAll(True,{'class':re.compile('station')}):
        td['class']='mealstation'
        stations += [td]
    
    
    # build breakfast
    breakfast = []
    for td in table.findAll(True,{'class':re.compile('breakfast')}):
        breakfast += [td]
    breakfast[0]['class'] = 'mealtime'
    breakfast[0]['colspan'] = 3
    
        
    lunch = []
    for td in table.findAll(True,{'class':re.compile('lunch')}):
        lunch += [td]
    lunch[0]['class'] = 'mealtime'
    lunch[0]['colspan'] = 3
    
    dinner = []
    for td in table.findAll(True,{'class':re.compile('dinner')}):
        dinner += [td]
    dinner[0]['class'] = 'mealtime'
    dinner[0]['colspan'] = 3
        
    final_table = BeautifulSoup()
    tabler = Tag(final_table,'table')
    tabler.insert(0,fr_head)
    final_table.insert(0,tabler)
    
    count = 1
    for food in breakfast:
        tr = Tag(final_table, 'tr')
        
        if food['class'] == 'mealtime':
            tr.insert(0,food)
        else:
            tr.insert(0,food)
            tr.insert(0, stations[count])
            count += 1
        tabler.insert(len(tabler.contents)-1, tr)
    count = 1
    for food in lunch:
        tr = Tag(final_table, 'tr')
        if food['class'] == 'mealtime':
            tr.insert(0,food)
        else:
            tr.insert(0,food)
            td = Tag(final_table, 'td')
            td.contents = stations[count].contents
            td['class'] = 'mealstation'
            tr.insert(0, td)
            count += 1
            
        tabler.insert(len(tabler.contents)-1, tr)
        
    count = 1
    for food in dinner:
        tr = Tag(final_table, 'tr')
        if food['class'] == 'mealtime':
            tr.insert(0,food)
        else:
            tr.insert(0,food)
            td = Tag(final_table, 'td')
            td.contents = stations[count].contents
            td['class'] = 'mealstation'
            tr.insert(0, td)
            count += 1
            
        tabler.insert(len(tabler.contents)-1, tr)
    
    tabler['class'] = 'mealtable'
    
    return final_table.prettify()#table.prettify()#fr_table

def get_frary_menu(today):
    data = []
    fr_url = "http://www.pomona.edu/administration/dining/menus/frary.aspx"
    fr_resp = requests.get(fr_url)
    fr_soup = BeautifulSoup(fr_resp.content)
    fr_head = BeautifulSoup("<thead><tr><td colspan=3>Frary</td></tr></thead>")
    #try:
    
    target_day = today.strftime("%A")
    
    day_div = fr_soup.find('div', text=target_day)
    if day_div == None:
        raise Exception('No menu available for today')
    
    table = fr_soup.findAll('table', {'class':'menu'})[today.isoweekday()-1] # find the right menu
    table.extract()
    
    table['class'] = 'mealtable'
    
    stations = []
    for td in table.findAll(True,{'class':re.compile('station')}):
        td['class']='mealstation'
        stations += [td]
    
        
    final_table = BeautifulSoup()
    tabler = Tag(final_table,'table')
    tabler.insert(0,fr_head)
    final_table.insert(0,tabler)

    # if we get an error here, it's probably becase
    # it's the weekend - no breakfast or lunch, just bruuunch
    try:
        # build breakfast
        breakfast = []
        for td in table.findAll(True,{'class':re.compile('breakfast')}):
            breakfast += [td]
        
            breakfast[0]['class'] = 'mealtime'
            breakfast[0]['colspan'] = 3
        
            
        lunch = []
        for td in table.findAll(True,{'class':re.compile('lunch')}):
            lunch += [td]
        lunch[0]['class'] = 'mealtime'
        lunch[0]['colspan'] = 3
        
        count = 1
        for food in breakfast:
            tr = Tag(final_table, 'tr')
            
            if food['class'] == 'mealtime':
                tr.insert(0,food)
            else:
                tr.insert(0,food)
                tr.insert(0, stations[count])
                count += 1
            tabler.insert(len(tabler.contents)-1, tr)
        count = 1
        for food in lunch:
            tr = Tag(final_table, 'tr')
            if food['class'] == 'mealtime':
                tr.insert(0,food)
            else:
                tr.insert(0,food)
                td = Tag(final_table, 'td')
                td.contents = stations[count].contents
                td['class'] = 'mealstation'
                tr.insert(0, td)
                count += 1
                
            tabler.insert(len(tabler.contents)-1, tr)
            
        
    except:
        pass
    
    dinner = []
    for td in table.findAll(True,{'class':re.compile('dinner')}):
        dinner += [td]
    dinner[0]['class'] = 'mealtime'
    dinner[0]['colspan'] = 3
    
    
   
    count = 1
    for food in dinner:
        tr = Tag(final_table, 'tr')
        if food['class'] == 'mealtime':
            tr.insert(0,food)
        else:
            tr.insert(0,food)
            td = Tag(final_table, 'td')
            td.contents = stations[count].contents
            td['class'] = 'mealstation'
            tr.insert(0, td)
            count += 1
            
        tabler.insert(len(tabler.contents)-1, tr)
    
    tabler['class'] = 'mealtable'
    
    return final_table.prettify()#table.prettify()#fr_table

def get_malott_menu(today):
    url = "http://www.scrippscollege.edu/students/dining-services/index.php"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content)
    head = BeautifulSoup("<thead><tr><td colspan=3>Malott Commons</td></tr></thead>")
    
    target = soup.find('div',{'id':'right_column_content'}) 
    target.extract()
    meals = []
    for meal in target.findAll('ul'):
        meal.extract()
        meals += [meal]
        
    labels = []
    for title in target.findAll('p'):
        title.extract()
        labels += [title]
    
    final_table = BeautifulSoup()
    table = Tag(final_table, 'table')
    final_table.insert(0, table)
    table.insert(0,head)
    table['class']='mealtable'
    for meal in meals:
        tr = Tag(final_table, 'tr')
        td = Tag(final_table, 'td')
        tr.insert(0,td)
        td['class']='mealtime'
        td.contents = labels[1].contents
        table.insert(len(table.contents)-1,tr)
        labels = labels[1:]
        for food in meal.findAll('li'):
            tr = Tag(final_table, 'tr')
            td = Tag(final_table, 'td')
            tr.insert(0, td)
            td.contents = food.contents
            table.insert(len(table.contents)-1,tr)
    
    return final_table.prettify()

@cache_page(60*60*7)
def main(request):
    today = datetime.now()
    data = []
    #Mudd
    hm_table = get_hm_menu(today)

    #Scripps
    sc_table = get_malott_menu(today)
    #Pitzer
    pz_table = get_pitzer_menu(today)
    
    #CMC
    cm_table = get_cm_menu(today)
    
    #Frank
    frank_table = get_frank_menu(today)
    
    #Frary
    frary_table = get_frary_menu(today)
    
    #Oldenborg
    olden_table = ""
    
    return render_to_response('menu/main.html',
                              {
                               'pztable':pz_table,
                               'hmtable':hm_table,
                               'sctable':sc_table,
                               'cmtable':cm_table,
                               'frank':frank_table,
                               'frary':frary_table,
                               'olden':olden_table,
                               'data': data
                               })