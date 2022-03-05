from django.apps import apps
from django.conf import settings

from celery import shared_task
from kaplan import open_bilingualfile
import requests

import html

@shared_task
def translate_doc(file_instance_id, query_id, char_limit=1024):
    SegmentModel = apps.get_model('app', 'Segment')
    file_instance = apps.get_model('app', 'File').objects.get(id=file_instance_id)
    query = {'language': 'tr_TR' if file_instance.source_language == 'tr' else 'en_XX'}

    cur_len = 0
    target = {}
    source_units = {}
    for tu in open_bilingualfile(file_instance.bilingual_file.path).gen_translation_units():
        target[str(tu.attrib['id'])] = {}
        source_unit = {}
        for segment in tu:
            if segment.tag.endswith('ignorable'):
                continue
            source_text= ''
            if segment[0].text is not None:
                source_text += segment[0].text
            for child in segment[0]:
                if child.tail is not None:
                    source_text += child.tail
            if len(source_text) < char_limit - cur_len:
                segments = SegmentModel.objects.filter(source=source_text) | SegmentModel.objects.filter(reviewed_source=source_text)
                segments = segments.exclude(target='', reviewed_target='')
                if len(segments) > 0:
                    segment_hit = segments[0]
                    target[str(tu.attrib['id'])][str(segment.attrib['id'])] = segment_hit.reviewed_target if segment_hit.reviewed_target != '' else segment_hit.target
                else:
                    source_unit[str(segment.attrib['id'])] = html.escape(source_text)

                cur_len += len(source_text)
            else:
                break
        if source_unit != {}:
            source_units[tu.attrib['id']] = source_unit

    if source_units != {}:
        query['units'] = source_units

        r = requests.post(settings.NMT_BACKEND, json=query)

        for tu_i, unit in r.json()['units'].items():
            for s_i, segment in unit.items():
                target[tu_i][s_i] = html.escape(segment)

                new_segment = SegmentModel()
                new_segment.source_language = file_instance.source_language
                new_segment.target_language = file_instance.target_language
                new_segment.source = source_units[tu_i][s_i]
                new_segment.target = segment
                new_segment.save()

    query_instance = apps.get_model('app', 'TranslationQuery').objects.get(id=query_id)
    query_instance.content['target'] = target
    query_instance.status = 3
    query_instance.save(no_override=True)

@shared_task
def translate_text(source, query_id, char_limit=1024):
    SegmentModel = apps.get_model('app', 'Segment')
    query_instance = apps.get_model('app', 'TranslationQuery').objects.get(id=query_id)
    query = {'language': 'tr_TR' if query_instance.source_language == 'tr' else 'en_XX'}

    cur_len = 0
    target = {}
    source_units = {}
    for i, unit in enumerate(source):
        target[str(i)] = {}
        unit = unit.strip()
        if unit == '':
            target[str(i)] = {str(i): unit}
            continue
        if len(unit) < char_limit - cur_len:
            segments = SegmentModel.objects.filter(source=unit) | SegmentModel.objects.filter(reviewed_source=unit)
            segments = segments.exclude(target='', reviewed_target='')
            if len(segments) > 0:
                segment_hit = segments[0]
                target[str(i)] = {str(i): segment_hit.reviewed_target if segment_hit.reviewed_target != '' else segment_hit.target}
            else:
                source_units[str(i)] = {str(i): unit}
            cur_len += len(unit)
        else:
            break

    if source_units != {}:
        query['units'] = source_units

        r = requests.post(settings.NMT_BACKEND, json=query)
        for tu_i, unit in r.json()['units'].items():
            for s_i, segment in unit.items():
                target[tu_i][s_i] = html.escape(segment)

                new_segment = SegmentModel()
                new_segment.source_language = query_instance.source_language
                new_segment.target_language = query_instance.target_language
                new_segment.source = source_units[tu_i][s_i]
                new_segment.target = segment
                new_segment.save()

    query_instance = apps.get_model('app', 'TranslationQuery').objects.get(id=query_id)
    query_instance.content['target'] = target
    query_instance.status = 3
    query_instance.save(no_override=True)
