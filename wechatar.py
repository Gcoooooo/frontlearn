import datetime
import logging
import logging.handlers
import os
import base64
import threading
from flask import Flask, request, render_template, request, make_response, app, redirect, jsonify, session, url_for
import hashlib
import urllib.request
import json
import ctypes
import pymysql.cursors
import configparser
import gevent
import random
from flask_cors import CORS, cross_origin
import math
import hmac
import time

LOG_FILE = 'tst.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=100 * 1024 * 1024, backupCount=10)
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

logger = logging.getLogger('tst')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

config = configparser.ConfigParser()

# initial mysql connetcion
with open('wechatar.conf', 'r') as cfgfile:
    config.read_file(cfgfile)
    db_config = config._sections['db']
    wechat_config = config._sections['wechat']
db = pymysql.connect(**db_config)

app.debug = True
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.secret_key = 'sdkSGF2F346sdfjJPJ'


# @app.route('/test/')
# def test():
#     logger.info('test 1 !!!')
#     if 'lottery_ready' not in session:
#         session['lottery_ready'] = 0
#     pass
#     session['lottery_ready'] = 1
#     return redirect('/test2/')

# @app.route('/test2/')
# def test2():
#     if session.get('lottery_ready') == 1:
#         logger.info('test 2 !!!')
#         session['lottery_ready'] = 0
#         return str(session.get('lottery_ready'))
#     else:
#         return redirect('/test/')

@app.route('/')
def root():
    return render_template('root.html')


@app.route('/ar/')
def ar():
    session['content'] = request.args.get('type')
    return redirect('/ar/' + session['content'])


@app.route('/ar/lottery/')
def ar_lottery():
    if ('lottery_lock' not in session) or (session.get('lottery_lock') == 1):
        session['lottery_lock'] = 0
    if 'content' not in session:
        session['content'] = 'lottery'
    if session.get('openid'):
        session['lottery_lock'] = 1
        return render_template('morelogo.html', openid=session.get('openid'))
    else:
        return redirect(
            'https://open.weixin.qq.com/connect/oauth2/authorize?appid=' + wechat_config['appid'] + '&redirect_uri=' + wechat_config['redirect_uri'] + '&response_type=code&scope=snsapi_userinfo&#wechat_redirect')
        #return redirect('https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx2e7288fdd5f458b7&redirect_uri=http%3a%2f%2fwx.10085.cn%2ftestoauth%2f&response_type=code&scope=snsapi_userinfo&#wechat_redirect')

# @app.route('/vr/lottery/')
# def vr_lottery():
#     if 'openid' not in session:
#         return redirect('/ar/lottery/')
#     openid = session.get('openid')
#     sita = math.radians(random.randint(80, 100))
#     phai_candidate_deg = list(range(-70, -20)) + list(range(200, 251))
#     phai = math.radians(random.choice(phai_candidate_deg))
#     r = 15
#     x = r * math.sin(sita) * math.cos(phai)
#     y = r * math.cos(sita)
#     z = r * math.sin(sita) * math.sin(phai)
#     background_mp3_url = "https://oss.wechatvr.org/chinamobile/background_mp3.mp3"
# #    background_url = "https://oss.wechatvr.org/chinamobile/qj" + str(random.randint(1, 5)) + ".jpg"
#     background_url = "https://oss.wechatvr.org/chinamobile/qj" + str(random.choice([1,2,3,5])) + ".jpg"
#     logo_url_random = ('https://oss.wechatvr.org/chinamobile/mobile_ios_logo.png', 'https://oss.wechatvr.org/meetA3s/logo_10086.png', 'https://oss.wechatvr.org/meetA3s/logo_MIGU.png')
#     logo_url = logo_url_random[random.randint(0, 2)]
#     session['lottery_lock'] = 1
#     return render_template('A3s_ios.html',x=x, y=y, z=z, background_url=background_url,
#                            logo_url=logo_url,background_mp3_url=background_mp3_url,openid=openid)


# @app.route('/ar/chinamobile/')
# def chinamobile_auth():
#     if 'content' not in session:
#         session['content'] = 'chinamobile'
#     if session.get('openid'):
#         scanline_url = "https://oss.wechatvr.org/chinamobile/scanline.png"
#         logo1_url = "https://oss.wechatvr.org/chinamobile/logo1.png"
#         logo2_url = "https://oss.wechatvr.org/chinamobile/logo2.png"
#         return render_template('armobile.html', openid=session.get('openid'), scanline_url=scanline_url,
#                                logo1_url=logo1_url,
#                                logo2_url=logo2_url)
#     else:
#         return redirect(
#             'https://open.weixin.qq.com/connect/oauth2/authorize?appid=' + wechat_config['appid'] + '&redirect_uri=' + wechat_config['redirect_uri'] + '&response_type=code&scope=snsapi_userinfo&#wechat_redirect')

#
# @app.route('/model_control/')
# def model_control():
#         return render_template('model_control.html', openid='ox5HZ1HOZ0j0Be3tvYF7WqO8QWKs')
#
#
# @app.route('/ar/fenjiu/')
# def ar_fenjiu():
#     return render_template('arfenjiu.html')
#
# @app.route('/Fen/')
# def Fen():
#     return render_template('Fen.html')


@app.route('/image-recong/chinamobile/', methods=['POST'])
def recong_chinamobile():
    #pic = request.get_data()
    #base64pic = pic[23:]
    #imgdata = base64.b64decode(base64pic)
    #filename = 'mismatch_pic/' + str(time.time()) + '.jpeg'
    #file = open(filename, 'wb')
    #file.write(imgdata)
    #file.close()
    #so = ctypes.cdll.LoadLibrary
    #lib = so("./libsurf.so")
    #result = lib.surf_match(
        #"serverpic/c1.jpg serverpic/c2.jpg serverpic/c3.jpg serverpic/c4.jpg serverpic/c5.jpg serverpic/c6.jpg".encode(
            #"utf-8"), filename.encode("utf-8"))
    #cmd = './surf serverpic/c1.jpg serverpic/c2.jpg serverpic/c3.jpg serverpic/c4.jpg serverpic/c5.jpg serverpic/c6.jpg ' + filename
    #logger.info(cmd)
    #logger.info(result)
    #if result == 1:
        #os.system("mv " + filename + " match_pic/")
        #return 'match'
    #else:
        #return 'mismatch'
    return 'match'

