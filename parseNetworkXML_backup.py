import xml.etree.ElementTree as ET
import csv
import string
import timeTools


def getDateAffils(usedIDs, fn='pubmed_result.xml'):
    print fn
    data = ET.parse(open(fn))
    paperAffils = []
    errPapers = []
    root = data.getroot()

    articles = root.getchildren()
    n = len(articles)
    i = 0
    for art in articles:
        i += 1
        timeTools.loadingbar(i, n)
        mCit = art[0]
        ID = mCit.find('PMID').text
        if ID not in usedIDs:
            usedIDs.append(ID)
            mcitArt = mCit.find('Article')
            date = mCit.find('DateCompleted')
            authlist = mcitArt.find('AuthorList')
            date_affils = [date]
            if authlist is not None:
                for auth in authlist:
                    if(auth.find('Affiliation') is not None):
                        affil = auth.find('Affiliation').text
                        date_affils.append(affil)
                if(len(date_affils) > 2):
                    paperAffils.append(date_affils)
            else:
                errPapers.append(art)
    return paperAffils, usedIDs


def makeCSV(papAffils):
    # writes a csv for a paperAffils (output of getDateAffils)
    output = open('csv_test.csv', 'w')
    csvwriter = csv.writer(output, delimiter=';')
    for affils in papAffils:
        # first check if date is none
        if affils[0] is None:
            date = [0, 0, 0]
        else:
            date = [affils[0][0].text,
                    affils[0][1].text,
                    affils[0][2].text]
        row = date
        for item in affils[1:]:
            row.append(filter(lambda x: x in string.printable, item))
        csvwriter.writerow(row)
    output.close()

