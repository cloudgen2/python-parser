#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from  __future__ import print_function
from datetime import datetime, timedelta
from argparse import ArgumentParser
from datetime import datetime
import errno
import fileinput
import getpass
import inspect
import json
import os
from os import stat,listdir,path
from os.path import expanduser, isfile, join
import pwd
from pwd import getpwuid
import re
import shutil
import signal
import socket
import subprocess
from subprocess import Popen, PIPE
import sys
import time
from time import gmtime, strftime
try:
    from subprocess import DEVNULL
except:
    DEVNULL = open(os.devnull, 'w')
try:
    import ConfigParser as configparser
except:
    import configparser
try:
    basestring
except NameError:
    basestring = str
try:
    import requests
except:
    pass
try:
    raw_input
except NameError:
    raw_input = input

Ditu_BASE_VERSION=22
import hashlib 
class DituColor:
    INVERT_GRAY='\033[40m'
    INVERT_RED='\033[41m'
    INVERT_GREEN='\033[42m'
    INVERT_AMBER='\033[43m'
    INVERT_BLUE='\033[44m'
    INVERT_ORCHID='\033[45m'
    INVERT_TURQUOISE='\033[46m'
    INVERT_WHITE='\033[47m'

    LIGHT_GRAY='\033[90m'
    LIGHT_RED='\033[91m'
    LIGHT_GREEN='\033[92m'
    LIGHT_AMBER='\033[93m'
    LIGHT_BLUE='\033[94m'
    LIGHT_ORCHID='\033[95m'
    LIGHT_TURQUOISE='\033[96m'
    WHITE='\033[97m'

    DARK_GRAY='\033[30m'
    DARK_RED='\033[31m'
    DARK_GREEN='\033[32m'
    DARK_AMBER='\033[33m'
    DARK_BLUE='\033[34m'
    DARK_ORCHID='\033[35m'
    DARK_TURQUOISE='\033[36m'
    LIGHT_GRAY='\033[37m'

    BOLD='\033[1m'
    ITALICS='\033[3m'
    FLASHING='\033[5m'
    UNDERLINE='\033[4m'
    END='\033[0m'

class DituCode:
    DEBUG=100
    START=101
    ELAPSE=102
    EXEC=103
    SET=104
    APPEND=105
    REGEX_COMPILE=106
    SHELL=107
    CONFIG_LOADED=108
    SET_CONFIG=109
    ADD_SECTION=110
    DONE=111
    LIB_NOT_FOUND=112
    OK=200
    CREATED=201
    GIT_SUCCESS=203
    INSTALLED=204
    DituObj=300
    APP_DituObj=302
    TEST_RESULT=303
    GENERAL_ERROR=500
    TEST_FAILED=501
    SET_ERROR=502
    GIT_FAILED=503
    INSTALL_FAILED=504
    IMPORT_ERROR=505
    FILE_NOT_EXISTS=506
    FOLDER_NOT_EXISTS=507
    RECORD_NOT_FOUND=508
    CONFIG_VALUE_REQUIRED=521

class DituType:
    BOOL=0
    INT=1
    FLOAT=2
    STRING=3
    STR_DATE=4
    STR_EMAIL=5
    STR_FILENAME=6
    STR_IDENTIFIER=7
    STR_NAME=8
    STR_PATH=9
    STR_WORD=10
    STR_TAG=11

class DituMode:
    DEFAULT=1
    DEBUG=2
    TEST=3
    GEN_TEST=4

