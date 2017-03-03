import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Count
from fetch_data.models import Morcha, Post, Battalion
from fetch_data.models import Weaksignal, Backup, Offline
import calendar_utils
import serializers


class QuerySetProcessors:
    def __init__(self):
        pass

    @staticmethod
    def get_weaksignals_data_morcha(start, end, pk):
        weaksignal = Weaksignal.objects.filter(start__gte=start, start__lt=end, morcha=pk)
        return weaksignal

    @staticmethod
    def get_backup_data_morcha(start, end, pk):
        backup = Backup.objects.filter(start__gte=start, start__lt=end, morcha=pk)
        return backup

    @staticmethod
    def get_offline_data_morcha(start, end, pk):
        offline = Offline.objects.filter(start__gte=start, start__lt=end, morcha=pk)
        return offline

    @staticmethod
    def get_weaksignals_data_post(start, end, pk):
        weaksignal = Weaksignal.objects.filter(start__gte=start, start__lt=end, morcha__post=pk)
        return weaksignal

    @staticmethod
    def get_backup_data_post(start, end, pk):
        backup = Backup.objects.filter(start__gte=start, start__lt=end, morcha__post=pk)
        return backup

    @staticmethod
    def get_offline_data_post(start, end, pk):
        offline = Offline.objects.filter(start__gte=start, start__lt=end, morcha__post=pk)
        return offline

    @staticmethod
    def get_weaksignals_data_battalion(start, end, pk):
        weaksignal = Weaksignal.objects.filter(start__gte=start, start__lt=end, morcha__post__battalion=pk)
        return weaksignal

    @staticmethod
    def get_backup_data_battalion(start, end, pk):
        backup = Backup.objects.filter(start__gte=start, start__lt=end, morcha__post__battalion=pk)
        return backup

    @staticmethod
    def get_offline_data_battalion(start, end, pk):
        offline = Offline.objects.filter(start__gte=start, start__lt=end, morcha__post__battalion=pk)
        return offline


class FetchData:
    def __init__(self):
        pass

    @staticmethod
    def get_data_morcha(start, end, pk):
        weaksignal = QuerySetProcessors.get_weaksignals_data_morcha(start, end, pk)
        offline = QuerySetProcessors.get_offline_data_morcha(start, end, pk)
        backup = QuerySetProcessors.get_backup_data_morcha(start, end, pk)
        return weaksignal, offline, backup

    @staticmethod
    def get_data_post(start, end, pk):
        weaksignal = QuerySetProcessors.get_weaksignals_data_post(start, end, pk)
        offline = QuerySetProcessors.get_offline_data_post(start, end, pk)
        backup = QuerySetProcessors.get_backup_data_post(start, end, pk)
        return weaksignal, offline, backup

    @staticmethod
    def get_data_battalion(start, end, pk):
        weaksignal = QuerySetProcessors.get_weaksignals_data_battalion(start, end, pk)
        offline = QuerySetProcessors.get_offline_data_battalion(start, end, pk)
        backup = QuerySetProcessors.get_backup_data_battalion(start, end, pk)
        return weaksignal, offline, backup


