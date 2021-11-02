#!/usr/bin/env python
import os

import django
import argparse

from django.db import models
from django.utils import timezone


def get_arguments():
    parser = argparse.ArgumentParser(description='Fetch student data from Trix. And prints it in the order: number - username - course - assignment - timestamp - solved - with help - by self')
    parser.add_argument(
        '--username-list',
        required=True,
        nargs='+',
        dest='username_list',
        help='A list of Student user shortnames. Example: --username-list username1 username2 username3'
    )
    parser.add_argument(
        '--subject-shortname',
        type=str,
        dest='subject_shortname',
        help='The shortname of a subject. This is unique.'
    )
    parser.add_argument(
        '--period-shortname',
        type=str,
        dest='period_shortname',
        help='The shortname of a period/semester. This is unique together with the subject shortname.'
    )

    return vars(parser.parse_args())

def do_solved_queryset(out, solved_queryset):
    if solved_queryset.exists():
        for solved in solved_queryset:
            out += f'{solved.solved_datetime} - yes - '
            if solved.howsolved == 'bymyself':
                out += ' no - yes'
            else:
                out += ' yes - no'
    else:
        out += f'{timezone.now()} - no - no - no'
    
    print(out)
    


if __name__ == "__main__":
    
    # For development:
    os.environ.setdefault('DJANGOENV', 'develop')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trix.project.settingsproxy")
    django.setup()

    from trix.trix_core import models as core_models


    argument_dict = get_arguments()

    at = 0
    assignments = core_models.Assignment.objects.all()
    period_tag = None
    course_tag = None
    if argument_dict['subject_shortname'] != None :
        subject = argument_dict['subject_shortname']
        try:
            course_tag = core_models.Tag.objects.get(tag=subject, category='c')
            assignments = assignments.filter(tags=course_tag)
        except core_models.Tag.DoesNotExist:
            print(f'!!!{subject} Does not exist!!!')
    if argument_dict['period_shortname'] != None:
        period = argument_dict['period_shortname']
        try:
            period_tag = core_models.Tag.objects.get(tag=period, category='p')
            assignments = assignments.filter(tags=period_tag)
        except:
            print(f'!!!{period} Does not exist!!!')

    

    for user_shortname in argument_dict['username_list']:
        try:
            for assignment in assignments:
                user = core_models.User.objects.get(email=user_shortname)
                solved_queryset = core_models.HowSolved.objects.filter(assignment=assignment, user=user)
                subject_name = ''
                if course_tag != None:
                    subject_name = course_tag
                else:
                    for c in assignment.tags.filter(category='c'):
                        subject_name += f'{c}/'
                    subject_name = subject_name[:-1]
                if period_tag != None:
                    out = f'{at} - {user_shortname} - {period_tag} - {subject_name} - {assignment} - '
                    do_solved_queryset(out, solved_queryset)
                else:
                    for p in assignment.tags.filter(category='p'):
                        out = f'{at} - {user_shortname} - {p} - {subject_name} - {assignment} - '
                        do_solved_queryset(out, solved_queryset)

                at += 1
        except core_models.User.DoesNotExist:
            print(f'!!!{user_shortname} Not found!!!')


        


   