class DituObj(object):
    __data__=dict()
    __debug_start__=False
    __isDebug__=False
    __log__     =''
    __mode__    =DituMode.DEFAULT
    __options__=''
    __previous_type__=''
    __regex__=dict()
    __startTime__=datetime.now()
    __test__=''

    def __coloredMessage(self,color=None):
        if color is None :
            if self.__message() == '':
                return ''
            else:
                return "%s%s%s" % (self.__coloredMessage_color,\
                    self.__message(),self.__coloredMessage_termination)
        else:
            if color == '' or not self.msgUseColor():
                self.__coloredMessage_color=''
                self.__coloredMessage_termination=''
            else:
                self.__coloredMessage_color=color
                self.__coloredMessage_termination= DituColor.END
            return self

    def __get__(self,x):
        if x in DituObj.__data__:
            if self.mode() == DituMode.GEN_TEST \
                and DituObj.__data__[x]['useRegexForTest'] \
                and DituObj.__data__[x]['regexString'] is not None \
                and DituObj.__data__[x]['regexString'] != '':
                return self.subEscape(DituObj.__data__[x]['regexString'],r"##\1")
            else:
                return DituObj.__data__[x]['value']
        else:
            raise Exception("Record in DituObj Not Found. You should Create Record before use.")

    def __header(self,color=None):
        if color is None:
            return "%s%s@%s::%s(%s) <%s> %s%s" % (self.__header_color,\
                self.username(),self.local(),self.appName(),self.versionHeader(),\
                self.pid(),self.code(),self.__header_termination)
        else:
            if color == '' or not self.msgUseColor():
                self.__header_color=''
                self.__header_termination=''
            else:
                self.__header_color=color
                self.__header_termination=DituColor.END
        return self

    def __message(self,x=None):
        return self.query('__message' ,x)

    def __previousType(self,preType=None):
        if preType is None:
            return DituObj.__previous_type__
        else:
             DituObj.__previous_type__=preType
        return self

    def __tag(self,x=None):
        return self.query('__tag',x)

    def __tagMsg(self,color=None,outterColor=None):
        if color is None:
            if self.__tag() == '' or not self.msgUseColor():
                return ': '
            else:
                return "%s[%s%s%s%s%s]:%s " % (self.__tagMsg_outterColor,\
                    self.__tagMsg_termination,self.__tagMsg_color,\
                    self.__tag(),self.__tagMsg_termination,\
                    self.__tagMsg_outterColor,self.__tagMsg_termination)
        else:
            if color == '':
                self.__tagMsg_color=''
                self.__tagMsg_outterColor=''
                self.__tagMsg_termination=''
            else:
                self.__tagMsg_color=color
                self.__tagMsg_outterColor=outterColor
                self.__tagMsg_termination= DituColor.END
            return self

    def __timeMsg(self,color=None):
        if color is None:
            return "%s%s%s" % (self.__timeMsg_color,self.now()[0],\
                self.__timeMsg_termination)
        else:
            if color == '' or not self.msgUseColor():
                self.__timeMsg_color=''
                self.__timeMsg_termination=''
            else:
                self.__timeMsg_color=color
                self.__timeMsg_termination= DituColor.END
            return self

    def __set__(self,name,value,line,previousLine):
        if name in DituObj.__data__:
            if DituObj.__data__[name]['value'] != value:
                if DituObj.__data__[name]['type'] == DituType.STRING:
                    if not isinstance(value,basestring):
                        raise Exception("%s using string type" % name)
                    value=value.strip()
                elif DituObj.__data__[name]['type'] == DituType.INT:
                    if not isinstance(value,int):
                        raise Exception("%s using int type" % name)
                DituObj.__data__[name]['value']=value
                if DituObj.__data__[name]['original'] is None \
                        or DituObj.__data__[name]['original'] == '':
                    DituObj.__data__[name]['original']=value
                if DituObj.__data__[name]['debug']:
                    self.debug_msg_set(name,value,\
                        previousLine,line)
            return self
        else:
            raise Exception("Record in DituObj Not Found. You should Create Record before use.")

    def DituBaseVersion(self,x=None):
        return self.query('DituBaseVersion',x)

    def appName(self,x=None):
        return self.query('appName',x)

    def appendLog(self,x):
        if not isinstance(x,basestring):
            return self
        x=x.strip()
        if x != "":
            if DituObj.__log__ != '':
                DituObj.__log__='%s\n%s' % (DituObj.__log__,x)
            else:
                DituObj.__log__=x
        return self

    def appendTestPlan(self,x):
        if not isinstance(x,basestring):
            return self
        x=x.strip()
        if x != "":
            if DituObj.__test__ != '':
                DituObj.__test__='%s\n%s' % (DituObj.__test__,x)
            else:
                DituObj.__test__=x
        return self

    def argumentOption(self,shortOption=None,dest=None,action="store",\
        help="",longOption=""):
        if shortOption is None:
            result=''
            for i in sorted(self.__opt__):
                if result != '':
                    result=result + '\n'
                result="%s-%s --%s" % (result,i,\
                    self.__opt__[i]['longOption'])
            return result
        else:
            if dest is not None:
                if shortOption not in self.__opt__:
                    self.__opt__[shortOption]=dict()
                if longOption == '':
                    longOption=self.splitHypen(dest)
                if help == '':
                    help="Set the value of %s" % dest
                self.__opt__[shortOption]['longOption']=longOption
                self.__opt__[shortOption]['action']=action
                self.__opt__[shortOption]['dest']=dest
                self.__opt__[shortOption]['help']=help
                self.__opt__[shortOption]['flushed']=False
            return self

    def author(self,x=None):
        return self.query('author',x)

    def splitHypen(self,name):
        s1=self.subFirstCap(r'\1-\2',name)
        return self.subAllCapRegex(r'\1-\2',s1).lower()

    def code(self,x=None):
        return self.query('code',x)

    def command(self,name=None,desc=''):
        if name is None:
            result=''
            for i in sorted(self.__cmd__):
                if result != '':
                    result=result + ', '
                result=result + i
            return result
        else:
            if name not in self.__cmd__:
                self.__cmd__[name]=desc
            else:
                raise Exception("Command %s has been set already!" % name)
        return self

    def createItem(self,name,type='',isOption=False,debug=True,\
        logable=True,useRegexForTest=False, default=None,\
        regex=None):
        if type=='':
            type=self.__previousType()
        self.__previousType(type)
        if regex is not None:
            regexString=regex
            regex=re.compile(regex)
        if name not in DituObj.__data__:
            regexString=''
            if type >= DituType.STRING:
                if default is None:
                    default=''
                if regex is None:
                    regexString='.+'
            elif type == DituType.BOOL:
                if default is None:
                    default=False
                if regex is None:
                    regex='(True|False)'
            elif type == DituType.INT:
                if default is None:
                    default=0
                if regex is None:
                    regexString='\-?\d+'
            elif type == DituType.FLOAT:
                if default is None:
                    default=0.0
                if regex is None:
                    regexString='\-?\d+(\.\d+)?'
            if type == DituType.STR_DATE:
                if default is None:
                    default=strftime("%Y-%m-%d",gmtime())
                if regex is None:
                    regex=re.compile('\d{4}-\d{2}-\d{2}')
                    regexString='\d{4}-\d{2}-\d{2}'
            DituObj.__data__[name]=dict()
            DituObj.__data__[name]['type'] =type
            DituObj.__data__[name]['debug'] =debug
            DituObj.__data__[name]['logable'] =logable
            DituObj.__data__[name]['useRegexForTest'] =useRegexForTest
            DituObj.__data__[name]['default'] =default
            DituObj.__data__[name]['original'] =default
            DituObj.__data__[name]['value'] =default
            DituObj.__data__[name]['regex'] =regex
            DituObj.__data__[name]['isOption'] =isOption
            DituObj.__data__[name]['regexString'] =regexString
        return self

    def critical_msg(self,msg,tag='',code=None):
        if code is None:
            code=DituCode.GENERAL_ERROR
        self.__tag(tag).__message(msg).code(code) \
            .__timeMsg(DituColor.BOLD + DituColor.ITALICS + \
            DituColor.DARK_AMBER) \
            .__header(DituColor.BOLD + DituColor.DARK_AMBER) \
            .__coloredMessage(DituColor.ITALICS + DituColor.LIGHT_AMBER) \
            .__tagMsg(DituColor.FLASHING + DituColor.LIGHT_RED,\
            DituColor.LIGHT_AMBER)
        self.print("%s" % (self.formattedLog()))
        return self

    def debug(self,x=None):
        if x is not None:
            if isinstance(x,bool):
                DituObj.__isDebug__=x
            return self
        else:
            return DituObj.__isDebug__

    def debug_mode_start(self):
        if not DituObj.__debug_start__ :
            self.debug_msg("Debug Mode","STARTED",DituCode.START)
        DituObj.__debug_start__=True
        return self

    def debug_msg(self,msg,tag='',code=100,line=None,\
        debug=None):
        if debug is None:
            debug=self.debug()
        if not debug:
            return self
        if line is None:
            line=self.previousLine()
        if tag is not None:
            self.__tag(tag)
        self.__message("#%s %s" % (line,msg)).code(code) \
            .__timeMsg(DituColor.BOLD + DituColor.ITALICS + \
            DituColor.DARK_ORCHID) \
            .__header(DituColor.BOLD + DituColor.DARK_ORCHID) \
            .__coloredMessage(DituColor.ITALICS + DituColor.LIGHT_ORCHID) \
            .__tagMsg(DituColor.LIGHT_GRAY,DituColor.LIGHT_ORCHID)
        self.print("%s" % (self.formattedLog()))
        return self

    def debug_msg_elapse(self,allowDebug=None,line=None):
        if allowDebug is None and self.arg.command == 'test':
            allowDebug=True
        if line is None:
            line=self.previousLine()
        self.debug_msg("The time elapse: %s" % self.elapse(),'ELAPSE',\
            DituCode.ELAPSE,line,allowDebug)
        return self

    def debug_msg_set(self,name,value,previousLine=None,line=None,code=None):
        if code is None:
            code=DituCode.SET
        if previousLine is None:
            previousLine=self.previousLine()
        if line is None:
            line=self.line()
        self.debug_msg('%s="%s" (line: #%s)' % (name,value,\
            line),'SET',code ,previousLine)
        return self

    def echo(self,x):
        if isinstance(x,basestring):
            result=self.subEscaped(x)
            self.print(result)
            if self.mode() == DituMode.GEN_TEST:
                self.appendTestPlan("%s" % result)
            elif self.mode() == DituMode.TEST:
                self.appendLog("%s" % result)
        elif isinstance(x,list):
            self.print(x[0])
            if self.mode() == DituMode.GEN_TEST:
                self.appendTestPlan("%s" % x[1])
            elif self.mode() == DituMode.TEST:
                self.appendLog("%s" % x[0])
        else:
            self.print(x['value'])
            if x['useRegexForTest'] and self.mode() == DituMode.GEN_TEST:
                self.appendTestPlan("%s" % x['regexString'])
            else:
                self.appendLog("%s" % x['value'])
        return self

    @staticmethod
    def elapse():
        return datetime.now() - DituObj.__startTime__

    def error(self,x=None):
        return self.query('error',x)

    def errorType(self,x=None):
        if x:
            self.query('errorType',x) \
                .error(True) \
                .critical_msg("%s Error. Program trminated at (line #%d)"\
                % (x,self.previousLine()),\
                "ABORTED",DituCode.GENERAL_ERROR)\
                .debug_msg_elapse(self.line(),True)
        else:
            return self.query('errorType')

    def flushOptions(self):
        for shortOption in sorted(self.__opt__):
            if not self.__opt__[shortOption]['flushed'] :
                longOption=self.__opt__[shortOption]['longOption']
                action=self.__opt__[shortOption]['action']
                dest=self.__opt__[shortOption]['dest']
                help=self.__opt__[shortOption]['help']
                self.parser.add_argument("-" + shortOption,'--' + longOption,\
                    action=action,dest=dest,help=help)
                self.__opt__[shortOption]['flushed']=True
        return self

    def formattedLog(self):
        return "%s %s %s\n  %s" % (self.__timeMsg(),self.__header(),\
            self.__tagMsg(),self.__coloredMessage())

    def info_msg(self,msg,tag='',code=None):
        if code is None:
            code=DituCode.DituObj
        if tag is not None:
            self.__tag(tag)
        self.__message(msg).code(code) \
            .__timeMsg(DituColor.BOLD + DituColor.ITALICS + \
            DituColor.DARK_BLUE) \
            .__header(DituColor.BOLD + DituColor.DARK_BLUE) \
            .__coloredMessage(DituColor.ITALICS + DituColor.LIGHT_BLUE) \
            .__tagMsg(DituColor.LIGHT_AMBER,DituColor.LIGHT_BLUE)
        self.print("%s" % (self.formattedLog()))
        return self

    def item(self,x):
        if x not in DituObj.__data__:
            raise Exception("Record in DituObj Not Found. You should Create Record before use.")
        return DituObj.__data__[x]

    def itemDefault(self,name,value=None):
        if name in DituObj.__data__:
            if value is None:
                return DituObj.__data__[name]['default']
            elif DituObj.__data__[name]['regex'] is not None:
                if not isinstance(value,basestring):
                    raise Exception("Default value error.")
                value=value.strip()
                if DituObj.__data__[name]['regex'].sub('',value).strip() != '':
                    raise Exception("Default value not match regex.")
            DituObj.__data__[name]['value'] =value
            return self
        else:
            raise Exception("Record in DituObj Not Found. You should Create Record before use.")

    def itemOriginal(self,x):
        if x in DituObj.__data__:
            if DituObj.__data__[x]['original'] is not None and \
                DituObj.__data__[x]['original'] != '':
                return DituObj.__data__[x]['original']
            else:
                return DituObj.__data__[x]['value']
        else:
            raise Exception("Record in DituObj Not Found. You should Create Record before use.")

    def itemRegex(self,name,regex=None):
        if name not in DituObj.__data__:
            raise Exception("Record in DituObj Not Found. You should Create Record before use.")
        if regex is None:
            return DituObj.__data__[name]['regex']
        else:
            DituObj.__data__[name]['regexString']=regex
            DituObj.__data__[name]['regex']=re.compile(regex)
        return self

    def itemRegexString(self,x):
        if x not in DituObj.__data__:
            raise Exception("Record in DituObj Not Found. You should Create Record before use.")
        return self.subEscape(DituObj.__data__[x]['regexString'],r"##\1")

    def lastUpdate(self,x=None):
        return self.query('lastUpdate',x)

    @staticmethod
    def line():
        return inspect.currentframe().f_back.f_lineno

    def listCommands(self):
        return "The list of commands: %s" % (self.command())

    def local(self,x=None):
        return self.query('local',x)

    def log(self):
        return DituObj.__log__

    def majorVersion(self,x=None):
        if x is not None:
            self.query('version',"%s.%s" % (x,self.minorVersion()))
        return self.query('majorVersion',x)

    def message(self,x=None):
        return self.query('message',x)

    def minorVersion(self,x=None):
        if x is not None:
            self.query('version',"%s.%s" % (self.majorVersion(),x))
        return self.query('minorVersion',x)

    def msgUseColor(self,x=None):
        return self.query('msgUseColor',x)

    def mode(self,value=None):
        if value is None:
            return DituObj.__mode__
        elif not isinstance(value,int):
            raise Exception("Invalid Mode setting")
        elif value >= DituMode.DEFAULT or value <= DituMode.GEN_TEST:
            DituObj.__mode__=value
            if value == DituMode.DEBUG or value == DituMode.GEN_TEST:
                self.debug(True)
        else:
            raise Exception("Invalid Mode setting")
        return self

    def nextVersion(self):
        return [ "%s.%s" % (self.majorVersion(),self.minorVersion() + 1),
            "\d+\.\d+"]

    def notDefined(self,item):
        return self.critical_msg("%s is not defined" % item,"%s UNKOWN" % item.Upper())
    
    @staticmethod
    def now():
        return [str(datetime.now()),"\d{4}-\d{2}-\d{2} \d{2}\:\d{2}\:\d{2}\.\d{6}"]

    def options(self):
        return DituObj.__options__

    def originalName(self):
        return self.itemOriginal('appName')

    def parseShell(self,text):
        result=self.regex("shellSpace").sub("%20",text)
        result=self.regex("paramParser").findall(result)
        for i,item in enumerate(result):
            result[i]=self.regex("urlSpace").sub(" ",self.regex("quote")\
                .sub('',item))
        return result

    @staticmethod
    def pid():
        return os.getpid()

    @staticmethod
    def prePreviousLine():
        return inspect.currentframe().f_back.f_back.f_back.f_lineno

    @staticmethod
    def previousLine():
        return inspect.currentframe().f_back.f_back.f_lineno

    @staticmethod
    def print(msg):
        print("%s" % msg)

    def query(self,name,value=None):
        if value is None:
            return self.__get__(name)
        else:
            line=self.previousLine()
            previousLine=self.prePreviousLine()
            return self.__set__(name,value,line,previousLine)

    def regex(self,name,value=None):
        if value is not None:
            DituObj.__regex__[name]=re.compile(value)
            return self
        elif self.regexExists(name):
            return DituObj.__regex__[name]
        else:
            self.critical_msg("Key not found in DituObj.","REQUIRED",DituCode.GENERAL_ERROR)
            raise Exception("Key not found in DituObj. You should Create Record before use.")

    def regexExists(self,x):
        return x in DituObj.__regex__

    def safe_msg(self,msg,tag='',code=None):
        if code is None:
            code=DituCode.OK
        if tag is not None:
            self.__tag(tag)
        self.__message(msg).code(code)
        result="%s %s%s" % (self.code(),self.__tagMsg(),self.__coloredMessage())
        self.__timeMsg(DituColor.BOLD + DituColor.ITALICS + \
            DituColor.DARK_TURQUOISE) \
            .__header(DituColor.BOLD + DituColor.DARK_TURQUOISE) \
            .__coloredMessage(DituColor.ITALICS + DituColor.LIGHT_TURQUOISE) \
            .__tagMsg(DituColor.LIGHT_GREEN,DituColor.LIGHT_TURQUOISE)
        self.print("%s" % (self.formattedLog()))
        return self

    def subAllCapRegex(self,replaceBy,text):
        return self.regex("allCapRegex").sub(replaceBy,text)

    def subBrace(self,text,replaceBy=''):
        return self.regex("brace").sub(replaceBy,text)

    def subClassName(self,text,replaceBy=''):
        return self.regex("classname").sub(replaceBy,text)

    def subEscape(self,text,replaceBy=r"\\\1"):
        return self.regex("escape").sub(replaceBy,text)

    def subEscaped(self,text,replaceBy=r"\1"):
        return self.regex("escaped").sub(replaceBy,text)

    def subFirstCap(self,replaceBy,text):
        return self.regex("firstCap").sub(replaceBy,text)

    def getFirstInteger(self,text):
        return self.regex("firstInteger").sub(r"\1",text)

    def getDomain(self,text):
        return self.regex("domain_url").sub('',text)

    def tag(self,x=None):
        return self.query('tag',x)

    def testLogMessage(self,flush=True):
        if self.__message() == '':
            return ''
        self.__coloredMessage('').__tagMsg('')
        result="%s %s%s" % (self.code(),self.__tagMsg(),self.__coloredMessage())
        if flush:
            self.__tag('').__message('').code(0)
        return result

    def testPlan(self):
        return DituObj.__test__

    def trim(self,text,replaceBy=''):
        return self.regex("trim").sub(replaceBy,text)

    def useNextVersion(self,x=None):
        return self.query('useNextVersion',x)

    def useRegexForTest(self,name,action):
        if not isinstance(action,bool):
            raise Exception("You should boolean to set useRegexForTest.")
        if name not in DituObj.__data__:
            raise Exception("Record in DituObj Not Found. You should Create Record before use.")
        DituObj.__data__[name]['useRegexForTest']=action
        return self

    def userID(self):
        return [ os.getuid(),"\d+"]

    def username(self,x=None):
        return self.query('username',x)

    def version(self,x=None):
        if x is not None:
            ver=self.regex('integer').findall(x)
            if len(ver)>1:
                self.query('majorVersion',int(ver[0]))
                self.query('minorVersion',int(ver[1]))
        return self.query('version',x)

    def versionHeader(self):
        return self.version()

    def __init__(self):
        self.regex("firstCap",r'(.)([A-Z][a-z]+)') \
            .regex("allCapRegex",r'([a-z0-9])([A-Z])') \
            .regex("shellSpace",r"\\ ") \
            .regex("urlSpace",r"%20") \
            .regex("domain_url",r"^https?://|/.*$") \
            .regex('brace',r"[\[\]]") \
            .regex('classname',r"\([^\)]*\)|:") \
            .regex("trim",r"^[\s\n]+|[\s\n]+$") \
            .regex("escape",r"([\[\]\(\)\*\?\+\|\\])") \
            .regex("escaped",r"##\\?([\[\]\(\)\*\?\+\|\\])") \
            .regex("absPath",r"^\/([^\/]+\/|[^\/]+)*$") \
            .regex("firstInteger",r"[^\d]*(\d+).*") \
            .regex("integer",r"\d+") \
            .regex("quote",r"^[\"']|[\"']$") \
            .regex("paramParser",r"'[^'\"]*\"[^\"]*\"[^']*'|\"[^'\"]*'[^']*'[^\"]*\"|\"[^\"]*\"|'[^']*'|[^\s\\\"'\|]+|\|")
        self.__tagMsg_color=''
        self.__tagMsg_outterColor=''
        self.__tagMsg_termination=''
        self.__coloredMessage_color=''
        self.__coloredMessage_termination=''
        self.createItem('username',DituType.STRING) \
            .useRegexForTest('username',True) \
            .createItem('local') \
            .createItem('msgUseColor',DituType.BOOL) \
            .msgUseColor(True) \
            .createItem('appName',DituType.STRING,True) \
            .createItem('version') \
            .createItem('tag','',True) \
            .createItem('message','',True) \
            .createItem('__message','',False,False) \
            .createItem('__tag','',False,False) \
            .createItem('code',DituType.INT,False,False)
        self.__opt__=dict()
        self.__cmd__=dict()
        self.parser=ArgumentParser()
        self.arg=False
        self.createItem('regexName',DituType.STR_DATE) \
            .createItem('DituBaseVersion',DituType.INT) \
            .createItem('error',DituType.BOOL) \
            .createItem('errorType',DituType.STRING) \
            .DituBaseVersion(Ditu_BASE_VERSION)
        self.__DituObj_inited=False
        self.username(pwd.getpwuid(self.userID()[0])[ 0])
        self.local(socket.gethostname())
        self.__DituObj_inited=True
        self.createItem('lastUpdate',DituType.STR_DATE) \
            .useRegexForTest('lastUpdate',True) \
            .createItem('author',DituType.STRING) \
            .useRegexForTest('author',True) \
            .createItem('useNextVersion',DituType.BOOL) \
            .useNextVersion(True) \
            .createItem('majorVersion',DituType.INT) \
            .createItem('minorVersion')

