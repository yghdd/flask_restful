import uuid

import os
from flask import request
from flask_restful import Api, Resource, fields, marshal_with, marshal, reqparse
from sqlalchemy import or_
from werkzeug.datastructures import FileStorage

import settings
from models import *
from dao import *

api = Api()


def init_api(app):
    api.init_app(app)  # 创建api


class UserApi(Resource):  # 声明user资源
    def get(self):
        # 读取参数中的var
        key = request.args.get('key')
        if key:
            result = {'state': 'fail', 'msg': '查无数据'}
            # 搜索用户信息 val = id/name
            users = query(User).filter(or_(User.id == key, User.name == key))
            print('all',users.all())
            print('first',users.first())
            if users.count():  # 如果查询的数据不为0
                result['state'] = 'ok'
                result['msg'] = '查询成功'

                result['data'] = [user.json for user in users]
                print(users.first().json )

            return result
            # 从数据库中查询所有数据
        users = queryAll(User)
        print(users)
        return {'state': 'ok', 'date': [user.json for user in users]}

    def post(self):
        # 从上传的form对象中取出name和phone
        name = request.form.get('name')

        print(name)
        # 将数据保存到数据库
        user = User()
        user.name = name
        add(user)
        return {'state': 'ok', 'msg': '添加{}用户成功'.format(name)}

    def delete(self):

        id = int(request.args.get('id'))
        print(id)
        user = queryById(User, id)
        delete(user)
        return {'state': 'ok', 'msg': '删除{}号用户成功'.format(id)}
    def put(self):
        id = request.form.get('id')
        user =queryById(User,id)
        user.name=request.form.get('name')
        add(user)
        return {'state':'ok','msg':user.name+'已更新完成'}

class ImageApi(Resource):
    img_fields={
        'id':fields.Integer,
        'name':fields.String,
        'url':fields.String
    }

    def get(self):
        return {'state':'ok',
                'data':[{'name':'科技','url':'/static/image/A6.jpg'}]}



class MusicApi(Resource):
    #穿件request参数的解析器
    parser = reqparse.RequestParser()
    # 向参数解析器中添加请求参数说明
    parser.add_argument('key',dest='name',type=str,required = True,help='必须提供name 的参数')
    parser.add_argument('id',type=int,help='请确定id的值是否为数值类型')
    parser.add_argument('tag',action='append',required=True,help='至少提供一个类型')
    parser.add_argument('session',location='cookies',required=True)
    music_fields={'id':fields.Integer,
                  'name':fields.String,
                  'music_url':fields.String(attribute='url'),
                  'singer':fields.String}
    get_out_fields={
        'state':fields.String(default='ok'),
        'data':fields.Nested(music_fields)
    }
    @marshal_with(get_out_fields)
    def get(self):

        # 按name 检索
        #通过request参数解析器，开始解析请求参数
        #如果请求三个不能满足条件，则直接返回参数相关的help说明
        args = self.parser.parse_args()
        #从args中读取name请求参数的值
        name = args.get('name')
        tag=args.get('tag')
        # 用localtion获取采参数
        session = args.get('session')
        return {'msg':'搜索{}音乐不存在{}标签'.format(name,tag)}

        # # 查询所有Image
        # musics=queryAll(Music).all()
        # data={
        #     'data':musics
        # }
        # return (data,self.get_out_fields)

class UploadApi(Resource):

    # 定制输入的参数
    parser = reqparse.RequestParser()
    parser.add_argument("img",
                        type=FileStorage,
                        location='files',
                        required=True,
                        help='必须提供一个名为img的File表单参数')

    def post(self):
        # 验证 请求参数是否满足条件
        args = self.parser.parse_args()

        # 保存上传的文件
        uFile:FileStorage = args.get('img')
        print('上传的文件名:', uFile.filename)

        newFileName = str(uuid.uuid4()).replace('-', '')
        newFileName += "."+ uFile.filename.split('.')[-1]

        uFile.save(os.path.join(settings.MEDIA_DIR, newFileName))

        return {'msg':'上传成功!',
                'path':'/static/uploads/{}'.format(newFileName)}

# 将资源添加到API中，并声明uri
# ------------------------
api.add_resource(UserApi, '/user/')
api.add_resource(ImageApi,'/images/')
api.add_resource(MusicApi,'/music/')
api.add_resource(UploadApi,'/upload/')