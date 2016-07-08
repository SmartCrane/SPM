# -*- coding: UTF-8 -*-
'''
Created on 2015年6月3日

@author: Administrator
'''
import datetime
import json
import traceback

import cx_Oracle
import django
from django.contrib.auth import login as normallogin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import logout, redirect_to_login
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.db.models.query import QuerySet
from django.http.response import HttpResponse, HttpResponseRedirect, \
    HttpResponseServerError
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.template.response import TemplateResponse
from django.utils.encoding import smart_text, force_text
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
import xlrd

from SPM import settings
from SPM.customauthentication import customlogin
from SPM.models import TabBdataCommonOrg, TabBdataFacSpeciality, \
    TabBdataFacCategory, TabBdataFacSpInfo, Elementsreation, \
    TabBdataCommonPagesu, TabBdataFacInSp, TabBdataFacInSpInfo, \
    TabBdataCommonUser, ViewBdataCommonOrg, TabBdataFacOutSp, \
    TabBdataFacOutSpInfo, CustomUser, ViewBdataCommonUserOrg, OrgQueryType, \
    OdsInSpInfo, TabBdataOrgPrivileges,\
    ViewBdataSpmExaOrg,viewBdataSpmExaUser,OdsUserOrgInfo,OrgDic
from cPickle import loads


#判断当前用户和当前出入usercode是否相同，不相同则退出之前session重新登录，若用户不存在跳转登录页面
def comparesessionuser(usercode,sessionuser,request):
    if usercode == sessionuser.username:
        return True
    else:
        try:
            user = CustomUser.objects.get(username=usercode)
            if user:
                logout(request)
                user.backend='django.contrib.auth.backends.ModelBackend'
                normallogin(request, user)
                return True
        except CustomUser.DoesNotExist:
            logout(request)
            return False

def read_excel(request):
    #print request
    #print request.FILES
    input_excel = request.FILES['file']
    workbook = xlrd.open_workbook(file_contents=input_excel.read())
    # 根据sheet索引或者名称获取sheet内容
    sheet = workbook.sheet_by_index(0) # sheet索引从0开始
    rows = sheet.nrows # 行数
    cols = sheet.ncols # 列数

    info = sheet.cell(0,10)
    people = sheet.cell(12,17).value
    mobile = sheet.cell(12,20).value
    email = sheet.cell(12,22).value
    organdtime = sheet.cell(10,0).value
    templatedesigner = sheet.cell(10,17).value
    designermphone = sheet.cell(10,19).value
    designertel = sheet.cell(10,22).value
    ret = {}
    ret['people'] = people
    ret['mobile'] = mobile
    ret['email']  = email
    ret['organdtime']  = organdtime
    ret['templatedesigner']  = templatedesigner
    ret['designermphone']  = designermphone
    ret['designertel']  = designertel
    ret['rows']  = []

    #str = ""
    for rownum in range(15,rows):
        row = sheet.row_values(rownum)
        #ret['rows'].append(row)
        flag = 0;
        for colnum in range(1,23):
            if(row[colnum] != ""):
                flag = 1
                break;
        if(flag == 1):
            data = {}
            #data["index"] = row[0]
            data["spname"] = row[1]
            data["spmodel"] = row[2]
            data["spserialnumbe"] = row[3]
            data["amount"] = row[4]
            data["unit"] = row[5]
            data["goodslocation"] = row[6]
            data["specification"] = row[7]
            data["spvalue"] = row[8]
            ssid = TabBdataFacSpeciality.objects.filter(sname=row[9])
            data["sid"] = ssid[0].sid
            data["sidname"] = ssid[0].sname
            
            cid = TabBdataFacCategory.objects.filter(cname="其他",sid=ssid[0].sid)
            data["cid"] = cid[0].cid
            data["cidname"] = cid[0].cname
            data["supplier"] = row[11]
            data["manufacturer"] = row[12]
            if row[13]:
                date = xlrd.xldate_as_tuple(row[13],0)
                data["factorydate"] = str(date[0])+"-"+str(date[1])+"-"+str(date[2])
            if row[14]:
                date = xlrd.xldate_as_tuple(row[14],0)
                data["effectivedate"] = str(date[0])+"-"+str(date[1])+"-"+str(date[2])
            data["source"] = row[15]
            date = xlrd.xldate_as_tuple(row[16],0)
            data["indate"] = str(date[0])+"-"+str(date[1])+"-"+str(date[2])
            date = xlrd.xldate_as_tuple(row[17],1)
            data["intime"] = str(date[3])+":"+str(date[4])+":"+str(date[5])
            data["inuser"] = row[18]
            remarkarray = []
            remarkstr = ""
            data["remark1"] = ""
            data["remark2"] = ""
            data["remark3"] = ""
            data["remark4"] = ""
            data["remark5"] = ""
            if row[19]:
                remarkarray.append(row[19])
                data["remark1"] = row[19]
            if row[20]:
                remarkarray.append(row[20])
                data["remark2"] = row[20]
            if row[21]:
                remarkarray.append(row[21])
                data["remark3"] = row[21]
            if row[22]:
                remarkarray.append(row[22])
                data["remark4"] = row[22]
            if row[23]:
                remarkarray.append(row[23])
                data["remark5"] = row[23]
            if len(remarkarray) == 1:
                remarkstr = remarkarray[0]
            else:
                for oneremark in remarkarray:
                    idx = remarkarray.index(oneremark)+1
                    remarkstr += str(idx) +"."+ oneremark +"<br/>"
            data["remark"] = remarkstr
            ret['rows'].append(data)
    try:
        json.dumps(ret)
    except Exception, e:
        print Exception,e
    print json.dumps(ret)
    response = HttpResponse(json.dumps(ret))
    return response

if __name__ == '__main__':
    read_excel()

def login(request):
    return render_to_response('spm/login.html',locals(), context_instance=RequestContext(request))
def ttt(request):
    print settings.DATABASES['default']['HOST']
    return render_to_response('spm/tes.html',locals(), context_instance=RequestContext(request))
def err_log(request):
    file_object = open('D:/Apache24/logs/error.log')
    try:
        all_the_text = file_object.readlines()
        arr = []
        for str in all_the_text:
            st = force_text(str, encoding='gbk', strings_only=False, errors='strict')
            arr.append(st)
    except:
        traceback.print_exc()
    finally:
        file_object.close()
    return render_to_response('spm/err_log.html',locals(), context_instance=RequestContext(request))