class DituBase(DituObj):
    __configFileExists__=False
    __configFileChecked__=False
    __host_dict__=None
    __host_list__=None
    __host_record__=None
    __ip_dict__=None
    __here__=__file__
    __latest_version__=None
    __localhosts__=None
    __local_ip__=''
    __need_update__=False
    __originalPath__=os.getcwd()
    __tempFolder__=None
    __unique_host_list__=None

    def __process_host__(self):
        if DituBase.__unique_host_list__ is None:
            d={}
            if DituBase.__host_dict__ is None:
                DituBase.__host_dict__={}
            if DituBase.__host_record__ is None:
                DituBase.__host_record__={}
            if DituBase.__localhosts__ is None:
                DituBase.__localhosts__={}
            if DituBase.__ip_dict__ is None:
                DituBase.__ip_dict__={}
            with open('/etc/hosts') as f:
                lines=f.readlines()
                for line in lines:
                    if '#' in line:
                        pass
                    elif '::' in line:
                        pass
                    elif '127.0.0.1' in line:
                        temp=self.trim(line).split()
                        for dns in temp:
                            if dns!='127.0.0.1':
                                DituBase.__localhosts__[dns]=True
                            if 'jump-' in dns:
                                if not dns in DituBase.__host_record__:
                                    DituBase.__host_record__[dns]="%s\t%s" % (self.local_ip(),dns)
                                DituBase.__host_dict__[dns]=self.local_ip()
                                if self.local_ip() in DituBase.__ip_dict__:
                                    DituBase.__ip_dict__[self.local_ip()]="%s %s" %(DituBase.__ip_dict__[self.local_ip()],dns)
                                else:
                                    DituBase.__ip_dict__[self.local_ip()]=dns
                    elif '127.0.1.1' in line:
                        temp=self.trim(line).split()
                        for dns in temp:
                            if dns!='127.0.1.1':
                                DituBase.__localhosts__[dns]=True
                            if 'jump-' in dns:
                                if not dns in DituBase.__host_record__:
                                    DituBase.__host_record__[dns]="%s\t%s" % (self.local_ip(),dns)
                                DituBase.__host_dict__[dns]=self.local_ip()
                                if self.local_ip() in DituBase.__ip_dict__:
                                    DituBase.__ip_dict__[self.local_ip()]="%s %s" %(DituBase.__ip_dict__[self.local_ip()],dns)
                                else:
                                    DituBase.__ip_dict__[self.local_ip()]=dns
                    else:
                        temp=self.trim(line)
                        if temp != '':
                            splited_line=temp.split()
                            if len(splited_line) > 1:
                                d[splited_line[1]]=temp
                                for token in splited_line:
                                    ip=splited_line[0]
                                    if token != ip:
                                        first_dns=splited_line[1]
                                        if token == first_dns:
                                            DituBase.__host_record__[first_dns]="%s\t%s" % (ip,first_dns)
                                        else:                            
                                            DituBase.__host_record__[first_dns]="%s %s" % (DituBase.__host_record__[first_dns],token)
                                        DituBase.__host_dict__[token]=ip
                                        if ip in DituBase.__ip_dict__:
                                            DituBase.__ip_dict__[ip]="%s,%s" %(DituBase.__ip_dict__[ip],token)
                                        else:
                                            DituBase.__ip_dict__[ip]=token
            DituBase.__unique_host_list__=[]
            for k in sorted(d):
                DituBase.__unique_host_list__.append(k)
            if self.mode() == DituMode.DEBUG:
                self.info_msg("%s reocords found in /etc/hosts" % str(len(k)),"READING HOSTS")
        return self

    def __search_host__(self,user):
        if user not in self.__host_list__:
            self.__host_list__[user]=[]
        for host in self.unique_host_list():
            if self.check_remote_user(host,self.remote_root(),user):
                self.__host_list__[user].append(host)
        return self

    def __sudo_test__(self,msg='.'):
        if self.isSudo():
            return self
        self.clearStd().std(Popen(['sudo','-S','echo']+ msg.split(),\
            stdin=PIPE,stdout=PIPE,stderr=PIPE,universal_newlines=True)\
            .communicate('\n'))
        trial=0
        while self.stdout() != msg.strip() and trial < 3:
            sudoPassword=getpass.getpass('[sudo] password for %s: ' % self.username())
            self.clearStd().std(subprocess.Popen(['sudo','-S','echo']+ \
                msg.split(),stdin=PIPE,stdout=PIPE,stderr=PIPE,\
                universal_newlines=True).communicate("%s\n" % sudoPassword))
            trial=trial + 1
        if trial < 3:
            self.isSudo(True)
        return self.isSudo()

    def addArguments(self):
        return self.argumentOption("d","debug","store_true","Set debug mode")

    def addCommands(self):
        return self.command("info","")

    def addCommandArguments(self):
        return self.flushOptions() \
            .argumentOption('c','command','store',self.listCommands())\
            .flushOptions()

    def chdir(self,path):
        os.chdir(path)
        return self

    def checkConfigFile(self):
        if DituBase.__configFileChecked__:
            return self
        if self.isFile(self.configFile()):
            DituBase.__configFileExists__=True
            self.config=configparser.ConfigParser()
            self.config.read(self.configFile())
            if self.mode() == DituMode.GEN_TEST:
                self.debug_msg("Configuration file: /.##*",\
                "LOADED",DituCode.CONFIG_LOADED)
            else:
                self.debug_msg("Configuration file: %s" % (self.configFile()),\
                "LOADED",DituCode.CONFIG_LOADED)
        else:
            self.config=configparser.ConfigParser()
            DituBase.__configFileExists__=False
        DituBase.__configFileChecked__=True
        return self

    def check_remote_user(self,host,remote_root,user):
        self.remote_root_command("echo ~%s" % user,host,remote_root)
        rm_home=self.stdout()
        if self.mode()==DituMode.DEBUG:
            print("Home location for %s@%s using root:%s is %s" % (user,host,remote_root,rm_home))
        if self.stderr() != '':
            return False
        elif ("~" in rm_home or rm_home==''):
            return False
        else:
            return rm_home

    def check_update(self):
        v=self.latest_version()
        if DituBase.__need_update__:
            return "New version: %s Found!" % v 
        else:
            return "You are using the most updated version."

    def chmod(self,fileList,option="+x"):
        return self.shell("chmod %s %s" % (option,fileList))

    def clearStd(self):
        return self.stdout('').stderr('')

    def configSection(self,x=None) :
        return self.query('configSection',x)

    def configName(self,x=None):
        return self.query('configName',x)

    def configValue(self,x=None):
        return self.query('configValue',x)

    def configFilePath(self,x=None) :
        return self.query('configFilePath',x)

    def configFile(self,x=None):
        return self.query('configFile',x)

    def configFileExists(self):
        self.checkConfigFile()
        return DituBase.__configFileExists__

    def configPath(self,x=None):
        return self.query('configPath',x)

    def copy_to_user_local_bin(self):
        if self.fullPath()[0] != self.install_path():
            self.sudo_cp(self.fullPath()[0],self.install_path())
        else:
            self.info_msg("The current one has been installed to %s" % self.fullPath()[0],"INSTALLATION SKIPPED")
        return self

    def cp(self,source,dest):
        return self.shell("cp %s %s" % (source,dest))

    def create_user(self,uid,user,home):
        if not self.has_user(user):
            self.sudo_shell("sudo groupadd -g %s %s" % (uid,user))\
                .sudo_shell("sudo useradd -g %s -u %s -m -d %s -s /bin/bash %s" % (uid,uid,home,user))
        return self

    def create_hosts_file_temp(self,host):
        source='/tmp/hosts'
        c=["# Create Date: %s" % self.today(),"127.0.0.1 	localhost %s" % host,'']
        d=self.host_record()
        for k in sorted(d):
            if host in d[k]:
                splitted=self.trim(d[k]).split()
                if len(splitted)>2:
                    c.append(d[k].replace(host))
            else:
                c.append(d[k])
        c.append('')
        c.append('# The following lines are desirable for IPv6 capable hosts')
        c.append('::1 ip6-localhost ip6-loopback')
        c.append('fe00::0 ip6-localnet')
        c.append('ff00::0 ip6-mcastprefix')
        c.append('ff02::1 ip6-allnodes')
        c.append('ff02::2 ip6-allrouters')
        c.append('ff02::3 ip6-allhosts')
        c.append('')
        if self.isFile(source):
            self.sudo_rm(source)
        fp=open(source,"w+")
        fp.write('\n'.join(c))
        fp.close()
        return self

    def create_system_daemon(self,systemd,description,type,user,working_dir,command):
        self.create_system_daemon_temp(systemd,description,type,user,working_dir,command)
        self.sudo_mv("/tmp/%s" % systemd,"/etc/systemd/system/")
        return self

    def create_system_daemon_temp(self,systemd,description,type,user,working_dir,command):
        source="/tmp/%s" % systemd
        c=['[Unit]','Description=%s' % description,'','[Service]']
        c.append('Type=%s' % type)
        c.append('User=%s' % user)
        c.append('WorkingDirectory=%s' % working_dir)
        c.append('Environment="PATH=/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin"')
        c.append('ExecStart=%s' % command)
        c.append('')
        c.append('[Install]')
        c.append('WantedBy=multi-user.target')
        if self.isFile(source):
            self.sudo_rm(source)
        fp=open(source,"w+")
        fp.write('\n'.join(c))
        fp.close()
        return self

    @staticmethod
    def date():
        return [ strftime("%Y%m%d",gmtime()),"\d{8}"]

    def destination(self,x=None):
        return self.query('destination',x)

    @staticmethod
    def dirpath():
        return [ os.getcwd(),"(\/[^\/]+)+"]

    def download_host(self,x=None):
        return self.query('download_host',x)

    def download_url(self,x=None):
        return self.query('download_url',x)

    @staticmethod
    def findOwner(filename):
        return [ getpwuid(stat(filename).st_uid).pw_name,"[A-Za-z0-9_\.\-\s]+"]

    @staticmethod
    def fullPath():
        return [ path.abspath(DituBase.thisFile()),"(\/[^\/]+)+"]

    def has_user(self, user):
        return 'uid=' in self.shell('id %s' % user).stdout()

    def install_path(self):
        return "/usr/local/bin/%s"  % self.appName()

    def getConfig(self,section,name,warning=True):
        self.checkConfigFile()
        value=None
        if not self.config.has_section(section):
            try:
                self.config.add_section(section)
                self.debug_msg("%s (line: #%s)" % (section,\
                    self.previousLine()) ,"ADD SECTION",DituCode.ADD_SECTION)
            except:
                if warning:
                    self.critical_msg("Section: %s is not invalid" % (section),\
                        "ADD FAILED")
                self.error(True)
        if self.config.has_section(section):
            try:
                value=self.config.get(section,name)
            except:
                if warning:
                    self.critical_msg("config not found: %s" % (name),\
                        "FAILED")
                self.error(True)
        return value

    def here(self,here):
        DituBase.__here__=here
        return self

    @staticmethod
    def home():
        return expanduser("~")

    def host(self,x=None):
        if x is not None:
            if self.nslookup(x):
                self.query('host',x)
                self.debug_msg("after setting self.host()=%s" % self.query('host'))
                return self
            else:
                self.critical_msg("Cannot resolve host: %s" % x, "EXECUTION ERROR")
                self.error(True)
                return self
        else:
            self.debug_msg("getting self.host()=%s" % self.query('host'))
            return self.query('host')

    def host_dict(self):
        if DituBase.__host_dict__ is None:
            self.__process_host__()
        return DituBase.__host_dict__

    def host_list(self, user):
        if DituBase.__host_list__ is None:
            DituBase.__host_list__={}
        if user not in DituBase.__host_list__:
            self.__search_host__(user)
        return DituBase.__host_list__[user]

    def host_record(self):
        if DituBase.__host_record__ is None:
            self.__process_host__()
        return DituBase.__host_record__

    def info(self):
        msg1="%s version %s.%s by %s on %s" % (self.appName(),self.majorVersion(),\
            self.minorVersion(),self.author(),self.lastUpdate())
        msg2="DituBase v.%s" % self.DituBaseVersion()
        
        if len(sys.version.split('\n'))>1:
            msg3="Python %s" % sys.version.split('\n')[0]
            major=self.getFirstInteger(sys.version.split('\n')[0]).split('.')[0]
            msg4=self.subBrace(sys.version.split('\n')[1])
        elif len( sys.version.split('['))>1:
            msg3="Python %s" % sys.version.split('[')[0]
            major=self.getFirstInteger(sys.version.split('[')[0]).split('.')[0]
            msg4=self.subBrace(sys.version.split('[')[1])
        else:
            msg4=''
        msg5="%s" % self.check_update()
        msg6="Command for installation:" 
        if major =='3':      
            msg7="curl -fsSL %s | python3" % self.download_url()
        else:
            msg7="curl -fsSL %s | python" % self.download_url()
        starLine=[]
        space=[]
        space1=[]
        space2=[]
        space3=[]
        space4=[]
        space5=[]
        space6=[]
        space7=[]
        maxLen=len(msg1)
        if len(msg2) > maxLen :
            maxLen=len(msg2)
        if len(msg3) > maxLen :
            maxLen=len(msg3)
        if len(msg4) > maxLen :
            maxLen=len(msg4)
        if len(msg5) > maxLen :
            maxLen=len(msg5)
        if len(msg6) > maxLen :
            maxLen=len(msg6)
        if len(msg7) > maxLen :
            maxLen=len(msg7)
        for i in range(1,maxLen - len(msg1) + 1):
            space1.append(' ')
        msg1=msg1 + ''.join(space1)
        for i in range(1,maxLen - len(msg2)+ 1):
            space2.append(' ')
        msg2=msg2 + ''.join(space2)
        for i in range(1,maxLen - len(msg3) + 1):
            space3.append(' ')
        msg3=msg3 + ''.join(space3)
        for i in range(1,maxLen - len(msg4) + 1):
            space4.append(' ')
        msg4=msg4 + ''.join(space4)
        for i in range(1,maxLen - len(msg5) + 1):
            space5.append(' ')
        msg5=msg5 + ''.join(space5)
        for i in range(1,maxLen - len(msg6) + 1):
            space6.append(' ')
        msg6=msg6 + ''.join(space6)
        for i in range(1,maxLen - len(msg7) + 1):
            space7.append(' ')
        msg7=msg7 + ''.join(space7)
        for i in range(1,maxLen + 5):
            starLine.append("*")
        for i in range(1,maxLen + 1):
            space.append(" ")
        print(''.join(starLine))
        print('* %s *' % ''.join(space))
        print('* %s *' % msg1)
        print('* %s *' % msg2)
        print('* %s *' % msg3)
        print('* %s *' % msg4)
        print('* %s *' % ''.join(space))
        print('* %s *' % msg5)
        print('* %s *' % msg6)
        print('* %s *' % msg7)
        print('* %s *' % ''.join(space))
        print(''.join(starLine))

    def ip_dict(self):
        if DituBase.__ip_dict__ is None:
            self.__process_host__()
        return DituBase.__ip_dict__

    @staticmethod
    def isDir(theFile):
        return path.isdir(theFile)

    @staticmethod
    def isFile(theFile):
        theResult=path.isfile(theFile)
        return theResult

    def isSudo(self,x=None):
        if x is None:
            self.debug_msg(self.query("isSudo"),"SUDO",DituCode.DEBUG)
        return self.query("isSudo",x)

    def lastCommand(self,x=None):
        return self.query('lastCommand',x)

    def latest_version(self):
        try:
            import requests
            if DituBase.__latest_version__ is None:
                if self.nslookup(self.download_host()):
                    req=requests.get(self.download_url())
                    if str(req.status_code)=='200':
                        for line in req.content.decode('utf8').splitlines():
                            if 'self.appName' in line and self.appName() in line:
                                majorVersion=int(self.regex('afterBracket').sub("",self.regex('majorVersion').sub("",line)))
                                minorVersion=int(self.regex('afterBracket').sub("",self.regex('minorVersion').sub("",line)))
                                if majorVersion > self.majorVersion() or (majorVersion == self.majorVersion() and minorVersion> self.minorVersion()):
                                    DituBase.__need_update__=True
                                    DituBase.__latest_version__="%d.%d" % (majorVersion,minorVersion)
                                else:
                                    DituBase.__latest_version__="%d.%d" % (self.majorVersion(),self.majorVersion())
                else:
                    self.critical_msg("Cannot Resolve Host name: %s!" % self.download_host(),"CONNECTION FAILED")
        except:
            pass
        return DituBase.__latest_version__

    @staticmethod
    def listFiles(mypath):
        onlyfiles=[f for f in listdir(mypath) if isfile(join(mypath,f))]
        return onlyfiles

    def local_ip(self):
        if DituBase.__local_ip__ == '':
            self.shell('ip addr|grep inet|grep global|cut -f1 -d/')
            DituBase.__local_ip__=self.trim(self.stdout()).split()[1]
        return DituBase.__local_ip__

    def localhosts(self):
        if DituBase.__localhosts__ is None:
            self.__process_host__()
        return DituBase.__localhosts__

    def md5(self,s):
        return hashlib.md5(s.encode('utf-8')).hexdigest()

    def me(self):
        return getpass.getuser()

    def mkdir(self,fileList,option="-p"):
        return self.shell("mkdir %s %s" % (option,fileList))

    def name(self,x=None):
        return self.query('name',x)

    def nslookup(self, dns):
        return self.shell('nslookup %s' % self.getDomain(dns)).stdout()!=''\
            and 'NXDOMAIN' not in self.stdout()

    @staticmethod
    def originalPath():
        return DituBase.__originalPath__

    def owner(self,x=None):
        return self.query('owner',x)

    def parseCommand(self):
        self.debug_msg("Parse Command","PARSE COMMAND",DituCode.OK,self.line())
        if self.arg.command == "info" :
            self.info()
        return self

    def path(self,x):   
        x=self.trim(x)
        if x.startswith('/'):
            return path.abspath(x)
        else:
            return path.abspath(path.join(self.dirpath()[0],x))

    def parseArgs(self):
        if not self.arg:
            self.arg=self.parser.parse_args()
        return self

    def preParseArgs(self):
        if not self.arg:
            self.arg=self.parser.parse_args()
        if self.arg.debug is not None and self.arg.debug:
            self.mode(DituMode.DEBUG).debug_mode_start()
        return self

    def preParseCommand(self):
        self.debug_msg("Pre Parse Command","PREPARSE COMMAND",DituCode.OK,self.line())
        return self

    def printStdout(self):
        print(self.stdout())
        return self

    def regexName(self,x=None):
        return self.query('regexName',x)

    def remote_apt_install(self,app,host='',remote_root=''):
        r,host,remote_root=self.verify_remote_root(host,remote_root)
        if r:
            self.remote_root_command("sudo apt install -y %s" % app,host,remote_root)
        return self

    def remote_apt_upgrade(self,host='',remote_root=''):
        r,host,remote_root=self.verify_remote_root(host,remote_root)
        if r:
            self.remote_root_command("sudo apt update",host,remote_root)\
                .remote_root_command("sudo apt -y upgrade",host,remote_root)
            if self.stderr()!='' and 'WARNING' not in self.stderr():
                self.critical_msg('Error in execution:\n%s' % self.stderr())
            else:
                result = ""
                for line in self.stdout().splitlines():
                    if "upgraded," in line:
                        result =  "%s" %  self.trim(line)
                self.info_msg("Updated to %s\n    %s" % (host,result), "UPDATE DONE")
        return self

    def remote_cmd(self,cmd,host,remote_user):
        conn='%s@%s' % (remote_user,host)
        bash_cmd='/bin/bash -c "%s"' % cmd 
        self.clearStd().std(Popen(['ssh','-o','StrictHostKeychecking=no',conn,bash_cmd],stdin=PIPE,stdout=PIPE,stderr=PIPE,universal_newlines=True).communicate('\n'))
        if self.stderr():
            self.critical_msg("Error found:%s" % self.stderr(),"EXECUTION ERROR")
        return self

    def remote_create_user(self,uid,user,home,host='',remote_root=''):
        r,host,remote_root=self.verify_remote_root(host,remote_root)
        if r:
            if not self.remote_has_user(user):
                self.remote_root_command("sudo groupadd -g %s %s" % (uid,user),host,remote_root)\
                    .remote_root_command("sudo useradd -g %s -u %s -m -d %s -s /bin/bash %s" % (uid,uid,home,user),host,remote_root)
        return self

    def remote_has_user(self, user,host='',remote_root=''):
        r,host,remote_root=self.verify_remote_root(host,remote_root)
        if r:
            return 'uid=' in self.remote_root_command('id %s' % user,host,remote_root).stdout()
        return False

    def remote_onbehalf(self,user,cmd):
        if self.ssl_cert() != '' and self.isFile(self.ssl_cert()):
            self.sudo_chmod(self.ssl_cert(),"600")\
                .sudo_chown(self.ssl_cert(),"%s:%s" % (self.me(),self.me()))\
                .clearStd().std(Popen(['ssh','-o','StrictHostKeychecking=no','-i',\
                self.ssl_cert(),
                '%s@%s' % (self.remote_root(),self.host()),\
                'sudo su - %s /bin/bash -c "%s"' % (user,cmd)],\
                stdin=PIPE,stdout=PIPE,stderr=PIPE,\
                universal_newlines=True).communicate('\n'))
        else:
            self.clearStd().std(Popen(['ssh','-o','StrictHostKeychecking=no',\
                '%s@%s' % (self.remote_root(),self.host()),\
                'sudo su - %s /bin/bash -c "%s"' % (user,cmd)],\
                stdin=PIPE,stdout=PIPE,stderr=PIPE,\
                universal_newlines=True).communicate('\n'))
        return self

    def remote_root(self,x=None):
        return self.query('remote_root',x)

    def remote_root_command(self,cmd,host='',remote_root=''):
        r,host,remote_root=self.verify_remote_root(host,remote_root)
        if r:
            if self.mode()==DituMode.DEBUG:
                print("%s@%s using cmd: %s" % (remote_root,host,cmd))
            conn='%s@%s' % (remote_root,host)
            bash_cmd='/bin/bash -c "%s"' % cmd 
            if self.ssl_cert() != '' and self.isFile(self.ssl_cert()):
                self.sudo_chmod(self.ssl_cert(),"600")\
                    .sudo_chown(self.ssl_cert(),"%s:%s" % (self.me(),self.me()))\
                    .clearStd().std(Popen(['ssh','-i',self.ssl_cert(),'-o',\
                    'StrictHostKeychecking=no',conn,bash_cmd],\
                    stdin=PIPE,stdout=PIPE,stderr=PIPE,universal_newlines=True).communicate('\n'))
            else:
                self.clearStd().std(Popen(['ssh','-o','StrictHostKeychecking=no',conn,\
                    bash_cmd],stdin=PIPE,stdout=PIPE,stderr=PIPE,\
                    universal_newlines=True).communicate('\n'))
            if self.mode()==DituMode.DEBUG:
                print(self.stderr())
        return self

    def remote_user(self,x=None):
        return self.query('remote_user',x)

    def remote_takeowner(self,path,user,host='',remote_root=''):
        r,host,remote_root=self.verify_remote_root(host,remote_root)
        if r:
            return self.remote_root_command("sudo chown -R %s:%s %s" \
                % (user,user,path),host,remote_root)
        return self

    def rm(self,fileList,option="-rf"):
        return self.shell("rm %s %s" % (option,fileList))

    def saveConfFile(self):
        self.mkdir(self.configPath())
        with open(self.configFile(),'w') as f1:
            self.config.write(f1)
        self.chmod("%s" % (self.configPath()),"700 -R")
        if self.mode() == DituMode.GEN_TEST:
            self.debug_msg("Saving Configuration file: ##(##\/##[^##\/##]##+##)##+",\
            "DONE",DituCode.DONE)
        else:
            self.debug_msg("Saving Configuration file: %s" % (self.configFile()),\
            "DONE",DituCode.DONE)

    @staticmethod
    def scriptName():
        return [path.basename(DituBase.fullPath()[0]),"[^\/?\*^\$]+"]

    @staticmethod
    def scriptPath():
        return path.dirname(DituBase.fullPath()[0])

    def send_hosts_file(self,host='',remote_root='',success_msg=None):
        r,host,remote_root=self.verify_remote_root(host,remote_root)
        if r:
            self.create_hosts_file_temp(host)
            self.send_system_file('/tmp/hosts','/etc/',success_msg,host,remote_root)
        return self

    def send_system_file(self,source,target,success_msg=None,host='',remote_root=''):
        r,host,remote_root=self.verify_remote_root(host,remote_root)
        if r:
            fname_split=source.split('/')
            fn=fname_split[len(fname_split)-1]
            tmp_fname='/tmp/%s' % fn
            self.clearStd().std(Popen(['scp','-o','StrictHostKeychecking=no',\
                source,'%s@%s:/tmp' % (remote_root,host)],\
                stdin=PIPE,stdout=PIPE,stderr=PIPE,\
                universal_newlines=True).communicate('\n'))
            if self.stderr()=='':
                self.remote_root_command('sudo chown root:root %s && sudo cp %s %s' \
                    % (tmp_fname,tmp_fname,target),host,remote_root)
                self.remote_root_command('sudo chmod 777 %s;sudo rm -rf %s' \
                    % (tmp_fname,tmp_fname),host,remote_root)
                if self.stderr() != '':
                    self.critical_msg('Error in execution: %s' \
                        % self.stderr(),'EXECUTION ERROR')
                else:
                    if success_msg is None:
                        success_msg="System file sent to %s:" % (host)
                    self.info_msg(success_msg,"FILE SENT")
                    self.remote_root_command('sudo ls -lash %s' \
                        % target,host,remote_root)
                    for line in self.stdout().split('\n'):
                        line_split=line.split()
                        fname=line_split[len(line_split)-1]
                        if fn==fname:
                            print("    %s" % self.trim(line))
            else:
                self.critical_msg("Sending file to %s@%s with error: %s" \
                    % (remote_root,host,self.stderr()),"EXECUTION ERROR")
        return self

    def self_update(self,msg="Installation completed!"):
        if self.nslookup(self.download_host()):
            req=requests.get(self.download_url())
            if str(req.status_code) == '200':
                fname="/tmp/%s-%s" % (self.appName(),self.timestamp()[0])
                fp=open(fname,"w")
                fp.write(req.content.decode('utf8'))    
                fp.close()
                self.sudo_cp(fname,self.install_path())
                self.sudo_shell("chmod +x %s" % self.install_path())
                self.safe_msg(msg,"INSTALLATION")
            else:
                self.critical_msg("Failed to download!","DONWLOAD FAILED")
        else:
            self.critical_msg("Cannot Resolve Host name: %s!" \
                % self.download_host(),"DONWLOAD FAILED")

    def set_original_owner(self,dir,owner="root:root"):
        if self.__sudo_test__():
            self.tempFolder()
            sourceFile="%s/.original-owner" % self.tempFolder()
            targetFile="%s/.original-owner" % dir
            fp=open(sourceFile,"w+")
            fp.write("%s\n" % owner)
            fp.close()
            self.sudo_mv(sourceFile,targetFile)
            self.sudo_chown(targetFile)
        return self

    def setConfig(self,section,name,value):
        self.checkConfigFile()
        if not self.config.has_section(section):
            try:
                self.config.add_section(section)
                self.debug_msg("%s (line: #%s)" % (section,\
                    self.previousLine()) ,"ADD SECTION",DituCode.ADD_SECTION)
            except:
                self.critical_msg("Section: %s is not invalid" % (section),\
                    "ADD FAILED")
        if self.config.has_section(section):
            try:
                self.config.set(section,name,value)
                self.debug_msg("%s['%s']=%s (line: #%s)" % (section,\
                    name,value,self.previousLine()) ,"SET CONFIG",\
                        DituCode.SET_CONFIG)
            except:
                self.critical_msg("Setting config: %s=%s" % (name,value),\
                    "FAILED")
        return self

    def sha1(self,s):
        return hashlib.sha1(s.encode('utf-8')).hexdigest()

    # Update 2021-12-20
    def shell(self,command,showResult=False,ignoreError=False):
        self.clearStd()
        try:
            self.std(Popen(['/bin/bash','-c',command],stdin=PIPE,stdout=PIPE,\
                stderr=PIPE,universal_newlines=True).communicate('\n'))
            self.debug_msg("shell: %s" % command,'SHELL',100,self.previousLine())
        except:
            if 'level=info' not in self.stderr():
                self.info_msg("shell: %s" % command,'SHELL')
                self.critical_msg("Error: '%s'" % self.stderr(),'SHELL ERROR')
            else:
                self.debug_msg("shell: %s" % command,'SHELL',100,self.previousLine())
                self.debug_msg("stderr: %s" % self.stderr(),'SHELL',100,self.previousLine())
        if self.stderr()!='':
            if not ignoreError:
                self.critical_msg("Error: '%s'" % self.stderr(),'SHELL ERROR')
        elif showResult:
            print(self.stdout())
        return self

    def showConfigFile(self):
        if self.configFileExists():
            self.safe_msg("Config file: %s" % (self.configFile()) ,"EXISTS")
        else:
            self.critical_msg("Config file: %s" % (self.configFile()) ,"NOT EXISTS")

    def source(self,x=None):
        return self.query('source',x)

    def start(self):
        self.addCommands().addArguments().addCommandArguments() \
            .preParseArgs().parseArgs().preParseCommand()
        self.parseCommand()
        self.lastCommand(self.arg.command)
        return self.debug_msg_elapse()

    def std(self,std):
        if std[0] is None:
            stin=''
        else:
            stin=std[0]
        if std[1] is None:
            sterr=''
        else:
            sterr=std[1]
        return self.stdout(stin).stderr(sterr)

    def stderr(self,x=None):
        return self.query('stderr',x)

    def stdout(self,x=None):
        return self.query('stdout',x)

    def ssl_cert(self,x=None):
        return self.query('ssl_cert',x)

    def sudo(self,command):
        parsedCommand=self.parseShell(command)
        self.clearStd().debug_msg("Sudo Shell command (line: #%s): %s"\
            % (self.previousLine(),command) ,"SUDO")
        p=Popen(['sudo','-S'] + parsedCommand,stdin=PIPE,\
            stdout=PIPE,stderr=PIPE,universal_newlines=True)
        return self.std(p.communicate('\n'))

    def sudo_chown(self,fileList,owner="root:root"):
        if self.__sudo_test__():
            self.clearStd().std(Popen(['sudo','-S','chown',\
                owner,fileList],stdin=PIPE,\
                stdout=PIPE,stderr=PIPE,universal_newlines=True).communicate('\n'))
        return self

    def sudo_chmod(self,fileList,option="+x"):
        if self.__sudo_test__():
            self.clearStd().std(Popen(['sudo','-S','chmod',\
                option,fileList],stdin=PIPE,\
                stdout=PIPE,stderr=PIPE,universal_newlines=True).communicate('\n'))
        return self

    def sudo_cp(self,source,dest):
        if self.__sudo_test__():
            self.clearStd().std(Popen(['sudo','-S','cp',\
                source,dest],stdin=PIPE,stdout=PIPE,\
                stderr=PIPE,universal_newlines=True).communicate('\n'))
        return self

    def sudo_echo(self,msg=' '):
        if self.__sudo_test__(msg):
            self.print(self.stdout())
        return self

    def sudo_mkdir(self,fileList,option="-p"):
        if self.__sudo_test__():
            self.clearStd().std(Popen(['sudo','-S','mkdir',\
                option,fileList],stdin=PIPE,\
                stdout=PIPE,stderr=PIPE,universal_newlines=True).communicate('\n'))
        return self

    def sudo_mv(self,source,dest):
        if self.__sudo_test__():
            self.clearStd().std(Popen(['sudo','-S','mv',\
                source,dest],stdin=PIPE,stdout=PIPE,\
                stderr=PIPE,universal_newlines=True).communicate('\n'))
        return self

    def sudo_rm(self,fileList,option="-rf"):
        if self.__sudo_test__():
            self.clearStd().std(Popen(['sudo','-S',\
                'rm',option,fileList],stdin=PIPE,stdout=PIPE,\
                stderr=PIPE,universal_newlines=True).communicate('\n'))
        return self

    def sudo_shell(self,command):
        if self.__sudo_test__():
            self.sudo(command)
        return self

    def tempFolder(self):
        if DituBase.__tempFolder__ is not None:
            return DituBase.__tempFolder__
        if self.originalName() == '':
            return "%s/.tmp" % self.home()
        if self.isDir("/dev/shm"):
            DituBase.__tempFolder__="/dev/shm/%s/%s" \
                % (self.username(),self.originalName())
        elif self.isDir("/tmp"):
            DituBase.__tempFolder__="/tmp/%s/%s" \
                % (self.username(),self.originalName())
        return DituBase.__tempFolder__

    def testConfigFile(self):
        return "%s/%s.cfg" % (self.tempFolder(),self.appName())

    @staticmethod
    def thisFile():
        return DituBase.__here__

    @staticmethod
    def thisOwner():
        return DituBase.findOwner(DituBase.fullPath()[0])

    @staticmethod
    def timestamp():
        return [ "%s" % (int(time.time())),"\d{10,}"]

    @staticmethod
    def today():
        return [ strftime("%Y-%m-%d",gmtime()),"\d{4}-\d{2}-\d{2}"]

    def type(self,optionType=None):
        return self.query('optionType',optionType)

    def unique_host_list(self):
        if DituBase.__unique_host_list__ is None:
            self.__process_host__()
        return DituBase.__unique_host_list__

    def unzip(self,source,dest):
        self.shell("unzip %s -d %s" %(source,dest))

    def update_ssh(self,keysFile,showErr=True,host='',remote_root=''):
        r,host,remote_root=self.verify_remote_root(host,remote_root)
        if r:
            rt_cn='%s@%s' % (remote_root,host)
            rm_tmp_path='/tmp/authorized_keys'
            conn='%s:%s' % (rt_cn,rm_tmp_path)
            rm_usr=self.remote_user()
            usr_prv="%s:%s" % (rm_usr,rm_usr)
            usr_cn="%s@%s" % (rm_usr,host)
            cert=self.ssl_cert()
            rm_home=self.check_remote_user(host,remote_root,rm_usr)
            if self.stderr() != '':
                if showErr:
                    self.critical_msg("Error in execution:\n%s" % (self.stderr()),\
                        "EXECUTION ERROR") 
            elif ("~" in rm_home or rm_home=='') :
                if showErr:
                    self.critical_msg("Remote User Home Not found in %s\n  '%s'" % \
                        (usr_cn,rm_home),"REMOTE HOME NOT FOUND") 
            else:
                rm_ssh_root="%s/.ssh" % rm_home
                if cert == '':
                    cmd="scp -o StrictHostKeychecking=no %s %s" % (keysFile,conn)
                else:
                    cmd="scp -o StrictHostKeychecking=no -i %s %s %s" % (cert,keysFile,conn)
                self.shell(cmd)
                rm_cmd="%s %s;%s %s;%s %s %s/;%s %s/authorized_keys;sudo chown %s -R %s; sudo chmod 700 %s" \
                    % ('sudo mkdir -p',rm_ssh_root,'sudo chmod 777',rm_ssh_root,'sudo cp',\
                    rm_tmp_path,rm_ssh_root,'sudo chmod 600',rm_ssh_root,usr_prv,rm_ssh_root,rm_ssh_root)
                self.remote_root_command(rm_cmd,host,remote_root)
                if self.stderr() == '':
                    result="Remote SSH has been updated for User %s:%s" % (usr_cn,rm_home)
                    if cert!='':
                        result="Using cert file: %s\n  %s" %(cert,result)
                    self.info_msg(result,"SSH KEY UPDATED")
                elif not showErr:
                    pass
                else:
                    self.critical_msg("Error in %s@%s:%s\n%s" % (rm_usr,host,rm_home\
                        ,self.stderr()),"EXECUTION ERROR")
        return self

    def uploadFile(self,source_folder,target_folder,fn,host='',remote_user=''):
        r,host,remote_user=self.verify_remote_user(host,remote_user)
        if r:
            self.shell("scp %s/%s %s@%s:%s/" % (source_folder,fn,remote_user,host,target_folder))\
                .remote_cmd('ls -lash %s' % target_folder,host,remote_user)\
                .info_msg("The %s uploaded to %s:" % (fn,target_folder),"REMOTE FOLDER")
            for line in self.stdout().split('\n'):
                line_split=line.split()
                if len(line_split) > 0:
                    fname=line_split[len(line_split)-1]
                    if fn in fname:
                        print("    %s" % self.trim(line))
        return self

    def verify_remote_root(self,host='',remote_root=''):
        if (host=='' or not host) and self.host()!='':            
            host=self.host()
        if remote_root=='':
            if self.remote_root()!='':
                remote_root=self.remote_root()
            else:
                remote_root='ubuntu'
        if host=='':
            self.notDefined("Host")
            return False,'',''
        elif remote_root=='':
            self.notDefined("Remote Root")
            return False,'',''
        elif host in self.localhosts():
            self.critical_msg("Should not update localhost: %s!" % host,"HOST ERROR")
            return False,'',''
        else:
            return True,host,remote_root

    def verify_remote_user(self,host='',remote_user=''):
        if (host=='' or not host) and self.host()!='':
            host=self.host()
        if remote_user=='':
            if self.remote_user()!='':
                remote_user=self.remote_user()
        if host=='':
            self.notDefined("Host")
            return False,'',''
        elif remote_user=='':
            self.notDefined("Remote User")
            return False,'',''
        elif host in self.localhosts():
            self.critical_msg("Should not update localhost: %s!" % host,"HOST ERROR")
            return False,'',''
        else:
            return True,host,remote_user

    def __init__(self):
        DituObj.__init__(self)
        self.regex("appName",r"^.*appName\(['\"]?")\
            .regex("author",r"^.*author\(['\"]?")\
            .regex("lastUpdate",r"^.*lastUpdate\(['\"]?")\
            .regex("majorVersion",r"^.*majorVersion\(['\"]?")\
            .regex("minorVersion",r"^.*minorVersion\(['\"]?") \
            .regex("afterBracket",r"['\"]?\).*$")\
            .createItem('configSection',DituType.STRING).createItem('stdout','',False,False)\
            .createItem('stderr','',False,False)\
            .createItem('lastCommand').createItem('download_host').createItem('download_url')\
            .createItem('name').createItem('optionType').createItem('owner').createItem('configName')\
            .createItem('configValue').createItem('configFilePath','',False,False)\
            .createItem('configPath','',False,False).createItem('configFile','',False,False)\
            .createItem('host',DituType.STR_IDENTIFIER).createItem('remote_root')\
            .createItem('remote_user').createItem('ssl_cert')\
            .createItem('destination',DituType.STR_PATH,False,False).createItem('source')\
            .createItem('isSudo',DituType.BOOL)

