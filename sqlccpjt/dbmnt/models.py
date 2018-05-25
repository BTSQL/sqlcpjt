




# Create your models here.
# class DBLogs(Document):
# 	server_id = StringField(max_Length=10, required =True)
# 	host_nm = StringField()
# 	op_dtm = StringField(max_Length=20)
# 	execute_cnt = DecimalField()
# 	logquery_cnt_dict = DecimalField()
# 	exe_sel_cnt = DecimalField()
# 	exe_dml_cnt = DecimalField()
# 	table_lock_cnt = DecimalField()
# 	table_lock_rate = DecimalField()
# 	row_lock_cnt = DecimalField()
# 	deadlock_cnt = DecimalField()
# 	access_denied_errors = DecimalField()
# 	delayed_errors = DecimalField()
# 	server_access_errors = DecimalField()
# 	server_access_maxcnt_error= DecimalField()
# 	total_sql_cmd_error = DecimalField()
# 	sum_err_cnt = DecimalField()
# 	table_locks_waited= DecimalField()
# 	meta = {'indexes': ['op_dtm',]}
# class Processlist(Document):
# 	server_id = StringField(max_Length=10, required =True)
# 	op_dtm = StringField(max_Length=20)
# 	pid = StringField()
# 	user = StringField()
# 	host = StringField()
# 	db = StringField()
# 	command = StringField()
# 	time = DecimalField()
# 	state = StringField()
# 	info = StringField()
# 	time_ms = DecimalField()
# 	stage = StringField()
# 	max_stage = StringField()
# 	progress = DecimalField()
# 	mem_used = DecimalField()
# 	examined_row = DecimalField()
# 	query_id = StringField()
# 	info_binary = StringField()
# 	tid = StringField()

class SqlcDBLogs(models.Model):
    server = models.ForeignKey('MntServer', on_delete=models.CASCADE)
    op_dtm = models.DateField()




