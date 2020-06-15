#!/usr/bin/python3

#pip3 install libpff-python
import pypff
import pprint
import re
from Algorithms.Marketing import PageRank

def parse_pst_folder(base, messages: dict = {}):
    for folder in base.sub_folders:
        if folder.number_of_sub_folders:
           messages = parse_pst_folder(folder, messages)

        for message in folder.sub_messages:
            if message.transport_headers == None:
                continue

            #print(message.transport_headers)

            start = message.transport_headers.find('Date: ')
            end   = message.transport_headers.find('Subject: ', start + 10)
            date_email = message.transport_headers[start:end]
            if not re.search('2019', date_email):
                continue

            start = message.transport_headers.find('From: ')
            end   = message.transport_headers.find('To: ', start + 10)
            from_email_section = message.transport_headers[start:end]

            start = message.transport_headers.find('To: ')
            end   = message.transport_headers.find(': ', start + 10)
            to_email_section = message.transport_headers[start:end]

            all_froms = re.findall('(<)([a-zA-Z\.\-_]*?)(@schuetz\-dental\.de)(>)', from_email_section)

            if len(all_froms) < 1 or len(all_froms[0]) < 2 or all_froms[0][1] == 'd.eichhorn':
                continue

            email_from = all_froms[0][1]
            all_tos = re.findall('(<)([a-zA-Z\.\-_]*?)(@schuetz\-dental\.de)(>)', to_email_section)

            if len(all_tos) < 1:
                continue

            email_to = []
            for tos in all_tos:
                if len(tos) < 2 or tos[1] == 'd.eichhorn':
                    continue

                email_to.append(tos[1])

            # consider to add cc as well

            if email_from not in messages:
                messages[email_from] = []

            messages[email_from] += email_to

    return messages

pff_file = pypff.file()

pff_file.open('../archive.pst')
root = pff_file.get_root_folder()

messages = parse_pst_folder(root)
ranking = PageRank.PageRank(messages, True)
ranks = ranking.calculateRanks(20, None)

pprint.pprint(ranks)

pff_file.close()