#     return HttpResponse(ss)
@login_required
def outsp(request):
    if request.GET.get('usercode') and request.user:
        if not comparesessionuser(request.GET.get('usercode'),request.user,request):
            return HttpResponseRedirect('/spm')
    try:
        currentuser = TabBdataCommonUser.objects.get(usercode = request.user.username)
    except TabBdataCommonUser.DoesNotExist:
        return  HttpResponseServerError('当前登录用户不存在')
    userdeptid = ViewBdataCommonUserOrg.objects.filter(usercode=request.user.username).order_by('orglevel').first().orgid
    try:
        username = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        host = settings.DATABASES['default']['HOST']
        name = settings.DATABASES['default']['NAME']
        db = cx_Oracle.connect(username,password,'%s/%s'%(host,name))
    except:
        return  HttpResponseServerError('数据库连接错误')
    cursor = db.cursor()
    spcodeSQL = "select in_out_record_gen('%s','%s','%s') from dual"%(userdeptid,"A","")
    cursor.execute(spcodeSQL)
    recordid = cursor.fetchall()[0][0]
    return render_to_response('spm/outsp.html',locals(), context_instance=RequestContext(request))

@login_required
def insp(request):
    if request.GET.get('usercode') and request.user:
        if not comparesessionuser(request.GET.get('usercode'),request.user,request):
            return HttpResponseRedirect('/spm')
    try:
        currentuser = TabBdataCommonUser.objects.get(usercode = request.user.username)
    except TabBdataCommonUser.DoesNotExist:
        return  HttpResponseServerError('当前登录用户不存在')
    hideleft = request.GET.get('hideleft')
    hidetop = request.GET.get('hidetop')
    currentuserorg = ViewBdataCommonUserOrg.objects.filter(usercode=currentuser.usercode)
    userdeptid = ViewBdataCommonUserOrg.objects.filter(usercode=currentuser.usercode).order_by('orglevel').first().orgid
    try:
        username = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        host = settings.DATABASES['default']['HOST']
        name = settings.DATABASES['default']['NAME']
        db = cx_Oracle.connect(username,password,'%s/%s'%(host,name))
    except:
        return  HttpResponseServerError('数据库连接错误')
#     cursor = db.cursor()
#     spcodeSQL = "select in_out_record_gen('%s','%s','%s') from dual"%(userdeptid,"A","")
#     cursor.execute(spcodeSQL)
#     recordid = cursor.fetchall()[0][0]
    return render_to_response('spm/insp.html',locals(), context_instance=RequestContext(request))

@login_required
def SPM_Query(request):
    if request.GET.get('usercode') and request.user:
        if not comparesessionuser(request.GET.get('usercode'),request.user,request):
            return HttpResponseRedirect('/spm')
    try:
        currentuser = TabBdataCommonUser.objects.get(usercode = request.user.username)
    except TabBdataCommonUser.DoesNotExist:
        return  HttpResponseServerError('当前登录用户不存在')
    userdepts = ViewBdataCommonUserOrg.objects.filter(usercode=request.user.username).order_by('orglevel').first()
    userquerytype = ""
    try:
        userquerytype = OrgQueryType.objects.get(orgid = userdepts.orgid).querytype
    except:
        userquerytype = ""
    hideleft = request.GET.get('hideleft')
    hidetop = request.GET.get('hidetop')
    deptelement = Elementsreation.objects.get(relationcode="E7");
    specialtyelement = Elementsreation.objects.get(relationcode="l0");
    categoryelement = Elementsreation.objects.get(relationcode="yw");
    depteleid = deptelement.attributeid
    specialtyid = specialtyelement.attributeid
    categoryid = categoryelement.attributeid
    pagesu = TabBdataCommonPagesu.objects.get(pageid="Z9VBp");
    exppagesu = TabBdataCommonPagesu.objects.get(pageid="pr5JR");
    mstraddr = pagesu.mstraddr
    jsonurladdr = json.loads(pagesu.urladdr)
    expjsonurladdr = json.loads(exppagesu.urladdr)
    expevt = expjsonurladdr['evt']
    expsrc = expjsonurladdr['src']
    evt = jsonurladdr['evt']
    src = jsonurladdr['src']
    visMode = jsonurladdr['visMode']
    reportViewMode = jsonurladdr['reportViewMode']
    reportID = jsonurladdr['reportID']
    server = jsonurladdr['server']
    Project = jsonurladdr['Project']
    port = jsonurladdr['port']
    share = jsonurladdr['share']
    hiddensections = jsonurladdr['hiddensections']
    uid = jsonurladdr['uid']
    pwd = jsonurladdr['pwd']
    promptAnswerMode = jsonurladdr['promptAnswerMode']
    return render_to_response('spm/query2.html',locals(), context_instance=RequestContext(request))

def ods_SPM_Query(request):
    if request.GET.get('usercode') and request.user:
        if not comparesessionuser(request.GET.get('usercode'),request.user,request):
            return HttpResponseRedirect('/spm')
    try:
        currentuser = TabBdataCommonUser.objects.get(usercode = request.user.username)
    except TabBdataCommonUser.DoesNotExist:
        return  HttpResponseServerError('当前登录用户不存在')
    userdepts = ViewBdataCommonUserOrg.objects.filter(usercode=request.user.username).order_by('orglevel').first()
    userquerytype = ""
    try:
        userquerytype = OrgQueryType.objects.get(orgid = userdepts.orgid).querytype
    except:
        userquerytype = ""
    hideleft = request.GET.get('hideleft')
    hidetop = request.GET.get('hidetop')
    deptelement = Elementsreation.objects.get(relationcode="E7");
    specialtyelement = Elementsreation.objects.get(relationcode="l0");
    categoryelement = Elementsreation.objects.get(relationcode="yw");
    depteleid = deptelement.attributeid
    specialtyid = specialtyelement.attributeid
    categoryid = categoryelement.attributeid
    pagesu = TabBdataCommonPagesu.objects.get(pageid="m9GtU");
    exppagesu = TabBdataCommonPagesu.objects.get(pageid="pr5JR");
    mstraddr = pagesu.mstraddr
    jsonurladdr = json.loads(pagesu.urladdr)
    expjsonurladdr = json.loads(exppagesu.urladdr)
    expevt = expjsonurladdr['evt']
    expsrc = expjsonurladdr['src']
    evt = jsonurladdr['evt']
    src = jsonurladdr['src']
    visMode = jsonurladdr['visMode']
    reportViewMode = jsonurladdr['reportViewMode']
    reportID = jsonurladdr['reportID']
    server = jsonurladdr['server']
    Project = jsonurladdr['Project']
    port = jsonurladdr['port']
    share = jsonurladdr['share']
    hiddensections = jsonurladdr['hiddensections']
    uid = jsonurladdr['uid']
    pwd = jsonurladdr['pwd']
    promptAnswerMode = jsonurladdr['promptAnswerMode']
    return render_to_response('spm/query2.html',locals(), context_instance=RequestContext(request))
