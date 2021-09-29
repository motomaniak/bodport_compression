import os

from celery import current_app

from django import forms
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from .tasks import compress_file


class FileUploadForm(forms.Form):
    bin_file = forms.FileField(required=True)


class HomeView(View):
    def get(self, request):
        form = FileUploadForm()
        return render(request, 'compressor/home.html', {'form': form})

    def post(self, request):
        form = FileUploadForm(request.POST, request.FILES)
        context = {}

        if form.is_valid():
            file_path = os.path.join(
                settings.FILES_DIR, request.FILES['bin_file'].name)

            with open(file_path, 'wb+') as fp:
                for chunk in request.FILES['bin_file']:
                    fp.write(chunk)

            #delay the task for the redis server
            task = compress_file.delay(file_path)

            context['task_id'] = task.id
            context['task_status'] = task.status

            # render new page to display results
            return render(request, 'compressor/task.html', context)

        context['form'] = form

        return render(request, 'compressor/home.html', context)


class TaskView(View):
    # Gets the results from the delayed task and returns it as JSON data
    # task_id is the redis/celery task_id
    def get(self, request, task_id):
        task = current_app.AsyncResult(task_id)
        response_data = {'task_status': task.status, 'task_id': task.id}

        if task.status == 'SUCCESS':
            response_data['results'] = task.get()

        return JsonResponse(response_data)
