# -*- coding: UTF-8 -*-
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    speciality = models.ManyToManyField('TabBdataFacSpeciality',blank=True,null=True)
#用户信息
class TabBdataCommonUser(models.Model):
    userid = models.CharField(primary_key=True, max_length=32)
    usercode = models.CharField(max_length=64, blank=True)
    username = models.CharField(max_length=64, blank=True)
    password = models.CharField(max_length=100, blank=True)
    invaldate = models.DateField(blank=True, null=True)
    authmode = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255, blank=True)
    unlocktime = models.DateField(blank=True, null=True)
    menutype = models.CharField(max_length=255, blank=True)
    lastlogin = models.DateTimeField(blank=True, null=True)
    errcount = models.IntegerField(blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    validtime = models.CharField(max_length=255, blank=True)
    maccode = models.CharField(max_length=128, blank=True)
    ipaddress = models.CharField(max_length=128, blank=True)
    email = models.CharField(max_length=255, blank=True)
    mesid = models.CharField(max_length=64, blank=True)
    initinfoprovider = models.CharField(max_length=32, blank=True)
    ad_flag = models.CharField(max_length=1, blank=True)
    def __unicode__(self):
        return self.username
    class Meta:
        managed = False
        db_table = 'tab_bdata_common_user'  
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'
        
#组织机构   
class TabBdataCommonOrg(models.Model):
    orgid = models.CharField(primary_key=True, max_length=32)
    orgcode = models.CharField(max_length=32, blank=True)
    orgname = models.CharField(max_length=64, blank=True)
    orglevel = models.CharField(max_length=32, blank=True)
    parentorgid = models.CharField(max_length=32, blank=True)
    orgseq = models.CharField(max_length=512, blank=True)
    orgtype = models.CharField(max_length=12, blank=True)
    orgaddr = models.CharField(max_length=256, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    manaposition = models.IntegerField(blank=True, null=True)
    managerid = models.IntegerField(blank=True, null=True)
    orgmanager = models.CharField(max_length=128, blank=True)
    linkman = models.CharField(max_length=30, blank=True)
    linktel = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=128, blank=True)
    weburl = models.CharField(max_length=512, blank=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True)
    area = models.CharField(max_length=30, blank=True)
    createtime = models.DateTimeField(blank=True, null=True)
    lastupdate = models.DateField(blank=True, null=True)
    sortno = models.BigIntegerField(blank=True, null=True)
    isleaf = models.CharField(max_length=255, blank=True)
    subcount = models.IntegerField(blank=True, null=True)
    remark = models.CharField(max_length=500, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    org_order = models.IntegerField(blank=True, null=True)
    def __unicode__(self):
        return self.orgname
    class Meta:
        managed = False
        db_table = 'tab_bdata_common_org'  
        verbose_name = '组织机构'
        verbose_name_plural = '组织机构'
#专业
class TabBdataFacSpeciality(models.Model):
    sid = models.CharField(primary_key=True, max_length=64)
    sname = models.CharField(max_length=50, blank=True)
    emscode = models.CharField(max_length=50, blank=True)
    erpscode = models.CharField(max_length=50, blank=True)
    sindex = models.FloatField(blank=True, null=True)
    def __unicode__(self):
        return self.sname
    class Meta:
        managed = False
        db_table = 'tab_bdata_fac_speciality'
        verbose_name = '专业'
        verbose_name_plural = '专业'    
#种类
class TabBdataFacCategory(models.Model):
    cid = models.CharField(primary_key=True, max_length=32)
    cname = models.CharField(max_length=100, blank=True)
    mcid = models.CharField(max_length=32, blank=True)
    mcname = models.CharField(max_length=100, blank=True)
    scid = models.CharField(max_length=32, blank=True)
    scname = models.CharField(max_length=100, blank=True)
    sid = models.CharField(max_length=64, blank=True)
    def __unicode__(self):
        return self.cname
    class Meta:
        managed = False
        db_table = 'tab_bdata_fac_category'
        verbose_name = '种类'
        verbose_name_plural = '种类'
#备品备件
class TabBdataFacSpInfo(models.Model):
    spencode = models.CharField(primary_key=True, max_length=32)
    orgid = models.ForeignKey(TabBdataCommonOrg, db_column='orgid', blank=True, null=True)
    spname = models.CharField(max_length=64, blank=True)
    sid = models.CharField(max_length=64, blank=True)
    cid = models.CharField(max_length=32, blank=True)
    mcid = models.CharField(max_length=32, blank=True)
    scid = models.CharField(max_length=32, blank=True)
    spmodel = models.CharField(max_length=50, blank=True)
    spserialnumbe = models.CharField(max_length=32, blank=True)
    amount = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=20, blank=True)
    goodslocationcode = models.CharField(max_length=10, blank=True)
    spvalue = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    supplier = models.CharField(max_length=200, blank=True)
    manufacturers = models.CharField(max_length=50, blank=True)
    specification = models.CharField(max_length=100, blank=True)
    qualification = models.CharField(max_length=200, blank=True)
    factorydate = models.DateField(blank=True, null=True)
    effectivedate = models.DateField(blank=True, null=True)
    spstatus = models.FloatField(blank=True, null=True)
    remark1 = models.CharField(max_length=1000, blank=True)
    remark2 = models.CharField(max_length=1000, blank=True)
    remark3 = models.CharField(max_length=1000, blank=True)
    source = models.CharField(max_length=255, blank=True)
    emspid = models.CharField(max_length=100, blank=True)
    encode = models.CharField(max_length=32, blank=True)
    encodedesc = models.CharField(max_length=255, blank=True)
    def __unicode__(self):
            return self.spname
    class Meta:
        managed = False
        db_table = 'tab_bdata_fac_sp_info'
        verbose_name = '备品备件'
        verbose_name_plural = '备品备件'
#ElementAttributeId
class Elementsreation(models.Model):
    relationcode = models.CharField(primary_key=True, max_length=64)
    promptname = models.CharField(max_length=64, blank=True)
    attributeid = models.CharField(max_length=32, blank=True)
    def __unicode__(self):
            return self.promptname
    class Meta:
        managed = False
        db_table = 'elementsreation'
        verbose_name = 'ElementAttributeId'
        verbose_name_plural = 'ElementAttributeId' 
#页面配置   
class TabBdataCommonPagesu(models.Model):
    pageid = models.CharField(primary_key=True, max_length=32)
    buttonid = models.CharField(max_length=32, blank=True)
    buttonname = models.CharField(max_length=64, blank=True)
    roleid = models.CharField(max_length=32, blank=True)
    mstraddr = models.CharField(max_length=250, blank=True)
    urladdr = models.CharField(max_length=1000, blank=True)
    def __unicode__(self):
            return self.buttonname
    class Meta:
        managed = False
        db_table = 'tab_bdata_common_pagesu'
        verbose_name = '页面配置'
        verbose_name_plural = '页面配置' 
#入库单
class TabBdataFacInSp(models.Model):
    recordid = models.CharField(primary_key=True, max_length=32)
    invoiceno = models.CharField(max_length=50, blank=True)
    operdatetime = models.DateTimeField(blank=True, null=True)
    operuser = models.CharField(max_length=30, blank=True)
    source = models.CharField(max_length=255, blank=True)
    remark = models.CharField(max_length=255, blank=True)
    opertype = models.CharField(max_length=20, blank=True)
    def __unicode__(self):
            return self.recordid
    class Meta:
        managed = False
        db_table = 'tab_bdata_fac_in_sp'
        verbose_name = '入库单'
        verbose_name_plural = '入库单' 
#出库单
class TabBdataFacOutSp(models.Model):
    recordid = models.CharField(primary_key=True, max_length=32)
    pickingunit = models.CharField(max_length=50, blank=True)
    sid = models.CharField(max_length=32, blank=True)
    operdatetime = models.DateTimeField(blank=True, null=True)
    operuser = models.CharField(max_length=30, blank=True)
    auditor = models.CharField(max_length=30, blank=True)
    pickingman = models.CharField(max_length=30, blank=True)
    direction = models.CharField(max_length=256, blank=True)
    remark = models.CharField(max_length=256, blank=True)
    totalsum = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    opertype = models.CharField(max_length=20, blank=True)
    def __unicode__(self):
            return self.recordid
    class Meta:
        managed = False
        db_table = 'tab_bdata_fac_out_sp'
        verbose_name = '出库单'
        verbose_name_plural = '出库单' 
#入库单详细
class TabBdataFacInSpInfo(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    recordid = models.ForeignKey(TabBdataFacInSp, db_column='recordid')
    spencode = models.ForeignKey('TabBdataFacSpInfo', db_column='spencode', blank=True, null=True)
    serialnumbe = models.FloatField(blank=True, null=True)
    spname = models.CharField(max_length=64, blank=True)
    spmodel = models.CharField(max_length=50, blank=True)
    suname = models.CharField(max_length=64, blank=True)
    specification = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=20, blank=True)
    amount = models.FloatField(blank=True, null=True)
    priceperunit = models.FloatField(blank=True, null=True)
    totalprice = models.FloatField(blank=True, null=True)
    source = models.CharField(max_length=255, blank=True)
    remark = models.CharField(max_length=255, blank=True)
    def __unicode__(self):
            return self.spname
    class Meta:
        managed = False
        db_table = 'tab_bdata_fac_in_sp_info'
        verbose_name = '入库单详细'
        verbose_name_plural = '入库单详细'
#出库单详细
class TabBdataFacOutSpInfo(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    spencode = models.ForeignKey('TabBdataFacSpInfo', db_column='spencode', blank=True, null=True)
    recordid = models.ForeignKey(TabBdataFacOutSp, db_column='recordid', blank=True, null=True)
    serialnumbe = models.FloatField(blank=True, null=True)
    spname = models.CharField(max_length=50, blank=True)
    spmodel = models.CharField(max_length=50, blank=True)
    suname = models.CharField(max_length=50, blank=True)
    specification = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=20, blank=True)
    amount = models.FloatField(blank=True, null=True)
    priceperunit = models.FloatField(blank=True, null=True)
    totalprice = models.FloatField(blank=True, null=True)
    direction = models.CharField(max_length=255, blank=True)
    remark = models.CharField(max_length=255, blank=True)
    outopertype = models.CharField(max_length=32, blank=True)
    def __unicode__(self):
            return self.spname
    class Meta:
        managed = False
        db_table = 'tab_bdata_fac_out_sp_info'
        verbose_name = '出库单详细'
        verbose_name_plural = '出库单详细'
#组织机构关系
class ViewBdataCommonOrg(models.Model):
    parentorgid = models.CharField(primary_key=True,max_length=64, blank=True)
    parentorgname = models.CharField(max_length=64, blank=True)
    orgid = models.CharField(max_length=64, blank=True)
    orgname = models.CharField(max_length=64, blank=True)
    orglevel = models.CharField(max_length=64, blank=True)
    def __unicode__(self):
            return self.orgname
    class Meta:
        managed = False
        db_table = 'view_bdata_common_org'
        verbose_name = '组织机构视图'
        verbose_name_plural = '组织机构视图'
#人员单位关系视图
class ViewBdataCommonUserOrg(models.Model):
    usercode = models.CharField(primary_key=True,max_length=64, blank=True)
    username = models.CharField(max_length=64, blank=True)
    orgid = models.CharField(max_length=64, blank=True)
    orgname = models.CharField(max_length=64, blank=True)
    orglevel = models.CharField(max_length=64, blank=True)
    def __unicode__(self):
            return self.username
    class Meta:
        managed = False
        db_table = 'view_bdata_common_user_org'
        verbose_name = '人员单位关系视图'
        verbose_name_plural = '人员单位关系视图'
STATUS_CHOICES = [
    ('d', 'Draft'),
    ('p', 'Published'),
    ('w', 'Withdrawn'),
]
def get_org_info():
    info_list = []
    alldept = TabBdataCommonOrg.objects.all()
    for dept in alldept:
        str = (dept.orgid,dept.orgname)
        info_list.append(str)
    return info_list
#单位查询类型
class OrgQueryType(models.Model):
    orgid = models.CharField(blank=True, max_length=64,choices=get_org_info())
    querytype = models.CharField(blank=True, max_length=64)
    def __unicode__(self):
            return self.orgid
    class Meta:
        db_table = 'spm_org_query_type'
        verbose_name = '单位查询类型'
        verbose_name_plural = '单位查询类型'
#入库记录暂存
class OdsInSpInfo(models.Model):
    organdtime = models.CharField(max_length=255, blank=True)
    templatedesigner = models.CharField(max_length=255, blank=True)
    designermphone = models.CharField(max_length=255, blank=True)
    designertel = models.CharField(max_length=255, blank=True)
    reporteduser = models.CharField(max_length=255, blank=True)
    reportedtel = models.CharField(max_length=255, blank=True)
    reportedemail = models.CharField(max_length=255, blank=True)
    serialnumbe = models.CharField(max_length=255, blank=True)
    spname = models.CharField(max_length=255, blank=True)
    spmodel = models.CharField(max_length=255, blank=True)
    spserialnumbe = models.CharField(max_length=255, blank=True)
    amount = models.CharField(max_length=255, blank=True)
    unit = models.CharField(max_length=255, blank=True)
    goodslocationcode = models.CharField(max_length=255, blank=True)
    specification = models.CharField(max_length=255, blank=True)
    spvalue = models.CharField(max_length=255, blank=True)
    sname = models.CharField(max_length=255, blank=True)
    cname = models.CharField(max_length=255, blank=True)
    supplier = models.CharField(max_length=255, blank=True)
    manufacturers = models.CharField(max_length=255, blank=True)
    factorydate = models.CharField(max_length=255, blank=True)
    effectivedate = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=255, blank=True)
    indate = models.CharField(max_length=255, blank=True)
    intime = models.CharField(max_length=255, blank=True)
    inuser = models.CharField(max_length=32, blank=True)
    remark1 = models.CharField(max_length=255, blank=True)
    remark2 = models.CharField(max_length=255, blank=True)
    remark3 = models.CharField(max_length=255, blank=True)
    remark4 = models.CharField(max_length=255, blank=True)
    remark5 = models.CharField(max_length=255, blank=True)
    opertime = models.DateTimeField(blank=True, null=True)
    operuser = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'ods_in_sp_info'
        managed = False

