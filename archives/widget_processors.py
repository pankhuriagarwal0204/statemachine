import datetime
import pytz
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.db.models import Q
from django.db.models.functions import ExtractHour
from fetch_data.models import Intrusion, Morcha, Post, Battalion
import calendar_utils
import serializers


class QuerysetProcessors:
    def __init__(self):
        pass

    @staticmethod
    def get_verified_data_morcha(start, end, pk):
        verified = Intrusion.objects.filter(verified_datetime__gte=start, verified_datetime__lt=end, morcha=pk)
        return verified

    @staticmethod
    def get_non_human_data_morcha(start, end, pk):
        non_human = Intrusion.objects.filter(non_human_intrusion_datetime__gte=start,
                                             non_human_intrusion_datetime__lt=end, morcha=pk)
        return non_human

    @staticmethod
    def get_neutralized_data_morcha(start, end, pk):
        neutralized = Intrusion.objects.filter(neutralized_datetime__gte=start,
                                               neutralized_datetime__lt=end, morcha=pk)
        return neutralized

    @staticmethod
    def get_detected_data_morcha(start, end, pk):
        detected = Intrusion.objects.filter(detected_datetime__gte=start,
                                            detected_datetime__lt=end, morcha=pk)
        return detected

    @staticmethod
    def get_verified_data_post(start, end, pk):
        verified = Intrusion.objects.filter(verified_datetime__gte=start, verified_datetime__lt=end, morcha__post=pk)
        return verified

    @staticmethod
    def get_non_human_data_post(start, end, pk):
        non_human = Intrusion.objects.filter(non_human_intrusion_datetime__gte=start,
                                             non_human_intrusion_datetime__lt=end, morcha__post=pk)
        return non_human

    @staticmethod
    def get_neutralized_data_post(start, end, pk):
        neutralized = Intrusion.objects.filter(neutralized_datetime__gte=start,
                                               neutralized_datetime__lt=end, morcha__post=pk)
        return neutralized

    @staticmethod
    def get_detected_data_post(start, end, pk):
        detected = Intrusion.objects.filter(detected_datetime__gte=start,
                                            detected_datetime__lt=end, morcha__post=pk)
        return detected

    @staticmethod
    def get_verified_data_battalion(start, end, pk):
        verified = Intrusion.objects.filter(verified_datetime__gte=start, verified_datetime__lt=end,
                                            morcha__post__battalion=pk)
        return verified

    @staticmethod
    def get_non_human_data_battalion(start, end, pk):
        non_human = Intrusion.objects.filter(non_human_intrusion_datetime__gte=start,
                                             non_human_intrusion_datetime__lt=end, morcha__post__battalion=pk)
        return non_human

    @staticmethod
    def get_neutralized_data_battalion(start, end, pk):
        neutralized = Intrusion.objects.filter(neutralized_datetime__gte=start,
                                               neutralized_datetime__lt=end, morcha__post__battalion=pk)
        return neutralized

    @staticmethod
    def get_detected_data_battalion(start, end, pk):
        detected = Intrusion.objects.filter(detected_datetime__gte=start,
                                            detected_datetime__lt=end, morcha__post__battalion=pk)
        return detected


