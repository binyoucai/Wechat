import hashlib

from flask import Blueprint, request
from wechatpy import parse_message
from wechatpy.replies import TextReply, ImageReply, VoiceReply, MusicReply

from App.settings import IMAGE_DIR, FACE_DIR, WX_TOKEN
from App.views.ext_api_tool.tencent_face import access_api
from App.views.ext_api_tool.tulingrobot import Robot
from App.views.ext_api_tool.utils import img_download, img_upload

weixin = Blueprint('wechat', __name__)


@weixin.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":  # 判断请求方式是GET请求
        my_signature = request.args.get('signature')  # 获取携带的signature参数
        my_timestamp = request.args.get('timestamp')  # 获取携带的timestamp参数
        my_nonce = request.args.get('nonce')  # 获取携带的nonce参数
        my_echostr = request.args.get('echostr')  # 获取携带的echostr参数

        token = WX_TOKEN

        # 进行字典排序
        data = [token, my_timestamp, my_nonce]
        data.sort()

        # 拼接成字符串
        temp = ''.join(data)

        # 进行sha1加密
        mysignature = hashlib.sha1(temp.encode('utf8')).hexdigest()

        # 加密后的字符串可与signature对比，标识该请求来源于微信
        print('开始验证中')
        if my_signature == mysignature:
            return my_echostr
    #  如果是post请求代表微信给我们把用户消息转发过来了
    if request.method == "POST":
        xml = request.data
        msg = parse_message(xml)
        # 文本信息
        if msg.type == 'text':
            robot = Robot()
            tuling_msgs = robot.chat(msg.content)
            msg_data = ''
            for tuling in tuling_msgs:
                msg_data += tuling
            reply = TextReply(content=msg_data, message=msg)
            xml = reply.render()
            return xml
        #  图片信息
        elif msg.type == 'image':
            name = img_download(msg.image, msg.source)
            print(IMAGE_DIR + name)
            r = access_api(IMAGE_DIR + '/' + name)
            if r == 'success':
                media_id = img_upload(msg.type, FACE_DIR + '/' + name)
                reply = ImageReply(media_id=media_id, message=msg)
            else:
                reply = TextReply(content='人脸检测失败，请上传1M以下人脸清晰的照片', message=msg)
            xml = reply.render()
            return xml
        #  语音消息
        elif msg.type == 'voice':
            reply = VoiceReply(media_id=msg.media_id, message=msg)
            xml = reply.render()
            return xml

        else:
            reply = TextReply(content='抱歉，功能构建中', message=msg)
            xml = reply.render()
            return xml
