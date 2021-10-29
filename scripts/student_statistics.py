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
        required=True,
        dest='subject_shortname',
        help='The shortname of a subject. This is unique.'
    )
    parser.add_argument(
        '--period-shortname',
        type=str,
        required=True,
        dest='period_shortname',
        help='The shortname of a period/semester. This is unique together with the subject shortname.'
    )

    return vars(parser.parse_args())


if __name__ == "__main__":
    
    # For development:
    os.environ.setdefault('DJANGOENV', 'develop')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trix.project.settingsproxy")
    django.setup()

    from trix.trix_core import models as core_models


    argument_dict = get_arguments()

    now = timezone.now()
    at = 0
    course_name = argument_dict['subject_shortname']
    period = argument_dict['period_shortname']
    course_tag = core_models.Tag.objects.get(tag=course_name, category='c')
    period_tag = core_models.Tag.objects.get(tag=period, category='p')
    for user_shortname in argument_dict['username_list']:
        for assignment in core_models.Assignment.objects.filter_by_tags(tags=[course_tag, period_tag]):
            user = core_models.User.objects.get(email=user_shortname)
            solved_queryset = core_models.HowSolved.objects.filter(assignment=assignment, user=user)
            out = f'{at} - {user_shortname} - {course_name} - {assignment} - '
            if solved_queryset.exists():
                for solved in solved_queryset:
                    out += f'{solved.solved_datetime} - yes - '
                    if solved.howsolved == 'bymyself':
                        out += ' no - yes'
                    else:
                        out += ' yes - no'
            else:
                out += f'{now} - no - no - no'
            
            print(out)
            at += 1


        


   