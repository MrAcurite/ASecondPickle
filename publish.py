import glob
import json
import os
import datetime
import shutil

wd = 'Desktop/ASecondPickle'
os.chdir(os.path.join(os.path.expanduser("~"), wd))

infoloc = 'info.json'
linkbase = 'https://mracurite.github.io/ASecondPickle/{__file__}.html'

os.system('git fetch')
os.system('git rebase origin/main')

with open('base.html', 'r') as base_file:
    base_html_str = base_file.read()

if os.path.isfile(infoloc):
    with open(infoloc, 'r') as f:
        info = json.load(f)
    timestamps = info['timestamps']
    docs = info['docs']
    titles = info['titles']
else:
    timestamps, docs, titles = [], [], []
    
pdf_list = glob.glob("*.pdf")

for pdf_name in pdf_list:
    new_doc = pdf_name[:-4]
    if not (new_doc in docs):
        if input("Publish {}: [Y/N]\n".format(new_doc).lower()) == 'y':
            new_title = input("Title: ")
            new_timestamp = datetime.datetime.now().timestamp()
            
            timestamps.append(new_timestamp)
            titles.append(new_title)
            docs.append(new_doc)
            
ftitle = titles[0]
flink = linkbase.format(__file__ = docs[0])
ltitle = titles[-1]
llink = linkbase.format(__file__ = docs[-1])
            
lastcopy = False

for i, (ts, doc, title) in enumerate(zip(timestamps, docs, titles)):
    
    if i == 0:
        ptitle = ftitle
        plink = flink
    else:
        ptitle = titles[i-1]
        plink = linkbase.format(__file__ = docs[i-1])
    if i == len(docs) - 1:
        ntitle = ltitle
        nlink = llink
        lastcopy = True
    else:
        ntitle = titles[i+1]
        nlink = linkbase.format(__file__ = docs[i+1])
        
    ID = i
    
    dt = datetime.datetime.fromtimestamp(ts)
    date = dt.strftime("%B %d, %Y")
    year = dt.year
    month = dt.month
    
    replace_dict = {
            '{__id__}' : ID,
            '{__title__}' : title,
            '{__date__}' : date,
            '{__year__}' : year,
            '{__month__}' : month,
            '{__file__}' : doc,
            '{__ftitle__}' : ftitle,
            '{__flink__}' : flink,
            '{__ptitle__}' : ptitle,
            '{__plink__}' : plink,
            '{__ntitle__}' : ntitle,
            '{__nlink__}' : nlink,
            '{__ltitle__}' : ltitle,
            '{__llink__}' : llink
        }
    
    new_html = base_html_str
    for target, insert in replace_dict.items():
        new_html = str(insert).join(new_html.split(target))
    
    new_file_loc = doc + '.html'
    with open(new_file_loc, 'w') as f:
        f.write(new_html)
        
    if lastcopy:
        shutil.copy(new_file_loc, 'index.html')
    
        
info = {
        'timestamps' : timestamps,
        'docs' : docs,
        'titles' : titles
        }

with open(infoloc, 'w') as f:
    json.dump(info, f)
    
os.system('git add *')
os.system(datetime.datetime.now().strftime('git commit -m "Publishing %B %d, %Y"'))
os.system('git push -u origin main')
