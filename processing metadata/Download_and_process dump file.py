# coding: utf-8

# Data downloading and initially processing
import json
import os
import os.path
import gzip
import time
import re


# Function for downloading the dump file
def download_file(file_name, url, dir_path):
    # fname: the name you want to give to the downloaded file
    # origin: the download URL
    # cache_subdir: the file path
    file_name = file_name + '.gz'
    try:
        path = get_file(fname=file_name, origin=url, cache_subdir=dir_path)
    except:
        print('Error')
        raise
 
    
# Functions for processing the dump file   
def write_output(data_lst, fw):
    fw.write('\t'.join(data_lst))
    fw.write('\n')             

def process(decompression_dir, file_name, processed_dir, start_time, expire_time):
    print('Start to process...')
    
    filepath = decompression_dir + file_name
    tgt_filename = processed_dir + file_name + '_processed.txt'
    input = open(filepath, 'rt', encoding='utf-8')
    fw = open(tgt_filename, 'w', encoding='utf-8')

    tagRE = re.compile(r'(.*?)<(/?\w+)[^>]*>(?:([^<]*)(<.*?>)?)?')
    
    title = ''
    entity_type = ''
    revision_id = ''
    pre_revision_id = ''
    timestamp = ''
    user_name = ''
    edit_type = ''
    edit_date = ''
    edit_time = ''
    edit_timestamp = edit_date + ' ' + edit_time

    is_revision_id = False
    is_contributor = False
    is_valid = False

    for line in input:
        if '<' not in line:  
            continue
        m = tagRE.search(line)
        if not m:
            continue
        tag = m.group(2)
        if tag == 'page':
            page = []
            redirect = False
        elif tag == 'revision':
            is_revision_id = not is_revision_id
        elif tag == '/revision':
            edit_timestamp = edit_date + ' ' + edit_time
            if (int(edit_date[:4]) < int(start_time)) or (int(edit_date[:4]) > int(expire_time)):
                is_valid = False
            if is_valid:
                write_output([title, entity_type, revision_id, pre_revision_id, edit_timestamp, user_name, edit_type], fw)
            # Reset all information
            entity_type = ''
            revision_id = ''
            pre_revision_id = ''
            user_name = ''
            edit_type = ''
            edit_date = ''
            edit_time = ''

            is_revision_id = False
            is_contributor = False
            is_valid = False


        elif tag == 'contributor' or tag == '/contributor':
            is_contributor = not is_contributor
        elif tag == 'id' and is_contributor:
            user_id = m.group(3)
        elif tag == 'username':
            user_name = m.group(3)
        elif tag == 'id' and is_revision_id: 
            revision_id = m.group(3)
        elif tag == 'parentid':
            pre_revision_id = m.group(3)
        elif tag == 'title':
            title = m.group(3)
        elif tag == '/page':
            colon = title.find(':')

        elif tag == 'timestamp':
            timestamp = m.group(3)
            date_str = re.search('\d{4}\-\d+\-\d+', timestamp)
            if date_str:
                edit_date = date_str.group(0)

            date_str = re.search('\d+:\d+:\d+', timestamp)
            if date_str:
                edit_time = date_str.group(0)

        elif tag == 'model':
            model = m.group(3)
            if (model == 'wikibase-item') or (model == 'wikibase-property'):
                is_valid = True
                entity_type = m.group(3)
            else:
                is_valid = False
        elif tag == 'comment':
            edit_type = m.group(3)


    input.close()
    fw.close()
    print('Finish processing')
    
    
    
# ==================================================================================================

# Get the download URL from the dumpstatus file
path = 'dumpstatus.json'
result = open(path,"r")
data = json.load(result)
dump_url = data['jobs']['xmlstubsdumprecombine']['files']['wikidatawiki-20220401-stub-meta-history.xml.gz']['url']
    
start = time.time()
file_name = dump_url.split('-')[4][:-3]    # filename
dir_path='E:/stub_current/'      # filepath
download_url = 'https://dumps.wikimedia.org' + url
    
if not os.path.exists(dir_path):
    os.mkdir(dir_path)
if not os.path.exists(decompression_dir):
    os.mkdir(decompression_dir)
if not os.path.exists(processed_dir):
    os.mkdir(processed_dir)
   
             
# Downloading
download_file(file_name, download_url, dir_path)
print('Finish downloading')
 
             
# Processing    
decompression_dir = 'E:/stub_history/'
file_name = 'stub-history.xml'
processed_dir = 'E:/wiki_editlog/2021_processed/' 
start_time = '2021'
expire_time = '2022'  
process(decompression_dir, file_name, processed_dir, start_time, expire_time)