@login_required
def SPM(request):
    if request.GET.get('usercode') and request.user:
        if not comparesessionuser(request.GET.get('usercode'),request.user,request):
            return HttpResponseRedirect('/spm')
    try:
        currentuser = TabBdataCommonUser.objects.get(usercode = request.user.username)
    except TabBdataCommonUser.DoesNotExist:
        return  HttpResponseServerError('当前登录用户不存在')
    userdepts = ViewBdataCommonUserOrg.objects.filter(usercode=request.user.username).order_by('orglevel').first()
    userquerytype = ""
    try:
        userquerytype = OrgQueryType.objects.get(orgid = userdepts.orgid).querytype
    except:
        userquerytype = ""
    hideleft = request.GET.get('hideleft')
    hidetop = request.GET.get('hidetop')
    deptelement = Elementsreation.objects.get(relationcode="E7");
    specialtyelement = Elementsreation.objects.get(relationcode="l0");
    categoryelement = Elementsreation.objects.get(relationcode="yw");
    depteleid = deptelement.attributeid
    specialtyid = specialtyelement.attributeid
    categoryid = categoryelement.attributeid
    pagesu = TabBdataCommonPagesu.objects.get(pageid="Nb9r4");
    mstraddr = pagesu.mstraddr
    jsonurladdr = json.loads(pagesu.urladdr)
    evt = jsonurladdr['evt']
    src = jsonurladdr['src']
    visMode = jsonurladdr['visMode']
    currentViewMedia = jsonurladdr['currentViewMedia']
    documentID = jsonurladdr['documentID']
    server = jsonurladdr['server']
    Project = jsonurladdr['Project']
    port = jsonurladdr['port']
    share = jsonurladdr['share']
    hiddensections = jsonurladdr['hiddensections']
    uid = jsonurladdr['uid']
    pwd = jsonurladdr['pwd']
    promptAnswerMode = jsonurladdr['promptAnswerMode']
    return render_to_response('spm/query1.html',locals(), context_instance=RequestContext(request))

@login_required
def insp_query(request):
    if request.GET.get('usercode') and request.user:
        if not comparesessionuser(request.GET.get('usercode'),request.user,request):
            return HttpResponseRedirect('/spm')
    try:
        currentuser = TabBdataCommonUser.objects.get(usercode = request.user.username)
    except TabBdataCommonUser.DoesNotExist:
        return  HttpResponseServerError('当前登录用户不存在')
    userdepts = ViewBdataCommonUserOrg.objects.filter(usercode=request.user.username).order_by('orglevel').first()
    userquerytype = ""
    try:
        userquerytype = OrgQueryType.objects.get(orgid = userdepts.orgid).querytype
    except:
        userquerytype = ""
    hideleft = request.GET.get('hideleft')
    hidetop = request.GET.get('hidetop')
    deptelement = Elementsreation.objects.get(relationcode="E7");
    specialtyelement = Elementsreation.objects.get(relationcode="l0");
    categoryelement = Elementsreation.objects.get(relationcode="yw");
    depteleid = deptelement.attributeid
    specialtyid = specialtyelement.attributeid
    categoryid = categoryelement.attributeid
    pagesu = TabBdataCommonPagesu.objects.get(pageid="Ju3Rn");
    mstraddr = pagesu.mstraddr
    jsonurladdr = json.loads(pagesu.urladdr)
    evt = jsonurladdr['evt']
    src = jsonurladdr['src']
    print src+"---"
    visMode = jsonurladdr['visMode']
    currentViewMedia = jsonurladdr['currentViewMedia']
    documentID = jsonurladdr['documentID']
    server = jsonurladdr['server']
    Project = jsonurladdr['Project']
    port = jsonurladdr['port']
    share = jsonurladdr['share']
    hiddensections = jsonurladdr['hiddensections']
    uid = jsonurladdr['uid']
    pwd = jsonurladdr['pwd']
    promptAnswerMode = jsonurladdr['promptAnswerMode']
    return render_to_response('spm/insp_query.html',locals(), context_instance=RequestContext(request))

def queryspdata(request):
    spname = request.GET.get('spname')
    if request.GET.get('spmodel'):
        spmodel = request.GET.get('spmodel')
        fitsp = TabBdataFacSpInfo.objects.filter(spname__contains=spname).filter(spmodel__contains=spmodel)[0:10]
    else:
        fitsp = TabBdataFacSpInfo.objects.filter(spname__contains=spname)[0:10]
    ss = []
    for sp in fitsp:
        spstr = sp.spname+";"+sp.spmodel
        s = {"text":spstr}
        ss.append(s)
    response = HttpResponse(json.dumps(ss,ensure_ascii = False), content_type="application/json")
    return response

def queryinspdata(request):
    spname = request.GET.get('spname')
    if request.GET.get('spmodel'):
        spmodel = request.GET.get('spmodel')
        fitsp = TabBdataFacInSpInfo.objects.filter(spname__contains=spname).filter(spmodel__contains=spmodel)[0:10]
    else:
        fitsp = TabBdataFacInSpInfo.objects.filter(spname__contains=spname)[0:10]
    ss = []
    for sp in fitsp:
        spstr = sp.spname+";"+sp.spmodel
        s = {"text":spstr}
        ss.append(s)
    response = HttpResponse(json.dumps(ss,ensure_ascii = False), content_type="application/json")
    return response

def queryrecorddata(request):
    try:
        record = request.GET.get('record')
        if record:
            fitsp = TabBdataFacInSp.objects.filter(recordid__contains=record)[0:10]
        else:
            fitsp = TabBdataFacInSp.objects.all()[0:10]
    except:
        traceback.print_exc()
    ss = []
    for sp in fitsp:
        spstr = sp.recordid
        s = {"text":spstr}
        ss.append(s)
    response = HttpResponse(json.dumps(ss,ensure_ascii = False), content_type="application/json")
    return response

def get_filter_data(request):
    userdepts = ViewBdataCommonUserOrg.objects.filter(usercode=request.user.username)
    alldepts = ViewBdataCommonOrg.objects.none()
    for dept in userdepts:
        depts = ViewBdataCommonOrg.objects.filter(parentorgid = dept.orgid).order_by('orglevel','orgname')
        alldepts = alldepts|depts
    alldept = []
    filter_data={}
    for dept in alldepts:
        onedept = {"id":dept.orgid,"text":dept.orgname}
        alldept.append(onedept)
#     specialitys = TabBdataFacSpeciality.objects.all()
    specialitys =request.user.speciality.all()
    allspeciality = []
    for speciality in specialitys:
        onespeciality = {"id":speciality.sid,"text":speciality.sname}
        allspeciality.append(onespeciality)
    filter_data["dept"] = alldept
    filter_data["speciality"] = allspeciality
    response = HttpResponse(json.dumps(filter_data,ensure_ascii = False), content_type="application/json")
    return response

@csrf_exempt
def reload_category(request):
    allcategory = []
    sids = request.POST.getlist('sids[]')
    try:
        if len(sids)==0 or len(sids[0])==0:
            categorys =TabBdataFacCategory.objects.all()
        else:
            categorys = []
            for sid in sids:
                category = TabBdataFacCategory.objects.filter(sid = sid)
                for c in category:
                    categorys.append(c)
        for cate in categorys:
            onecategory = {"id":cate.cid,"text":cate.cname,"sid":cate.sid}
            allcategory.append(onecategory)
        allcategory.insert(0,{"id":"","text":u"全部种类"})
        response = HttpResponse(json.dumps(allcategory,ensure_ascii = False), content_type="application/json")
        return response
    except:
        traceback.print_exc()

