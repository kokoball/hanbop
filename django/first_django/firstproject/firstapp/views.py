from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect,HttpResponse,FileResponse
from .forms import UploadForm
from .models import FileUpload
from django.conf import settings
import os

# Create your views here.

# *********************************************************
#                   html파일 나타내는 view
# *********************************************************

# 인덱스 템플릿
def index(request):
    return render(request,'index.html',{})

# 파일 업로드 페이지
def upload_file(request):
    reset(request)
    if request.method=='POST':
        form=UploadForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('file_list')
    else:
        form=UploadForm()
    return render(request,'upload.html',{
        'form':form
    })
from .extract_wav import extract_wav
from .storage_upload import upload_blob
from .video_transcripts import transcribe_model_selection_gcs
import argparse

# 로딩페이지
# : 모델에 적용 후 완료시 file_list로 넘어가는 작업 필요
def loading(request):
    files =FileUpload.objects.all()
    file = files[0]
    file_path=file.pic.path

    file_name = file.pic
    file_name = str(file_name).split('.')[0]
    print('##########',file_name)
    gs_uri = f'gs://my_first_ko/{file_name}'

    path_to_wav = extract_wav(file_path)
    path_to_mediadir = path_to_wav.split(file_name)[0]
    print('########extract_wav completed')

    upload_blob(bucket_name='my_first_ko', source_file_name=path_to_wav, destination_blob_name=file_name)

    print('########upload to storage completed')

    transcribe_model_selection_gcs(path_to_mediadir, file_name, gs_uri, 'default')
    print('########script completed')

# 파일 업로드 시 리스트 보여주는 페이지
def file_list(request):
    loading(request)
    files=FileUpload.objects.all()
    file = files[0]
    file_path=file.pic.path
    file_name = file.pic
    mediadir = file_path.split(str(file_name))[0]
    file_name = str(file_name).split('.')[0]

    print(mediadir)

    files = os.listdir(mediadir)
    file_list = []
    for file in files:
        if (file.split('.')[-1] == 'csv'):
            file_list.append(file)
    context={
        'files': file_list,
    }
    return render(request,'list.html',context)




# *********************************************************
#                   내부에서 작동하는 코드
# *********************************************************

# 내부의 필요없는 파일을 삭제해주는 함수
def reset(request):
    files=FileUpload.objects.all()
    files.delete()

    return redirect('upload_file')

# file_list의 파일 클릭 시 다운하는 함수
def down(request,selected_file):
    files=FileUpload.objects.all()
    file = files[0]
    file_path=file.pic.path
    file_name = file.pic
    mediadir = file_path.split(str(file_name))[0]
    print(selected_file)

    import mimetypes 
    import urllib
    file_path = mediadir + str(selected_file)
    with open(file_path, 'rb') as fh: 
        response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_path)[0]) 
        # response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % file_name 
        return response

# 출처: https://www.devoops.kr/69 [데브웁스]
#     content = open(mediadir + str(selected_file)).read()
#     response = HttpResponse(open(content, 'rb'), content_type='text/css')
#     response['Content-Disposition'] = 'attachment; filename="file.css"'
#     return response