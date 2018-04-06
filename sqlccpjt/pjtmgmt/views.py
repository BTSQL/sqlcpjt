from django.shortcuts import get_object_or_404 , render
from pjtmgmt.models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from pjtmgmt.forms import *
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
import pymysql
from datetime import datetime

from django.contrib import messages



# Create your views here

class SqlcProjectLV(ListView):
    model = SqlcProject
    template_name = 'pjtmgmt/sqlcpjtlist.html'

    # 본인 프로젝트만 볼수 있다.
    def get_queryset(self):
        return SqlcProject.objects.filter(owner=self.request.user)



## form에 디폴트 값 셋팅 하기
class SqlcProjectCV(LoginRequiredMixin, CreateView):


    form_class = SqlcProjectForm
    template_name = 'pjtmgmt/add_sqlcpjt.html'
    success_url = reverse_lazy('pjtlist')


    def get_form_kwargs(self, **kwargs):

        # 초기값으로 셋팅
        self.initial  = {'sta_eff_dt': datetime.today().strftime("%Y%m%d"),
               'end_eff_dt': '20181231',
               'owner' : self.request.user,
               'prod_id'  : SqlcProd.objects.get(prod_id='FREE') #디폴트로 공짜 상품 넣어줌
               }

        kwargs = super(SqlcProjectCV,self).get_form_kwargs(**kwargs)
        kwargs['user'] = self.request.user

        return kwargs


    def form_valid(self, form):
        print(" Debug :" )
        form.instance.owner = self.request.user
        return super(SqlcProjectCV, self).form_valid(form)

    def form_invalid(self, form):
        print("form is invalid")
        return super(SqlcProjectCV, self).form_invalid(form)



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


## 본인의 선택한 프로젝트의 ID로 저장 되도록 수정 필요
## 모델 폼으로 변경 필요
class MntServerCV(LoginRequiredMixin, CreateView):

    form_class = SqlcServerForm
    template_name = 'pjtmgmt/add_mntserver.html'

    #pjtid = get_object_or_404(pk, pk=kwargs['pk'])


    #success_url = reverse_lazy(self.reque )



    def get_success_url(self):
        return reverse_lazy('detailpjt', kwargs={'pk': self.kwargs['pk']})

    def get_form_kwargs(self, **kwargs):

        pjtid = self.kwargs['pk']
        # 초기값으로 셋팅
        self.initial = {'project': SqlcProject.objects.get(id=pjtid)  # 디폴트로 소속프로젝트 값 셋팅
                        }

        kwargs = super(MntServerCV,self).get_form_kwargs(**kwargs)
        kwargs['pjtid'] = pjtid

        return kwargs


    ## 오류시에 메시지 발송 하기
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

        # error_code = 1 : 접속이상
        # error_code = 10 : 로그설정이상
        # error_code = 100 : 글로벌상태 이상
        # error_code = 1000 : Infomation Schema Porcesslist 이상
        # error_code = 10000 : Infomation Schema 응답시간 확인
        # error_code = 0 : 정상

        db = None
        error_code = 0
        error_msg = ''

        try:

            db = pymysql.connect(host=db_server_ip, port=int(db_access_port), user=db_acnt_id,
                                 passwd=db_acnt_pwd)

        except Exception as e:
            # error_msg = error_msg + str(e)
            print(" 접속이 되지 않습니다. ")
            error_code = error_code + 1

        try:
            sql = 'SELECT 1 FROM mysql.slow_log ;'
            cursor = db.cursor()
            cursor.execute(sql)
            cursor.close()

        except Exception as e:
            # print(e)
            error_code = error_code + 10

        try:
            sql = """ show global status ; """
            cursor = db.cursor()
            cursor.execute(sql)
            cursor.close()

        except Exception as e:
            # error_msg = error_msg + str(e)
            # print(e)
            error_code = error_code + 100

        try:
            sql = """ SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST ; """
            cursor = db.cursor()
            cursor.execute(sql)
            cursor.close()

        except Exception as err:
            # print(str(type(err)))
            # error_msg = error_msg + str(e)
            # print('Handling run-time error:', err)
            error_code = error_code + 1000

        try:
            sql = """ SELECT time, count, total FROM INFORMATION_SCHEMA.QUERY_RESPONSE_TIME; """
            cursor = db.cursor()
            cursor.execute(sql)
            cursor.close()

        except Exception as e:
            error_code = error_code + 10000

        if error_code == 0:
            print('접속성공')
            form.instance.owner = self.request.user
            return super(MntServerCV, self).form_valid(form)

        else:
            print(str(error_code))

        return super(MntServerCV, self).form_valid(form)

    def check_server(self, server_ip, acnt_id, acnt_pwd):
        pass


