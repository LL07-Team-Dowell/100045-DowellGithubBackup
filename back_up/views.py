from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt

from dowellfunction.dowellconnection import dowellconnection
from dowellfunction.dowelleventid import get_event_id
from dowellfunction.population import targeted_population

import os
import git
import zipfile
from mega import Mega
import time
from datetime import datetime
import string
import random



@csrf_exempt
def index(request):
    return JsonResponse({"Status":"Server is working"})

@csrf_exempt
def repositoryClone(request):
    try:
        repository_name = "100058-dowelleditor_backend"
        repository_url= "https://github.com/LL04-Finance-Dowell/100058-dowelleditor_backend.git"
        function_number="100058"
        path="/home/100045/Repository"

        os.chdir(path)
        os.system(f'git clone {repository_url}')
        filename ="post-merge"
        paths=f"/home/100045/Repository{repository_name}/.git/hooks"
        completepath = os.path.join(paths, filename)
        post_merge = open(completepath, "w")
        line=["!/bin/sh \n","touch /var/www/100045_pythonanywhere_com_wsgi.py \n"]
        post_merge.writelines(line)
        post_merge.close()
        os.chdir(paths)
        os.system("chmod +x post-merge")

        field ={
            "eventId":get_event_id(),
            "repository_details": {
                "repository_name":repository_name,
                "repository_url":repository_url,
                "function_number":function_number,
                "webhook_link":f"https://100090.pythonanywhere.com/backup/{repository_name}/"
                }
            }
        inserted_data = dowellconnection("dowellbackup","repository","repository","repository_list","100045001","ABCDE","insert",field)

        return JsonResponse({
            "inserted_id":inserted_data,
            "status":f"{repository_name} has been clonned .",
            "webhook_link":f"https://100090.pythonanywhere.com/backup/{repository_name}/"
            })
    except:
        return JsonResponse({
            "status":f"{repository_name} was not clonned ."
            })

@csrf_exempt
def webhookss(request , repository_name):
    if request.method == 'POST':
        repo = git.Repo(f'/home/100045/Repository/{repository_name}/.git')
        origin = repo.remotes.origin
        origin.pull()

        def zipdir(path, ziph):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        ziph.write(os.path.join(root, file))
        eventId=get_event_id()
        zip_file_name = f'{repository_name} {eventId}.zip'
        time.sleep(10)

        pathname= f'/home/100045/Zip files/{zip_file_name}'
        zipf = zipfile.ZipFile(pathname, 'w', zipfile.ZIP_DEFLATED)
        zipdir(f'/home/100045/Repository/{repository_name}', zipf)
        zipf.close()
        time.sleep(10)

        field ={
            "eventId":eventId,
            "backup_reports":{
                "function_number":repository_name.split("-")[0],
                "zip_file_name":zip_file_name
                }
            }
        inserted_data = dowellconnection("dowellbackup","repository","backup_reports","backup_reports","100045003","ABCDE","insert",field)
        time.sleep(10)

        mega = Mega()
        m = mega.login("mdashsharma95@gmail.com", "Q1e2r3s4$")
        Folder = m.find("github")
        m.upload(pathname, Folder[0])
        time.sleep(10)

        return JsonResponse({
            "inserted_data":inserted_data,
            "Response":'Updated PythonAnywhere successfully',
            "status":"200"
        })
    else:
        return JsonResponse({
            "Response":'Failed to upload.',
            "status":"400"
        })



