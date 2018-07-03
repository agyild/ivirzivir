try:
    import requests
    import bs4
except ModuleNotFoundError as e:
    print(f'Error: Module "{e.name}" not found!')
    exit()

clisturl = input('Elective List URL: ')
# clisturl = 'http://ects.bilgi.edu.tr/Elective/Detail?catalog_electiveId=10813&OfferStyleId=20&CourseAbbr=MUS'
cfinal = list()
pnumber = 1
ptrackr = ''
while True:
    clist = requests.get(clisturl + f'&Page={pnumber}')
    clistsoup = bs4.BeautifulSoup(clist.text, 'lxml')
    if clistsoup.h1.a.text == ptrackr:
        break
    ptrackr = clistsoup.h1.a.text
    pnumber += 1

    for t in clistsoup(class_='panel-title'):
        cpageurl = 'http://ects.bilgi.edu.tr' + t.a['href']
        cpage = requests.get(cpageurl)
        try:
            cpagesoup = bs4.BeautifulSoup(cpage.text, 'lxml')
        except:
            cpagesoup = bs4.BeautifulSoup(cpage.text, 'html.parser')
        if cpagesoup('td')[20].string != 'Fully Online':
            continue
        cfinal.append((t.a.string, t('a')[1].string, cpageurl))

print(f'DONE!\n{len(cfinal)} result(s) have been found.\n')
for t in cfinal: print(f'{t[0]}: {t[1]} @ {t[2]}')