# @app.route('/turntable/')
# def turntable():
#     if ('lottery_lock' not in session) or (session.get('lottery_lock') == 0):
#         return redirect('/ar/lottery/')
#     if 'openid' not in session:
#         return redirect('/ar/lottery/')
#     session['lottery_lock'] = 0
#     return render_template('turntable.html')


@app.route('/prize_new/', methods=['GET','POST'])
def get_prize_new():
    # if ('openid' not in session) or session.get('openid') == None:
        # return redirect('https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx2e7288fdd5f458b7&redirect_uri=http%3a%2f%2fwx.10085.cn%2ftestoauth%2f&response_type=code&scope=snsapi_userinfo&#wechat_redirect')
    #if ('lock' not in session) or (session.get('lock') == 1):
        #return redirect('https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx2e7288fdd5f458b7&redirect_uri=http%3a%2f%2fwx.10085.cn%2ftestoauth%2f&response_type=code&scope=snsapi_userinfo&#wechat_redirect')
    #session['lock']=1
    # if ('lock' not in session) or (session.get('lock') == 1):
        # return redirect('https://open.weixin.qq.com/connect/oauth2/authorize?appid=' + wechat_config['appid'] + '&redirect_uri=' + wechat_config['redirect_uri'] + '&response_type=code&scope=snsapi_userinfo&#wechat_redirect')
    openid = session['openid']
    #openid="test"
    status = session['status']
    #subscribe = session['subscribe']
    logger.info(status)

    time_now = datetime.datetime.now()
    time_now_str = time_now.strftime("%Y-%m-%d %H:%M:%S")
    date = time_now.strftime("%Y-%m-%d")
    dict_new = { 'date': date, 'openid': openid, 'rest_number': 2, 'time_now_str': time_now_str}

    if status == '3001':
        try:
            db.ping()
            with db.cursor() as cursor:
                sql = '''INSERT INTO lottery_info(openid,date,rest_number) VALUES("{openid}","{date}","{rest_number}");'''
                sql = sql.format(**dict_new)
                cursor.execute(sql)
                db.commit()
        except Exception as err:
            db.rollback()
            logger.info(err)
        prize = 'coin'
        return jsonify({'prize': prize})

    # 先查看user该日的抽奖次数是否已经用�?
    try:           # 先判用户是否有过抽奖记录
        db.ping()
        with db.cursor() as cursor:
            sql = '''SELECT count(*) FROM lottery_info where openid="{openid}" and date="{date}"'''
            sql = sql.format(**dict_new)
            cursor.execute(sql)
            # global prize
            openid_exist = cursor.fetchall()
            openid_exist = openid_exist[0][0]
            logger.info('openid_exist'+str(openid_exist))
            db.commit()
    except Exception as err:
        db.rollback()
        logger.info(err)
    if openid_exist == 1:   # 有抽奖记录的情况�?
        try:
            db.ping()
            with db.cursor() as cursor:
                sql = '''SELECT rest_number FROM lottery_info where openid="{openid}" and date="{date}"'''
                sql = sql.format(**dict_new)
                cursor.execute(sql)
                # global prize
                rest_num = cursor.fetchall()
                rest_num = rest_num[0][0]
                logger.info('rest_num' + str(rest_num))
                db.commit()
        except Exception as err:
            db.rollback()
            logger.info(err)
        if rest_num<1:   # 如果抽奖机会已经用完
            prize = 'thanks'
            return jsonify({'prize': prize})
        else:   # 如果还有抽奖机会
            try:
                db.ping()
                with db.cursor() as cursor:
                    sql = '''UPDATE lottery_info SET rest_number=rest_number-1 where openid="{openid}" and date="{date}"'''
                    sql = sql.format(**dict_new)
                    cursor.execute(sql)
                    db.commit()
            except Exception as err:
                db.rollback()
                logger.info(err)
    else:   # 如果用户还没有抽奖记�?
        try:
            db.ping()
            with db.cursor() as cursor:
                sql = '''INSERT INTO lottery_info(openid,date,rest_number) VALUES("{openid}","{date}","{rest_number}");'''
                sql = sql.format(**dict_new)
                cursor.execute(sql)
                db.commit()
        except Exception as err:
            db.rollback()
            logger.info(err)


    # 在奖池里拿一个将给user
    try:
        db.ping()
        with db.cursor() as cursor:
            sql = '''SELECT count(*) FROM prize_pool_new where release_time<="{time_now_str}" and isnull=0'''
            sql = sql.format(**dict_new)
            cursor.execute(sql)
            # global prize
            prize_exist = cursor.fetchall()
            prize_exist = prize_exist[0][0]
            logger.info('prize_exist'+str(prize_exist))
            db.commit()
    except Exception as err:
        db.rollback()
        logger.info(err)
    if prize_exist == 0:   # 如果没有�?
        prize = 'thanks'
        return jsonify({'prize': prize})
    else:   # 有奖
        try:
            db.ping()
            with db.cursor() as cursor:
                sql = '''SELECT prize_type,release_time FROM prize_pool_new where release_time<="{time_now_str}" and isnull=0 limit 1'''
                sql = sql.format(**dict_new)
                cursor.execute(sql)
                # global prize
                result_info = cursor.fetchall()
                get_prize = result_info[0][0]
                get_time = result_info[0][1]
                # logger.info('prize'+get_prize)
                db.commit()
        except Exception as err:
            db.rollback()
            logger.info(err)
        prize = get_prize
        logger.info(get_time)
        time_dict = {'get_time': get_time}
        try:
            db.ping()
            with db.cursor() as cursor:
                sql = '''UPDATE prize_pool_new SET isnull=1 where release_time="{get_time}"'''
                sql = sql.format(**time_dict)
                logger.info(sql)
                cursor.execute(sql)
                db.commit()
        except Exception as err:
            db.rollback()
            logger.info(err)

        return jsonify({'prize': prize,'openid':openid})


