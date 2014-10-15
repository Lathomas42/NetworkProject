import xml.etree.ElementTree as ET
import csv
import string


def getDateAffils(usedIDs, fn='pubmed_result.xml'):

    fn_csv = fn[:-4] + '.csv'
    output = open(fn_csv, 'w')
    writer = csv.writer(output, delimiter=';')
    writer.writerow(['Date', 'affils'])
    """
    ids_csv = open('ids_list.csv','w')
    ids_writer = csv.writer(ids_csv)
    """
    data = ET.iterparse(open(fn))
    i = 0
    for e, art in data:
        if art.tag == 'PubmedArticle':
            if i % 1000 == 0:
                print i
            i += 1
            mCit = art[0]
            ID = mCit.find('PMID').text
            if ID not in usedIDs:
                #usedIDs.append(ID)
                mcitArt = mCit.find('Article')
                date = mCit.find('DateCreated')
                authlist = mcitArt.find('AuthorList')
                date_affils = [date]
                if authlist is not None:
                    for auth in authlist:
                        if(auth.find('Affiliation') is not None):
                            affil = auth.find('Affiliation').text
                            date_affils.append(affil)
                    if(len(date_affils) > 2):
                        # writer.writerow(date_affils)
                        if date_affils[0] is None:
                            date = [ID, 0, 0, 0]
                        else:
                            date = [ID, date_affils[0][0].text,
                                    date_affils[0][1].text,
                                    date_affils[0][2].text]
                        for item in date_affils[1:]:
                            date.append(filter(lambda x: x in string.printable, item))
                        writer.writerow(date)
            art.clear()
    output.close()



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