class Gito(DituBase):
    __b__=[]
    __p__=[]
    __r__={}
    __q__={}

    def __all_prjs__(self,projectRoot=None):
        if projectRoot is None:
            projectRoot=self.originalPath()
        self.__reset_prjs()
        self.shell('for PW in $(find %s -type d -name .git);' \
            % projectRoot + ' do echo ${PW%/.git};done')
        if self.stderr()=='':
            self.prjs(self.stdout())
        self.debug_msg('Prjects count: %d' % len(self.prjs()),\
            'GIT PROJECTS',100,self.line())
        return self

    def __all_brs__(self,p):
        self.__reset_branches()
        self.shell('cd %s && for BR in $(git branch -a|grep "^\s*remotes/origin"|grep -v HEAD); do echo ${BR##*/};done' % p)
        if self.stderr()=='':
            self.branches(self.stdout())
        self.debug_msg('Branches count: %d' % len(self.branches()), 'GIT BRANCHES',100,self.line())
        return self

    def __checkout__(self,p,b):
        self.__fetch__(p,b)
        if self.cmd(p,'checkout %s' % b,True,True):
            for l in self.stdout().split('\n'):
                if self.trim(l)!='':
                    print("    %s" % l)
        return self

    def __fetch__(self,p,b):
        if not self.__isLocal__(p,b):
            self.cmd(p,'branch --track %s  remotes/origin/%s' % (b,b))
        return self
    
    def __isLocal__(self,p,b):
        # if checkout locally, rev-parse --verify returns a raw 20-byte SHA-1
        self.cmd(p,'rev-parse --verify %s' % b,False)
        return self.trim(self.stdout())!=''

    def __pull__(self,p,b):
        self.__checkout__(p,b)
        if self.cmd(p,'reset --hard',False,True):
            self.cmd(p,'pull origin %s' % b,True,True)
            for l in self.stdout().split('\n'):
                if self.trim(l)!='' and ('HEAD' in l or 'Current' in l):
                    print("    %s" % l)
        return self

    def __push__(self,pj):
        l=''
        if self.cmd(pj,'rev-parse --abbrev-ref HEAD',False):
            for j in self.stdout().split('\n'):
                if self.trim(j)!='':
                    l=j
                    if l!='':
                        if self.cmd(pj,'push origin %s' % l):
                            self.info_msg("Project Name: %s\n  Branch Name: %s" \
                                % (pj,l),"GIT PUSH" )
        return l

    def __reset_branches(self):
        Gito.__b__=[]
        return self

    def __reset_prjs(self):
        Gito.__p__=[]
        return self

    def __reset_result(self):
        Gito.__r__={}
        Gito.__q__={}
        return self

    def __scan__(self,projectRoot=None):
        self.branch(['master','dl']).keyword('BASE_VERSION=').pull(True,projectRoot)
        return self

    def branch(self,x=None):
        return self.query('branch',x)

    def branches(self,x=None):
        if x is None:
            return Gito.__b__
        else:
            if isinstance(x,basestring):
                if '\n' in x:
                    for l in x.split('\n'):
                        Gito.__b__.append(l)
                else:
                    Gito.__b__.append(x)
        return self

    def branches_size(self):
        return len(Gito.__b__)

    def checkCommit(self,p):
        needCommit=False
        if self.cmd(p,'status'):
            for l in self.stdout().split('\n'):
                if self.trim(l)!='' and 'not staged' in l:
                    needCommit=True
        return needCommit

    def cmd(self,pj,cmd,showResult=True,ignoreError=False):
        self.shell('cd %s && git %s' % (pj,cmd),showResult,ignoreError)
        return self.stderr()=='' or 'level=info' in self.stderr()

    def commit_push(self,pj):
        l=''
        if self.cmd(pj,'add .'):
            if self.cmd(pj,'commit -m "Update Core"'):
                l=self.__push__(pj)
        return l

    def isGitDir(self,dir):
        return self.isDir(self.path('%s/.git' % dir))

    def keyword(self,x=None):
        return self.query('keyword',x)

    def list(self,fileList,projectList,display=True,projectRoot=None):
        if not self.isFile(fileList) or not self.isFile(projectList):
            self.debug_msg('FileList and ProjectList Not Found','LIST',100,self.line())
            self.scan(fileList,projectList,display,projectRoot)
        else:
            self.debug_msg('FileList and ProjectList Found:\n    %s\n    %s' \
                % (fileList,projectList),'LIST',100,self.line())
            self.readFileList(fileList,projectList,display)

    def mergeMaster(self,pj,br):
        if self.cmd(pj,'checkout master',True,True):
            if self.cmd(pj,'pull origin %s' % br,True,True):
                if self.cmd(pj,'push origin master',True):
                    self.info_msg("Project Name: %s\n  Branch Name: master" % pj,"GIT PUSH" )
        return self

    def prjs(self,x=None):
        if x is None:
            return Gito.__p__
        else:
            if isinstance(x,basestring):
                if '\n' in x:
                    for l in x.split('\n'):
                        Gito.__p__.append(l)
                else:
                    Gito.__p__.append(x)
        return self

    def prjs_size(self):
        return len(Gito.__p__)

    def pull(self,display=True,projectRoot=None,branch=None):
        self.__all_prjs__(projectRoot)
        if self.keyword() != '':
            self.__reset_result()
        for p in self.prjs():
            shown=False
            location='Project Location: %s,\n  ' % p
            self.debug_msg('%s' % location, 'GIT PULL',100,self.line())
            self.__all_brs__(p)
            if branch is None and self.branch()!='':
                branch=self.branch()
            if branch is None:
                for b in self.branches():
                    if display:
                        if not shown:
                            shown=True
                            self.info_msg('%sBranch Name: %s' % (location,b),"GIT",DituCode.EXEC)
                        else:
                            print('  %sBranch Name: %s%s' % (DituColor.ITALICS+DituColor.LIGHT_BLUE,b,DituColor.END) )
                        self.__pull__(p,b)
                    if self.keyword()!='':
                        self.search(p,not shown)
            else:
                if isinstance(branch,list):
                    for b in branch:
                        if b in self.branches():
                            if display:
                                if not shown:
                                    shown=True
                                    self.info_msg('%sBranch Name: %s' % (location,b),"GIT",DituCode.EXEC)
                                else:
                                    print('  %sBranch Name: %s%s' % (DituColor.ITALICS+DituColor.LIGHT_BLUE,b,DituColor.END) )
                            self.__pull__(p,b)
                            if self.keyword()!='':
                                self.search(p,not shown)
                elif branch in self.branches():
                    if display:
                        if not shown:
                            shown=True
                            self.info_msg('%sBranch Name: %s' % (location,branch),"GIT",DituCode.EXEC)
                        else:
                            print('  %sBranch Name: %s%s' % (DituColor.ITALICS+DituColor.LIGHT_BLUE,b,DituColor.END) )
                    self.__pull__(p,branch)
                    if self.keyword()!='':
                        self.search(p,not shown)
        if self.keyword()!='' and display:
            self.info_msg("'%s' found in %d projects" % \
                (self.keyword(),len(self.resultProjects())),"SEARCH RESULTS")
            for r in self.resultProjects():
                print("    %s" % r)
            self.info_msg("'%s' found in %d files" % \
                (self.keyword(),len(self.resultFiles())),"SEARCH RESULTS")
            for r in self.resultFiles():
                print("    %s" % r)
        return self

    def push(self,branch=None):
        self.__all_prjs__()
        if self.keyword() != '':
            self.__reset_result()
        for p in self.prjs():
            shown=False
            location='Project Location: %s,\n  ' % p
            self.__all_brs__(p)
            if branch is None and self.branch()!='':
                branch=self.branch()
            if branch is None:
                for b in self.branches():
                    if self.checkCommit(p):
                        if not shown:
                            shown=True
                            self.info_msg('%sBranch Name: %s' % (location,b),"GIT",DituCode.EXEC)
                        else:
                            print('  %sBranch Name: %s%s' % (DituColor.ITALICS+DituColor.LIGHT_BLUE,b,DituColor.END) )
                        self.__push__(p)
            else:
                if isinstance(branch,list):
                    for b in branch:
                        if b in self.branches():
                            if self.checkCommit(p):
                                if not shown:
                                    shown=True
                                    self.info_msg('%sBranch Name: %s' % (location,b),"GIT",DituCode.EXEC)
                                else:
                                    print('  %sBranch Name: %s%s' % (DituColor.ITALICS + DituColor.LIGHT_BLUE,b,DituColor.END) )
                                self.__push__(p)
                elif branch in self.branches():
                    if self.checkCommit(p):
                        if not shown:
                            shown=True
                            self.info_msg('%sBranch Name: %s' % (location,branch),"GIT",DituCode.EXEC)
                        else:
                            print('  %sBranch Name: %s%s' % (DituColor.ITALICS+DituColor.LIGHT_BLUE,b,DituColor.END) )
                        self.__push__(p)
        return self

    def readFileList(self,fileList,projectList,display=True):
        with open(fileList) as f:
            ln1=f.readlines()
            for line in ln1:
                fl1=self.trim(line)
                if fl1!='':
                    self.resultFiles(fl1)
        with open(projectList) as f:
            ln2=f.readlines()
            for line in ln2:
                pj2=self.trim(line)
                if pj2!='':
                    self.resultProjects(pj2)
        if display:
            self.scanResult(True)
        return self

    def resultFiles(self,x=None):
        if x is None:
            return Gito.__r__
        else:
            if isinstance(x,basestring):
                if '\n' in x:
                    for l in x.split('\n'):
                        Gito.__r__[self.path(l)]=True
                else:
                    Gito.__r__[self.path(x)]=True
        return self

    def resultProjects(self,x=None):
        if x is None:
            return Gito.__q__
        else:
            if isinstance(x,basestring):
                if '\n' in x:
                    for l in x.split('\n'):
                        Gito.__q__[l]=True
                else:
                    Gito.__q__[x]=True
        return self

    def scan(self,fileList,projectList,display=True,projectRoot=None):
        self.__scan__(projectRoot)
        fp=open(fileList,"w+")
        for fl in self.resultFiles():
            fp.write('%s\n' % fl)
        fp.close()
        fp2=open(projectList,"w+")
        for pj in self.resultProjects():
            fp2.write('%s\n' %  pj)
        fp2.close()
        return self

    def scanResult(self,warnEmpty=False):
        if len(self.resultProjects())==0 and len(self.resultFiles())==0:
            if warnEmpty:
                self.critical_msg('Previous Search Result is empty, please execute: %s -c scan' \
                    % self.appName(),"PREVIOUS RESULTS")
        else:
            self.info_msg("Found in %d projects" % \
                len(self.resultProjects()),"PREVIOUS SEARCH RESULTS")
            for r in self.resultProjects():
                print("    %s" % r)
            self.info_msg("Found in %d files" % \
                len(self.resultFiles()),"PREVIOUS SEARCH RESULTS")
            for r in self.resultFiles():
                print("    %s" % r)
        return self

    def search(self,p,showResult=True):
        hasResult=False
        self.shell('cd %s && grep -r "%s" --exclude-dir=.git .' % (p,self.keyword()))
        for l in self.stdout().split('\n'):
            if self.trim(l)!='':
                if not hasResult:
                    if showResult:
                        print("  Result for: %s" % self.keyword())
                    hasResult=True
                path="%s/%s" % (p,l.split(":")[0])
                if p not in self.resultProjects():
                    self.resultProjects(p)
                if path not in self.resultFiles():
                    if showResult:
                        print("    %s" % path)
                    self.resultFiles(path)
        return self

    def __init__(self,fromClass=None):
        DituBase.__init__(self)
        self.createItem("branch",DituType.STR_NAME)\
            .createItem("keyword",DituType.STR_NAME)
        if fromClass is not None:
            self.appName(fromClass.appName())\
                .lastUpdate(fromClass.lastUpdate())\
                .author(fromClass.author())\
                .majorVersion(fromClass.majorVersion())\
                .minorVersion(fromClass.minorVersion())

