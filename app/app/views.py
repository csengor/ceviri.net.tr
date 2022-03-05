from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import render

from pathlib import Path
import tempfile

from kaplan import open_bilingualfile
from kaplan.kxliff import KXLIFF

from .models import File, TranslationQuery
from .tasks import translate_doc

# Create your views here.

def home(request):
    if request.method == 'POST':
        source_language = request.POST['source_language']
        target_language = 'en' if source_language == 'tr' else 'tr'
        if request.POST.get('type') == 'doc':
            incoming_file = request.FILES['source']
            with tempfile.TemporaryDirectory() as tempdir:
                tempfile_path = Path(tempdir) / incoming_file.name
                with open(tempfile_path, 'wb') as f:
                    f.write(incoming_file.read())
                new_file = File(source_language=source_language,
                                target_language=target_language)
                if tempfile_path.suffix.lower() in ['.kxliff', '.sdlxliff', '.xliff']:
                    new_file.bilingual_file.save(tempfile_path.name, open(tempfile_path, 'rb'))
                else:
                    KXLIFF.new(str(tempfile_path), source_language, target_language).save(tempdir)
                    new_file.source_file.save(tempfile_path.name, open(tempfile_path, 'rb'))
                    temp_bfile_path = tempfile_path.with_suffix(tempfile_path.suffix + '.kxliff')
                    new_file.bilingual_file.save(temp_bfile_path.name, open(temp_bfile_path, 'rb'))
                new_file.save()

                new_query = TranslationQuery()
                new_query.content = {
                    'type': 'doc',
                    'file_id': new_file.id
                }
                new_query.save()

            return JsonResponse({'secret':new_query.secret})

        elif request.POST.get('type') == 'text':
            source_text = request.POST['source_text'].split('\n')

            new_query = TranslationQuery()
            new_query.content = {
                'type': 'text',
                'text': source_text
            }
            new_query.save()

            return JsonResponse({'secret':new_query.secret})

    return render(request, 'app/home.html')

def query(request, query_secret):
    query = TranslationQuery.objects.get(secret=query_secret)

    if query.status == 3:
        response_dict = {
            'status': 'ready',
            'type': query.content['type'],
        }

        if query.content['type'] == 'doc':
            file_instance = File.objects.get(id=query.content['file_id'])

            bilingual_file = open_bilingualfile(file_instance.bilingual_file.name)

            for tu_i, unit in query.content['target'].items():
                for s_i, segment in unit.items():
                    bilingual_file.update_segment('<target>{0}</target>'.format(segment),
                                                  tu_i,
                                                  s_i)
            with tempfile.TemporaryDirectory() as tempdir:
                if file_instance.source_file is not None:
                    bilingual_file.generate_target_translation(tempdir,
                                                               file_instance.source_file.name)
                    tempfile_path = Path(tempdir, Path(file_instance.source_file.name).name)
                else:
                    bilingual_file.save(tempdir)
                    tempfile_path = Path(tempdir, bilingual_file.name)

                file_instance.delete()
                query.delete()

                return FileResponse(open(tempfile_path, 'rb'))

        else:
            translation = ''
            for i, unit in query.content['target'].items():
                translation += unit[i] + '\n'
            response_dict['translation'] = translation

            query.delete()

        return JsonResponse(response_dict)
    else:
        return HttpResponse(status=204)

def terms_and_conditions(request):
    return render(request, 'terms-and-conditions.html')