def get_dda(request):
    jsda = {"total":9,"rows": [
        {'spname':'sdrswrds','spmodel': '213444'},
        {'spname':'223444','spmodel': '213444'},
    ],
    "footer":[
        {"spname":"总计","spmodel":282.35},
    ]}
    response = HttpResponse(json.dumps(jsda,ensure_ascii = False), content_type="application/json")
    return response

def get_user_speciality(request):
    specialitys = TabBdataFacSpeciality.objects.all()
    allspeciality = []
    for speciality in specialitys:
        onespeciality = {"id":speciality.sid,"text":speciality.sname}
        allspeciality.append(onespeciality)
    response = HttpResponse(json.dumps(allspeciality,ensure_ascii = False), content_type="application/json")
    return response

def get_common_org(request):
    
    orgs = TabBdataCommonOrg.objects.all()
    allorg = []
    for org in orgs :
        oneorg = {"id":org.orgcode ,"text":org.orgname}
        allorg.append(oneorg)
    lorg={"id":0,"text":"全部单位"}
    allorg.append(lorg)
    response = HttpResponse(json.dumps(allorg,ensure_ascii = False), content_type="application/json")
    return response

def get_speciality_category(request):
    sid = request.GET.get('sid')
    categorys = TabBdataFacCategory.objects.filter(sid = sid)
    allcategory = []
    for category in categorys:
        onecategory = {"id":category.cid,"text":category.cname}
        allcategory.append(onecategory)
    response = HttpResponse(json.dumps(allcategory,ensure_ascii = False), content_type="application/json")
    return response

@transaction.commit_on_success
@csrf_exempt
def insert_database(request):
    isimport = request.GET.get('isimport')
    try:
        recordid = ""
        try:
            username = settings.DATABASES['default']['USER']
            password = settings.DATABASES['default']['PASSWORD']
            host = settings.DATABASES['default']['HOST']
            name = settings.DATABASES['default']['NAME']
            db = cx_Oracle.connect(username,password,'%s/%s'%(host,name))
        except:
            return  HttpResponseServerError('error')
        cursor = db.cursor()
        spcodeSQL = """select generate_key(5) from dual"""
        serialnumbeSQL = """select generate_key(32) from dual"""
        postdata = request.POST.get('data')
        facinspnum = request.POST.get('spnum')
        currentuser = TabBdataCommonUser.objects.get(usercode = request.user.username)
        userdeptid = ViewBdataCommonUserOrg.objects.filter(usercode=currentuser.usercode).order_by('orglevel').first().orgid
        if facinspnum:
            recordidSQL = "select in_out_record_gen('%s','%s','%s') from dual"%(userdeptid,"A",facinspnum)
            cursor.execute(recordidSQL)
            recordid = cursor.fetchall()[0][0]
        else:
            recordidSQL = "select in_out_record_gen('%s','%s','%s') from dual"%(userdeptid,"A","")
            cursor.execute(recordidSQL)
            recordid = cursor.fetchall()[0][0]
        facindate = str(request.POST.get('date'))
        facintime = str(request.POST.get('time'))

        facinoperuser = request.POST.get('operuser')
        facindatetimestr = u"%s %s"%(facindate,facintime)
        facindatetime = datetime.datetime.strptime(facindatetimestr,'%Y-%m-%d %H:%M:%S')
        print (facindatetime)
        jsondata = json.loads(postdata)
        #入库单更新
        facinsp = TabBdataFacInSp()
        facinsp.recordid=recordid
        facinsp.operdatetime=facindatetime
        facinsp.operuser=facinoperuser
