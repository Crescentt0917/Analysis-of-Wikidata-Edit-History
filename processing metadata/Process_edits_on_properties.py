#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd

col_name = ['entity_id', 'entity_type', 'edit_id', 'prev_edit_id', 'edit_timestamp', 'editor_name', 'comment', 'edit_type', 'edit_info']
p = pd.read_csv("E:/wiki_editlog/property.txt", sep='\t', header=None)
p.columns = col_name
p['type'] = ''

# Normalisation
p.loc[(p['edit_type'].str.contains('wbeditentity-update')),'type'] = 'term'
p.loc[(p['edit_type'].str.contains('wbeditentity-update')) & ((p['edit_info'].str.contains('Property')) | (p['edit_info'].str.contains('statement')) | (p['edit_info'].str.contains('claim')) | (p['edit_info'].str.contains('value'))),'type'] = 'statement'
p.loc[(p['edit_type'].str.contains('wbeditentity-update')) & ((p['edit_info'].str.contains('label'))),'type'] = 'label'
p.loc[(p['edit_type'].str.contains('wbeditentity-update')) & ((p['edit_info'].str.contains('alias'))),'type'] = 'alias'
p.loc[(p['edit_type'].str.contains('rotect')),'type'] = 'protect'
p.loc[((p['edit_type'].str.contains('Restore')) | (p['edit_type'].str.contains('Revert'))),'type'] = 'revert'
p.loc[(p['edit_type'].str.contains('Changed data type')),'type'] = 'change data type'
p.loc[((p['edit_type'] == '/* restore') | (p['edit_type'] == '/* undo')), 'type'] = 'revert'    # revert
p.loc[(p['edit_type'].str.contains('claim')), 'type'] = 'claim'
p.loc[(p['edit_type'].str.contains('qualifier')), 'type'] = 'qualifier' 
p.loc[(p['edit_type'].str.contains('reference')), 'type'] = 'reference'
p.loc[(p['edit_type'].str.contains('label')), 'type'] = 'label'
p.loc[(p['edit_type'].str.contains('description')), 'type'] = 'description'
p.loc[(p['edit_type'].str.contains('alias')), 'type'] = 'alias'
p.loc[(p['edit_type'].str.contains('override')), 'type'] = 'override'
p.loc[(p['edit_type'].str.contains('/* wbeditentity-create')), 'type'] = 'create'
p.loc[(p['edit_type'] == '/* wbsetlabeldescriptionaliases'), 'type'] = 'term'

p = p.drop(['entity_type', 'prev_edit_id', 'comment'], axis=1)


# Extracting keywords
term = p.loc[p['type'] == 'term']
language_list = [info.split(' */')[-2].split('|')[-1] for info in term['edit_info']]
term['info'] = language_list

alias = p.loc[p['type'] == 'alias']
language_list = [info.split('|')[1].split(' */')[0] for info in alias['edit_info']]
alias['info'] = language_list

description = p.loc[p['type'] == 'description']
language_list = [info.split('|')[1].split(' */')[0] for info in description['edit_info']]
description['info'] = language_list

label = p.loc[p['type'] == 'label']
language_list = [info.split('|')[1].split(' */')[0] for info in label['edit_info']]
label['info'] = language_list

statement = p.loc[p['type'] == 'statement']
p_id_list = []
for info in statement['edit_info']:
    if 'Property:' in info:
        p_id_list.append(info.split('[[')[1].split(']]')[0])
    elif 'hanging' in info:
        p_id_list.append('Property:P' + info.split('P')[1].split(' ')[0])
    else:
        p_id_list.append('')
statement['info'] = p_id_list

claim = p.loc[p['type'] == 'claim']
p_id_list = [info.split('[[')[1].split(']]')[0] for info in claim['edit_info']]
claim['info'] = p_id_list

qualifier = p.loc[p['type'] == 'qualifier']
p_id_list = [info.split('[[')[1].split(']]')[0] for info in qualifier['edit_info']]
qualifier['info'] = p_id_list

reference = p.loc[p['type'] == 'reference']
p_id_list = [info.split('[[')[1].split(']]')[0] for info in reference['edit_info']]
reference['info'] = p_id_list

create = p.loc[p['type'] == 'create']
language_list = [info.split('|')[1].split(' */')[0] for info in create['edit_info']]
create['info'] = language_list

revert = p.loc[p['type'] == 'revert']
target_edit_list = []
for info in revert['edit_info']:
    if '||' in info:
        target_edit_list.append(info.split('||')[1].split('|')[0])
    else:
        target_edit_list.append('')
revert['info'] = target_edit_list

change_data_type = p.loc[p['type'] == 'change data type']
change_data_type['info'] = ''

protect = p.loc[p['type'] == 'protect']
protect['info'] = ''

override = p.loc[p['type'] == 'override']
override['info'] = ''

property = pd.concat([alias,change_data_type, claim, create, description, label, override, protect, qualifier, reference, revert, term, statement], axis=0)
property['edit_info'] = property['edit_info'].astype(str)
content_list = [info.split('*/ ')[-1] for info in property['edit_info']]
property['content'] = content_list
property = property.drop(['edit_info'], axis=1)

# Export the final dataset
property.to_csv('E:/wiki_editlog/property_processed.txt', sep='\t', header=False, index=False)

