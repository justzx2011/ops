#coding:utf-8

""" 执行mysql语句 """
from ops import settings
from ops.model.mysql_server import MysqlServer


class AllMachineInfo(object):
    @property
    def machine_list(self):
        db = MysqlServer(settings.DATABASES)
        sql = "select `serverip`,`publicip`,`idcname`,`memsize`,`cpunum`,`disksize`,`serverrack`,`sn`, \
        `stype`,`os`,`sname`,`mstatus`,`cname`,`cinfo`,`comment`,zc_machine.`mid` from zc_machine left join zc_idc on zc_machine.rid = zc_idc.rid \
        left join zc_service on zc_machine.service = zc_service.sid left join zc_contact on \
        zc_machine.ccid = zc_contact.ccid"
        result = db.run_sql(sql)
        db.close()
        return result

    @property
    def add_host_select(self):
        db = MysqlServer(settings.DATABASES)
        sql_idc = "select `rid`,`idcname` from zc_idc"
        sql_project = "select `sid`,`sname` from zc_service"
        sql_contact = "select `ccid`,`cname` from zc_contact"
        sql_status = "select `mstatus` from zc_machine group by `mstatus`"
        result_idc = db.run_sql(sql_idc)
        result_project = db.run_sql(sql_project)
        result_contact = db.run_sql(sql_contact)
        result_status = db.run_sql(sql_status)
        db.close()
        return result_idc, result_project, result_contact, result_status

    @staticmethod
    def add_host_check(result):
        db = MysqlServer(settings.DATABASES)
        sql = "select `serverip` from zc_machine where serverip='%s'" % result
        result = db.run_sql(sql)
        db.close()
        return result

    @staticmethod
    def add_host(result):
        db = MysqlServer(settings.DATABASES)
        sql = "insert into zc_machine (serverip, publicip , rid, memsize, cpunum, disksize, \
        serverrack, sn, stype, os, service, mstatus, ccid, comment, createtime) \
        values ('%s', '%s', '%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%d', '%s', '%s')" % \
        (result["server_ip"], result["public_ip"], int(result["idc_name"]), result["mem_size"],
         result["cpu_num"], result["disk_size"], result["server_rack"], result["sn"],
         result["server_type"], result["os"], int(result["project_name"]), result["server_status"],
         int(result["server_contact"]), result['comment'], result['create_time'])
        db.execute_sql(sql)
        db.close()

    @staticmethod
    def modify_host(result):
        db = MysqlServer(settings.DATABASES)
        sql = "select `serverip`,`publicip`,`idcname`,`memsize`,`cpunum`,`disksize`,`serverrack`,`sn`, \
        `stype`,`os`,`sname`,`mstatus`,`cname`,`cinfo`,`comment`,zc_machine.`mid` from zc_machine left join zc_idc on zc_machine.rid = zc_idc.rid \
        left join zc_service on zc_machine.service = zc_service.sid left join zc_contact on \
        zc_machine.ccid = zc_contact.ccid where mid='%s'" % result
        result = db.run_sql(sql)
        db.close()
        return result

    @staticmethod
    def modify_host_update(result, mid):
        db = MysqlServer(settings.DATABASES)
        sql = "update zc_machine set serverip='%s', publicip='%s', rid='%d', memsize='%s', cpunum='%s', \
         disksize='%s', serverrack='%s', sn='%s', stype='%s', os='%s', service='%d', mstatus='%s', ccid='%d', \
          comment='%s', modifytime='%s' where mid='%d' " % \
        (result["server_ip"], result["public_ip"], int(result["idc_name"]), result["mem_size"],
         result["cpu_num"], result["disk_size"], result["server_rack"], result["sn"],
         result["server_type"], result["os"], int(result["project_name"]), result["server_status"],
         int(result["server_contact"]), result['comment'], result['modify_time'], int(mid))
        db.execute_sql(sql)
        db.close()

    @staticmethod
    def delete_host(result):
        db = MysqlServer(settings.DATABASES)
        sql = "delete from zc_machine where mid='%d'" % int(result)
        db.execute_sql(sql)
        db.close()

    @staticmethod
    def search_hosts(result):
        db = MysqlServer(settings.DATABASES)
        sql = "select `serverip`,`publicip`,`idcname`,`memsize`,`cpunum`,`disksize`,`serverrack`,`sn`, \
        `stype`,`os`,`sname`,`mstatus`,`cname`,`cinfo`,`comment`,zc_machine.`mid` from zc_machine left join \
        zc_idc on zc_machine.rid = zc_idc.rid left join zc_service on zc_machine.service = zc_service.sid \
        left join zc_contact on zc_machine.ccid = zc_contact.ccid where serverip like '%%%s%%' and publicip like \
        '%%%s%%' and zc_machine.rid like '%%%s%%' and memsize like '%%%s%%' and cpunum \
        like '%%%s%%' and disksize like '%%%s%%' and serverrack like '%%%s%%' and sn like '%%%s%%' and stype like \
        '%%%s%%' and os like '%%%s%%' and service like '%%%s%%' and mstatus like '%%%s%%' and zc_machine.ccid like '%%%s%%' and \
        comment like '%%%s%%'" % (result["server_ip"], result["public_ip"], result["idc_name"], result["mem_size"],
        result["cpu_num"], result["disk_size"], result["server_rack"], result["sn"], result["server_type"], result["os"],
        result["project_name"], result["server_status"], result["server_contact"], result['comment'])
        result = db.run_sql(sql)
        db.close()
        return result

    @staticmethod
    def search_hosts_quick(result):
        db = MysqlServer(settings.DATABASES)
        sql = "select `serverip`,`publicip`,`idcname`,`memsize`,`cpunum`,`disksize`,`serverrack`,`sn`, \
        `stype`,`os`,`sname`,`mstatus`,`cname`,`cinfo`,`comment`,zc_machine.`mid` from zc_machine left join \
        zc_idc on zc_machine.rid = zc_idc.rid left join zc_service on zc_machine.service = zc_service.sid \
        left join zc_contact on zc_machine.ccid = zc_contact.ccid where serverip like '%%%s%%'" % result
        result = db.run_sql(sql)
        db.close()
        return result

    @property
    def distribute_host(self):
        db = MysqlServer(settings.DATABASES)
        sql = "select zc_service.`sid`, zc_service.`sname`, count(*) from zc_machine left join zc_service on \
        zc_machine.service = zc_service.sid group by service"
        sql_count = "select count(*) from zc_machine"
        result = db.run_sql(sql)
        result_count = db.run_sql(sql_count)
        db.close()
        return result, result_count

    @staticmethod
    def distribute_host_search(result):
        db = MysqlServer(settings.DATABASES)
        sql = "select `serverip`,`publicip`,`idcname`,`memsize`,`cpunum`,`disksize`,`serverrack`,`sn`, \
        `stype`,`os`,`sname`,`mstatus`,`cname`,`cinfo`,`comment`,zc_machine.`mid` from zc_machine left join \
        zc_idc on zc_machine.rid = zc_idc.rid left join zc_service on zc_machine.service = zc_service.sid \
        left join zc_contact on zc_machine.ccid = zc_contact.ccid where zc_machine.service = '%s'" % result
        result = db.run_sql(sql)
        db.close()
        return result

    @staticmethod
    def room_list():
        db = MysqlServer(settings.DATABASES)
        sql = "select `rid`,`idcname`,`contact`,`phone`,`comments` from zc_idc"
        sql_count = "select zc_idc.rid,count(zc_machine.serverip) from zc_machine right join zc_idc on zc_idc.rid = zc_machine.rid group by zc_idc.rid"
        result = db.run_sql(sql)
        result_count = db.run_sql(sql_count)
        db.close()
        return result, result_count

    @staticmethod
    def get_room_modify(result):
        db = MysqlServer(settings.DATABASES)
        sql = "select `idcname`,`contact`,`phone`,`comments` from zc_idc where rid=%d" % int(result)
        result = db.run_sql(sql)
        db.close()
        return result

    @staticmethod
    def set_room_modify(result, result_rid):
        db = MysqlServer(settings.DATABASES)
        sql = "update zc_idc set idcname='%s',contact='%s',phone='%s',comments='%s' where zc_idc.rid='%d'" % (
            result["room_name"], result["room_contact"], result["contact_phone"], result["room_comment"], int(result_rid)
        )
        db.execute_sql(sql)
        db.close()

    @staticmethod
    def delete_room_modify(result):
        db = MysqlServer(settings.DATABASES)
        sql = "delete from zc_idc where zc_idc.rid='%d'" % int(result)
        db.execute_sql(sql)
        db.close()

    @staticmethod
    def add_room_check(result):
        db = MysqlServer(settings.DATABASES)
        sql = "select `idcname` from zc_idc where idcname='%s'" % result
        result = db.run_sql(sql)
        db.close()
        return result

    @staticmethod
    def set_add_room(result):
        db = MysqlServer(settings.DATABASES)
        sql = "insert into zc_idc (idcname,contact,phone,comments) values ('%s','%s','%s','%s')" % (
            result["room_name"], result["room_contact"], result["contact_phone"], result["room_comment"]
        )
        db.execute_sql(sql)
        db.close()

    @staticmethod
    def get_project_list():
        db = MysqlServer(settings.DATABASES)
        sql = "select zc_service.sid,zc_service.sname from `zc_service`"
        result = db.run_sql(sql)
        db.close()
        return result

    @staticmethod
    def delete_project(result):
        db = MysqlServer(settings.DATABASES)
        sql = "delete from zc_service where sid='%d'" % int(result)
        db.execute_sql(sql)
        db.close()

    @staticmethod
    def get_contact_list():
        db = MysqlServer(settings.DATABASES)
        sql = "select `ccid`,`cname`,`cinfo` from zc_contact"
        result = db.run_sql(sql)
        db.close()
        return result

    @staticmethod
    def delete_contact(result):
        db = MysqlServer(settings.DATABASES)
        sql = "delete from zc_contact where ccid='%d'" % int(result)
        db.execute_sql(sql)
        db.close()

    @staticmethod
    def add_project_check(result):
        db = MysqlServer(settings.DATABASES)
        sql = "select `sname` from zc_service where sname='%s'" % result
        result = db.run_sql(sql)
        db.close()
        return result

    @staticmethod
    def set_add_project(result):
        db = MysqlServer(settings.DATABASES)
        sql = "insert into zc_service (sname) values ('%s')" % result
        db.execute_sql(sql)
        db.close()

    @staticmethod
    def add_contact_check(result):
        db = MysqlServer(settings.DATABASES)
        sql = "select `cname` from zc_contact where cname='%s'" % result
        result = db.run_sql(sql)
        db.close()
        return result

    @staticmethod
    def set_add_contact(result):
        db = MysqlServer(settings.DATABASES)
        sql = "insert into zc_contact (cname,cinfo) values ('%s','%s')" % (result["contact_name"], result["contact_info"])
        db.execute_sql(sql)
        db.close()