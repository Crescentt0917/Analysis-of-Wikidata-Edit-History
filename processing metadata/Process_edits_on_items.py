# coding: utf-8

import pandas as pd
import numpy as np

col_name = ['entity_id', 'entity_type', 'edit_id', 'prev_edit_id', 'edit_timestamp', 'editor_name', 'comment', 'edit_type', 'edit_info']
edits_q = pd.read_csv('E:/wiki_editlog/item.txt', sep='\t', header=None)
edits_q.columns = col_name

# Normalisation
edit_type_list = []
for edit_type in edits_q['edit_type']:
        
    if edit_type == '/* wbmergeitems-from':
        edit_type_list.append('be merged from')
    elif edit_type == '/* wbmergeitems-to':
        edit_type_list.append('be merged to')
    elif edit_type == '/* wbcreateredirect':
        edit_type_list.append('redirect')
        
    elif edit_type == '/* wbsetlabeldescriptionaliases' or edit_type == '/* wbeditentity-update' or '/* wbeditentity-update-languages' in edit_type:
        edit_type_list.append('change entity terms')
    elif edit_type == '/* wbeditentity-override':
        edit_type_list.append('override entity')
        
    elif edit_type == '/* wbsetlabel-set':
        edit_type_list.append('change label')
    elif edit_type == '/* wbsetlabel-add':
        edit_type_list.append('add label')
    elif edit_type == '/* wbsetlabel-remove':
        edit_type_list.append('remove label')
        
    elif edit_type == '/* wbsetdescription-set':
        edit_type_list.append('change description')
    elif edit_type == '/* wbsetdescription-add':
        edit_type_list.append('add description')
    elif edit_type == '/* wbsetdescription-remove':
        edit_type_list.append('remove description')
        
    elif edit_type == '/* wbsetaliases-remove':
        edit_type_list.append('remove alias')
    elif edit_type == '/* wbsetaliases-set' or edit_type == '/* wbsetaliases-update':
        edit_type_list.append('change alias')
    elif edit_type == '/* wbsetaliases-add':
        edit_type_list.append('add alias')
        
    elif edit_type == '/* wbcreateclaim-create' or edit_type == '/* wbsetclaim-create':
        edit_type_list.append('add claim')
    elif edit_type == '/* wbsetclaim-update' or edit_type == '/* wbsetclaimvalue':
        edit_type_list.append('change claim')
    elif edit_type == '/* wbremoveclaims-remove' or edit_type == '/* wbremoveclaims-update':
        edit_type_list.append('remove claim')  
        
    elif edit_type == '/* wbremovereferences-remove' or edit_type == '/* wbremovereferences-update':
        edit_type_list.append('remove reference')
    elif edit_type == '/* wbsetreference-set':
        edit_type_list.append('change reference')
    elif edit_type == '/* wbsetreference-add':
        edit_type_list.append('add reference') 

    elif edit_type == '/* wbsetqualifier-update':
        edit_type_list.append('change qualifier')
    elif edit_type == '/* wbsetqualifier-add':
        edit_type_list.append('add qualifier')
    elif edit_type == '/* wbremovequalifiers-remove' or edit_type == '/* wbremovequalifiers-update':
        edit_type_list.append('remove qualifier')
        
    elif edit_type == '/* clientsitelink-remove' or edit_type == '/* wbsetsitelink-remove':
        edit_type_list.append('remove sitelink')
    elif edit_type == '/* clientsitelink-update' or edit_type == '/* wbsetsitelink-set':
        edit_type_list.append('change sitelink')
    elif edit_type == '/* wbsetsitelink-set-both':
        edit_type_list.append('change sitelink & badges')
    elif edit_type == '/* wbsetsitelink-add-both':
        edit_type_list.append('add sitelink & badges')
    elif edit_type == '/* wbsetsitelink-set-badges':
        edit_type_list.append('change badges')
    elif edit_type == '/* wbsetsitelink-add':
        edit_type_list.append('add sitelink')
    elif edit_type == '/* wblinktitles-connect':
        edit_type_list.append('connect sitelinks')
        
    elif 'Protected "' in edit_type:
        edit_type_list.append('protect')
    elif 'Changed protection settings' in edit_type:
        edit_type_list.append('change protection settings')
    elif 'Changed protection level' in edit_type:
        edit_type_list.append('change protection level')
    elif 'Removed protection' in edit_type:
        edit_type_list.append('remove protection')
        
    elif edit_type == '/* undo':
        edit_type_list.append('undo')
    elif 'Undid revision ' in edit_type or 'Undo revision ' in edit_type:
        edit_type_list.append('undo')
    elif 'Undid edits ' in edit_type or 'Undo edits ' in edit_type: 
        edit_type_list.append('undo')
    elif 'rollback' in edit_type or 'undid' in edit_type:
        edit_type_list.append('undo')
        
    elif edit_type == '/* restore':
        edit_type_list.append('revert')
    elif edit_type == '[[WD' or 'Reverted to revision ' in edit_type or 'Reverted page to revision ' in edit_type or 'Restored revision ' in edit_type:
        edit_type_list.append('revert')
    elif 'revert' in edit_type or 'Reverted ' in edit_type:
        edit_type_list.append('revert')
    elif 'rv' in edit_type or 'Rv ' in edit_type:
        edit_type_list.append('revert')
    elif 'Revert' in edit_type:
        edit_type_list.append('revert')
        
    else:
        edit_type_list.append('')
        