class SqlcProjectUV(LoginRequiredMixin, UpdateView):

    form_class = ProjectForm
    template_name = 'pjtmgmt/update_sqlcpjt.html'
    success_url = reverse_lazy('pjtlist')

    ##form_class.fields["photos"].queryset = Photo.objects.filter(user=request.user)

    #fields = ['project_nm', 'project_desc', 'ownername', 'prod_id']
    #template_name = 'pjtmgmt/update_sqlcpjt.html'
    #success_url = reverse_lazy('pjtlist')


    #def get(self, request, *args, **kwargs):
    #    self.object = SqlcProjects.objects.get(ownername=self.request.user)
    #    formClass = self.get_form_class()
    #    form = self.get_form(formClass)
    #    form.fields["ownername"].queryset =

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(SqlcProjectUV, self).form_valid(form)


    def get_queryset(self):
        return SqlcProjects.objects.filter(ownername=self.request.user)




class SqlcProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = SqlcProject
    success_url = reverse_lazy('pjtlist')
    template_name = 'pjtmgmt/confirm_delete.html'


class SqlcProjectDV(LoginRequiredMixin, DetailView):
    model = SqlcProject
    template_name = 'pjtmgmt/detail_sqlcpjt.html'


class MntGroupCV(LoginRequiredMixin, CreateView):

    form_class = MntGroupForm
    template_name = 'pjtmgmt/add_mntgroup.html'
    #success_url = reverse_lazy('detailpjt', kwards={'pk': self.pk})


    # form_class = ProjectForm(initial={'sta_eff_dt': datetime.today().strftime("%Y%m%d"),
    # 'end_eff_dt': '20181231'})

    def get_form_kwargs(self, **kwargs):
       # self.initial = {'sta_eff_dt': datetime.today().strftime("%Y%m%d"),
       #                 'end_eff_dt': '20181231',
       #                 'ownername': self.request.user
       #                 }

        kwargs = super(MntGroupCV, self).get_form_kwargs(**kwargs)

        return kwargs

    def form_valid(self, form):
        print(" Debug :")
        form.instance.owner = self.request.user

        return super(MntGroupCV, self).form_valid(form)

    def form_invalid(self, form):
        print("form is invalid")






class MntServerUV(LoginRequiredMixin , UpdateView) :
    model = MntServer
    fields = ['project', 'server_nm', 'db_server_ip', 'db_access_port', 'db_acnt_id',
              'db_acnt_pwd', 'server_desc', 'is_available']
    template_name = 'pjtmgmt/add_mntserver.html'
    success_url = reverse_lazy('pjtlist')

    ## 오류시에 메시지 발송 하기
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

        # error_code = 1 : 접속이상
        # error_code = 10 : 로그설정이상
        # error_code = 100 : 글로벌상태 이상
        # error_code = 1000 : Infomation Schema Porcesslist 이상
        # error_code = 10000 : Infomation Schema 응답시간 확인
        # error_code = 0 : 정상

        db = None
        error_code = 0
        error_msg = ''

        try:

            db = pymysql.connect(host=db_server_ip, port=int(db_access_port), user=db_acnt_id,
                                 passwd=db_acnt_pwd)

        except Exception as e:
            # error_msg = error_msg + str(e)
            print(" 접속이 되지 않습니다. ")
            error_code = error_code + 1

        try:
            sql = 'SELECT 1 FROM mysql.slow_log ;'
            cursor = db.cursor()
            cursor.execute(sql)
            cursor.close()

        except Exception as e:
            # print(e)
            error_code = error_code + 10

        try:
            sql = """ show global status ; """
            cursor = db.cursor()
            cursor.execute(sql)
            cursor.close()

        except Exception as e:
            # error_msg = error_msg + str(e)
            # print(e)
            error_code = error_code + 100

        try:
            sql = """ SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST ; """
            cursor = db.cursor()
            cursor.execute(sql)
            cursor.close()

        except Exception as err:
            # print(str(type(err)))
            # error_msg = error_msg + str(e)
            # print('Handling run-time error:', err)
            error_code = error_code + 1000

        try:
            sql = """ SELECT time, count, total FROM INFORMATION_SCHEMA.QUERY_RESPONSE_TIME; """
            cursor = db.cursor()
            cursor.execute(sql)
            cursor.close()

        except Exception as e:
            # error_msg = error_msg + str(e)
            # print(e)
            error_code = error_code + 10000

        if error_code == 0:
            print('접속성공')
            form.instance.owner = self.request.user
            # form.save()
            return super(MntServerUV, self).form_valid(form)

        else:
            # print(e)
            print(str(error_code))

        return super(MntServerUV, self).form_valid(form)

    def check_server(self, server_ip, acnt_id, acnt_pwd):
        pass


class MntServerDeleteView(LoginRequiredMixin, DeleteView):
    model = MntServer
    success_url = reverse_lazy('pjtlist')
    template_name = 'pjtmgmt/confirm_delete.html'
