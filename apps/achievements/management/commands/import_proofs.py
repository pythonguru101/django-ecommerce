import os
import shutil
import MySQLdb as mysql
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from apps.achievements.models import Record, RecordProof
from apps.utils import upload_to

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
"""


def file_copy(name):
    img_to_name = upload_to(name)
    img_from = os.path.join(settings.MEDIA_ROOT, 'uploads', 'userphotos',
                            name)
    img_to = os.path.join(settings.MEDIA_ROOT, 'uploads', 'achievements',
                          img_to_name)

    if os.path.isfile(img_from):
        shutil.copyfile(img_from, img_to)
        return "uploads/achievements/%s" % img_to_name
    else:
        return False


def import_proofs():
    conn = mysql.connect(
        host="localhost",
        user="root",
        passwd="chill",
        charset="utf8",
        use_unicode=True
    )
    cursor = conn.cursor()
    records = Record.objects.all()

    for i, record in enumerate(records):
        query = "SELECT * FROM powerball.ru.kmp_members_records \
WHERE record=%s AND record_date='%s';" % (record.value, record.created_at)
        cursor.execute(query)
        proof = cursor.fetchall()[0]

        image = file_copy(proof[6])
        if image:
            RecordProof.objects.create(
                record=record,
                image=image
            )
            print ("%s. copy %s to %s" % (i, proof[6], image))
    cursor.close()
    conn.close()


class Command(BaseCommand):
    args = ''
    help = 'import old powerball.ru'
    can_import_settings = True

    def handle(self, *args, **options):
        import_proofs()
        self.stdout.write('import')