class PyParser(DituBase):

    __core_code__=[]
    __footer_code__=[]
    __header_code__=[]
    __target_appName__=''
    __target_author__=''
    __target_core_version__='0'
    __target_lastUpdate__=''
    __target_majorVersion__='0'
    __target_minorVersion__='0'
    __target_prj__=''

    def baseFolder(self):
        self.createFolder()
        return "%s/.local/lib/%s" % (self.home(),self.appName())

    def coreCode(self,x=None):
        if x is None:
            return PyParser.__core_code__
        else:
            PyParser.__core_code__.append(x)
        return self

    def createFolder(self):
        dir="%s/.local/lib/%s/include" % (self.home(),self.appName())
        if not self.isDir(dir):
            self.mkdir('%s/build' % dir)
            self.mkdir('%s/core' % dir)
            self.mkdir('%s/footer' % dir)
            self.mkdir('%s/header' % dir)
        return self

    def filePath(self,x=None):
        if x is not None:
            if self.regex('absPath').sub('',x)!='':            
                x=self.path(('%s/%s' % (self.originalPath(),x)))
        return self.query('filePath',x)

    def footerCode(self,x=None):
        if x is None:
            return PyParser.__footer_code__
        else:
            PyParser.__footer_code__.append(x)
        return self

    def generateCore(self,filepath,core_name):
        self.debug_msg('Start Processing...',"GENERATE CORE",100,self.line())\
            .parsePython(filepath)\
            .includePath('%s/include/core/%s.%d.py' % (self.baseFolder(),core_name,self.targetCoreVersion()))
        fp=open(self.includePath(),"w")
        fp.write(''.join(self.coreCode()).replace(self.targetPrj(),core_name))
        fp.close()
        return self

    def headerCode(self,x=None):
        if x is None:
            return PyParser.__header_code__
        else:
            PyParser.__header_code__.append(x)
        return self

    def includePath(self,x=None):
        if x is not None:
            if self.regex('absPath').sub('',x)!='':            
                x=self.path(('%s/%s' % (self.originalPath(),x)))
        return self.query('includePath',x)

    def latestCore(self,x=None,y=None):
        if x is not None:
            if y is not None:
                if self.regex('absPath').sub('',x)!='':            
                    x=self.path(('%s/%s' % (self.originalPath(),x)))
                self.debug_msg("latestCorePath=%s" % x,"SET",100,self.line())
                fplist=[]
                self.clearStd().std(Popen(['/bin/bash','-c',\
                    'find %s -type f -name "%s.*"' % (x,y)],\
                    stdin=PIPE,stdout=PIPE,stderr=PIPE,\
                    universal_newlines=True).communicate('\n'))
                self.debug_msg("Search Result:%s" % self.stdout(),"I/O",100,self.line())
                for line in self.stdout().splitlines():
                    fplist.append(self.trim(line))
                if len(fplist)>0:
                    fplist.sort(reverse=True)
                    self.query('latestCore',fplist[0])
                    return self
                else:
                    self.debug_msg("Can't find any Core files in %s" % x\
                        ,"EXECUTIVE",100,self.line())
            else:
                self.debug_msg("Unknow Project" ,"EXECUTIVE",100,self.line())
            return self
        else:
            return self.query('latestCore',x)

    def readCore(self,filepath):
        self.debug_msg('Start Processing...',"READ CORE",100,self.line())
        self.parsePython(filepath)
        self.includePath('%s/include/core/%s.%d.py' % (self.baseFolder(),self.targetPrj(),self.targetCoreVersion()))
        fp=open(self.includePath(),"w")
        fp.write(''.join(self.coreCode()))
        fp.close()
        self.includePath('%s/include/header/%s-header.%s.%s.%s.py' % \
            (self.baseFolder(),self.targetAppName(),self.targetPrj(),self.targetMajorVersion(),self.targetMinorVersion()))
        fp=open(self.includePath(),"w")
        fp.write(''.join(self.headerCode()))
        fp.close()
        self.includePath('%s/include/footer/%s-footer.%s.%s.%s.py' % \
            (self.baseFolder(),self.targetAppName(),self.targetPrj(),self.targetMajorVersion(),self.targetMinorVersion()))
        fp=open(self.includePath(),"w")
        fp.write(''.join(self.footerCode()))
        fp.close()
        return self

    def parsePython(self,filepath,nextVersion=False):
        in_header=True
        insideCore=False
        self.resetPythonParser()
        if not self.isFile(filepath):
            self.critical_msg("File not found: %s" % filepath, "PARSE PYTHON")
            return self
        with open(filepath) as f:
            n=0
            lines=f.readlines()
            self.debug_msg('Reading File: %s with #%d lines' % (filepath,len(lines)),"PARSE PYTHON",100,self.line())
            for line in lines:
                n=n+1
                token=line.split()
                if len(token)>0:
                    if 'BASE_VERSION' in token[0]:
                        token_split=token[0].split('_')
                        if len(token_split)>1:
                            if not token_split[0].startswith('.') and '(' not in token_split[0]:
                                in_header=False
                                insideCore=True
                                core_version_split=token[0].split('=')
                                if len(core_version_split)>1:
                                    self.targetPrj(token_split[0])
                                    self.targetCoreVersion(int(core_version_split[1]))
                                    self.coreCode(line).debug_msg('Core Code： Start: %s (%s) = %d (found in line #%d)' \
                                        % (core_version_split[0],self.targetPrj(),self.targetCoreVersion(),n),\
                                        "PARSE PYTHON",100,self.line())
                            else:
                                if insideCore:
                                    self.coreCode(line).debug_msg('Core Code: Similar wording of BASE_VERSION, "%s" (found in line #%d)' \
                                        % (token[0],n),\
                                        "PARSE PYTHON",100,self.line())
                                elif in_header:
                                    self.headerCode(line)
                                else:
                                    self.footerCode(line)
                        else:
                            if insideCore:
                                self.coreCode(line)
                            elif in_header:
                                self.headerCode(line)
                            else:
                                self.footerCode(line)
                    elif token[0]=='if' and len(token)>1 and token[1]=='__name__':
                        if insideCore:
                            self.coreCode('\n').coreCode(line)
                        elif in_header:
                            self.headerCode('\n').headerCode(line)
                        else:
                            self.footerCode('\n').footerCode(line)
                    elif token[0]=='class' and len(token)>1:
                        if len(self.targetPrj())>0: 
                            cname=self.subClassName(token[1])
                            if cname!=self.targetPrj() and (cname=='%sColor' % self.targetPrj() \
                                or cname=='%sCode' % self.targetPrj() or cname=='%sType' % self.targetPrj() \
                                or cname=='%sMode' % self.targetPrj() or cname=='%sObj' % self.targetPrj() \
                                or cname=='%sBase' % self.targetPrj()):
                                insideCore=True
                                if len(self.coreCode())>1:
                                    self.coreCode('\n')
                                self.coreCode(line)\
                                    .debug_msg('Core Class: %s (found in line #%d)' \
                                    % (token[1],n),\
                                    "PARSE PYTHON",100,self.line())
                            else:
                                if insideCore:
                                    insideCore=False
                                self.debug_msg('Non-core Class: %s (found in line #%d)' \
                                    % (cname,n),\
                                    "PARSE PYTHON",100,self.line())
                                if in_header:
                                    if len(self.headerCode())>1:
                                        self.headerCode('\n')
                                    self.headerCode(line)
                                else:
                                    if len(self.footerCode())>1:
                                        self.footerCode('\n')
                                    self.footerCode(line)
                        else:
                            if insideCore:
                                self.coreCode('\n').coreCode(line)
                            elif in_header:
                                self.headerCode('\n').headerCode(line)
                            else:
                                self.footerCode('\n').footerCode(line)
                    elif 'def'==token[0]:
                        if insideCore:
                            self.coreCode('\n').coreCode(line)
                        elif in_header:
                            self.headerCode('\n').headerCode(line)
                        else:
                            self.footerCode('\n').footerCode(line)
                    else:
                        if insideCore:
                            self.coreCode(line)
                        elif in_header:
                            self.headerCode(line)
                        else:
                            if 'self.appName(' in line \
                                and '.majorVersion(' in line \
                                and '.minorVersion(' in line:
                                t=self.trim(self.regex('afterBracket').sub('',self.regex('appName').sub('',line)))
                                if not t.startswith('%'):
                                    self.targetAppName(t)\
                                        .debug_msg("appName=%s" % self.targetAppName(),"PARSE PYTHON",100,self.line())
                                t=self.trim(self.regex('afterBracket').sub("",self.regex('majorVersion').sub("",line)))
                                if not t.startswith('%'):
                                    self.targetMajorVersion(int(t))\
                                        .debug_msg("majorVersion=%d" % self.targetMajorVersion(),"PARSE PYTHON",100,self.line())
                                t=self.trim(self.regex('afterBracket').sub("",self.regex('minorVersion').sub("",line)))
                                if not t.startswith('%'):
                                    if nextVersion:
                                        self.targetMinorVersion(int(t)+1)
                                    else:
                                        self.targetMinorVersion(int(t))
                                    self.debug_msg("minorVersion=%d" % self.targetMinorVersion(),"PARSE PYTHON",100,self.line())
                                t=self.trim(self.regex('afterBracket').sub("",self.regex('author').sub("",line)))
                                if not t.startswith('%'):
                                    self.targetAuthor(t)\
                                        .debug_msg("author=%s" % self.targetAuthor(),"PARSE PYTHON",100,self.line())     
                                t=self.trim(self.regex('afterBracket').sub("",self.regex('lastUpdate').sub("",line)))
                                if not t.startswith('%'):
                                    self.targetLastUpdate(t)\
                                        .debug_msg("lastUpdate=%s" % self.targetLastUpdate(),"PARSE PYTHON",100,self.line())
                                self.footerCode('        self.%s("%s").%s("%s").%s("%s").majorVersion(%d).minorVersion(%d)\n' % \
                                    ('appName',self.targetAppName(),'lastUpdate',self.today()[0],'author',\
                                    self.targetAuthor(),self.targetMajorVersion(),self.targetMinorVersion()))
                            else:
                                self.footerCode(line)
                elif self.trim(line)=='':
                    pass
                elif insideCore:
                    self.coreCode(line)
                else:
                    if in_header:
                        self.headerCode(line)
                    else:
                        self.footerCode(line)
        return self

    def resetCoreCode(self):
        PyParser.__core_code__=[]
        return self

    def resetFooterCode(self):
        PyParser.__footer_code__=[]
        return self

    def resetHeaderCode(self):
        PyParser.__header_code__=[]
        return self

    def resetPythonParser(self):
        return self.targetAuthor('')\
            .resetCoreCode()\
            .resetHeaderCode()\
            .resetFooterCode()\
            .targetAppName('')\
            .targetCoreVersion(0)\
            .targetLastUpdate('')\
            .targetMajorVersion(0)\
            .targetMinorVersion(0)\
            .targetPrj('')

    def targetAppName(self,x=None):
        if x is None:
            return PyParser.__target_appName__
        else:
            PyParser.__target_appName__=x
        return self

    def targetAuthor(self,x=None):
        if x is None:
            return PyParser.__target_author__
        else:
            PyParser.__target_author__=x
        return self

    def targetCoreVersion(self,x=None):
        if x is None:
            return PyParser.__target_core_version__
        else:
            PyParser.__target_core_version__=x
        return self

    def targetLastUpdate(self,x=None):
        if x is None:
            return PyParser.__target_lastUpdate__
        else:
            PyParser.__target_lastUpdate__=x
        return self

    def targetMajorVersion(self,x=None):
        if x is None:
            return PyParser.__target_majorVersion__
        else:
            PyParser.__target_majorVersion__=x
        return self

    def targetMinorVersion(self,x=None):
        if x is None:
            return PyParser.__target_minorVersion__
        else:
            PyParser.__target_minorVersion__=x
        return self

    def targetDir(self,x=None):
        return self.query('targetDir',x)

    def targetPrj(self,x=None):
        return self.query('targetPrj',x)

    def updateCore(self,filepath):
        self.debug_msg('Start Processing...',"UPDATE core",100,self.line())\
            .parsePython(filepath,True)\
            .latestCore('%s/include/core/' % self.baseFolder() ,self.targetPrj())
        if self.latestCore() != '' and self.isFile(self.latestCore()):
            with open(self.latestCore()) as f:
                self.resetCoreCode()
                lines=f.readlines()
                for line in lines:
                    token=line.split()
                    if len(token)>0:
                        if 'BASE_VERSION' in token[0]:
                            token_split=token[0].split('_')
                            if len(token_split)>1:
                                if not token_split[0].startswith('.'):
                                    prj2=token_split[0]
                                    core_version_split=token[0].split('=')
                                    if len(core_version_split)>1:
                                        core_version2=core_version_split[1]
                    self.coreCode(line)
            #if True or int(core_version2)!=self.targetCoreVersion():
            self.includePath('%s/include/build/%s.%s.%d.%d.py' % \
                (self.baseFolder(),self.targetAppName(),self.targetPrj(),self.targetMajorVersion(),self.targetMinorVersion()))
            fp=open(self.includePath(),"w")
            fp.write(''.join(self.headerCode()))
            fp.write('\n')
            fp.write(''.join(self.coreCode()))
            fp.write('\n')
            fp.write(''.join(self.footerCode()))
            fp.write('\n')
            fp.close()
            self.rm(filepath).cp(self.includePath(),filepath).info_msg("updated %s from %d -> %s" \
                % (self.targetPrj(), self.targetCoreVersion(),core_version2),"CORE UPDATE")
            #self.info_msg("%s is already using %s v.%d already!" % (self.targetAppName(),self.targetPrj(),int(core_version2)))
        else:
            self.critical_msg('Please use -c generate-core to pre generate cores files','FILE NOT FOUND')
        return self

    def __init__(self,fromClass=None):
        DituBase.__init__(self)
        self.createItem('filePath',DituType.STR_PATH)\
            .createItem('includePath',DituType.STR_PATH)\
            .createItem('latestCore',DituType.STR_PATH)\
            .createItem('targetDir',DituType.STR_PATH)\
            .createItem('targetPrj',DituType.STRING)
        if fromClass is not None:
            self.appName(fromClass.appName())\
                .lastUpdate(fromClass.lastUpdate())\
                .author(fromClass.author())\
                .majorVersion(fromClass.majorVersion())\
                .minorVersion(fromClass.minorVersion())
            
