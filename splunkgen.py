"""
Script to generate data to be ingested by Splunk. Objective is te Create
an index that is used to fill a KV-store. Second objective is to add and
modify records, so the splunk scripts/spl's have to keep up.
"""
import random
import datetime
import time

def random_quote(words):
    # Extract random quote (length 5 to 15) from textfile
    quotelen = random.randrange(5, 15)  # Tweak quotelength?
    quotestart = random.randrange(len(words) - quotelen)
    quote = words[quotestart]
    for i in range(1, quotelen):
        quote = quote + ' ' + words[quotestart+i]
    return quote

def create_record(nr, words):
    curtime = time.strftime('%Y-%m-%d %H:%M:%S')
    # Create name by picking random first- and surnames
    fname = random.choice(open('firstnames.txt').readlines()).strip()
    sname = random.choice(open('surnames.txt').readlines()).strip()
    name = '{} {}'.format(fname, sname.capitalize())
    severity = random.randrange(5) + 1
    status = random.choice(['raw', 'rare', 'medium', 'welldone', 'charcoal'])
    story = random_quote(words)
    res = random.choice(['Y', 'N'])
    record = ('{},NUMBER="{}",OWNER="{}",SEVERITY="{}",STATUS="{}",'
              'STORY="{}",SYSMODTIME="{}",RESTRICTED="{}"'
              .format(curtime, nr, name, severity, status, story, curtime, res))
    with open('sm9_test.log', 'a') as logfile:
        logfile.write(record + '\n')
    print('+'*15, 'Record created:')
    print(record)

def update_record(rnr, words):
    with open('sm9_test.log','r') as logfile:
        allrecords = logfile.readlines()
    # Find all records with NUMBER="<rnr>"
    subs = 'NUMBER="{}"'.format(rnr)
    selrecords = [i for i in allrecords if subs in i]
    selrecord = selrecords[-1] # Select last record found
    curtime = time.strftime('%Y-%m-%d %H:%M:%S')
    newrecord = curtime + ',' + selrecord.split(',', maxsplit=1)[1]
    newrecord = newrecord.split('STORY=')[0]
    oldquote = selrecord.split('STORY="')[1]
    oldquote = oldquote.split('",SYSMODTIME')[0]
    newquote = random_quote(words)
    newrecord = '{}STORY="{}\n{}"'.format(newrecord, oldquote, newquote)
    res = random.choice(['Y', 'N'])
    newrecord = '{},SYSMODTIME="{}",RESTRICTED="{}"'.format(newrecord,
                                                            curtime,
                                                            res)
    with open('sm9_test.log', 'a') as logfile:
        logfile.write(newrecord + '\n')
    print('='*15, 'Record updated:')
    print(newrecord)

def generate_data():
    # Prepare text to quote in records by splitting text file in words
    with open('text.txt', 'r') as text: # Origin for quoted texts
        lines = text.readlines()
    words = []
    for line in lines:
        linewords = line.split()
        for word in linewords:
            words.append(word)

    for nr in range(100):  # Tweak number of records generated
        create_record(nr, words)
        time.sleep(5)      # Tweak how 'fast' records are generated
        # Updating records will occur seldom at first, but ist will be at a
        # ratio of 1 to 3 at the end
        rnr = random.randrange(300) # Tweak update probability
        if (rnr <= nr):
            update_record(rnr, words)

if __name__ == '__main__':
    generate_data()
