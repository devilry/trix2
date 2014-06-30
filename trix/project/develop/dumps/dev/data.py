#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been automatically generated.
# Instead of changing it, create a file called import_helper.py
# and put there a class called ImportHelper(object) in it.
#
# This class will be specially casted so that instead of extending object,
# it will actually extend the class BasicImportHelper()
#
# That means you just have to overload the methods you want to
# change, leaving the other ones inteact.
#
# Something that you might want to do is use transactions, for example.
#
# Also, don't forget to add the necessary Django imports.
#
# This file was generated with the following command:
# manage.py dumpscript trix_core --traceback
#
# to restore it, run
# manage.py runscript module_name.this_script_name
#
# example: if manage.py is at ./manage.py
# and the script is at ./some_folder/some_script.py
# you must make sure ./some_folder/__init__.py exists
# and run  ./manage.py runscript some_folder.some_script

from django.db import transaction

class BasicImportHelper(object):

    def pre_import(self):
        pass

    # You probably want to uncomment on of these two lines
    # @transaction.atomic  # Django 1.6
    # @transaction.commit_on_success  # Django <1.6
    def run_import(self, import_data):
        import_data()

    def post_import(self):
        pass

    def locate_similar(self, current_object, search_data):
        # You will probably want to call this method from save_or_locate()
        # Example:
        #   new_obj = self.locate_similar(the_obj, {"national_id": the_obj.national_id } )

        the_obj = current_object.__class__.objects.get(**search_data)
        return the_obj

    def locate_object(self, original_class, original_pk_name, the_class, pk_name, pk_value, obj_content):
        # You may change this function to do specific lookup for specific objects
        #
        # original_class class of the django orm's object that needs to be located
        # original_pk_name the primary key of original_class
        # the_class      parent class of original_class which contains obj_content
        # pk_name        the primary key of original_class
        # pk_value       value of the primary_key
        # obj_content    content of the object which was not exported.
        #
        # You should use obj_content to locate the object on the target db
        #
        # An example where original_class and the_class are different is
        # when original_class is Farmer and the_class is Person. The table
        # may refer to a Farmer but you will actually need to locate Person
        # in order to instantiate that Farmer
        #
        # Example:
        #   if the_class == SurveyResultFormat or the_class == SurveyType or the_class == SurveyState:
        #       pk_name="name"
        #       pk_value=obj_content[pk_name]
        #   if the_class == StaffGroup:
        #       pk_value=8

        search_data = { pk_name: pk_value }
        the_obj = the_class.objects.get(**search_data)
        #print(the_obj)
        return the_obj


    def save_or_locate(self, the_obj):
        # Change this if you want to locate the object in the database
        try:
            the_obj.save()
        except:
            print("---------------")
            print("Error saving the following object:")
            print(the_obj.__class__)
            print(" ")
            print(the_obj.__dict__)
            print(" ")
            print(the_obj)
            print(" ")
            print("---------------")

            raise
        return the_obj


importer = None
try:
    import import_helper
    # We need this so ImportHelper can extend BasicImportHelper, although import_helper.py
    # has no knowlodge of this class
    importer = type("DynamicImportHelper", (import_helper.ImportHelper, BasicImportHelper ) , {} )()
except ImportError as e:
    if str(e) == "No module named import_helper":
        importer = BasicImportHelper()
    else:
        raise

import datetime
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType

try:
    import dateutil.parser
except ImportError:
    print("Please install python-dateutil")
    sys.exit(os.EX_USAGE)

def run():
    importer.pre_import()
    importer.run_import(import_data)
    importer.post_import()