edits_q['type'] = edit_type_list


# Split the whole dataset into different categories
edits_q_protect = edits_q[edits_q['type'].isin(['protect', 'change protection level', 'change protection settings', 'remove protection'])]
edits_q_merge = edits_q[edits_q['type'].isin(['be merged from', 'be merged to', 'redirect'])]
edits_q_change_terms = edits_q[edits_q['type'] == 'change entity terms']
edits_q_override = edits_q[edits_q['type'] == 'override entity']
edits_q_label = edits_q[edits_q['type'].isin(['add label', 'change label', 'remove label'])]
edits_q_description = edits_q[edits_q['type'].isin(['add description', 'change description', 'remove description'])]
edits_q_alias = edits_q[edits_q['type'].isin(['add alias', 'change alias', 'remove alias'])]
edits_q_claim = edits_q[edits_q['type'].isin(['add claim', 'change claim', 'remove claim'])]
edits_q_reference = edits_q[edits_q['type'].isin(['add reference', 'change reference', 'remove reference'])]
edits_q_qualifier = edits_q[edits_q['type'].isin(['add qualifier', 'change qualifier', 'remove qualifier'])]
edits_q_sitelink = edits_q[edits_q['type'].isin(['add sitelink', 'change sitelink', 'remove sitelink', 'add sitelink & badges', 'change sitelink & badges', 'change badges', 'connect sitelinks'])]
edits_q_revert = edits_q[edits_q['type'] == 'revert']
edits_q_undo = edits_q[edits_q['type'] == 'undo']


