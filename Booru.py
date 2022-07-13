import sys
import time
import termuxgui as gu
import threading
import requests
import base64
import re
from io import BytesIO

def getimage(theimg, thenum):
    global selection
    tag = theimg
    page = thenum
    search = requests.get("https://%s/index.php?page=dapi&s=post&q=index&limit=1&pid=%d&tags=%s"%(selection, page, tag))

    regex = "file_url=\"(https:\\/\\/[\\w.\\/-]*)\""
    finder = re.search(regex, search.text)
    checker = re.search("\.mp4", finder.group(1))
    if (checker == None):
        buffimg = BytesIO(requests.get(finder.group(1)).content)
        finalim = buffimg.getvalue()
    else:
        buffimg = BytesIO(requests.get("https://cdn.discordapp.com/attachments/929565544334647356/996643118663348324/IMG_20220713_000340.png").content)
        finalim = buffimg.getvalue()
    return finalim

def downloadim(theimg, thenum):
    global selection
    tag = theimg
    page = thenum
    search = requests.get("https://%s/index.php?page=dapi&s=post&q=index&limit=1&pid=%d&tags=%s"%(selection, page, tag))

    regex = "file_url=\"(https:\\/\\/[\\w.\\/-]*)\""
    finder = re.search(regex, search.text)

    file = requests.get(finder.group(1))

    #filetype = file.headers.get('content-type')

    #fname = getFilename(file.headers.get('content-disposition'))
    fname = finder.group(1).rsplit('/', 1)

    finalname = "/sdcard/Download/" + fname[1]

    with open(finalname, 'wb') as f:
        f.write(file.content)

def defimg():
    default = BytesIO(requests.get("https://cdn.discordapp.com/attachments/929565544334647356/996076390849986761/IMG_20220711_103133.png").content)
    default1 = default.getvalue()
    return default1

number = 1

with gu.Connection() as c:

    Activity = gu.Activity(c, dialog=True)


    Layout = gu.LinearLayout(Activity)


    Text = gu.TextView(Activity, "BooruSearch", Layout)
    Text.settextsize(40)
    Text.setmargin(5)


    BooruSel = gu.Spinner(Activity, Layout)
    BooruList = ["safebooru.org", "gelbooru.com", "api.rule34.xxx"]
    BooruSel.setlist(BooruList)
    BooruSel.setmargin(5)


    ST = gu.TextView(Activity, "Search term: same way as in any booru", Layout)
    Searchbox = gu.EditText(Activity, "", Layout)
    ST.setmargin(5)


    buttons = gu.LinearLayout(Activity, Layout, False)


    btn1 = gu.Button(Activity, "search", buttons)


    for ev in c.events():


        if ev.type == gu.Event.itemselected and ev.value["id"] == BooruSel:
            selection = ev.value["selected"]


        if ev.type == gu.Event.destroy and ev.value["finishing"]:
            sys.exit()


        if ev.type == gu.Event.click and ev.value["id"] == btn1:
            b = gu.Activity(c)
            La = gu.LinearLayout(b)
            arg = Searchbox.gettext()
            
            Image = gu.ImageView(b, La)
            Bts = gu.LinearLayout(b, La, False)
            La.setlinearlayoutparams(1)
            Bts.setlinearlayoutparams(0)
            Bts0 = gu.Button(b, "Back", Bts)
            Bts1 = gu.Button(b, "Next", Bts)
            Bts2 = gu.Button(b, "Download", Bts)
            try:
                url = getimage(arg, 1)
                Image.setimage(url)
            except:
                url = defimg()
                Image.setimage(url)


        if ev.type == gu.Event.click and ev.value["id"] == Bts0:
            number = number - 1
            if number == 0:
                number = 1

            try:
                url = getimage(arg, number)
                Image.setimage(url)
            except:
                url = defimg()
                Image.setimage(url)

            
        if ev.type == gu.Event.click and ev.value["id"] == Bts1:
                number = number + 1
                try:
                    url = getimage(arg, number)
                    Image.setimage(url)
                except:
                    url = defimg()
                    Image.setimage(url)

        if ev.type == gu.Event.click and ev.value["id"] == Bts2:
            downloadim(arg, number)

    time.sleep(20)
