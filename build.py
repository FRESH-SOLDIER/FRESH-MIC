# Rebuilds index.html from src/template.html + src/data.json
import json
t=open('src/template.html').read(); d=open('src/data.json').read()
assert d.startswith('{')
d='{"embed":true,'+d[1:]   # live site plays Deezer previews in the page
open('index.html','w').write(t.replace('/*DATA*/',d))
print('built index.html',len(t)+len(d),'bytes')
