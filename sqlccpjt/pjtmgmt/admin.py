from django.contrib import admin

# Register your models here.
from pjtmgmt.models import *

# Register your models here.



class SqlcProjectsAdmin(admin.ModelAdmin):
    list_display = ('ownername', 'created_dt','project_nm','prod_id' )

class SqlcProdAdmin(admin.ModelAdmin):
    list_display = ('prod_id', 'prod_nm', 'prod_desc', 'tot_user_qty','tot_server_qty')



#admin.site.register(SqlcProjects, SqlcProjectsAdmin)
admin.site.register(SqlcProd, SqlcProdAdmin)
admin.site.register(MntServer)
admin.site.register(MntGroup)
admin.site.register(SqlcProject)