class TabBdataOrgPrivileges(models.Model):
    parentorgid = models.CharField(max_length=32, blank=True)
    orgid = models.CharField(max_length=32, blank=True)

    class Meta:
        managed = False
        db_table = 'tab_bdata_org_privileges'
        
class ViewBdataSpmExaOrg(models.Model):
    #id = models.CharField(primary_key=True, max_length=32)
    orgid = models.CharField(primary_key=True, max_length=32)
    orgcode = models.CharField(max_length=32, blank=True)
    
    
    
    orgname = models.CharField(max_length=68, blank=True)
    orglevel = models.CharField(max_length=32, blank=True)
    parentorgid = models.CharField(max_length=132, blank=True)
    orgseq = models.CharField(max_length=512, blank=True)
    orgtype = models.CharField(max_length=12, blank=True)
    orgaddr = models.CharField(max_length=256, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    manaposition = models.IntegerField(blank=True, null=True)
    managerid = models.IntegerField(blank=True, null=True)
    orgmanager = models.CharField(max_length=128, blank=True)
    linkman = models.CharField(max_length=30, blank=True)
    linktel = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=128, blank=True)
    weburl = models.CharField(max_length=512, blank=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True)
    area = models.CharField(max_length=30, blank=True)
    createtime = models.DateTimeField(blank=True, null=True)
    lastupdate = models.DateField(blank=True, null=True)
    sortno = models.BigIntegerField(blank=True, null=True)
    isleaf = models.CharField(max_length=1, blank=True)
    subcount = models.IntegerField(blank=True, null=True)
    remark = models.CharField(max_length=512, blank=True)
    longitude =models.CharField(max_length=64, blank=True)
    latitude =models.CharField(max_length=64, blank=True)
    #longitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    #latitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    def __unicode__(self):
        return self.orgname
    class Meta:
        managed = False
        db_table = 'view_bdata_spm_exa_org'  
        verbose_name = '组织机构view'
        verbose_name_plural = '组织机构view'
    