def import_data():
    # Initial Imports

    # Processing model: User

    from trix.trix_core.models import User

    trix_core_user_1 = User()
    trix_core_user_1.password = u'pbkdf2_sha256$12000$6qEBQVnjeivy$kXhstjtqHt+XauVf1JZWIBmtmHSkiTURu/hUR9UXnps='
    trix_core_user_1.last_login = dateutil.parser.parse("2014-06-30T20:50:48.679561+00:00")
    trix_core_user_1.is_active = True
    trix_core_user_1.is_admin = True
    trix_core_user_1.email = u'grandma@example.com'
    trix_core_user_1 = importer.save_or_locate(trix_core_user_1)

    # Processing model: Tag

    from trix.trix_core.models import Tag

    trix_core_tag_1 = Tag()
    trix_core_tag_1.tag = u'inf1000'
    trix_core_tag_1.category = u'c'
    trix_core_tag_1 = importer.save_or_locate(trix_core_tag_1)

    trix_core_tag_2 = Tag()
    trix_core_tag_2.tag = u'v\xe5r2014'
    trix_core_tag_2.category = u'p'
    trix_core_tag_2 = importer.save_or_locate(trix_core_tag_2)

    trix_core_tag_3 = Tag()
    trix_core_tag_3.tag = u'host2014'
    trix_core_tag_3.category = u'p'
    trix_core_tag_3 = importer.save_or_locate(trix_core_tag_3)

    trix_core_tag_4 = Tag()
    trix_core_tag_4.tag = u'host2013'
    trix_core_tag_4.category = u'p'
    trix_core_tag_4 = importer.save_or_locate(trix_core_tag_4)

    trix_core_tag_5 = Tag()
    trix_core_tag_5.tag = u'inf1100'
    trix_core_tag_5.category = u'c'
    trix_core_tag_5 = importer.save_or_locate(trix_core_tag_5)

    trix_core_tag_6 = Tag()
    trix_core_tag_6.tag = u'uke1'
    trix_core_tag_6.category = u''
    trix_core_tag_6 = importer.save_or_locate(trix_core_tag_6)

    trix_core_tag_7 = Tag()
    trix_core_tag_7.tag = u'oblig1'
    trix_core_tag_7.category = u''
    trix_core_tag_7 = importer.save_or_locate(trix_core_tag_7)

    trix_core_tag_8 = Tag()
    trix_core_tag_8.tag = u'uke2'
    trix_core_tag_8.category = u''
    trix_core_tag_8 = importer.save_or_locate(trix_core_tag_8)

    trix_core_tag_9 = Tag()
    trix_core_tag_9.tag = u'oblig2'
    trix_core_tag_9.category = u''
    trix_core_tag_9 = importer.save_or_locate(trix_core_tag_9)

    # Processing model: Course

    from trix.trix_core.models import Course

    trix_core_course_1 = Course()
    trix_core_course_1.description = u'Grunnkurs i objektorientert programmering. '
    trix_core_course_1.course_tag = trix_core_tag_1
    trix_core_course_1.active_period = trix_core_tag_2
    trix_core_course_1 = importer.save_or_locate(trix_core_course_1)

    trix_core_course_1.admins.add(trix_core_user_1)

    trix_core_course_2 = Course()
    trix_core_course_2.description = u'Grunnkurs i programmering for naturvitenskapelige anvendelser'
    trix_core_course_2.course_tag = trix_core_tag_5
    trix_core_course_2.active_period = trix_core_tag_2
    trix_core_course_2 = importer.save_or_locate(trix_core_course_2)

    trix_core_course_2.admins.add(trix_core_user_1)

    # Processing model: Assignment

    from trix.trix_core.models import Assignment

    trix_core_assignment_1 = Assignment()
    trix_core_assignment_1.title = u'Hello World'
    trix_core_assignment_1.text = u'Print hello world in the terminal.'
    trix_core_assignment_1.solution = u'``` java\r\npublic class HelloWorld {\r\n    public static void main(String [] args) {\r\n        System.out.println("Hello World!");\r\n    }\r\n}\r\n```'
    trix_core_assignment_1 = importer.save_or_locate(trix_core_assignment_1)

    trix_core_assignment_1.tags.add(trix_core_tag_1)
    trix_core_assignment_1.tags.add(trix_core_tag_2)
    trix_core_assignment_1.tags.add(trix_core_tag_6)
    trix_core_assignment_1.tags.add(trix_core_tag_7)

    trix_core_assignment_2 = Assignment()
    trix_core_assignment_2.title = u'Finn fem feil'
    trix_core_assignment_2.text = u'``` java\r\nclass Utskrift {\r\n    public stitac void main(String args) (\r\n        System.out.println("Beethoven skrev Skjebnesymfonien")\r\n        System.out.println("og \xe5tte andre symfonier.);\r\n    }\r\n}\r\n```'
    trix_core_assignment_2.solution = u'N\xf8kkelordet "static" er stavet feil.\r\n\r\nDet mangler hakeparenteser ("[]") etter "String" p\xe5 linje 2. Denne feilen oppdages ikke av kompilatoren, men av kj\xf8resystemet fordi det er lov \xe5 lage metoder uten "[]" der, bare ikke lov \xe5 bruke de som hoved-main-metoden n\xe5r man kj\xf8rer et program. Kj\xf8resystemet gir ofte litt mer uventede feilmeldinger enn kompilatoren, men disse vil du ogs\xe5 etter hvert l\xe6re deg \xe5 kjenne igjen.  I dette tilfellet f\xe5r vi f\xf8lgende feilmelding n\xe5r vi pr\xf8ver \xe5 kj\xf8re programmet: \r\n```\r\njava.lang.NoSuchMethodError: main\r\nException in thread "main"\r\n```\r\n\r\nSom vi ser s\xe5 betyr feilmeldingen at kj\xf8resystemmet ikke fant noen (riktig skrevet) main-metode. Det st\xe5r vanlig parentes i stedet for kr\xf8llparentes p\xe5 slutten av linje 2.\r\n\r\nDet mangler semikolon p\xe5 slutten av linje 3.\r\n\r\nAvsluttende anf\xf8rselstegn mangler p\xe5 linje 4.'
    trix_core_assignment_2 = importer.save_or_locate(trix_core_assignment_2)

    trix_core_assignment_2.tags.add(trix_core_tag_1)
    trix_core_assignment_2.tags.add(trix_core_tag_2)

    trix_core_assignment_3 = Assignment()
    trix_core_assignment_3.title = u'Sum (innlesning av tekst fra terminal)'
    trix_core_assignment_3.text = u'Lag et program som ber om og leser inn to heltall. Programmet skal deretter regne ut summen av de to tallene og skrive ut svaret.'
    trix_core_assignment_3.solution = u'``` java\r\nimport java.util.*;\r\n\r\nclass Sum {\r\n    public static void main(String[] args) {\r\n        Scanner tast = new Scanner(System.in);\r\n\r\n        System.out.print("Oppgi verdien til x: ");\r\n        int x = tast.nextInt();\r\n        System.out.print("Oppgi verdien til y: ");\r\n        int y = tast.nextInt();\r\n\r\n        int sum = x + y;\r\n\r\n        System.out.println("Summen av x og y er: " + sum);\r\n    }\r\n}\r\n```'
    trix_core_assignment_3 = importer.save_or_locate(trix_core_assignment_3)

    trix_core_assignment_3.tags.add(trix_core_tag_1)
    trix_core_assignment_3.tags.add(trix_core_tag_9)

    trix_core_assignment_4 = Assignment()
    trix_core_assignment_4.title = u'Utskrift og sum av oddetalls-array:'
    trix_core_assignment_4.text = u'Skriv et program som inneholder en heltalls-array med f\xf8lgende elementer: 1, 3, 5, 7, 9, 11, 13, 15, 17, 19.  Programmet skal inneholde en l\xf8kke som skriver ut indeksen og verdien for alle elementene i arrayen.'
    trix_core_assignment_4.solution = u'``` java\r\nclass Oddetall {\r\n  public static void main(String[] args) {\r\n    int[] oddetall = { 1, 3, 5, 7, 9, 11, 13, 15, 17, 19 };\r\n\r\n    for (int i = 0; i < oddetall.length; i++) {\r\n      System.out.println("oddetall[" + i + "] = " + oddetall[i]);\r\n    }\r\n  }\r\n}\r\n```'
    trix_core_assignment_4 = importer.save_or_locate(trix_core_assignment_4)

    trix_core_assignment_4.tags.add(trix_core_tag_1)
    trix_core_assignment_4.tags.add(trix_core_tag_2)
    trix_core_assignment_4.tags.add(trix_core_tag_7)

    trix_core_assignment_5 = Assignment()
    trix_core_assignment_5.title = u'Hello world'
    trix_core_assignment_5.text = u'Make a Hello class.'
    trix_core_assignment_5.solution = u"``` python\r\nclass Hello:\r\n    def __call__(self, text):\r\n        return 'Hello, %s!' % text\r\n\r\n    def __str__(self):\r\n        return 'Hello, World!'\r\n\r\na = Hello()\r\nprint a('students')  # looks like a function call!\r\nprint a              # print str(a) -> a.__str__()\r\n```"
    trix_core_assignment_5 = importer.save_or_locate(trix_core_assignment_5)

    trix_core_assignment_5.tags.add(trix_core_tag_5)

    trix_core_assignment_6 = Assignment()
    trix_core_assignment_6.title = u'Lek med datatyper'
    trix_core_assignment_6.text = u'Pr\xf8v \xe5 lage et program som bruker ALLE disse datatypene:\r\n\r\n- int\r\n- float\r\n- String\r\n- double\r\n- boolean\r\n- char'
    trix_core_assignment_6.solution = u''
    trix_core_assignment_6 = importer.save_or_locate(trix_core_assignment_6)

    trix_core_assignment_6.tags.add(trix_core_tag_1)
    trix_core_assignment_6.tags.add(trix_core_tag_2)
    trix_core_assignment_6.tags.add(trix_core_tag_7)
    trix_core_assignment_6.tags.add(trix_core_tag_8)

    # Processing model: HowSolved

    from trix.trix_core.models import HowSolved


    # Processing model: Permalink

    from trix.trix_core.models import Permalink

    trix_core_permalink_1 = Permalink()
    trix_core_permalink_1.title = u'Treningsoppgave til Oblig 1'
    trix_core_permalink_1.description = u'Dette er oppgaver som egner seg godt til trening til oblig 1. L\xf8s oppgavene stegvis og s\xf8rg for \xe5 bruke god tid p\xe5 oppgavene for \xe5 s\xf8rge for at du er best mulig rustet til \xe5 komme i m\xe5l.'
    trix_core_permalink_1 = importer.save_or_locate(trix_core_permalink_1)

    trix_core_permalink_1.tags.add(trix_core_tag_6)
    trix_core_permalink_1.tags.add(trix_core_tag_7)