# Export to multiple files
edits_q_protect.to_csv('E:/wiki_editlog/type/protect/edits_q_protect.txt' ,sep='\t' ,index=False ,header=False)
edits_q_merge.to_csv('E:/wiki_editlog/type/merge/edits_q_merge.txt' ,sep='\t' ,index=False ,header=False)
edits_q_change_terms.to_csv('E:/wiki_editlog/type/change_terms/edits_q_change_terms.txt' ,sep='\t' ,index=False ,header=False)
edits_q_override.to_csv('E:/wiki_editlog/type/override/edits_q_override.txt' ,sep='\t' ,index=False ,header=False)
edits_q_label.to_csv('E:/wiki_editlog/type/label/edits_q_label.txt' ,sep='\t' ,index=False ,header=False)
edits_q_description.to_csv('E:/wiki_editlog/type/description/edits_q_description.txt' ,sep='\t' ,index=False ,header=False)
edits_q_alias.to_csv('E:/wiki_editlog/type/alias/edits_q_alias.txt' ,sep='\t' ,index=False ,header=False)
edits_q_claim.to_csv('E:/wiki_editlog/type/claim/edits_q_claim.txt' ,sep='\t' ,index=False ,header=False)
edits_q_reference.to_csv('E:/wiki_editlog/type/reference/edits_q_reference.txt' ,sep='\t' ,index=False ,header=False)
edits_q_qualifier.to_csv('E:/wiki_editlog/type/qualifier/edits_q_qualifier.txt' ,sep='\t' ,index=False ,header=False)
edits_q_sitelink.to_csv('E:/wiki_editlog/type/sitelink/edits_q_sitelink.txt' ,sep='\t' ,index=False ,header=False)
edits_q_revert.to_csv('E:/wiki_editlog/type/revert/edits_q_revert.txt' ,sep='\t' ,index=False ,header=False)
edits_q_undo.to_csv('E:/wiki_editlog/type/undo/edits_q_undo.txt' ,sep='\t' ,index=False ,header=False)



#=============================================================================================================

'''
    Extracting keywords in each category.

'''
# Read sorted files
col_name = ['entity_id', 'entity_type', 'edit_id', 'prev_edit_id', 'edit_timestamp', 'editor_name', 'comment', 'edit_type', 'edit_info', 'type']
q_change_terms = pd.read_csv("E:/wiki_editlog/item/q_change_terms.txt", sep='\t', header=None)
q_create_item = pd.read_csv('E:/wiki_editlog/item/q_create_item.txt', sep='\t', header=None)
q_merge = pd.read_csv('E:/wiki_editlog/item/q_merge.txt', sep='\t', header=None)
q_override = pd.read_csv('E:/wiki_editlog/item/q_override.txt', sep='\t', header=None)
q_protect = pd.read_csv('E:/wiki_editlog/item/q_protect.txt', sep='\t', header=None)
q_label = pd.read_csv('E:/wiki_editlog/item/q_label.txt', sep='\t', header=None)
q_description = pd.read_csv('E:/wiki_editlog/item/q_description.txt', sep='\t', header=None)
q_alias = pd.read_csv('E:/wiki_editlog/item/q_alias.txt', sep='\t', header=None)
q_claim_ = pd.read_csv('E:/wiki_editlog/item/q_claim.txt', sep='\t', header=None)
q_qualifier = pd.read_csv('E:/wiki_editlog/item/q_qualifier.txt', sep='\t', header=None)
q_reference = pd.read_csv('E:/wiki_editlog/item/q_reference.txt', sep='\t', header=None)
q_sitelink = pd.read_csv('E:/wiki_editlog/item/q_sitelink.txt', sep='\t', header=None)
q_revert = pd.read_csv('E:/wiki_editlog/item/q_revert.txt', sep='\t', header=None)
q_undo = pd.read_csv("D:/wiki_editlog/item/q_undo.txt", sep='\t', header=None)


# change_terms
terms = q_change_terms.loc[q_change_terms['edit_type'] == '/* wbsetlabeldescriptionaliases']
content_list = []
languages_list = []
for info in terms['edit_info']:
    languages_list.append(info.split('|')[1].split(' */')[0])
    if len(info.split('*/ ')) > 1:
        content_list.append(info.split('*/ ')[1])
    else:
        content_list.append('')
terms['content'] = content_list
terms['languages'] = languages_list

terms = terms.drop(['entity_type', 'comment', 'type', 'edit_info'],axis=1)


update_languages_short = q_change_terms.loc[(q_change_terms['edit_type'] == '/* wbeditentity-update-languages-and-other-short') | (q_change_terms['edit_type'] == '/* wbeditentity-update-languages-short')]
content_list = []
languages_list = []
for info in update_languages_short['edit_info']:
    languages_list.append(info.split('||')[1].split(' */')[0])
    if len(info.split('*/ ')) > 1:
        content_list.append(info.split('*/ ')[1])
    else:
        content_list.append('')