#         facinsp.source="???????????"
#         facinsp.remark="???????????"
        facinsp.save()
        for one in jsondata:
            if one.get('spname') and one.get('sid') and one.get('amount'):
                cursor.execute(spcodeSQL)
                spcoderesult = cursor.fetchall()[0][0]
                cursor.execute(serialnumbeSQL)
                serialnumberesult = cursor.fetchall()[0][0]
                #更新备品备件表
                onesp = TabBdataFacSpInfo()
                onesp.spencode = spcoderesult
                onesp.spname = one.get('spname')
                onesp.sid = one.get('sid')
                
                #onesp.spmodel=one.get('spmodel')
                try:
                    onsporg = TabBdataCommonOrg.objects.get(orgid = request.POST.get('userorg'))
                except TabBdataCommonOrg.DoesNotExist:
                    transaction.rollback()
                    traceback.print_exc()
                    return  HttpResponseServerError('error')
                onesp.orgid = onsporg
                if one.get('cid'):
                    onesp.cid = one.get('cid')
                   
                else:
                    onecategory = TabBdataFacCategory.objects.filter(cname="其他",sid=one.get('sid'))
                    
                    p=onecategory[0].cname
                onesp.spmodel = one.get('spmodel')
                onesp.spserialnumbe = one.get('spserialnumbe')
                if one.get('amount'):
                    onesp.amount = float(one.get('amount'))
                onesp.unit = one.get('unit')
                onesp.goodslocationcode = one.get('goodslocation')
                if one.get('spvalue'):
                    onesp.spvalue = one.get('spvalue')
                onesp.supplier = one.get('supplier')
                onesp.manufacturers = one.get('manufacturer')
                onesp.specification = one.get('specification')
                onesp.qualification = one.get('qualification')
                if one.get('factorydate'):
                    onesp.factorydate = datetime.datetime.strptime(one.get('factorydate'),'%Y-%m-%d')
                if one.get('effectivedate'):
                    onesp.effectivedate = datetime.datetime.strptime(one.get('effectivedate'),'%Y-%m-%d')
                onesp.remark1 = one.get('remark')
                onesp.source = one.get('source')
                onesp.save()
                #更新入库单详细表
                facinspinfo = TabBdataFacInSpInfo()
                facinspinfo.id = serialnumberesult
                facinspinfo.recordid = facinsp
                facinspinfo.spencode = onesp
                facinspinfo.serialnumbe = jsondata.index(one)+1
                facinspinfo.spname = one.get('spname')
                facinspinfo.suname = one.get('supplier')
                facinspinfo.specification = one.get('specification')
                facinspinfo.unit = one.get('unit')
                #添加备品型号
                if one.get('spmodel'):
                    facinspinfo.spmodel=one.get('spmodel')
               # else :
               #     facinspinfo.spmodel='No_spmodel'
                
                if one.get('amount'):
                    facinspinfo.amount = one.get('amount')
                if one.get('spvalue'):
                    facinspinfo.priceperunit = one.get('spvalue')
                if one.get('spvalue') and one.get('amount'):
                    facinspinfo.totalprice = float(one.get('spvalue'))*float(one.get('amount'))
                facinspinfo.save()
                #更新入库记录暂存表
                if isimport:   #如果是导入模板的方式，则保存一份在临时表
                    odsinspinfo = OdsInSpInfo()
                    odsinspinfo.organdtime = str(request.POST.get('organdtime'))
                    odsinspinfo.templatedesigner = str(request.POST.get('templatedesigner'))
                    odsinspinfo.designermphone = str(request.POST.get('designermphone'))
                    odsinspinfo.designertel = str(request.POST.get('designertel'))
                    odsinspinfo.organdtime = str(request.POST.get('organdtime'))
                    odsinspinfo.reporteduser = str(request.POST.get('people'))
                    odsinspinfo.reportedtel = str(request.POST.get('mobile'))
                    odsinspinfo.reportedemail = str(request.POST.get('email'))
                    odsinspinfo.serialnumbe = jsondata.index(one)+1
                    odsinspinfo.spname = one.get('spname')
                    odsinspinfo.spmodel = one.get('spmodel')
                    if one.get('amount'):
                        odsinspinfo.amount = float(one.get('amount'))
                    odsinspinfo.unit = one.get('unit')
                    odsinspinfo.goodslocationcode = one.get('goodslocation')
                    odsinspinfo.specification = one.get('specification')
                    if one.get('spvalue'):
                        odsinspinfo.spvalue = one.get('spvalue')
                    speciality = TabBdataFacSpeciality.objects.get(sid=one.get('sid'))
                    #category = TabBdataFacCategory.objects.get(cid=one.get('cid'))
                    
                    if one.get('cid'):
                        category = TabBdataFacCategory.objects.get(cid=one.get('cid'))
                        odsinspinfo.cname = category.cname
                    else:
                        category = TabBdataFacCategory.objects.get(cname="其他",sid=one.get('sid'))
                        categorycid = onecategory[0].cid
                        odsinspinfo.cname = "其他"
                    odsinspinfo.sname = speciality.sname
                    #odsinspinfo.cname = category.cname
                    #odsinspinfo.cname = TabBdataFacCategory.objects.get(cid=category.cid,sid=one.get('sid'))
                    odsinspinfo.spserialnumbe = one.get('spserialnumbe')
                    odsinspinfo.supplier = one.get('supplier')
                    odsinspinfo.manufacturers = one.get('manufacturer')
                    if one.get('factorydate'):
                        odsinspinfo.factorydate = datetime.datetime.strptime(one.get('factorydate'),'%Y-%m-%d')
                    if one.get('effectivedate'):
                        odsinspinfo.effectivedate = datetime.datetime.strptime(one.get('effectivedate'),'%Y-%m-%d')
                    odsinspinfo.source = one.get('source')
                    odsinspinfo.indate = one.get('indate')
                    odsinspinfo.intime = one.get('intime')
                    odsinspinfo.inuser = one.get('inuser')
                    odsinspinfo.remark1 = one.get('remark1')
                    odsinspinfo.remark2 = one.get('remark2')
                    odsinspinfo.remark3 = one.get('remark3')
                    odsinspinfo.remark4 = one.get('remark4')
                    odsinspinfo.remark5 = one.get('remark5')
                    odsinspinfo.opertime = now()
                    odsinspinfo.operuser = request.user.username
                    odsinspinfo.save()
        response = HttpResponse(json.dumps({"status":"ok","recordid":recordid},ensure_ascii = False),content_type="application/json")
        return response
    except:
        transaction.rollback()
#         ss = traceback.format_exc()
        traceback.print_exc()
        if recordid:
            return  HttpResponseServerError(recordid[-5:])
        else:
            return  HttpResponseServerError('error')
@transaction.commit_on_success
@csrf_exempt
def out_database(request):
    try:
        postdata = request.POST.get('data')
        jsondata = json.loads(postdata)
        try:
            username = settings.DATABASES['default']['USER']
            password = settings.DATABASES['default']['PASSWORD']
            host = settings.DATABASES['default']['HOST']
            name = settings.DATABASES['default']['NAME']
            db = cx_Oracle.connect(username,password,'%s/%s'%(host,name))
        except:
            return  HttpResponseServerError('数据库连接错误')
        cursor = db.cursor()
        serialnumbeSQL = """select generate_key(32) from dual"""
        totalsum = 0
        facoutsp = TabBdataFacOutSp()
        facoutsp.recordid = request.POST.get('spnum')
        facoutdate = str(request.POST.get('date'))
        facouttime = str(request.POST.get('time'))
        facoutdatetimestr = u"%s %s"%(facoutdate,facouttime)
        facindatetime = datetime.datetime.strptime(facoutdatetimestr,'%Y-%m-%d %H:%M:%S')
        facoutsp.operdatetime = facindatetime
        facoutsp.opertype = "出库"
        facoutsp.pickingman = request.POST.get('pickingman')
        facoutsp.direction = request.POST.get('direction')
        facoutsp.remark = request.POST.get('remark')
        facoutsp.save()
        for one in jsondata:
            sp =TabBdataFacSpInfo.objects.get(encode = one['spencode'])
            if float(sp.amount)<float(one['amount']):
                transaction.rollback()
                return  HttpResponseServerError(u"%s数量不足"%sp.spname)
            else:
                sp.amount =float(sp.amount) - float(one['amount'])
                sp.save()
            if one['spvalue']:
                totalsum += float(one['spvalue']) * float(one['amount'])
            facoutspinfo = TabBdataFacOutSpInfo()
            cursor.execute(serialnumbeSQL)
            serialnumberesult = cursor.fetchall()[0][0]
            facoutspinfo.id = serialnumberesult
            facoutspinfo.spencode = sp
            facoutspinfo.recordid = facoutsp
            facoutspinfo.serialnumbe = jsondata.index(one)+1
            facoutspinfo.spname = sp.spname
            facoutspinfo.spmodel = sp.spmodel
            facoutspinfo.suname = sp.supplier
            facoutspinfo.specification = sp.specification
            facoutspinfo.unit = sp.unit
            facoutspinfo.amount = one['amount']
            facoutspinfo.priceperunit = sp.spvalue
            if one['spvalue']:
                facoutspinfo.totalprice = float(one['amount']) * float(one['spvalue'])
            facoutspinfo.save()
        facoutsp.totalsum = totalsum
        facoutsp.save()
        return HttpResponse('ok')
    except:
        transaction.rollback()
        ss = traceback.format_exc()
        traceback.print_exc()
        return  HttpResponseServerError('出库错误'+ss)