class Widgets:
    def __init__(self, date=None, timespan=None, level=None, pk=None):
        self.calendar = calendar_utils.calendar_iterators()
        self.level = level
        self.pk = pk
        self.timespan = timespan

        if timespan == 'day':
            self.start, self.end = self.calendar.daystartend(strdate=date)
        elif timespan == 'week':
            self.start, self.end = self.calendar.weekstartend(strdate=date)
        elif timespan == 'month':
            self.start, self.end = self.calendar.monthstartend(strdate=date)
        else:
            self.start, self.end = self.calendar.lastmonthstartend()

        if level == 'post':
            self.weaksignal, self.offline, self.backup = FetchData.get_data_post(self.start, self.end, self.pk)
        elif level == 'morcha':
            self.weaksignal, self.offline, self.backup = FetchData.get_data_morcha(self.start, self.end, self.pk)
        elif level == 'battalion':
            self.weaksignal, self.offline, self.backup = FetchData.get_data_battalion(self.start, self.end, self.pk)
        else:
            pass

    def get_weaksignal_count(self, daystart=None, dayend=None, object=False):
        if daystart and dayend:
            weaksignal = self.weaksignal.filter(start__gte=daystart, start__lt=dayend)
        else:
            weaksignal = self.weaksignal
        if object:
            return {
                'count': weaksignal.count()
            }
        else:
            return weaksignal.count()

    def get_offline_count_and_duration(self, daystart=None, dayend=None, object=False):
        if daystart and dayend:
            offline = self.offline.filter(start__gte=daystart, start__lt=dayend)
        else:
            offline = self.offline
        res = offline.aggregate(sum=Sum('duration'))

        if object:
            return {
                'count': offline.count(),
                'duration': res['sum']
            }
        else:
            return offline.count(), res['sum']

    def get_backup_count_and_duration(self, daystart=None, dayend=None, object=False):
        if daystart and dayend:
            backup = self.backup.filter(start__gte=daystart, start__lt=dayend)
        else:
            backup = self.backup
        res = backup.aggregate(sum=Sum('duration'))
        if object:
            return {
                'count': backup.count(),
                'duration': res['sum']
            }
        else:
            return backup.count(), res['sum']

    def get_unit_report(self):
        if self.level == 'morcha' and self.timespan == 'day':
            weaksignal_data = serializers.WeaksignalSerializer(self.weaksignal, many=True).data
            offline_data = serializers.OfflineSerializer(self.offline, many=True).data
            backup_data = serializers.BackupSerializer(self.backup, many=True).data
            obj = {
                'weaksignal': weaksignal_data,
                'offline': offline_data,
                'backup': backup_data
            }
            return obj
        elif self.level == 'post':
            if self.timespan == 'day' or self.timespan == 'week' or self.timespan == 'month':
                print self.timespan
                return self.get_unit_report_post()
            else:
                pass
        elif self.level == 'morcha' and self.timespan == 'week':
            return self.get_unit_report_for_week()
        elif self.level == 'morcha' and self.timespan == 'month':
            return self.get_unit_report_for_month()
        else:
            pass

    def get_unit_report_post(self):
        weak_signal = self.weaksignal.values('morcha').annotate(count=Count('start'))
        offline = self.offline.values('morcha').annotate(count=Count('start'), duration=Sum('duration'))
        backup = self.backup.values('morcha').annotate(count=Count('start'), duration=Sum('duration'))
        all_morchas = Morcha.objects.all().order_by('name')
        weak_signal_cache = {i['morcha']: i for i in weak_signal}
        offline_cache = {i['morcha']: i for i in offline}
        backup_cache = {i['morcha']: i for i in backup}

        all_morchas_stats = ({i.name: {'weak_signal': weak_signal_cache.get(i.pk, 0),
                                       'backup': backup_cache.get(i.pk, 0), 'offline': offline_cache.get(i.pk, 0)}} for
                             i in all_morchas)
        return all_morchas_stats

    def get_unit_report_for_week(self):
        temp_start = self.start
        temp_end = self.end
        res = []
        data = {}
        while True:
            dayend = temp_start + datetime.timedelta(days=1)
            offline_count, offline_duration = self.get_offline_count_and_duration(daystart=temp_start, dayend=dayend)
            backup_count, backup_duration = self.get_backup_count_and_duration(daystart=temp_start, dayend=dayend)
            obj = {
                'weaksignal_count': self.get_weaksignal_count(daystart=temp_start, dayend=dayend),
                'offline_count': offline_count,
                'offline_duration': offline_duration,
                'backup_count': backup_count,
                'backup_duration': backup_duration
            }
            val = {
                str(temp_start): obj
            }
            res.append(val)
            temp_start = dayend
            if temp_start == temp_end:
                break
            else:
                pass
        return res

    def get_unit_report_for_month(self):
        temp_start = self.start
        temp_end = self.end
        data = {}
        while True:
            if temp_start == temp_end or temp_start > temp_end:
                break
            elif temp_start + datetime.timedelta(days=7) > temp_end:
                weekend = temp_end
            else:
                weekend = temp_start + datetime.timedelta(days=7)
            offline_count, offline_duration = self.get_offline_count_and_duration(daystart=temp_start, dayend=weekend)
            backup_count, backup_duration = self.get_backup_count_and_duration(daystart=temp_start, dayend=weekend)
            obj = {
                'weaksignal_count': self.get_weaksignal_count(daystart=temp_start, dayend=weekend),
                'offline_count': offline_count,
                'offline_duration': offline_duration,
                'backup_count': backup_count,
                'backup_duration': backup_duration
            }
            data[str(temp_start)] = obj
            temp_start += datetime.timedelta(days=7)
        return data

    def check_object_exists(self):
        error = False
        message = ''
        try:
            if self.level == 'morcha':
                val = Morcha.objects.get(pk=self.pk)
            elif self.level == 'post':
                val = Post.objects.get(pk=self.pk)
            elif self.level == 'battalion':
                val = Battalion.objects.get(pk=self.pk)
            else:
                pass
        except ObjectDoesNotExist:
            error = True
            message = 'detail of %s for id %r not found' % (self.level, str(self.pk))
        finally:
            return error, message

    def get_on_backup_units(self):
        pass

    def get_total_devices(self):
        post = Post.objects.get(uuid=self.pk)
        morcha_set = post.morchas.all()
        total_qrt = 0
        total_kvx = 0
        for morcha in morcha_set:
            total_qrt += 1
            total_kvx += morcha.units.all().count()
        return total_kvx, total_qrt