update_languages_short['content'] = content_list
update_languages_short['languages_amount'] = languages_list

update_languages_short = update_languages_short.drop(['entity_type', 'comment', 'type', 'edit_info'],axis=1)


update_languages = q_change_terms.loc[(q_change_terms['edit_type'] == '/* wbeditentity-update-languages') | (q_change_terms['edit_type'] == '/* wbeditentity-update-languages-and-other')]
content_list = []
languages_amount = []
for info in update_languages_11['edit_info']:
    languages_amount.append(info.split('||')[1].split(' */')[0])
    if len(info.split('*/ ')) > 1:
        content_list.append(info.split('*/ ')[1])
    else:
        content_list.append('')
update_languages['content'] = content_list
update_languages['languages_amount'] = languages_amount

update_languages = update_languages.drop(['entity_type', 'comment', 'type', 'edit_info'],axis=1)


update_item = q_change_terms.loc[q_change_terms['edit_type'] == '/* wbeditentity-update']
content_list = []
for info in update_item['edit_info']:
    content_list.append(info.split('*/ ')[-1])    
update_item['content'] = content_list

update_item.loc[update_item['content'] == '0| */',['content']] = ''
update_item = update_item_11.drop(['entity_type', 'comment', 'type', 'edit_info'],axis=1)


# create
create_item_only = q_create_item.loc[q_create_item['edit_type'] == '/* wbeditentity-create-item']
create_item_only['content'] = [info.split('*/ ')[-1] for info in create_item_only['edit_info']]
create_item_only['language'] = ''
create_item_only = create_item_only.drop(['entity_type', 'comment', 'edit_info', 'type'], axis=1)

create_item = q_create_item.loc[q_create_item['edit_type'] == '/* wbeditentity-create']
create_item['language'] = [info.split('|')[1].split(' */')[0] for info in create_item['edit_info']]
create_item['content'] = [info.split('*/ ')[-1] for info in create_item['edit_info']]
create_item = create_item.drop(['entity_type', 'comment', 'edit_info', 'type'], axis=1)

q_create_item = pd.concat([create_item_only, create_item], axis=0)
q_create_item.to_csv('E:/wiki_editlog/type_processed/create_item/q_create_item.txt', index=False, sep='\t', header=False)


# merge
redirect = q_merge.loc[q_merge['edit_type'] == '/* wbcreateredirect']
redirect['target_item'] = [info.split('|')[3].split(' ')[0] for info in redirect['edit_info']]
redirect['content'] = [info.split('/* ')[-1] for info in redirect['edit_info']]
redirect = redirect.drop(['entity_type', 'comment', 'edit_info', 'type'], axis=1)

merge = q_merge.loc[q_merge['edit_type'] != '/* wbcreateredirect']
merge['target_item'] = [info.split('||')[1].split(' ')[0] for info in merge['edit_info']]
merge['content'] = [info.split('/* ')[-1] for info in merge['edit_info']]
merge = merge.drop(['entity_type', 'comment', 'edit_info', 'type'], axis=1)
merge_from = merge.loc[merge['edit_type'] == '/* wbmergeitems-from']
merge_to = merge.loc[merge['edit_type'] != '/* wbmergeitems-from']
merge_from['target_item'], merge_from['entity_id'] = merge_from['entity_id'], merge_from['target_item']
q_merge = pd.concat([merge_from, merge_to, redirect])
q_merge.to_csv('E:/wiki_editlog/type_processed/merge/q_merge.txt', sep='\t', index=False, header=False)


# override
q_override['content'] = [info.split('*/ ')[-1] for info in q_override['edit_info']] 
q_override = q_override.drop(['entity_type', 'comment', 'edit_info', 'type'], axis=1)
q_override.to_csv('E:/wiki_editlog/type_processed/override/q_override.txt',index=False, sep='\t', header=None)