@csrf_exempt
@transaction.commit_on_success
def out_org(request):
    try:
        postdata = request.POST.get('data')
        postorg=request.POST.get('parentorg')
        porgdata = json.loads(postdata)
        parentorgdata = str(postorg)
        try:
            username = settings.DATABASES['default']['USER']
            password = settings.DATABASES['default']['PASSWORD']
            host = settings.DATABASES['default']['HOST']
            name = settings.DATABASES['default']['NAME']
            db = cx_Oracle.connect(username,password,'%s/%s'%(host,name))
        except:
            return  HttpResponseServerError('数据库连接错误')
       
        parentorg=TabBdataCommonOrg.objects.get(orgname = parentorgdata)  
        parentorgid=parentorg.orgid   
        
        #获得所有可见单位信息
        select_orgids=[]
        for one in porgdata:
            #select_org=TabBdataCommonOrg.objects.get(orgcode=one['orgcode'])
            select_orgids.append(one['orgcode']) 
        #test=TabBdataOrgPrivileges.objects.all()
        #增加权限
        orgs=TabBdataOrgPrivileges.objects.filter(parentorgid=parentorgid)
        
        oneorgsid=[]
        for oneorgs in orgs:
            oneorgsid.append(oneorgs.orgid)
        
        for porgid in select_orgids:
                        
            if porgid not in oneorgsid:                
                
                orgpri=TabBdataOrgPrivileges()
                orgpri.parentorgid=parentorgid
                orgpri.orgid=porgid
           # orgpri.id=TabBdataOrgPrivileges.objects.all()[:-1][id]+1
                orgpri.save()
        #删除权限
        del_orgs=TabBdataOrgPrivileges.objects.filter(parentorgid=parentorgid)
        del_orgids=[]
        for del_org in del_orgs:
            del_orgids.append(del_org.orgid)
        
        for del_orgid in del_orgids:
            flag=False
            if del_orgid not in select_orgids:
                del_pri=TabBdataOrgPrivileges.objects.get(parentorgid =parentorgid,orgid=del_orgid)
                del_pri.delete()
            
        return HttpResponse('ok')
    except:
        transaction.rollback()
        ss = traceback.format_exc()
        traceback.print_exc()
        return  HttpResponseServerError('权限分配错误'+ss)
@csrf_exempt
def out_org_common(request):
    try:
        postdata = request.POST.get('data')
        
        porgdata = json.loads(postdata)
        
        try:
            username = settings.DATABASES['default']['USER']
            password = settings.DATABASES['default']['PASSWORD']
            host = settings.DATABASES['default']['HOST']
            name = settings.DATABASES['default']['NAME']
            db = cx_Oracle.connect(username,password,'%s/%s'%(host,name))
        except:
            return  HttpResponseServerError('数据库连接错误')
       
        with transaction.commit_on_success():  
            
              
            for one in porgdata:
                orgtable=TabBdataCommonOrg()
               
                orgtable.orgname =one['orgname']
                orgtable.orgid =one['orgid']
                orgtable.orgcode =one['orgcode']
                orgtable.orglevel =one['orglevel']
                orgtable.parentorgid =one['parentorgid']
           
                orgtable.orgseq =one['orgseq']
                orgtable.orgtype =one['orgtype']
                orgtable.orgaddr =one['orgaddr']
                orgtable.zipcode =one['zipcode']
                orgtable.manaposition =one['manaposition']
            
                orgtable.managerid =one['managerid']
                orgtable.orgmanager =one['orgmanager']
                orgtable.linkman =one['linkman']
                orgtable.linktel =one['linktel']
                orgtable.email =one['email']
            
                orgtable.weburl =one['weburl']
                orgtable.startdate =one['startdate']
                orgtable.enddate =one['enddate']
                orgtable.status =one['status']
                orgtable.area =one['area']
            
                orgtable.createtime =one['createtime']
                orgtable.lastupdate =one['lastupdate']
                orgtable.sortno =one['sortno']
                orgtable.isleaf =one['isleaf']
                orgtable.subcount =one['subcount'] 
            
                orgtable.remark =one['remark'] 
            
                   
                
            
                oc=OrgDic.objects.all()
                orgdictab=OrgDic()
                orgdictab.orgid=one['orgcode']
                orgdictab.orgname=one['orgname']
                orgdictab.orgcode=one['org_dic']
                orgtable.save()
                orgdictab.save()
                #保存自己对自己的操作权限
                orgown=TabBdataOrgPrivileges()
                orgown.parentorgid=one['orgcode']
                orgown.orgid=one['orgcode']
                orgown.save()
                    
                #经纬度
            #orgtable.longitude =one['longitude'] 
            #orgtable.latitude =one['latitude']   
            
        return HttpResponse('ok')
    except:
        transaction.rollback()
        ss = traceback.format_exc()
        traceback.print_exc()
        return  HttpResponseServerError('新增单位错误'+ss)


@csrf_exempt
def out_exa_user(request):
    try:
        postdata = request.POST.get('data')
        #orgcode=request.GET.get('orgname')
        porgdata = json.loads(postdata)
        get_orgcode=request.GET.get('orgname')
        try:
            username = settings.DATABASES['default']['USER']
            password = settings.DATABASES['default']['PASSWORD']
            host = settings.DATABASES['default']['HOST']
            name = settings.DATABASES['default']['NAME']
            db = cx_Oracle.connect(username,password,'%s/%s'%(host,name))
        except:
            return  HttpResponseServerError('数据库连接错误')
       
        with transaction.commit_on_success():
                 
            for one in porgdata:
                        
                orgtable=OdsUserOrgInfo()
                orgtable.opertime=now()
                orgtable.issyn='N'
            
                orgtable.userid =one['userid']
                orgtable.usercode =one['usercode']
                orgtable.password =one['password']
                orgtable.invaldate =one['invaldate']
                orgtable.username =one['username']
           
                orgtable.authmode =one['authmode']
                orgtable.status =one['status']
                orgtable.unlocktime =one['unlocktime']
                orgtable.menutype =one['menutype']
                orgtable.lastlogin =one['lastlogin']
            
                orgtable.errcount =one['errcount']
                orgtable.startdate =one['startdate']
                orgtable.enddate =one['enddate']
                orgtable.validtime =one['validtime']
                orgtable.maccode =one['maccode']
            
                orgtable.ipaddress =one['ipaddress']
                orgtable.email =one['email']
                orgtable.mesid =one['mesid']
                orgtable.initinfoprovider =one['initinfoprovider']
                orgtable.ad_flag =one['ad_flag']
            
                orgtable.orgcode =get_orgcode
                
                user_org=TabBdataCommonOrg.objects.get(orgcode=get_orgcode)
                get_orgname=user_org.orgname
                orgtable.orgname =get_orgname
              
                orgtable.save()
            #调用存储过程
        cursor = db.cursor()
            #spcodeSQL = "select in_out_record_gen('%s','%s','%s') from dual"%(userdeptid,"A","")
        #spcodeSQL = "TESTPRO"
        spcodeSQL = "SYN_USER_PRO"
        #ret=cursor.callproc(spcodeSQL)
        cursor.callproc(spcodeSQL)
        cursor.close()
        db.close()
        #return   ret
        '''cursor = db.cursor()
        result_list = cursor.callproc("TESTPRO")
        data=cursor.fetchall()
        
        for row in cursor.fetchall():
            print row[0]
            cursor.nextset()
        db.connection.commit()
        cursor.close()
        db.close()'''
            
        return HttpResponse('ok')
    except:
        transaction.rollback()
        ss = traceback.format_exc()
        traceback.print_exc()
        return  HttpResponseServerError('权限分配错误'+ss)


