import os
from pywinauto import Desktop, Application
from pywinauto.keyboard import send_keys
import time

### your chrome url shortcut path
short_cutpath = r'your\folder\path'
### dowloaded html file path
data_storage = r'your\folder\path'


### function
def delete_exist(long_path , name):
    """
    if html exist, delete the file
    """
    abso_path = long_path
    exist_name = name.replace('.lnk','.html')
    exist_name = exist_name.replace(' ','')
   
    if os.path.exists(f'{abso_path}\{exist_name}'):
        os.remove(f'{abso_path}\{exist_name}')
    else:
        pass

def similarweb_short_extract(shortcut_path):
    """
    extract the short of similar web chrome
    """
    return_list = None
    abo_path = shortcut_path
   
    ### retreive the ink file name
    return_list = os.listdir(abo_path)
    return_list = [list_dir for list_dir in return_list  if 'lnk' in list_dir]
   
    ### return path"
    return return_list

def html_downloader(list_web , abspath , data_storage):
    """
    download the html file of the website
    """
    ### start the shortcut
    os.startfile(f'{short_cutpath}\{list_web}')
    time.sleep(20)
   
    ### identify the short cut
    app = Application(backend = 'uia').connect(title_re = '.*Market Share Stats')
    send_keys('^s')
    time.sleep(10)
   
    ### check existing
    check_delete = delete_exist(data_storage , list_web)
   
    ### type the name of the path
    win = app.window(title_re = '.*Market Share Stats')
   
    ### go to another path first
    win.type_keys(short_cutpath,set_foreground=False)
    send_keys('~')
   
    ### go to target path
    win.type_keys(data_storage,set_foreground=False)
    send_keys('~')

    ### delete int and reduce space
    list_web = list_web.replace('.lnk','')
    list_web = list_web.replace(' ','')
    win.type_keys(list_web+'.html',set_foreground=False)
    send_keys('~')

    ### send yes
    time.sleep(5)
    send_keys('~')
   
    ### close the tab
    send_keys('^{F4}')
    
def main():
    ink_path = similarweb_short_extract(short_cutpath)
   
    ### looop through web
    for path in ink_path:
        html_downloader(path,short_cutpath ,data_storage)

if __name__ == '__main__':
    html_extract = main()
