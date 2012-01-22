import urllib2
import urllib
import re

searchURL = "https://my.pomona.edu/ics/Portal_Homepage.jnz?portlet=Claremont_Undergraduate_Course_Schedule"
termKey = "pg0$V$ddlTerm"
termVal = "2011;FA"
areaKey = "pg0$V$ddlDivision"
courseAreasURL = 'https://my.pomona.edu/ics/Portal_Homepage.jnz?portlet=Claremont_Undergraduate_Course_Schedule'

# Get list of course areas
response = urllib2.urlopen(courseAreasURL)
html = response.read()

# Trim out section containing course Area options
m= re.search('Course Area.+pomona',html,re.DOTALL)
courseAreaSection = m.group()

p2 = re.compile('<option value="([A-Z0-9/]+)">')
areaVals = p2.findall(courseAreaSection)

#Try getting an area

values = { termKey : termVal, areaKey : areaVals[4] }
data = urllib.urlencode(values)
req = urllib2.Request(searchURL,data)
response = urllib2.urlopen(req)
html = response.read()

f =open('result.html',"w")
f.write(html)
f.close()