class viewBdataSpmExaUser(models.Model):
    userid=models.CharField(max_length=32, blank=True)
    usercode=models.CharField(primary_key=True,max_length=64, blank=True)       
    password=models.CharField(max_length=100, blank=True)
    invaldate=models.DateTimeField()
    username=models.CharField(max_length=64, blank=True)
    authmode=models.CharField(max_length=255, blank=True)
    status=models.CharField(max_length=255, blank=True)
    unlocktime=models.DateTimeField()
    menutype=models.CharField(max_length=255, blank=True)
    lastlogin=models.DateTimeField()
    errcount=models.IntegerField(blank=True, null=True)
    startdate=models.DateTimeField()
    enddate=models.DateTimeField()
    validtime=models.CharField(max_length=255, blank=True)
    maccode=models.CharField(max_length=128, blank=True)
    ipaddress=models.CharField(max_length=128, blank=True)
    email=models.CharField(max_length=255, blank=True)
    mesid=models.CharField(max_length=64, blank=True)
    initinfoprovider=models.CharField(max_length=32, blank=True)
    ad_flag=models.CharField(max_length=1, blank=True)
    orgname=models.CharField(max_length=68, blank=True)
    orgcode=models.CharField(max_length=68, blank=True)
    def __unicode__(self):
        return self.username
    class Meta:
        managed = False
        db_table = 'view_bdata_spm_exa_user'  
        verbose_name = '额外用户view'
        verbose_name_plural = '额外用户view'