# protect
q_protect['content'] = q_protect['edit_info']
q_protect['edit_type'] = q_protect['type']
q_protect = q_protect.drop(['entity_type', 'comment', 'edit_info', 'type'], axis=1)
q_protect.to_csv('E:/wiki_editlog/type_processed/protect/q_protect.txt', sep='\t', index=False, header=False)


# label
language_list = []
content_list = []
for info in q_label['edit_info']:
    language_list.append(info.split('|')[1].split(' */')[0])
    if info.split('|')[0] != '0':
        content_list.append(info.split('*/ ')[1])
    else:
        content_list.append('')
q_label['language'] = language_list
q_label['content'] = content_list
q_label = q_label.drop(['entity_type', 'comment', 'type', 'edit_info'],axis=1)
q_label['prev_edit_id'] = q_label['prev_edit_id'].fillna(0).astype(int)
q_label['edit_timestamp'] = pd.to_datetime(q_label['edit_timestamp'])
q_label.to_csv('E:/wiki_editlog/type_processed/label/q_label.txt' ,sep='\t' ,index=False ,header=False)


# description
language_list = []
content_list = []
for info in q_description['edit_info']:
    language_list.append(info.split('|')[1].split(' */')[0])
    if info.split('|')[0] != '0':
        content_list.append(info.split('*/ ')[1])
    else:
        content_list.append('')
q_description['language'] = language_list
q_description['content'] = content_list
q_description = q_description.drop(['entity_type', 'comment', 'type', 'edit_info'],axis=1)
q_description.to_csv('E:/wiki_editlog/type_processed/description/q_description.txt' ,sep='\t' ,index=False ,header=False)


# alias
language_list = []
content_list = []
for info in q_alias['edit_info']:
    language_list.append(info.split('|')[1].split(' */')[0])
    if info.split('|')[0] != '0':
        content_list.append(info.split('*/ ')[1])
    else:
        content_list.append('')
q_alias['language'] = language_list
q_alias['content'] = content_list
q_alias = q_alias.drop(['entity_type', 'comment', 'type', 'edit_info'],axis=1)
q_alias.to_csv('E:/wiki_editlog/type_processed/q_alias.txt' ,sep='\t' ,index=False ,header=False)


# claim
claim = q_claim.loc[q_claim['edit_type'] != '/* wbremoveclaims-update']
remove_update = q_claim.loc[q_claim['edit_type'] == '/* wbremoveclaims-update']

claim['property_id'] = [info.split('[[')[1].split(']]')[0] for info in claim['edit_info']]
claim['content'] = [info.split(':')[2] for info in claim['edit_info']]

remove_update['property_id'] = ''
remove_update['content'] = ''
remove_update['edit_type'] = '/* wbsetclaims-remove'

q_claim = pd.concat([claim, remove_update], axis=0)
q_claim = q_claim.drop(['entity_type', 'comment', 'edit_info', 'type'], axis=1)
q_claim.to_csv('E:/wiki_editlog/type_processed/claim/q_claim.txt' ,sep='\t' ,index=False ,header=False)


# qualifier
qualifier = q_qualifier.loc[q_qualifier['edit_type'] != '/* wbremovequalifiers-update']
qualifier['property_id'] = [info.split('[[')[1].split(']]')[0] for info in qualifier['edit_info']]
qualifier['content'] = [info.split(':')[-1] for info in qualifier['edit_info']]

remove_update = q_qualifier.loc[q_qualifier['edit_type'] == '/* wbremovequalifiers-update']
remove_update['property_id'] = ''
remove_update['content'] = [info.split('*/ ')[-1] for info in remove_update['edit_info']]
remove_update['edit_type'] = '/* wbsetqualifier-remove'

q_qualifier = pd.concat([qualifier, remove_update], axis=0)
q_qualifier = q_qualifier.drop(['entity_type', 'comment',  'edit_info', 'type'], axis=1)
q_qualifier.to_csv('E:/wiki_editlog/type_processed/qualifier/q_qualifier.txt' ,sep='\t' ,index=False ,header=False)