def get_sp_data(request):
    userdepts = ViewBdataCommonUserOrg.objects.filter(usercode=request.user.username)
    alldeptids = []
    for dept in userdepts:
        depts = ViewBdataCommonOrg.objects.filter(parentorgid = dept.orgid)
        for de in depts:
            alldeptids.append(de.orgid)
    allsp = TabBdataFacSpInfo.objects.filter(amount__gt=0).filter(orgid__in=alldeptids)
    rows = []
    for sp in allsp:
        factorydatestr = ""
        effectivedatestr = ""
        spvaluestr = ""
        totalvalue = ""
        if sp.factorydate:
            factorydatestr = sp.factorydate.strftime('%Y-%m-%d')
        if sp.effectivedate:
            effectivedatestr = sp.effectivedate.strftime('%Y-%m-%d')
        if sp.spvalue:
            spvaluestr = float(sp.spvalue)
        if sp.amount and sp.spvalue:
            totalvalue = spvaluestr * float(sp.amount)
        spinfo = {"spencode": sp.encode,"spname": sp.spname,"totalvalue":totalvalue,
                  "spmodel": sp.spmodel,"spserialnumbe": sp.spserialnumbe,
                  "amount": sp.amount,"unit": sp.unit,"goodslocationcode": sp.goodslocationcode,
                  "spvalue": spvaluestr,"supplier": sp.supplier,"manufacturers": sp.manufacturers,
                  "specification": sp.specification,"qualification": sp.qualification,
                  "factorydate": factorydatestr,"effectivedate": effectivedatestr,
                  "spstatus": sp.spstatus,"remark1": sp.remark1,"source": sp.source,"emspid": sp.emspid
                  }
        rows.append(spinfo)
    allspdata = {"total":len(allsp),"rows":rows}
    response = HttpResponse(json.dumps(allspdata,ensure_ascii = False),content_type="application/json")
    return response

def get_org_data(request):
    '''userdepts = ViewBdataCommonUserOrg.objects.filter(usercode=request.user.username)
    alldeptids = []
    for dept in userdepts:
        depts = ViewBdataCommonOrg.objects.filter(parentorgid = dept.orgid)
        for de in depts:
            alldeptids.append(de.orgid)
    allsp = TabBdataFacSpInfo.objects.filter(amount__gt=0).filter(orgid__in=alldeptids)
    rows = []
    for sp in allsp:
        factorydatestr = ""
        effectivedatestr = ""
        spvaluestr = ""
        totalvalue = ""
        if sp.factorydate:
            factorydatestr = sp.factorydate.strftime('%Y-%m-%d')
        if sp.effectivedate:
            effectivedatestr = sp.effectivedate.strftime('%Y-%m-%d')
        if sp.spvalue:
            spvaluestr = float(sp.spvalue)
        if sp.amount and sp.spvalue:
            totalvalue = spvaluestr * float(sp.amount)'''
    pagesize=request.GET.get('rows')
    page=request.GET.get('page')
    parentorg=request.GET.get('parentorg')
    pnum=json.loads(page)
    psize=json.loads(pagesize)
    rows=[]
    selectorgcodes=[]
    if parentorg:        
        parorg=json.loads(parentorg)
        orgs=TabBdataCommonOrg.objects.all()
        for oneorg in orgs:
            if int(oneorg.orgcode) !=parorg:
                orgselected=TabBdataOrgPrivileges.objects.filter(parentorgid=parorg)
                for selectorg in orgselected:
                   selectorgcodes.append(selectorg.orgid)
                isSelect=False
                if oneorg.orgcode in selectorgcodes:
                    isSelect=True            
            
                orginfo={"orgname":oneorg.orgname,"orgcode":oneorg.orgcode,"isSelect":isSelect}
                rows.append(orginfo)
        alldatas={"total":len(rows),"rows":rows}
        response=HttpResponse(json.dumps(alldatas,ensure_ascii=False),content_type="application/json")
        return response
    else :
        
        listend=pnum*psize
        if pnum>1:
            liststart= (pnum-1) *  psize      
        else :
            liststart=0        
        allorg=TabBdataCommonOrg.objects.all()    
        for oneorg in allorg:        
        #oids=OrgDic.objects.all()
            orgdic=OrgDic.objects.get(orgid=oneorg.orgcode)
            orginfo={"orgname":oneorg.orgname,"org_order":oneorg.org_order,"org_dic":orgdic.orgcode ,"orgcode":oneorg.orgcode}
        #orginfo={"orgname":oneorg.orgname,"org_order":oneorg.org_order }
            rows.append(orginfo)    
        allspdata = {"total":len(allorg),"rows":rows[liststart:listend]}
        response = HttpResponse(json.dumps(allspdata,ensure_ascii = False),content_type="application/json")
        return response

def get_org_data_more(request):
    '''userdepts = ViewBdataCommonUserOrg.objects.filter(usercode=request.user.username)
    alldeptids = []
    for dept in userdepts:
        depts = ViewBdataCommonOrg.objects.filter(parentorgid = dept.orgid)
        for de in depts:
            alldeptids.append(de.orgid)
    allsp = TabBdataFacSpInfo.objects.filter(amount__gt=0).filter(orgid__in=alldeptids)
    rows = []
    for sp in allsp:
        factorydatestr = ""
        effectivedatestr = ""
        spvaluestr = ""
        totalvalue = ""
        if sp.factorydate:
            factorydatestr = sp.factorydate.strftime('%Y-%m-%d')
        if sp.effectivedate:
            effectivedatestr = sp.effectivedate.strftime('%Y-%m-%d')
        if sp.spvalue:
            spvaluestr = float(sp.spvalue)
        if sp.amount and sp.spvalue:
            totalvalue = spvaluestr * float(sp.amount)'''
    allorg=ViewBdataSpmExaOrg.objects.all()
    rows=[]
    for oneorg in allorg:
        orginfo={"orgid":oneorg.orgid,
                 "orgcode":oneorg.orgcode,
                 "orgname":oneorg.orgname,
                 "orglevel":oneorg.orglevel,
                 "parentorgid":oneorg.parentorgid,
                 "orgseq":oneorg.orgseq,
                 "orgtype":oneorg.orgtype,
                 "orgaddr":oneorg.orgaddr,
                 "zipcode":oneorg.zipcode,
                 "manaposition":oneorg.manaposition,
                 "managerid":oneorg.managerid,
                 "orgmanager":oneorg.orgmanager,
                 "linkman":oneorg.linkman,
                 "linktel":oneorg.linktel,
                 "email":oneorg.email,
                 "weburl":oneorg.weburl,
                 "startdate":oneorg.startdate,
                 "enddate":oneorg.enddate,
                 "status":oneorg.status,
                 "area":oneorg.area,
                 "createtime":oneorg.createtime,
                 "lastupdate":oneorg.lastupdate,
                 "sortno":oneorg.sortno,
                 "isleaf":oneorg.isleaf,
                 "subcount":oneorg.subcount,
                 "remark":oneorg.remark,
                 
                 #"org_dic":"",
                # "longitude":"",
                 #"latitude":"",
        
                 
                  }
        rows.append(orginfo)
      
    allspdata = {"total":len(allorg),"rows":rows}
    response = HttpResponse(json.dumps(allspdata,ensure_ascii = False),content_type="application/json")
    return response