class OdsUserOrgInfo(models.Model):
    userid = models.CharField(max_length=32)
    usercode = models.CharField(primary_key=True,max_length=64)
    password = models.CharField(max_length=100, blank=True)
    invaldate = models.DateField(blank=True, null=True)
    username = models.CharField(max_length=64, blank=True)
    authmode = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255, blank=True)
    unlocktime = models.DateField(blank=True, null=True)
    menutype = models.CharField(max_length=255, blank=True)
    lastlogin = models.DateTimeField(blank=True, null=True)
    errcount = models.IntegerField(blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    validtime = models.CharField(max_length=255, blank=True)
    maccode = models.CharField(max_length=128, blank=True)
    ipaddress = models.CharField(max_length=128, blank=True)
    email = models.CharField(max_length=255, blank=True)
    mesid = models.CharField(max_length=64, blank=True)
    initinfoprovider = models.CharField(max_length=32, blank=True)
    ad_flag = models.CharField(max_length=1, blank=True)
    orgcode = models.CharField(max_length=32, blank=True)
    orgname = models.CharField(max_length=64, blank=True)
    issyn=models.CharField(max_length=1, blank=True)
    opertime=models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ods_user_org_info'
        verbose_name = '添加用户临时表'
        verbose_name_plural = '添加用户临时表'

class OrgDic(models.Model):
    orgid = models.CharField(primary_key=True,max_length=32, blank=True)
    orgname = models.CharField(max_length=64, blank=True)
    orgcode = models.CharField(max_length=10, blank=True)

    class Meta:
        managed = False
        db_table = 'org_dic'
        verbose_name = '单位简称表'
        verbose_name_plural = '单位简称表'