# reference
reference = q_reference.loc[q_reference['edit_type'] != '/* wbremovereferences-update']
reference['property_id'] = [info.split('[[')[1].split(']]')[0] for info in reference['edit_info']]
reference['content'] = [info.split(':')[-1] for info in reference['edit_info']]

remove_update = q_reference_2.loc[q_reference_2['edit_type'] == '/* wbremovereferences-update']
remove_update['property_id'] = ''
remove_update['content'] = [info.split('*/ ')[-1] for info in remove_update['edit_info']] 
remove_update['edit_type'] = '/* wbsetreference-remove'

q_reference = pd.concat([q_reference, remove_update], axis=0)
q_reference = q_reference.drop(['entity_type', 'comment',  'edit_info', 'type'], axis=1)
q_reference.to_csv('E:/wiki_editlog/type_processed/reference/q_reference.txt' ,sep='\t' ,index=False ,header=False)


# site link
add = q_sitelink.loc[q_sitelink['edit_type'] == '/* wbsetsitelink-add']
add['site'] = [info.split('|')[1].split(' */')[0] for info in add['edit_info']] 
add['content'] = [info.split('*/ ')[1] for info in add['edit_info']] 

add_1 = q_sitelink_1.loc[(q_sitelink_1['edit_info'].str.contains('Add')) | (q_sitelink_1['edit_info'].str.contains('Moving'))]
add_1['site'] = ''
add_1['content'] = add_1['edit_info']
add_1 = add_1.drop(['edit_info'], axis=1)
add_1['edit_type'] = '/* wbsetsitelink-add'
add = pd.concat([add, add_1], axis=0)

remove_1 = q_sitelink.loc[q_sitelink['edit_type'] == '/* clientsitelink-remove']
remove_1['site'] = [info.split('||')[1].split(' */')[0] for info in remove_1['edit_info']] 
remove_1['content'] = [info.split('*/ ')[1] for info in remove_1['edit_info']]
remove_2 = q_sitelink.loc[q_sitelink['edit_type'] == '/* wbsetsitelink-remove']
remove_2['site'] = [info.split('|')[1].split(' */')[0] for info in remove_2['edit_info']]
remove_2['content'] = [info.split('*/ ')[1] for info in remove_2['edit_info']] 
remove_3 = q_sitelink_1.loc[(q_sitelink_1['edit_info'].str.contains('Removing')) | (q_sitelink_1['edit_info'].str.contains('remove')) | (q_sitelink_1['edit_info'].str.contains('removing'))]
remove_3['site'] = ''
remove_3['content'] = remove_3['edit_info']
remove_3 = remove_3.drop(['edit_info'], axis=1)
remove_3['edit_type'] = '/* wbsetsitelink-remove'
remove = pd.concat([remove_1, remove_2, remove_3], axis=0)

change_1 = q_sitelink.loc[q_sitelink['edit_type'] == '/* clientsitelink-update']
change_1['site'] = [info.split('|')[1] for info in change_1['edit_info']]
change_1['content'] = change_1['edit_info']
change_2 = q_sitelink.loc[q_sitelink['edit_type'] == '/* wbsetsitelink-set']
change_2['site'] = [info.split('|')[1].split(' */')[0] for info in change_2['edit_info']]
change_2['content'] = [info.split('*/ ')[1] for info in change_2['edit_info']]
change_3 = q_sitelink_1.loc[(q_sitelink_1['edit_info'].str.contains('Set')) | (q_sitelink_1['edit_info'].str.contains('updating')) | (q_sitelink_1['edit_info'].str.contains('change'))]
change_3['site'] = ''
change_3['content'] = change_3['edit_info']
change_3 = change_3.drop(['edit_info'], axis=1)
change_3['edit_type'] = '/* wbsetsitelink-set'
change = pd.concat([change_1, change_2, change_3], axis=0)