@app.route("/userPrizeInfo_new/", methods = ['POST'])
def userPrizeInfo_new():
    user_prize_info = request.get_json()
    user_prize_info['openid'] = session.get('openid')
    user_prize_info['prize_type'] = 'vivo'
    logger.info(user_prize_info)
    logger.info(len(user_prize_info))
    user_prize_info['get_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # if user_prize_info['prize_type'] == 'vivo':
    try:
        db.ping()
        with db.cursor() as cursor:
            sql = '''INSERT INTO winning_info_new(openid,get_time,phone_number,prize_type,username,address,idcard) VALUES
            ("{openid}","{get_time}","{phone_number}","{prize_type}","{username}","{address}","{idcard}");'''
            sql = sql.format(**user_prize_info)
            cursor.execute(sql)
            db.commit()
    except Exception as err:
        db.rollback()
        logger.info(err)

    return jsonify({'update': 'True'})

@app.route("/get_share/",methods=['GET','POST'])
def get_share():
    share_info = request.get_json()
    # share_info['openid'] = session.get('openid')
    time_now =  datetime.datetime.now()
    time_day = time_now.strftime("%Y-%m-%d")
    share_info['date'] = time_day
    #logger.info('share_info'+share_info)
    logger.info(share_info)
    share_info['prize_chance'] = 4
    share_info['share_chance'] = 0
    if share_info['shared']:
        try:
            db.ping()
            with db.cursor() as cursor:
                sql = '''SELECT count(*) FROM lottery_info where date="{date}" and openid="{openid}"'''
                sql = sql.format(**share_info)
                cursor.execute(sql)
                # global prize
                lottery_exist = cursor.fetchall()
                lottery_exist = lottery_exist[0][0]
                logger.info('lottery_exist' + str(lottery_exist))
                db.commit()
        except Exception as err:
            db.rollback()
            logger.info(err)
        if lottery_exist == 0:
            try:
                db.ping()
                with db.cursor() as cursor:
                    sql = '''INSERT INTO lottery_info(openid,date,rest_number) VALUES("{openid}","{date}","{prize_chance}");'''
                    sql = sql.format(**share_info)
                    cursor.execute(sql)
                    db.commit()
            except Exception as err:
                db.rollback()
                logger.info(err)
        else:
            try:
                db.ping()
                with db.cursor() as cursor:
                    sql = '''UPDATE lottery_info SET rest_number=rest_number+2 where date="{date}" and openid="{openid}"'''
                    sql = sql.format(**share_info)
                    logger.info(sql)
                    cursor.execute(sql)
                    db.commit()
            except Exception as err:
                db.rollback()
                logger.info(err)

        try:
            db.ping()
            with db.cursor() as cursor:
                sql = '''SELECT count(*) FROM share_info where date="{date}" and openid="{openid}"'''
                sql = sql.format(**share_info)
                cursor.execute(sql)
                # global prize
                share_exist = cursor.fetchall()
                share_exist = share_exist[0][0]
                logger.info('share_exist' + str(share_exist))
                db.commit()
        except Exception as err:
            db.rollback()
            logger.info(err)
        if share_exist == 0:
            try:
                db.ping()
                with db.cursor() as cursor:
                    sql = '''INSERT INTO share_info(openid,date,rest_number) VALUES("{openid}","{date}","{share_chance}");'''
                    sql = sql.format(**share_info)
                    cursor.execute(sql)
                    db.commit()
            except Exception as err:
                db.rollback()
                logger.info(err)
        else:
            try:
                db.ping()
                with db.cursor() as cursor:
                    sql = '''UPDATE share_info SET share_chance=share_chance-1 where date="{date}" and openid="{openid}"'''
                    sql = sql.format(**share_info)
                    logger.info(sql)
                    cursor.execute(sql)
                    db.commit()
            except Exception as err:
                db.rollback()
                logger.info(err)


@app.route("/chance_new/",methods=['GET','POST'])
def chance_new():
    openid = session.get('openid')
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    chance_dict = {'openid':openid, 'date':date, 'prize_chance': 3, 'share_chance': 1}

    try:  # 先判用户是否有过抽奖记录
        db.ping()
        with db.cursor() as cursor:
            sql = '''SELECT count(*) FROM lottery_info where openid="{openid}" and date="{date}"'''
            sql = sql.format(**chance_dict)
            cursor.execute(sql)
            openid_exist = cursor.fetchall()
            openid_exist = openid_exist[0][0]
            # logger.info('openid_exist'+str(openid_exist))
            db.commit()
    except Exception as err:
        db.rollback()
        logger.info(err)
    if openid_exist == 0:  # 无抽奖记录的情况�?
        try:
            db.ping()
            with db.cursor() as cursor:
                sql = '''INSERT INTO lottery_info(openid,date,rest_number) VALUES("{openid}","{date}","{prize_chance}");'''
                sql = sql.format(**chance_dict)
                cursor.execute(sql)
                db.commit()
        
        except Exception as err:
            db.rollback()
            logger.info(err)
    try:
        db.ping()
        with db.cursor() as cursor:
            sql_chance = '''SELECT rest_number FROM lottery_info where openid="{openid}" and date="{date}";'''
            sql_chance = sql_chance.format(**chance_dict)
            # logger.info(sql_chance)
            cursor.execute(sql_chance)
            prize_chance = cursor.fetchall()
            db.commit()
    except Exception as err:
        db.rollback()
        logger.info(err)
    prize_chance =prize_chance[0][0]

    # share_chance

    try:  # 先判用户是否有过抽奖记录
        db.ping()
        with db.cursor() as cursor:
            sql = '''SELECT count(*) FROM share_info where openid="{openid}" and date="{date}"'''
            sql = sql.format(**chance_dict)
            cursor.execute(sql)
            openid_exist = cursor.fetchall()
            openid_exist = openid_exist[0][0]
            # logger.info('openid_exist'+str(openid_exist))
            db.commit()
    except Exception as err:
        db.rollback()
        logger.info(err)
    if openid_exist == 0:  # 无抽奖记录的情况�?
        try:
            db.ping()
            with db.cursor() as cursor:
                sql = '''INSERT INTO share_info(openid,date,share_chance) VALUES("{openid}","{date}","{share_chance}");'''
                sql = sql.format(**chance_dict)
                cursor.execute(sql)
                db.commit()
        except Exception as err:
            db.rollback()
            logger.info(err)
    try:
        db.ping()
        with db.cursor() as cursor:
            sql_chance = '''SELECT share_chance FROM share_info where openid="{openid}" and date="{date}";'''
            sql_chance = sql_chance.format(**chance_dict)
            # logger.info(sql_chance)
            cursor.execute(sql_chance)
            share_chance = cursor.fetchall()
            db.commit()
    except Exception as err:
        db.rollback()
        logger.info(err)
    share_chance =share_chance[0][0]

    return jsonify({'prize_chance': prize_chance, 'share_chance':share_chance})

@app.route("/jssdktoken/", methods=['GET', 'POST'])
def jssdktoken():
    try:
        db.ping()
        with db.cursor() as cursor:
            sql_token = '''SELECT puttime FROM token where itemid= 1;'''
            # logger.info(sql_chance)
            cursor.execute(sql_token)
            puttime = cursor.fetchall()
            puttime = puttime[0][0]
            db.commit()
    except Exception as err:
        db.rollback()
        logger.info(err)

    tmp = int(time.time())
    # f = open('static/access_token.txt', 'r')
    # lines = f.readlines(2000)
    # f.close()
    if (tmp - float(puttime) > 7000):
        rqst = urllib.request.urlopen(
            'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxb1bcc9cc0803b026&secret=b22c41bdbc7b8b84412b794e12d5fa23')
        res = rqst.read()
        res = res.decode("utf-8")
        # logger.info('res:' + res)
        r_res = json.loads(res)
        newtoken = r_res['access_token']
        newputtime = str(time.time())
        token_dict = {'token':newtoken, 'puttime':newputtime}
        if r_res != None:
            try:
                db.ping()
                with db.cursor() as cursor:
                    sql = '''UPDATE token SET token="{token}",puttime="{puttime}" where itemid=1'''
                    sql = sql.format(**token_dict)
                    logger.info(sql)
                    cursor.execute(sql)
                    db.commit()
            except Exception as err:
                db.rollback()
                logger.info(err)
            # access_token = r_res['access_token']
            # expires_in = r_res['expires_in']
            # f = open('static/access_token.txt', 'w')
            # lines[1] = access_token + "\n"
            # lines[0] = str(time.time()) + "\n"
            # f.writelines(lines)
            # f.close()

        if newtoken:
            rqst2 = urllib.request.urlopen(
                'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=' + newtoken + '&type=jsapi')
            res2 = rqst2.read().decode('utf-8')
            ticket = json.loads(res2)
            JSAPI_TICKET = ticket['ticket']
            ticket_dic={'ticket':JSAPI_TICKET}
            try:
                db.ping()
                with db.cursor() as cursor:
                    newtoken_sql = '''UPDATE token SET ticket="{ticket}" where itemid=1'''
                    newtoken_sql = newtoken_sql.format(**ticket_dic)
                    logger.info(newtoken_sql)
                    cursor.execute(newtoken_sql)
                    db.commit()
            except Exception as err:
                db.rollback()
                logger.info(err)
    else:
        try:
            db.ping()
            with db.cursor() as cursor:
                sql_ticket = '''SELECT ticket FROM token where itemid= 1;'''
                logger.info(sql_ticket)
                cursor.execute(sql_ticket)
                JSAPI_TICKET = cursor.fetchall()
                JSAPI_TICKET = JSAPI_TICKET[0][0]
                db.commit()
        except Exception as err:
            db.rollback()
            logger.info(err)
    logger.info(JSAPI_TICKET)
    now = str(int(time.time()))
    noncestr = '%s' % time.time()
    # this url need to get from front end!!!!!!
    url = request.get_json()['url']
    logger.info(url)
    signature = 'jsapi_ticket=' + JSAPI_TICKET + '&noncestr=' + noncestr + '&timestamp=' + now + '&url=' + url
    logger.info(signature)
    m = hashlib.sha1()
    signature = signature.encode('utf-8')
    m.update(signature)
    signature = m.hexdigest()
    logger.info(signature)
    signature = {"timestamp": now, "nonceStr": noncestr, "signature": signature, "url": url}
    logger.info(signature)
    return jsonify(signature)

# @app.route("/jssdktoken/", methods=['GET', 'POST'])
# def jssdktoken():
    # url = request.get_json()['url']
    # rqsturl='http://221.176.66.251/operation/api/out/getJsSignature?accountId=5109afce-6b8f-4e9f-b706-36e7bf3e2f39&url='+url
    # logger.info('jssign_rqsturl:'+rqsturl)
    # jssign_rqst = urllib.request.urlopen(rqsturl)
    # jssign_json = jssign_rqst.read().decode("utf-8")
    # logger.info('jssign_json:'+jssign_json)
    # return jssign_json
    # #jssign_dict = json.loads(jssign_json)  # transcode the json value to python format
    # #STATUS=jssign_dict['status']
    # #if(STATUS==0):
    # #    jssign=jssign_dict['jsSignature']
    # #    timestamp=jssign_dict['timeStamp']
    # #    noncestr=jssign_dict['nonceStr']
     # #   return jsonify({"timestamp":timestamp, "nonceStr":noncestr, "signature":jssign, "url":url})
    # #else:
    # #    return jsonify({"timestamp":'None', "nonceStr":'None', "signature":'None', "url":url})

@app.route("/scanbehavior/", methods=['POST'])
def scanbehavior():
    scan_behavior_info = request.get_json()
    logger.info(scan_behavior_info)

    try:
        db.ping()
        with db.cursor() as cursor:
            sql = '''INSERT INTO scan_behavior(openid,url,location,terminal,os,browser,visit_time) VALUES
            ("{openid}","{url}","{location}","{terminal}","{os}","{browser}","{visit_time}");'''
            scan_behavior_info['visit_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql = sql.format(**scan_behavior_info)
            cursor.execute(sql)
            db.commit()
    except Exception as err:
        db.rollback()
        logger.info(err)
    return jsonify({'store': True})


# @app.route('/chinamobile/', methods=['POST'])
# def chinamobile():
#     pic = request.get_data()
#     base64pic = pic[23:]
#     imgdata = base64.b64decode(base64pic)
#     filename = 'mismatch_pic/' + str(time.time()) + '.jpeg'
#     file = open(filename, 'wb')
#     file.write(imgdata)
#     file.close()
#     so = ctypes.cdll.LoadLibrary
#     lib = so("./libsurf.so")
#     result = lib.surf_match(
#         "serverpic/c1.jpg serverpic/c2.jpg serverpic/c3.jpg serverpic/c4.jpg serverpic/c5.jpg serverpic/c6.jpg".encode(
#             "utf-8"), filename.encode("utf-8"))
#     cmd = './surf serverpic/c1.jpg serverpic/c2.jpg serverpic/c3.jpg serverpic/c4.jpg serverpic/c5.jpg serverpic/c6.jpg ' + filename
#     logger.info(cmd)
#     logger.info(result)
#     if result == 1:
#         os.system("mv " + filename + " match_pic/")
#         return 'match'
#     else:
#         return 'mismatch'


# @app.route('/mobile_ios/<openid>')
# def mobile_ios(openid):
#     sita = math.radians(random.randint(80, 100))
#     phai_candidate_deg = list(range(-70, -20)) + list(range(200, 251))
#     phai = math.radians(random.choice(phai_candidate_deg))
#     r = 15
#     x = r * math.sin(sita) * math.cos(phai)
#     y = r * math.cos(sita)
#     z = r * math.sin(sita) * math.sin(phai)
#     background_mp3_url = "https://oss.wechatvr.org/chinamobile/background_mp3.mp3"
#     logo_url = "https://oss.wechatvr.org/chinamobile/mobile_ios_logo.png"
# #    background_url = "https://oss.wechatvr.org/chinamobile/qj" + str(random.randint(1, 5)) + ".jpg"
#     background_url = "https://oss.wechatvr.org/chinamobile/qj" + str(random.choice([1,2,3,5])) + ".jpg"
#     # background_url = "/static/image/qj" + str(random.randint(1,5)) + ".jpg"
#     return render_template('mobile_ios.html', openid=openid, x=x, y=y, z=z, background_url=background_url,
#                            logo_url=logo_url,background_mp3_url=background_mp3_url)


# @app.route('/txvideo/<openid>')
# def txvideo(openid):
#     mobile_logo_url = "https://oss.wechatvr.org/chinamobile/mobile_logo.jpg"
#     poster_url = "https://oss.wechatvr.org/chinamobile/poster.jpg"
#     shareBtn_url = "https://oss.wechatvr.org/chinamobile/shareBtn.png"
#     pointer_url = "https://oss.wechatvr.org/chinamobile/pointer.png"
#     return render_template('txvideo.html', openid=openid, mobile_logo_url=mobile_logo_url, poster_url=poster_url,
#                            shareBtn_url=shareBtn_url, pointer_url=pointer_url)


# @app.route('/mobile_weibo/')
# def mobile_weibo():
#     sita = math.radians(random.randint(80, 100))
#     phai_candidate_deg = list(range(-70, -20)) + list(range(200, 251))
#     phai = math.radians(random.choice(phai_candidate_deg))
#     r = 15
#     x = r * math.sin(sita) * math.cos(phai)
#     y = r * math.cos(sita)
#     z = r * math.sin(sita) * math.sin(phai)
#     background_mp3_url = "https://oss.wechatvr.org/chinamobile/background_mp3.mp3"
#     logo_url = "https://oss.wechatvr.org/chinamobile/mobile_ios_logo.png"
# #    background_url = "https://oss.wechatvr.org/chinamobile/qj" + str(random.randint(1, 5)) + ".jpg"
#     background_url = "https://oss.wechatvr.org/chinamobile/qj" + str(random.choice([1,2,3,5])) + ".jpg"
#
#     # background_url = "/static/image/qj" + str(random.randint(1,5)) + ".jpg"
#     return render_template('mobile_weibo.html', openid='weibo', x=x, y=y, z=z, background_url=background_url,
#                            logo_url=logo_url,background_mp3_url=background_mp3_url)


# @app.route('/fenjiu/', methods = ['POST'])
# def fenjiu():
#     pic = request.get_data()
#     base64pic = pic[23:]
#     imgdata=base64.b64decode(base64pic)
#     filename = 'mismatch_pic/' + str(time.time()) + '.jpeg'
#     file=open(filename,'wb')
#     file.write(imgdata)
#     file.close()
#     so = ctypes.cdll.LoadLibrary
#     lib = so("./libsurf2.so")
#     result = lib.surf_match("serverpic/1.png serverpic/5.png serverpic/2.png serverpic/4.png serverpic/11.png serverpic/8.png serverpic/9.png serverpic/10.png".encode("utf-8"),filename.encode("utf-8"))
#     cmd = "serverpic/1.png serverpic/5.png serverpic/2.png serverpic/4.png serverpic/11.png serverpic/8.png serverpic/9.png serverpic/10.png"
#     logger.info(cmd)
#     logger.info(result)
#     if result==1:
#         os.system("mv " + filename + " match_pic/")
#         return 'match'
#     else:
#         return 'mismatch'
#@app.route('/webrtc_test_x5/')
#def webrtc_test_x5():
   # return render_template('webrtc_test_x5.html')
#@app.route('/webrtc_test/')
#def webrtc_test():
   # return render_template('webrtc_test.html')
#@app.route('/tracking_test/')
#def tracking_test():
#    return render_template('tracking_test.html')
#@app.route('/canvas_test/')
#def canvas_test():
#    return render_template('canvas_test.html')
#@app.route('/get_device_info/')
#def get_device_info():
#    return render_template('get_device_info.html')

#@app.route('/jscv_test/')
#def jsfeat():
#    return render_template('jscv_test.html')

#@app.route('/cubetest/')
#def cubetest():
#    return render_template('cubetest.html')
    
@app.route('/ar/luckyCat/')
def luckyCat():
    #if 'openid' not in session or session.get('openid') == None:
        #return redirect('https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx2e7288fdd5f458b7&redirect_uri=http%3a%2f%2fwx.10085.cn%2ftestoauth%2f&response_type=code&scope=snsapi_userinfo&#wechat_redirect')
    if ('lock' not in session) or (session.get('lock') == 1):
        return redirect('https://open.weixin.qq.com/connect/oauth2/authorize?appid=' + wechat_config['appid'] + '&redirect_uri=' + wechat_config['redirect_uri'] + '&response_type=code&scope=snsapi_userinfo&#wechat_redirect')
    session['lock']=1
    OPENID=session['openid']
    STATUS=session['status']
    logger.info(OPENID)
    #SUBSCRIBE=session['subscribe']
    #PHONESTATUS=session['phonestatus']
    return render_template('luckyCat.html',openid=OPENID,status=STATUS)
   # return render_template('luckyCat.html')


@app.route('/ar/luckyCat_ios/')
def luckyCat_ios():
    #if 'openid' not in session or session.get('openid') == None:
        #return redirect('https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx2e7288fdd5f458b7&redirect_uri=http%3a%2f%2fwx.10085.cn%2ftestoauth%2f&response_type=code&scope=snsapi_userinfo&#wechat_redirect')
    #if ('lock' not in session) or (session.get('lock') == 1):
        #return redirect('/ar/luckyCat')
        #return redirect('https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx2e7288fdd5f458b7&redirect_uri=http%3a%2f%2fwx.10085.cn%2ftestoauth%2f&response_type=code&scope=snsapi_userinfo&#wechat_redirect')
    # if ('lock' not in session) or (session.get('lock') == 1):
        # return redirect('https://open.weixin.qq.com/connect/oauth2/authorize?appid=' + wechat_config['appid'] + '&redirect_uri=' + wechat_config['redirect_uri'] + '&response_type=code&scope=snsapi_userinfo&#wechat_redirect')
    # session['lock']=1
    OPENID=session['openid']
    logger.info(OPENID)
    STATUS=session['status']
    #SUBSCRIBE=session['subscribe']
    #PHONESTATUS=session['phonestatus']
    sita = math.radians(random.randint(80, 100))
    phai_candidate_deg = list(range(-70, -20)) + list(range(200, 251))
    phai = math.radians(random.choice(phai_candidate_deg))
    r = 15
    x = r * math.sin(sita) * math.cos(phai)
    y = r * math.cos(sita)
    z = r * math.sin(sita) * math.sin(phai)
    background_mp3_url = "https://oss.wechatvr.org/chinamobile/background_mp3.mp3"
#    background_url = "https://oss.wechatvr.org/chinamobile/qj" + str(random.randint(1, 5)) + ".jpg"
    background_url = "https://oss.wechatvr.org/chinamobile/qj" + str(random.choice([1,2,3,5])) + ".jpg"
    logo_url_random = ('https://oss.wechatvr.org/chinamobile/mobile_ios_logo.png', 'https://oss.wechatvr.org/meetA3s/logo_10086.png')
    logo_url = logo_url_random[random.randint(0, 1)]
    session['lottery_lock'] = 1
    return render_template('luckyCat_ios.html',x=x, y=y, z=z, background_url=background_url,logo_url=logo_url,background_mp3_url=background_mp3_url,openid=OPENID,status=STATUS)
    #return render_template('luckyCat_ios.html',x=x, y=y, z=z, background_url=background_url,logo_url=logo_url,background_mp3_url=background_mp3_url,openid=OPENID)


# @app.route('/testoauth/', methods=['GET', 'POST'])
# def testoauth():
    # CODE = request.args.get('code')
    # if(CODE):
        # logger.info(CODE)
        # CODE=str(CODE)
        # #TIMESTAMP = str(int(round(time.time() * 1000)))
        # #logger.info(TIMESTAMP)
        # #NONCE = random.randint(100000, 999999)
        # #NONCE = str(NONCE)
        # #logger.info(NONCE)
        # #sign = 'cmos10086fn3bh40s1dyogpbh' + NONCE + TIMESTAMP
        # #logger.info(sign)
        # #token='qD9EUFCSJVQZJeDn'
        # #sign = sign.encode('utf-8')
        # #token = token.encode('utf-8')
        # #signature = hmac.new(token, sign, digestmod=hashlib.sha256).hexdigest()
        # #signature = str(signature)
        # #logger.info(signature)
        # #params = urllib.parse.urlencode({'appId': 'cmos10086fn3bh40s1dyogpbh', 'timestamp': TIMESTAMP, 'nonce': NONCE,'signature':signature})
        # #url='http://221.176.66.251/api/out/fans/'+CODE+'?%s' % params
        # url='http://221.176.66.251/operation/api/out/getFansInfoByOauth2?accountId=5109afce-6b8f-4e9f-b706-36e7bf3e2f39&code='+CODE
        # logger.info(url)
        # getuserinfo_rqst = urllib.request.urlopen(url)
        # getuserinfo_json = getuserinfo_rqst.read().decode("utf-8")
        # getuserinfo_dict = json.loads(getuserinfo_json)  # transcode the json value to python format
        # logger.info(getuserinfo_dict)
        # STATUS=getuserinfo_dict['status']
        # if(STATUS=='3001' or STATUS=='1000' or STATUS=='1001'):
            # STATUS=str(STATUS)
            # MESSAGE=getuserinfo_dict['message']
            # OPENID=getuserinfo_dict['openid']
            # logger.info('status:'+STATUS+' message:'+MESSAGE+' openid:'+OPENID)
            # return redirect('https://wechatvr.org/firstpage/?openid='+OPENID+'&status='+STATUS)      
        # else:
            # logger.info('No Data')
            # return redirect('https://wechatvr.org/firstpage/?openid=None&status='+STATUS)
         # #MESSAGE=getuserinfo_dict['message']
        # # if(getuserinfo_dict['data']):
            # # # try:
                # # # db.ping()
                # # # with db.cursor() as cursor:
                    # # # sql = '''INSERT INTO user(openid,nickname,headimgurl,sex,city_code,city,groupid,phoneStatus,province_code,province,ranking,subscribe,telephone,bindPhoneTime,subscribe_timeloc,unBindPhoneTime,unsubscribe_time) VALUES
                    # # # ("{openid}","{nickname}","{headimgurl}","{sex}","{city_code}","{city}","{groupid}","{phoneStatus}","{province_code}","{province}","{ranking}","{subscribe}","{telephone}","{bindPhoneTime}","{subscribe_timeloc}","{unBindPhoneTime}","{unsubscribe_time}");'''
                    # # # DATA['create_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # # # sql = sql.format(**DATA)
                    # # # cursor.execute(sql)
                    # # # db.commit()
            # # # except Exception as err:  # duplicate entry
                # # # db.rollback()
                # # # logger.info(err)
            # # DATA=getuserinfo_dict['data']
            # # OPENID = DATA['openid']
            # # #session['openid'] = OPENID
            # # SUBSCRIBE=DATA['subscribe']
            # # PHONESTATUS=DATA['phoneStatus']
            # # #session['subscribe']=SUBSCRIBE
            # # #session['phoneStatus']=phoneStatus
            # # STATUS=str(STATUS)
            # # #return redirect('https://wechatvr.org/firstpage/?openid='+OPENID+'&status='+STATUS+'&phonestatus='+PHONESTATUS)
            # # #return jsonify({'openid':OPENID, 'status':STATUS,'subscribe': SUBSCRIBE, 'phoneStatus':PHONESTATUS, 'message':MESSAGE})
            # # return redirect('https://wechatvr.org/firstpage/?openid='+OPENID+'&status='+STATUS+'&subscribe='+SUBSCRIBE+'&phonestatus='+PHONESTATUS)
        # # else: 
            # # STATUS=str(STATUS)  
            # # logger.info('No Data')
            # # #return redirect('https://wechatvr.org/firstpage/openid=1')
            # # return redirect('https://wechatvr.org/firstpage/?openid=None&status='+STATUS+'&subscribe=None&phonestatus=None')
            # # #return jsonify({'openid':'ERR', 'status':STATUS,'subscribe': 'ERR', 'phoneStatus':'ERR', 'message':MESSAGE})
    # else:
        # logger.info('auth false!!!')
        # return redirect('https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx2e7288fdd5f458b7&redirect_uri=http%3a%2f%2fwx.10085.cn%2ftestoauth%2f&response_type=code&scope=snsapi_userinfo&#wechat_redirect')

@app.route('/oauth/', methods=['GET', 'POST'])
def oauth():
    STATUS='1'
    CODE = request.args.get('code')
    access_token_rqst = urllib.request.urlopen(
        'https://api.weixin.qq.com/sns/oauth2/access_token?appid=' + wechat_config['appid'] + '&secret=' + wechat_config['secret'] + '&code=' + CODE + '&grant_type=authorization_code')
    # construct and request the link, will return a json value
    access_token_json = access_token_rqst.read().decode(
        "utf-8")  # the json object must be str, not bytes, need to be transcoded
    access_token_dict = json.loads(access_token_json)  # transcode the json value to python format
    logger.info(access_token_dict)
    if 'openid' in access_token_dict:
        OPENID = access_token_dict['openid']
        ACCESS_TOKEN = access_token_dict['access_token']
        userinfo_rqst = urllib.request.urlopen(
            'https://api.weixin.qq.com/sns/userinfo?access_token=' + ACCESS_TOKEN + '&openid=' + OPENID + '&lang=zh_CN')
        userinfo_json = userinfo_rqst.read().decode('utf-8')
        userinfo = json.loads(userinfo_json)
        logger.info(userinfo)
    else:
        logger.info('auth false!!!')
        return redirect('https://open.weixin.qq.com/connect/oauth2/authorize?appid=' + wechat_config['appid'] + '&redirect_uri=' + wechat_config['redirect_uri'] + '&response_type=code&scope=snsapi_userinfo&#wechat_redirect')
    return redirect('https://wechatvr.org/firstpage/?openid='+OPENID+'&status='+STATUS)

@app.route('/firstpage/',methods=['GET', 'POST'])
def firstpage():
    OPENID = request.args.get('openid')
    STATUS = request.args.get('status')
    try:
        db.ping()
        with db.cursor() as cursor:
            sql_token = '''SELECT puttime FROM token where itemid= 1;'''
            # logger.info(sql_chance)
            cursor.execute(sql_token)
            puttime = cursor.fetchall()
            puttime = puttime[0][0]
            logger.info(puttime)
            db.commit()
    except Exception as err:
        db.rollback()
        logger.info(err)

    tmp = int(time.time())
    # f = open('static/access_token.txt', 'r')
    # lines = f.readlines(2000)
    # f.close()
    if (tmp - float(puttime) > 7000):
        rqst = urllib.request.urlopen(
            'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxb1bcc9cc0803b026&secret=b22c41bdbc7b8b84412b794e12d5fa23')
        res = rqst.read()
        res = res.decode("utf-8")
        # logger.info('res:' + res)
        r_res = json.loads(res)
        newtoken = r_res['access_token']
        token=newtoken
        newputtime = str(time.time())
        token_dict = {'token':newtoken, 'puttime':newputtime}
        if r_res != None:
            try:
                db.ping()
                with db.cursor() as cursor:
                    sql = '''UPDATE token SET token="{token}",puttime="{puttime}" where itemid=1'''
                    sql = sql.format(**token_dict)
                    logger.info(sql)
                    cursor.execute(sql)
                    db.commit()
            except Exception as err:
                db.rollback()
                logger.info(err)
        
        if newtoken:
            rqst2 = urllib.request.urlopen(
                'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=' + newtoken + '&type=jsapi')
            res2 = rqst2.read().decode('utf-8')
            ticket = json.loads(res2)
            JSAPI_TICKET = ticket['ticket']
            ticket_dic={'ticket':JSAPI_TICKET}
            try:
                db.ping()
                with db.cursor() as cursor:
                    newtoken_sql = '''UPDATE token SET ticket="{ticket}" where itemid=1'''
                    newtoken_sql = newtoken_sql.format(**ticket_dic)
                    logger.info(newtoken_sql)
                    cursor.execute(newtoken_sql)
                    db.commit()
            except Exception as err:
                db.rollback()
                logger.info(err)
    else:
        try:
            db.ping()
            with db.cursor() as cursor:
                sql_ticket = '''SELECT token FROM token where itemid= 1;'''
                logger.info(sql_ticket)
                cursor.execute(sql_ticket)
                token = cursor.fetchall()
                token = token[0][0]
                db.commit()
        except Exception as err:
            db.rollback()
            logger.info(err)

    logger.info(token)
    urlstr='https://api.weixin.qq.com/cgi-bin/user/info?access_token=' + token + '&openid='+OPENID+'&lang=zh_CN'
    logger.info(urlstr)
    info_rqst = urllib.request.urlopen(urlstr)
    info_json = info_rqst.read().decode('utf-8')
    logger.info(info_json)
    infos = json.loads(info_json)
    logger.info(infos)
    if (infos['subscribe']==0):
        STATUS='3001'
    else:
        STATUS='1001'
    session['openid']=OPENID
    logger.info(session['openid'])
    session['status']=STATUS
    logger.info(session['status'])
    session['lock'] = 0
    #session['subscribe']=SUBSCRIBE
    #session['phonestatus']=PHONESTATUS
    #return jsonify({'openi123d':OPENID, 'status':STATUS,'subscribe': SUBSCRIBE, 'phoneStatus':PHONESTATUS})
    #OPENID = request.args.get('openid')
    #TATUS = request.args.get('status')
    #SUBSCRIBE = request.args.get('subscribe')
    #PHONESTATUS = request.args.get('phonestatus')
    #return jsonify({'openid':OPENID, 'status':STATUS,'subscribe': SUBSCRIBE, 'phoneStatus':PHONESTATUS})
    #return redirect('https://wechatvr.org/sessiontest/')
    return redirect('/ar/luckyCat/') 
    #return OPENID

@app.route('/yes/',methods=['GET', 'POST'])
def sessiontest():
    OPENID = request.args.get('openid')
    logger.info('OPENID:'+OPENID)
    return 'OPENID'+OPENID


@app.route('/bindPhone/',methods=['GET', 'POST'])
def bindPhone():
    user_info = request.get_json()
    logger.info(user_info)
    logger.info('@@@@@@@@@@@@@@@@@@')
    OPENID=user_info['openid']
    user_telNum=user_info['telnum']
    user_captcha=user_info['captcha']
    STATUS=0
    #try:
        #bindPhone_rqst = urllib.request.urlopen('http://221.176.66.251/operation/api/out/telbindbycaptcha' + '?openId='+ openid + '&telNum=' + user_telNum + '&captcha=' + user_captcha)
        #bindPhone_json = bindPhone_rqst.read().decode("utf-8")
        #bindPhone_dict = json.loads(bindPhone_json)  # transcode the json value to python format
        #logger.info(bindPhone_dict)
        #STATUS=bindPhone_dict['status']
        #STATUS=str(STATUS)
        #MESSAGE=bindPhone_dict['message']
        #return jsonify({'status': STATUS,'message':MESSAGE})
    #except Exception as err:
        #logger.info('bind phone err!')
    if(STATUS==0):
        session['status']='1000'
    STATUS=str(STATUS)
    return jsonify({'openid':OPENID,'telnum': user_telNum,'captcha':user_captcha,'status': '0','message':'TestSucess!'})


@app.route('/sendCaptcha/',methods=['GET','POST'])
def sendCaptcha():
   # try:
        #user_data=request.data()
        #logger.info(user_data)
        #user_info = json.loads(request.get_data())
        user_info=request.get_json()
        logger.info(user_info)
        logger.info('@@@@@@@@@@@@@@@@@@@')
        #return user_info
        OPENID=user_info['openid']
        logger.info(OPENID)
        user_telNum=user_info['telnum']
        logger.info(user_telNum)
    #try:
        #sendCaptcha_rqst = urllib.request.urlopen('http://221.176.66.251/operation/api/out/sendCaptcha' + '?openId='+ openid + '&telNum=' + user_telNum)
        #sendCaptcha_json = sendCaptcha_rqst.read().decode("utf-8")
        #sendCaptcha_dict = json.loads(sendCaptcha_json)  # transcode the json value to python format
        #logger.info(sendCaptcha_dict)
        #STATUS=sendCaptcha_dict['status']
        #STATUS=str(STATUS)
        #MESSAGE=sendCaptcha_dict['message']
    #except Exception as err:
        #logger.info('send Captcha err!')
        return jsonify({'openid':OPENID,'telnum':user_telNum,'status': '0','message':'TestSucess!!'})
    #except Exception as err:
        #logger.info('ERROR!!')
        #return jsonify({'openid':'err','telnum':'err','status': 'err','message':'TestFail!!'})



