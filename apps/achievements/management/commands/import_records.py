import datetime
import MySQLdb as mysql
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from apps.achievements.models import Category, Record
from apps.accounts.models import City
"""
    `kmp_members` (
        0   `id` int(11) NOT NULL AUTO_INCREMENT,
        1   `mtype` tinyint(4) DEFAULT '0',
        2   `email` varchar(60) DEFAULT '',
        3   `pass` varchar(32) DEFAULT '',
        4   `regdate` datetime DEFAULT '0000-00-00 00:00:00',
        5   `lastvisit` datetime DEFAULT '0000-00-00 00:00:00',
        6   `name` varchar(60) DEFAULT '',
        7   `dateofbirth` date DEFAULT '0000-00-00',
        8   `city` varchar(60) DEFAULT '0',
        9   `sex` tinyint(1) DEFAULT '0',
        10  `active` tinyint(1) DEFAULT '0',
        11  `activekey` varchar(8) DEFAULT '',
        12  `mainliga` int(11) DEFAULT '0',
        13  `userliga` int(11) DEFAULT '0',
        14  `userligapass` varchar(5) DEFAULT '',
        15  `newrecords` tinyint(1) DEFAULT '0'
    )
    `kmp_members_records` (
        0   `id` int(11) NOT NULL AUTO_INCREMENT,
        1   `member_id` int(4) DEFAULT '0',
        2   `record` int(11) DEFAULT '0',
        3   `record_date` datetime DEFAULT '0000-00-00 00:00:00',
        4   `record_stat_date` datetime DEFAULT '0000-00-00 00:00:00',
        5   `record_photo_prev` varchar(100) DEFAULT '',
        6   `record_photo` varchar(100) DEFAULT '',
        7   `record_comment` varchar(200) DEFAULT '',
        8   `record_show` tinyint(1) DEFAULT '0',
        9   `record_cheat` tinyint(1) DEFAULT '0',
        10  `record_liga` tinyint(1) DEFAULT '0',
        11  `month_record` tinyint(1) DEFAULT '0'
    )
    `kmp_mainliga_topics` (
        0   `id` int(11) NOT NULL AUTO_INCREMENT,
        1   `lurl` varchar(15) DEFAULT '',
        2   `parent` int(11) DEFAULT '0',
        3   `name` varchar(30) DEFAULT '',
        4   `ligadesc` text,
        5   `perpage` int(11) DEFAULT '0',
        6   `dshow` tinyint(1) DEFAULT '1',
        7   `dsort` smallint(6) DEFAULT '0'
    )
"""

def import_users():
    conn = mysql.connect(
        host = "localhost",
        user = "root",
        passwd = "chill",
        charset = "utf8",
        use_unicode = True
    )

    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM powerball.ru.kmp_members ORDER BY id;')
    users = cursor.fetchall()
    
    cursor.execute('SELECT * FROM powerball.ru.kmp_members_records ORDER BY id;')
    records = cursor.fetchall()
    
    categories_map = (
        (1, 8, 10, 11, 12, 13),
        (1, 2, 3, 4, 5, 6),
    )

    for i, user_row in enumerate(users):
        email = user_row[2].encode('utf-8')
        first_name, last_name = '', ''
        
        if len(user_row[6]) > 0:
            name = user_row[6].encode('utf-8')
            name = name.split()
            try:
                first_name, last_name = name[0], name[1:][0]
            except IndexError:
                first_name, last_name = name[0], ''
        
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = email[0:30],
            email = email,
            date_joined = user_row[4],
            last_login = user_row[5] or datetime.datetime.now()
        )
        
        user.set_password(user_row[3].encode('utf-8'))
        user.save()
        
        profile = user.profile
        profile.birthdate = user_row[7]
        profile.gender = user_row[9] + 1

        if len(user_row[8]) > 0:
            city, city_created = City.objects.get_or_create(
                                            name=user_row[8].encode('utf-8'))
            profile.city = city
        profile.save()
        
        print ("%s. %s %s <%s>" % (i, user.first_name, user.last_name, user.email))
        
        user_records = [r for r in records if r[1] == user_row[0]]
        for j, rec in enumerate(user_records):
            if rec[10] == 0:
                category_id = 1
            else:
                category_id = [c[1] for c in zip(*categories_map) 
                                if c[0]==rec[10]][0]

            record = Record.objects.create(
                user=user,
                category_id=category_id,
                value=rec[2],
                is_confirmed=True,
                created_at=rec[3],
                approved_at=rec[4],
                comment=rec[7].encode('utf-8')
            )
            print ("     %s. [%s]: %s - %s" % (j, record.created_at,
                                        record.value, record.comment))

    cursor.close()
    conn.close()



class Command(BaseCommand):
    args = ''
    help = 'import old powerball.ru'

    def handle(self, *args, **options):
        import_users()
        self.stdout.write('import')

#python manage.py dumpdata auth.user --natural --indent=2 > export/auth.json

#python manage.py dumpdata powerball.ru.accounts.City --natural --indent=2 > export/powerball.ru.account.City.json
#python manage.py dumpdata powerball.ru.accounts.Profile --natural --indent=2 > export/powerball.ru.account.Profile.json
#python manage.py dumpdata powerball.ru.accounts.ProfileRegistration --natural --indent=2 > export/powerball.ru.account.ProfileRegistration.json

#python manage.py dumpdata powerball.ru.achievements.Category --natural --indent=2 > export/powerball.ru.achievements.Category.json
#python manage.py dumpdata powerball.ru.achievements.Record --natural --indent=2 > export/powerball.ru.achievements.Record.json