class FetchData:
    def __init__(self):
        pass

    @staticmethod
    def get_data_morcha(start, end, pk):
        verified = QuerysetProcessors.get_verified_data_morcha(start, end, pk)
        neutralized = QuerysetProcessors.get_neutralized_data_morcha(start, end, pk)
        non_human = QuerysetProcessors.get_non_human_data_morcha(start, end, pk)
        detected = QuerysetProcessors.get_detected_data_morcha(start, end, pk)
        return verified, non_human, neutralized, detected

    @staticmethod
    def get_data_post(start, end, pk):
        verified = QuerysetProcessors.get_verified_data_post(start, end, pk)
        neutralized = QuerysetProcessors.get_neutralized_data_post(start, end, pk)
        non_human = QuerysetProcessors.get_non_human_data_post(start, end, pk)
        detected = QuerysetProcessors.get_detected_data_post(start, end, pk)
        return verified, non_human, neutralized, detected

    @staticmethod
    def get_data_battalion(start, end, pk):
        verified = QuerysetProcessors.get_verified_data_battalion(start, end, pk)
        neutralized = QuerysetProcessors.get_neutralized_data_battalion(start, end, pk)
        non_human = QuerysetProcessors.get_non_human_data_battalion(start, end, pk)
        detected = QuerysetProcessors.get_detected_data_battalion(start, end, pk)
        return verified, non_human, neutralized, detected

    @staticmethod
    def get_dangling_intrusion(pk=None, end=None):
        end = end - datetime.timedelta(days=1)
        monthstart = end - datetime.timedelta(days=30)
        old_verified = QuerysetProcessors.get_verified_data_morcha(start=monthstart, end=end, pk=pk)
        old_dangling = old_verified.filter(neutralized_datetime__isnull=True)
        return old_dangling


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
        elif timespan == 'recent':
            self.start, self.end = self.calendar.lastmonthstartend()
        else:
            self.start = None
            self.end = None

        if level == 'post':
            self.verified, self.non_human, self.neutralized, self.detected = FetchData.get_data_post(self.start,
                                                                                                     self.end,
                                                                                                     self.pk)
        elif level == 'morcha':
            self.verified, self.non_human, self.neutralized, self.detected = FetchData.get_data_morcha(self.start,
                                                                                                       self.end,
                                                                                                       self.pk)
        elif level == 'battalion':
            self.verified, self.non_human, self.neutralized, self.detected = FetchData.get_data_battalion(self.start,
                                                                                                          self.end,
                                                                                                          self.pk)
        else:
            pass

    def total_count(self, daystart=None, dayend=None):
        if daystart and dayend:
            return {
                'verified': self.verified.filter(verified_datetime__gte=daystart, verified_datetime__lt=dayend).count(),
                'neutralized': self.neutralized.filter(neutralized_datetime__gte=daystart,
                                                       neutralized_datetime__lt=dayend).count(),
                'non_human': self.non_human.filter(non_human_intrusion_datetime__gte=daystart,
                                                   non_human_intrusion_datetime__lt=dayend).count()
            }
        else:
            obj = {
                'verified': self.verified.count(),
                'neutralized': self.neutralized.count(),
                'non_human': self.non_human.count()
            }
            return obj

    def longest_intrusion(self):
        total = self.verified | self.non_human | self.neutralized
        total_filtered = total.filter(detected_datetime__gte=self.start).order_by('-duration', '-neutralized_datetime').first()
        return serializers.LongestIntrusionSerializer(total_filtered).data

    def get_intrusion_report(self):
        if self.timespan == 'month':
            return self.get_intrusion_report_for_month()
        elif self.timespan == 'recent':
            return self.get_intrusion_report_for_recent()
        elif self.timespan == 'week':
            return self.get_intrusion_report_for_week()
        elif self.timespan == 'day':
            if self.level == 'morcha':
                new, old = self.get_intrusion_report_all_morcha()
                data = new | old
                return serializers.IntrusionSerializer(data, many=True).data
            else:
                return self.get_intrusion_report_day_post()
        else:
            pass

    def get_intrusion_report_for_week(self):
        temp_start = self.start
        temp_end = self.end
        data = {}
        while True:
            dayend = temp_start + datetime.timedelta(days=1)
            obj = self.total_count(daystart=temp_start, dayend=dayend)
            if self.level == 'morcha':
                old_dangling = FetchData.get_dangling_intrusion(pk=self.pk, end=dayend)
                verified = QuerysetProcessors.get_verified_data_morcha(start=temp_start,
                                                                       end=dayend + datetime.timedelta(days=1),
                                                                       pk=self.pk)
                area_status = self.get_security_update(old=old_dangling, verified=verified)
                obj['area_status'] = area_status
            data[str(temp_start)] = obj
            temp_start = dayend
            if temp_start == temp_end:
                break
            else:
                pass
        return data

    def get_intrusion_report_for_month(self):
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
            obj = self.total_count(daystart=temp_start, dayend=weekend)
            data[str(temp_start)] = obj
            temp_start += datetime.timedelta(days=7)
        return data

    def get_intrusion_report_for_recent(self):
        total = self.verified | self.neutralized | self.non_human
        ts = total.extra(
            select={'confirmed_time': 'greatest(verified_datetime, detected_datetime, neutralized_datetime)'}).order_by(
            '-confirmed_time')[:5]
        return serializers.LongestIntrusionSerializer(ts, many=True).data

    def get_intrusion_report_all_morcha(self):
        new = self.verified | self.neutralized | self.non_human
        old = FetchData.get_dangling_intrusion(pk=self.pk, end=self.end)
        return new, old

    def get_intrusion_report_day_post(self):
        today = self.verified | self.neutralized | self.non_human
        total_verified = self.verified
        total_neutralized = self.neutralized
        total_non_human = self.non_human
        qs = today.values('morcha').annotate(c=Count('morcha'))

        for i in qs:
            try:
                morcha = i['morcha']
                self.verified = total_verified.filter(morcha=morcha)
                self.neutralized = total_neutralized.filter(morcha=morcha)
                self.non_human = total_non_human.filter(morcha=morcha)
                old_dangling = FetchData.get_dangling_intrusion(pk=morcha, end=self.end)
                area_secure = self.get_security_update(old=old_dangling, verified=self.verified)
                i['area_secure'] = area_secure
                i['count'] = self.total_count()
            except Exception as e:
                print e
                return
        return qs

    def get_hypersensitive_hour(self):
        total = self.verified | self.neutralized | self.non_human
        hour = total.annotate(hour=ExtractHour('verified_datetime', tzinfo=pytz.UTC)).values('hour').annotate(
            count=Count('id'))
        return hour

    def get_security_update(self, old=None, verified=None):
        if self.level == 'morcha' and self.timespan == 'day':
            old = FetchData.get_dangling_intrusion(pk=self.pk, end=self.end)
            verified = self.verified
        elif self.level == 'morcha' and self.timespan == 'week':
            pass
        old_data_status = False if old.count() > 0 else True
        verified_filtered_data = verified.filter(
            Q(neutralized_datetime__isnull=True) | Q(neutralized_datetime__gt=self.end))
        current_data_status = False if verified_filtered_data.count() > 0 else True
        return True if old_data_status and current_data_status else False

    def get_vulnerable_morcha(self):
        if self.level == 'morcha':
            return 'not supported for this level %s' % self.level
        else:
            res = self.detected.values('morcha__name', 'morcha__uuid').annotate(count=Count('verified_datetime'))
        return res

    def get_vulnerable_post(self):
        if self.level == 'morcha':
            return 'not supported for this level %s' % self.level
        elif self.level == 'post':
            return 'not supported for this level %s' % self.level
        else:
            res = self.detected.values('morcha__post__name', 'morcha__post__uuid').annotate(
                count=Count('verified_datetime'))
        return res

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
        except ObjectDoesNotExist as e:
            error = True
            message = 'detail of %s for id %r not found' % (self.level, str(self.pk))
        finally:
            return error, message