link = q_sitelink.loc[q_sitelink['edit_type'].str.contains('wblinktitles')]
site_list = []
content_list = []
for info in link['edit_info']:
    site_list.append(info.split('*/ ')[1].split(':')[0])
    content_list.append(info.split(', ')[-1].split(':')[0])
link['site'] = site_list
link['content'] = content_list

add_both =  q_sitelink.loc[q_sitelink['edit_type'] == '/* wbsetsitelink-add-both']
site_list = []
content_list = []
for info in add_both['edit_info']:
    site_list.append(info.split('|')[1].split(' */')[0])
    content_list.append(info.split(', ')[-1])
add_both['site'] = site_list
add_both['content'] = content_list

chenge_both = q_sitelink.loc[q_sitelink['edit_type'] == '/* wbsetsitelink-set-both']
site_list = []
content_list = []
for info in chenge_both['edit_info']:
    site_list.append(info.split('|')[1].split(' */')[0])
    content_list.append(info.split(', ')[-1])
chenge_both['site'] = site_list
chenge_both['content'] = content_list

change_badge = q_sitelink.loc[q_sitelink['edit_type'] == '/* wbsetsitelink-set-badges']
site_list = []
content_list = []
for info in change_badge['edit_info']:
    site_list.append(info.split('|')[1].split(' */')[0])
    content_list.append(info.split('*/ ')[-1])
change_badge['site'] = site_list
change_badge['content'] = content_list

q_sitelink = pd.concat([add, remove, change, link, add_both, chenge_both, change_badge], axis=0)
q_sitelink = q_sitelink.drop(['entity_type', 'comment', 'edit_info', 'type'], axis=1)
q_sitelink.to_csv('E:/wiki_editlog/type_processed/sitelink/q_sitelink.txt', sep='\t', index=False, header=False)


# revert
revert_1 = q_revert.loc[q_revert['edit_type'] == '/* restore']
edit_id_list = []
content_list = []
for info in revert_1['edit_info']:
    edit_id_list.append(int(info.split('||')[1].split('|')[0]))
    content_list.append(info.split('||')[1].split('|')[1])
revert_1['target_edit_id'] = edit_id_list
revert_1['content'] = content_list

revert_2 = q_revert.loc[q_revert['edit_type'] != '/* restore']
edit_id_list = []
for info in revert_2['edit_type']:
    if 'revision' in info:
        if 'last' not in info:
            edit_id_list.append(int(info.split('revision ')[1].split(' by')[0]))
        else:
            edit_id_list.append('')
    else:
        edit_id_list.append('')
revert_2['target_edit_id'] = edit_id_list
revert_2['content'] = revert_2['comment']

q_revert = pd.concat([revert_1,revert_2],axis=0)
q_revert = q_revert.drop(['entity_type', 'comment', 'edit_info', 'type'], axis=1)


undo_1 = q_undo.loc[q_undo['edit_type'] == '/* undo']
edit_id_list = []
content_list = []
for info in undo_1['edit_info']:
    edit_id_list.append(info.split('||')[1].split('|')[0])
    content_list.append(info.split('||')[1].split('|')[1])
undo_1['target_edit_id'] = edit_id_list
undo_1['content'] = content_list


undo_2 = q_undo.loc[q_undo['edit_type'] != '/* undo']
edit_id_list = []
for info in undo_2['edit_type']:
    if 'revision' in info:
        edit_id_list.append(info.split('revision ')[1].split(' by')[0])
    else:
        edit_id_list.append('')
undo_2['target_edit_id'] = edit_id_list
undo_2['content'] = undo_2['comment']


q_undo = pd.concat([undo_1,undo_2],axis=0)
q_undo = q_undo.drop(['entity_type', 'comment', 'edit_info', 'type'], axis=1)

q_revert = pd.concat([q_revert, q_undo], axis=0)
q_revert.to_csv('E:/wiki_editlog/type_processed/revert/q_revert.txt' ,sep='\t' ,index=False ,header=False)