#从额外试图中提取用户信息（usercode，username,orgname）
def get_exa_user(request):
   
    
    
    allorg=viewBdataSpmExaUser.objects.all()
    
    rows=[]
    for oneorg in allorg:
        orginfo={"userid":oneorg.userid,
                 "usercode":oneorg.usercode,
                 "password":oneorg.password,
                 "invaldate":oneorg.invaldate,
                 "username":oneorg.username,
                 "authmode":oneorg.authmode,
                 "status":oneorg.status,
                 "unlocktime":oneorg.unlocktime,
                 "menutype":oneorg.menutype,
                 "lastlogin":oneorg.lastlogin,
                 "errcount":oneorg.errcount,
                 "startdate":oneorg.startdate,
                 "enddate":oneorg.enddate,
                 "validtime":oneorg.validtime,
                 "maccode":oneorg.maccode,
                 "ipaddress":oneorg.ipaddress,
                 "email":oneorg.email,
                 "mesid":oneorg.mesid,
                 "initinfoprovider":oneorg.initinfoprovider,
                 "ad_flag":oneorg.ad_flag,
                 "orgname":oneorg.orgname,
                 "orgcode":oneorg.orgcode,
                  }
        rows.append(orginfo)
      
    allspdata = {"total":len(allorg),"rows":rows}
    response = HttpResponse(json.dumps(allspdata,ensure_ascii = False),content_type="application/json")
    return response
@csrf_exempt
def get_user_data(request):
    
    
    comusers=ViewBdataCommonUserOrg.objects.all()
        
    rows=[]
    for onecomuser in comusers:
       # userorgid=ViewBdataCommonUserOrg.objects.get(usercode=onecomuser.usercode)
        #comorgname=TabBdataCommonOrg.objects.get(orgcode=onecomuser.usercode)
        userinfo={"usercode":onecomuser.usercode,
                "username":onecomuser.username,
                "orgname":onecomuser.orgname,
                }
    
        rows.append(userinfo)
        alluserdata={"total":len(comusers),"rows":rows}
    
        
            
    response = HttpResponse(json.dumps(alluserdata,ensure_ascii = False),content_type="application/json")
    return response

def get_select_user_data(request):
    
    '''data =request.POST.get('data')
    usrseldata=json.loads(data)
    sel=usrseldata['sel']'''
    sel=request.GET.get('sel')
    if sel:
       # orgcode=request.GET().get('sel')
        oneorg=TabBdataCommonOrg.objects.get(orgcode=sel)
        comusers=ViewBdataCommonUserOrg.objects.filter(orgname=oneorg.orgname)
        
    else :
        comusers=ViewBdataCommonUserOrg.objects.all()
        
    rows=[]
    for onecomuser in comusers:
       # userorgid=ViewBdataCommonUserOrg.objects.get(usercode=onecomuser.usercode)
        #comorgname=TabBdataCommonOrg.objects.get(orgcode=onecomuser.usercode)
        userinfo={"usercode":onecomuser.usercode,
                "username":onecomuser.username,
                "orgname":onecomuser.orgname,
                }
    
        rows.append(userinfo)
        alluserdata={"total":len(comusers),"rows":rows}
    
        
            
    response = HttpResponse(json.dumps(alluserdata,ensure_ascii = False),content_type="application/json")
    return response


def logout_view(request):
    # 注销
    
    current_site = get_current_site(request)
    logout(request)
    return HttpResponseRedirect('http://'+current_site+'/portal/')
def get_org_info():
    info_list = []
    alldept = TabBdataCommonOrg.objects.all()
    for dept in alldept:
        str = (dept.orgid,dept.orgname)
        info_list.append(str)
    return info_list
def my_custom_page_not_found_view(request):
    return render_to_response('spm/404page.html')
def my_custom_error_view(request):
    return render_to_response('spm/500page.html')
@csrf_exempt
def Manage_User(request):
    if request.GET.get('usercode') and request.user:
        if not comparesessionuser(request.GET.get('usercode'),request.user,request):
            return HttpResponseRedirect('/spm')
    try:
        currentuser = TabBdataCommonUser.objects.get(usercode = request.user.username)
    except TabBdataCommonUser.DoesNotExist:
        return  HttpResponseServerError('当前登录用户不存在')
    userdeptid = ViewBdataCommonUserOrg.objects.filter(usercode=request.user.username).order_by('orglevel').first().orgid
    try:
        username = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        host = settings.DATABASES['default']['HOST']
        name = settings.DATABASES['default']['NAME']
        db = cx_Oracle.connect(username,password,'%s/%s'%(host,name))
    except:
        return  HttpResponseServerError('数据库连接错误')
    cursor = db.cursor()
    spcodeSQL = "select in_out_record_gen('%s','%s','%s') from dual"%(userdeptid,"A","")
    cursor.execute(spcodeSQL)
    recordid = cursor.fetchall()[0][0]
    return render_to_response('spm/manage_user.html',locals(), context_instance=RequestContext(request))
    
def Manage_Fac(request):
    
    return
def Manage_Cat(request):
    
    return 
def Manage_Org(request):
    if request.GET.get('usercode') and request.user:
        if not comparesessionuser(request.GET.get('usercode'),request.user,request):
            return HttpResponseRedirect('/spm')
    try:
        currentuser = TabBdataCommonUser.objects.get(usercode = request.user.username)
    except TabBdataCommonUser.DoesNotExist:
        return  HttpResponseServerError('当前登录用户不存在')
    userdeptid = ViewBdataCommonUserOrg.objects.filter(usercode=request.user.username).order_by('orglevel').first().orgid
    try:
        username = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        host = settings.DATABASES['default']['HOST']
        name = settings.DATABASES['default']['NAME']
        db = cx_Oracle.connect(username,password,'%s/%s'%(host,name))
    except:
        return  HttpResponseServerError('数据库连接错误')
    cursor = db.cursor()
    spcodeSQL = "select in_out_record_gen('%s','%s','%s') from dual"%(userdeptid,"A","")
    cursor.execute(spcodeSQL)
    recordid = cursor.fetchall()[0][0]
    return render_to_response('spm/manage_org.html',locals(), context_instance=RequestContext(request))
    


