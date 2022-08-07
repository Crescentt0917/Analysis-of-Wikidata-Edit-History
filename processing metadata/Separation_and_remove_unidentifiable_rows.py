
# coding: utf-8

import pandas as pd

# Separation of edits on items and properties
col_name = ['entity_id', 'entity_type', 'edit_id', 'prev_edit_id', 'edit_timestamp', 'editor_name', 'comment']
edits = pd.read_csv('E:/wiki_editlog/2021_processed/stub-history.xml_processed.txt', sep='\t', header=None)
edits.columns = col_name

edits_q = edits.loc[edits['entity_type'] == 'wikibase-item']
edits_p = edits.loc[edits['entity_type'] == 'wikibase-property']

print('edits_q has {} rows'.format(len(edits_q)))
print('edits_p has {} roes'.format(len(edits_p)))


# Remove unidentifiable records
edits_q.dropna(subset=['comment'],inplace=True)
edits_q.dropna(subset=['comment'],inplace=True)

edits_q['edit_type'], edits_q['edit_info'] = edits_q['comment'].str.split(':', 1).str
edits_p['edit_type'], edits_p['edit_info'] = edits_p['comment'].str.split(':', 1).str

unidentifiable_comments = ['[[wikidata',
                           'these are disambiguation pages. there is no "follows" for them',
                           'merging process is still going on',
                           'LTA',
                           'rvv',
                           'spam link addition',
                           'Why removing aliases?',
                           'Sock of Mạc Thái Tổ. Vandalism',
                           'nonsense. xwiki abuse',
                           'nonsense',
                           'Xem [[WD',
                           'wrong id',
                           'No reason to remove',
                           'not descriptions',
                           'Jflarsric-এর করা 1416211233 নং সংস্করণে পুনরানিত হয়েছে; Vandalism ([[',
                           'not useful',
                           'indescriptive',
                           'now blocked',
                           'inaccurate occupation + spam link',
                           'Disruptive editing.',
                           'Nonsense/gibberish text/not in project language',
                           'incorrect punctuation',
                           'incorrect phone number /missing country code',
                           'Banned user',
                           'to split',
                           'test edit',
                           'It is not vandalism',
                           'See talk page',
                           'שחזור']

for comment in unidentifiable_comments:
    edits_q = edits_q.drop(edits_q.index[(edits_q['edit_type'] == comment)], inplace=True)
    
print('edits_q now has {} rows'.format(len(edits_q)))
print('edits_p now has {} roes'.format(len(edits_p)))

edits_q.to_csv('E:/wiki_editlog/item.txt' ,sep='\t' ,index=False ,header=False)
edits_p.to_csv('E:/wiki_editlog/property.txt' ,sep='\t' ,index=False ,header=False)

