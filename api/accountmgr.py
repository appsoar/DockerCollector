# -*- coding: utf-8 -*-
# Copyright (c) 20016-2016 The Cloudsoar.
# See LICENSE for details.

#import bcrypt

from common.util import Result
from frame.Logger import Log
from frame.authen import ring8
from frame.errcode import FAIL, INVALID_PARAM_ERR
from mongodb.dbconst import ID
from mongoimpl.consoledb.userdbimpl import UserDBImpl


_ALL = "All"

class AccountMgr(object):
    def __init__(self):
        pass
    
    
    @ring8
    def accounts(self, user_id=''):
        if user_id:
            query = {ID:user_id}
        else:
            query = None
        
        rlt = UserDBImpl.instance().read_record_list(query, fields=['nick_name','join_time', 'avatar'])
        if rlt.success:
            for user in rlt.content:
                user['user_id'] = user.pop(ID)
        return rlt
    
    @ring8
    def account(self, user_id):
        user_id = user_id.strip()
        if user_id=='':
            return Result('', INVALID_PARAM_ERR, 'Invalid user id' )
        
        rlt = UserDBImpl.instance().read_record(user_id)
        if rlt.success:
            rlt.content['user_id'] = rlt.content.pop(ID)
            rlt.content['password'] = '$2a$10$f4UrYQDuijGdWkxO0GTA5uyHwjExLVll/o6Bdg629qfiFctqzijZW'
        return rlt
        
    @ring8
    def login(self, user_name, password):
        rlt = self.count({ID:user_name,'password':password})
        if rlt.success and rlt.content > 1:
            return Result('ok')
        else:
            Log(1, '[%s]login fail'%(user_name))
            return Result('', FAIL, 'user name or password invalid')
    
    
        
        
        
        
    
    
    