class DituMain(DituBase):

    def addArguments(self):
        super(DituMain, self).addArguments()
        self.argumentOption("f","filePath").argumentOption("D","targetDir")
        return self

    def addCommands(self):
        super(DituMain, self).addCommands()
        return self.command("self-update","").command("get-core","")\
            .command("install","").command("generate-core","")\
            .command("update-core","").command("list","").command("scan","").command("commit-all","")\
            .command("update-all","").command("update-all-commit","").command("update-project","")

    def parseArgs(self):
        super(DituMain, self).parseArgs()
        self.gito=Gito(self)
        self.ditu=PyParser(self)
        if self.arg.filePath is not None:
            self.ditu.filePath(self.arg.filePath)
        if self.arg.targetDir is not None:
            if self.gito.isGitDir(self.arg.targetDir):
                self.ditu.targetDir(self.arg.targetDir)
            else:
                self.critical_msg('There is no git info in folder: %s' % self.arg.targetDir)
        return self

    def list(self,display=True,projectRoot=None):
        if projectRoot is None:
            projectRoot=self.originalPath()
        sha1=self.sha1(projectRoot)
        fileList="%s/%s-file.txt" % (self.ditu.baseFolder(),sha1)
        projectList="%s/%s-project.txt" % (self.ditu.baseFolder(),sha1)
        self.gito.list(fileList,projectList,display,projectRoot)
        return self

    def commit_all(self):
        for pj in self.gito.resultProjects():
            self.commit(pj)
        return self

    def commit(self,pj):
        br=self.gito.commit_push(pj)
        if br!="master":
            self.gito.mergeMaster(pj,br)
        return self

    def parseCommand(self):
        super(DituMain, self).parseCommand()
        self.debug_msg("Parse Command","PARSE COMMAND",DituCode.OK,self.line())
        if self.arg.command=="self-update":
            self.info_msg("Starting download: %s" % self.download_url(), "DOWNLOAD")
            self.self_update()
        elif self.arg.command=="list":
            self.list()
        elif self.arg.command=="scan":
            self.scan()
        elif self.arg.command=="commit-all":
            self.list(False)
            self.commit_all()
        elif self.arg.command=="update-all":
            self.list(False)
            for fl in self.gito.resultFiles():
                self.ditu.updateCore(fl)
        elif self.arg.command=="update-all-commit":
            self.list(False)
            for fl in self.gito.resultFiles():
                self.ditu.updateCore(fl)
            self.commit_all()
        elif self.arg.command=="update-project":
            print(self.ditu.targetDir())
            self.list(False,self.ditu.targetDir())
            for fl in self.gito.resultFiles():
                self.ditu.updateCore(fl)
            self.commit_all()
        elif self.arg.command=="install":
            self.copy_to_user_local_bin()
        elif self.arg.command=="get-core":
            if self.ditu.filePath()=='':
                self.critical_msg("Please specify filename by -f or --file!","FILENAME MISSING")
            else:
                if self.isFile(self.ditu.filePath()):
                    self.ditu.readCore(self.ditu.filePath())
                else:
                    self.critical_msg("Error in opening file: %s" % self.ditu.filePath())
        elif self.arg.command=="generate-core":
            if self.ditu.filePath()=='':
                self.critical_msg("Please specify filename by -f or --file!","FILENAME MISSING")
            else:
                if self.isFile(self.ditu.filePath()):
                    self.ditu.generateCore(self.ditu.filePath(),'Ape')\
                        .generateCore(self.ditu.filePath(),'Ditu')\
                        .generateCore(self.ditu.filePath(),'Polka')\
                        .generateCore(self.ditu.filePath(),'Rio')\
                        .generateCore(self.ditu.filePath(),'Snap')
                else:
                    self.critical_msg("Error in opening file: %s" % self.ditu.filePath())
        elif self.arg.command=="update-core":
            if self.ditu.filePath()=='':
                self.critical_msg("Please specify filename by -f or --file!","FILENAME MISSING")
            else:
                if self.isFile(self.ditu.filePath()):
                    self.ditu.updateCore(self.ditu.filePath())
                else:
                    self.critical_msg("Error in opening file: %s" % self.ditu.filePath())
        return self

    def run(self):
        if not sys.stdin.isatty():
            if '<stdin>' == self.thisFile():
                self.self_update()
        else:
            self.start()
        return self

    def scan(self,display=True):
        sha1=self.sha1(self.originalPath())
        fileList="%s/%s-file.txt" % (self.ditu.baseFolder(),sha1)
        projectList="%s/%s-project.txt" % (self.ditu.baseFolder(),sha1)
        self.gito.scan(fileList,projectList,display)

    def __init__(self):
        DituBase.__init__(self)
        self.appName("ditu").lastUpdate("2021-12-29").author("Cloudgen").majorVersion(1).minorVersion(7)
        self.download_host('https://dl.riochain.io')\
            .download_url('%s/app/ditu' % self.download_host())\
            .run()

if __name__ == "__main__":
    dituMain = DituMain()
