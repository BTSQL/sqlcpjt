from django.shortcuts import render
from pjtmgmt.models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from pjtmgmt.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
import pymysql
from datetime import datetime


# Create your views here

class SqlcProjectLV(ListView):
    model = SqlcProjects
    template_name = 'pjtmgmt/sqlcpjtlist.html'

    # 본인 프로젝트만 볼수 있다.
    def get_queryset(self):
        return SqlcProjects.objects.filter(ownername=self.request.user)

"""
class SqlcProjects(models.Model):
    ownername    = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    created_dt   = models.DateTimeField(default=datetime.now, blank=False)
    project_nm   = models.CharField(max_length=255)
    project_desc = models.TextField()
    sta_eff_dt   = models.CharField(max_length=8)
    end_eff_dt   = models.CharField(max_length=8)
    prod_id = models.ForeignKey('SqlcProd',on_delete=models.CASCADE)

"""

#class SqlcProjectDV(DetailView):
#    pass


## form에 디폴트 값 셋팅 하기
class SqlcProjectCV(LoginRequiredMixin, CreateView):


    form_class = ProjectForm
    template_name = 'pjtmgmt/add_sqlcpjt.html'
    success_url = reverse_lazy('pjtlist')
    #form_class = ProjectForm(initial={'sta_eff_dt': datetime.today().strftime("%Y%m%d"),
                                 #'end_eff_dt': '20181231'})

    def get_form_kwargs(self, **kwargs):
        self.initial  = {'sta_eff_dt': datetime.today().strftime("%Y%m%d"),
               'end_eff_dt': '20181231',
               'ownername' : self.request.user
               }
        #instance = getattr(self, 'instance', None)

        """
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['sta_eff_dt'].widget.attrs['readonly'] = True
            self.fields['end_eff_dt'].widget.attrs['readonly'] = True
            self.fields['ownername'].widget.attrs['readonly'] = True
        """

        kwargs = super(SqlcProjectCV,self).get_form_kwargs(**kwargs)

        return kwargs


    def form_valid(self, form):
        print(" Debug :" )
        form.instance.owner = self.request.user
        #form.cleaned_data['ownername'] = self.request.user
        #form.cleaned_data['sta_eff_dt'] = datetime.today().strftime("%Y%m%d")
        #form.cleaned_data['end_eff_dt'] = '20181231'
        #form.ownername = self.request.user
        #form.sta_eff_dt = datetime.today().strftime("%Y%m%d")
        #form.end_eff_dt = '20181231'

        return super(SqlcProjectCV, self).form_valid(form)

    def form_invalid(self, form):
        print("form is invalid")

    #print("진입")
    #model = SqlcProjects
    #fields = ['project_nm', 'project_desc', 'ownername','prod_id']
    #template_name = 'pjtmgmt/add_sqlcpjt.html'
    #success_url = reverse_lazy('pjtlist')

    #print("진입2")
    #def form_valid(self, form):
    #    print("진입3")
    #    print('ttt')
        #form.cleaned_data['ownername'] = self.request.user
    #    form.instance.owner = self.request.user
        #form.save()
#    return super(SqlcProjectCV, self).form_valid(form)

    #def form_invalid(self, form):
    #    print ("form is invalid")
    #    return http.HttpResponse("form is invalid.. this is just an HttpResponse object")

    #form_class = ProjectForm
    #fields = ['project_nm', 'project_desc']

    #print('nnonono'# )

    #print('xxx')

    #def form_valid(self, form):
    #    print('ttt')
    #    form.ownername = self.request.user
    #    form.instance.owner = self.request.user
    #    return super().form_valid(form)


class SqlcProjectUV(LoginRequiredMixin, UpdateView):

    form_class = ProjectForm
    template_name = 'pjtmgmt/update_sqlcpjt.html'
    success_url = reverse_lazy('pjtlist')

    #fields = ['project_nm', 'project_desc', 'ownername', 'prod_id']
    #template_name = 'pjtmgmt/update_sqlcpjt.html'
    #success_url = reverse_lazy('pjtlist')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(SqlcProjectUV, self).form_valid(form)

    def get_queryset(self):
        return SqlcProjects.objects.filter(ownername=self.request.user)


class SqlcProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = SqlcProjects
    success_url = reverse_lazy('pjtlist')


class SqlcProjectDV(LoginRequiredMixin, DetailView):
    pass
    #model =


## 본인의 선택한 프로젝트의 ID로 저장 되도록 수정 필요
## 모델 폼으로 변경 필요
class MntServerCV(LoginRequiredMixin, CreateView):
    model = MntServer
    fields = '__all__'
    template_name = 'pjtmgmt/add_mntserver.html'
    success_url = reverse_lazy('pjtlist')

    def form_valid(self, form):
        print("진입3")
        print('ttt')

        db_server_ip = '%s' % self.request.POST['db_server_ip']
        db_access_port = '%s' % self.request.POST['db_access_port']
        db_acnt_id = '%s' % self.request.POST['db_acnt_id']
        db_acnt_pwd = '%s' % self.request.POST['db_acnt_pwd']

        print("ip : " + db_server_ip)
        print("port : " + db_access_port)
        print("id : " + db_acnt_id)
        print("pwd : " + db_acnt_pwd)


        #error_code = 1 : 접속이상
        #error_code = 10 : 로그설정이상
        #error_code = 100 : 글로벌상태 이상
        #error_code = 1000 : Infomation Schema Porcesslist 이상
        #error_code = 10000 : Infomation Schema 응답시간 확인
        #error_code = 0 : 정상

        db = None
        error_code = 0
        error_msg = ''

        try :

            db = pymysql.connect(host=db_server_ip, port=int(db_access_port), user=db_acnt_id,
                                 passwd=db_acnt_pwd)

        except Exception as e:
            #error_msg = error_msg + str(e)
            print(" 접속이 되지 않습니다. ")
            error_code = error_code + 1

        try:
            sql = 'SELECT 1 FROM mysql.slow_log ;'
            cursor = db.cursor()
            cursor.execute(sql)
            cursor.close()

        except Exception as e:
            #print(e)
            error_code = error_code + 10

        try:
            sql = """ show global status ; """
            cursor = db.cursor()
            cursor.execute(sql)
            cursor.close()

        except Exception as e:
            #error_msg = error_msg + str(e)
            #print(e)
            error_code = error_code + 100


        try:
            sql = """ SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST ; """
            cursor = db.cursor()
            cursor.execute(sql)
            cursor.close()

        except Exception as err:
            #print(str(type(err)))
            #error_msg = error_msg + str(e)
            #print('Handling run-time error:', err)
            error_code = error_code + 1000


        try:
            sql = """ SELECT time, count, total FROM INFORMATION_SCHEMA.QUERY_RESPONSE_TIME; """
            cursor = db.cursor()
            cursor.execute(sql)
            cursor.close()

        except Exception as e:
            #error_msg = error_msg + str(e)
            #print(e)
            error_code = error_code + 10000


        if error_code == 0 :
            print('접속성공')
            form.instance.owner = self.request.user
            # form.save()
            return super(MntServerCV, self).form_valid(form)

        else :
            #print(e)
            print(str(error_code))

        return super(MntServerCV, self).form_valid(form)


    def check_server(self, server_ip, acnt_id, acnt_pwd):
        return True

