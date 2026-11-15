"""
城市管理数字化平台 后端 API
启动：  python app.py    然后访问 http://127.0.0.1:5000/

接口分组：
  概览      GET /api/overview, /api/overview/charts
  设施      GET /api/infra, /api/infra/stats, POST /api/infra, DELETE /api/infra/<id>
  事件      GET /api/events, /api/events/stats, POST /api/events, DELETE /api/events/<id>
  任务      GET /api/tasks, /api/tasks/stats, POST /api/tasks, PUT /api/tasks/<id>
  维修      GET /api/repairs, POST /api/repairs
  环境      GET /api/devices, /api/env/trend
  下拉      GET /api/regions, /api/depts, /api/workers, /api/resources, /api/infra-types
  期末查询  GET /api/q1, /api/q2, /api/q3, /api/q4
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import db
from config import FLASK_HOST, FLASK_PORT, DEBUG
import datetime

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)


@app.before_request
def _log_req():
    if request.path.startswith('/api/'):
        body = ''
        if request.method in ('POST', 'PUT', 'DELETE'):
            try:
                body = request.get_data(as_text=True)[:200]
            except Exception:
                pass
        print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] >> {request.method} {request.path} {body}', flush=True)


@app.after_request
def _log_resp(resp):
    if request.path.startswith('/api/'):
        print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] << {request.method} {request.path} -> {resp.status_code}', flush=True)
    return resp

STATUS_MAP = {1: '待处理', 2: '处理中', 3: '已完成'}
TASK_STATUS = {1: '待开始', 2: '执行中', 3: '已完成'}
INFRA_STATUS = {1: '在用', 2: '报修', 3: '报废'}
RESOURCE_STATUS = {1: '可用', 2: '使用中', 3: '维修中'}
DEVICE_STATUS = {1: '在线', 0: '离线'}


def fmt_dt(v):
    if isinstance(v, datetime.datetime):
        return v.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(v, datetime.date):
        return v.strftime('%Y-%m-%d')
    return v


def clean(rows):
    return [{k: fmt_dt(v) for k, v in r.items()} for r in rows]


def ok(msg='成功', **extra):
    return jsonify({'code': 0, 'msg': msg, **extra})


def fail(msg, code=1):
    return jsonify({'code': code, 'msg': msg})


def db_err(e):
    s = str(e)
    if '1451' in s or 'foreign key constraint' in s:
        return '该记录被其他数据引用，无法删除（请先删除关联的子记录）'
    if '1452' in s:
        return '关联数据不存在，请检查外键引用'
    return f'操作失败：{s[:100]}'


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/api/regions')
def regions():
    return jsonify(clean(db.query("SELECT region_id,region_name FROM RT ORDER BY region_id")))


@app.route('/api/depts')
def depts():
    return jsonify(clean(db.query("SELECT dept_id,dept_name FROM DT ORDER BY dept_id")))


@app.route('/api/workers')
def workers():
    rows = clean(db.query("""SELECT w.worker_id,w.worker_name,w.dept_id,d.dept_name
        FROM WT w JOIN DT d ON w.dept_id=d.dept_id ORDER BY w.worker_id"""))
    return jsonify(rows)


@app.route('/api/resources')
def resources():
    return jsonify(clean(db.query("""SELECT resource_id,resource_name,resource_type,status
        FROM TRT ORDER BY resource_id""")))


@app.route('/api/infra-types')
def infra_types():
    return jsonify(['道路', '桥梁', '照明', '垃圾桶'])


@app.route('/api/event-types')
def event_types():
    return jsonify(['道路损坏', '设施故障', '垃圾堆积', '照明失效'])


@app.route('/api/overview')
def overview():
    infra_total = db.query_one("SELECT COUNT(*) c FROM IT")['c']
    infra_ok = db.query_one("SELECT COUNT(*) c FROM IT WHERE status=1")['c']
    infra_bad = db.query_one("SELECT COUNT(*) c FROM IT WHERE status=2")['c']
    ev_total = db.query_one("SELECT COUNT(*) c FROM ERT")['c']
    ev_done = db.query_one("SELECT COUNT(*) c FROM ERT WHERE event_status=3")['c']
    wk_total = db.query_one("SELECT COUNT(*) c FROM WT")['c']
    wk_busy = db.query_one(
        "SELECT COUNT(DISTINCT worker_id) c FROM TST WHERE task_status IN(1,2)")['c']
    dev_total = db.query_one("SELECT COUNT(*) c FROM MDT")['c']
    dev_online = db.query_one("SELECT COUNT(*) c FROM MDT WHERE online_status=1")['c']
    return jsonify({
        'infra_total': infra_total, 'infra_ok': infra_ok, 'infra_bad': infra_bad,
        'ev_total': ev_total, 'ev_done': ev_done,
        'ev_rate': round(ev_done / ev_total * 100, 1) if ev_total else 0,
        'wk_total': wk_total, 'wk_busy': wk_busy, 'wk_idle': wk_total - wk_busy,
        'dev_total': dev_total, 'dev_online': dev_online, 'dev_offline': dev_total - dev_online,
    })


@app.route('/api/overview/charts')
def overview_charts():
    trend = clean(db.query("""
        SELECT DATE_FORMAT(report_time,'%Y-%m-%d') d, COUNT(*) total,
               SUM(IF(event_status=3,1,0)) done
        FROM ERT GROUP BY d ORDER BY d
    """))
    types = clean(db.query(
        "SELECT event_type name, COUNT(*) value FROM ERT GROUP BY event_type ORDER BY value DESC"))
    return jsonify({'trend': trend, 'types': types})


@app.route('/api/infra')
def infra():
    region = request.args.get('region', '')
    typ = request.args.get('type', '')
    sql = """SELECT i.infra_id,i.infra_type,i.infra_name,i.location,i.install_time,i.status,
                    r.region_name FROM IT i JOIN RT r ON i.region_id=r.region_id WHERE 1=1"""
    args = []
    if region:
        sql += " AND r.region_name=%s"
        args.append(region)
    if typ:
        sql += " AND i.infra_type=%s"
        args.append(typ)
    sql += " ORDER BY i.infra_id LIMIT 300"
    rows = clean(db.query(sql, args))
    for r in rows:
        r['status_name'] = INFRA_STATUS.get(r['status'], '未知')
    return jsonify(rows)


@app.route('/api/infra/stats')
def infra_stats():
    by_type = clean(db.query(
        "SELECT infra_type name, COUNT(*) value FROM IT GROUP BY infra_type ORDER BY value DESC"))
    by_reg = clean(db.query("""SELECT r.region_name name, COUNT(i.infra_id) value
        FROM RT r LEFT JOIN IT i ON r.region_id=i.region_id GROUP BY r.region_id ORDER BY value DESC"""))
    return jsonify({'by_type': by_type, 'by_reg': by_reg})


@app.route('/api/infra', methods=['POST'])
def add_infra():
    d = request.json
    rid = db.execute_returning_id(
        "INSERT INTO IT(region_id,infra_type,infra_name,location,install_time,status) "
        "VALUES(%s,%s,%s,%s,%s,%s)",
        (d['region_id'], d['infra_type'], d['infra_name'], d.get('location', ''),
         d.get('install_time'), d.get('status', 1)))
    return ok('设施已新增', infra_id=rid)


@app.route('/api/infra/<int:iid>', methods=['DELETE'])
def del_infra(iid):
    try:
        db.execute("DELETE FROM IT WHERE infra_id=%s", (iid,))
        return ok('设施已删除')
    except Exception as e:
        return fail(db_err(e))


@app.route('/api/events')
def events():
    rows = clean(db.query("""SELECT e.event_id,e.event_type,e.event_title,e.report_time,e.event_status,
        c.real_name citizen, r.region_name region FROM ERT e
        JOIN CT c ON e.citizen_id=c.citizen_id JOIN RT r ON e.region_id=r.region_id
        ORDER BY e.event_id DESC LIMIT 200"""))
    for r in rows:
        r['status_name'] = STATUS_MAP.get(r['event_status'], '未知')
    return jsonify(rows)


@app.route('/api/events/stats')
def events_stats():
    by_type = clean(db.query(
        "SELECT event_type name, COUNT(*) value FROM ERT GROUP BY event_type ORDER BY value DESC"))
    by_reg = clean(db.query("""SELECT r.region_name name, COUNT(e.event_id) value
        FROM RT r LEFT JOIN ERT e ON r.region_id=e.region_id GROUP BY r.region_id ORDER BY value DESC"""))
    return jsonify({'by_type': by_type, 'by_reg': by_reg})


@app.route('/api/events', methods=['POST'])
def add_event():
    d = request.json
    eid = db.execute_returning_id(
        "INSERT INTO ERT(citizen_id,region_id,infra_id,event_title,event_content,event_type,report_time,event_status) "
        "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
        (d['citizen_id'], d['region_id'], d.get('infra_id'),
         d['event_title'], d.get('event_content', ''), d['event_type'],
         d.get('report_time'), d.get('event_status', 1)))
    return ok('事件已上报', event_id=eid)


@app.route('/api/events/<int:eid>', methods=['DELETE'])
def del_event(eid):
    try:
        db.execute("DELETE FROM ERT WHERE event_id=%s", (eid,))
        return ok('事件已删除')
    except Exception as e:
        return fail(db_err(e))


@app.route('/api/tasks')
def tasks():
    rows = clean(db.query("""SELECT t.task_id,t.task_start,t.task_end,t.task_status,
        e.event_id event,e.event_title event_title, w.worker_name worker, d.dept_name dept,
        tr.resource_name resource FROM TST t
        JOIN ERT e ON t.event_id=e.event_id JOIN WT w ON t.worker_id=w.worker_id
        JOIN DT d ON t.dept_id=d.dept_id
        LEFT JOIN TRT tr ON t.resource_id=tr.resource_id
        ORDER BY t.task_id DESC LIMIT 200"""))
    for r in rows:
        r['status_name'] = TASK_STATUS.get(r['task_status'], '未知')
    return jsonify(rows)


@app.route('/api/tasks/stats')
def tasks_stats():
    rtype = clean(db.query(
        "SELECT resource_type name, COUNT(*) value FROM TRT GROUP BY resource_type ORDER BY value DESC"))
    tstat = clean(db.query("""SELECT
        SUM(IF(task_status=3,1,0)) done, SUM(IF(task_status=2,1,0)) running,
        SUM(IF(task_status=1,1,0)) wait FROM TST"""))
    return jsonify({'rtype': rtype, 'tstat': tstat[0] if tstat else {}})


@app.route('/api/tasks', methods=['POST'])
def add_task():
    d = request.json
    tid = db.execute_returning_id(
        "INSERT INTO TST(event_id,worker_id,resource_id,dept_id,task_start,task_end,task_status,note) "
        "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
        (d['event_id'], d['worker_id'], d.get('resource_id'), d['dept_id'],
         d.get('task_start'), d.get('task_end'), d.get('task_status', 1),
         d.get('note', '')))
    if d.get('task_status', 1) in (2, 3):
        db.execute("UPDATE ERT SET event_status=%s WHERE event_id=%s",
                   (d['task_status'], d['event_id']))
    return ok('任务已派单', task_id=tid)


@app.route('/api/tasks/<int:tid>', methods=['PUT'])
def update_task(tid):
    d = request.json
    status = d.get('task_status')
    if status == 3 and not d.get('task_end'):
        d['task_end'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.execute(
        "UPDATE TST SET task_status=%s, task_end=%s WHERE task_id=%s",
        (status, d.get('task_end'), tid))
    row = db.query_one("SELECT event_id FROM TST WHERE task_id=%s", (tid,))
    if row:
        db.execute("UPDATE ERT SET event_status=%s WHERE event_id=%s",
                   (status, row['event_id']))
    return ok('任务状态已更新')


@app.route('/api/repairs')
def repairs():
    rows = clean(db.query("""SELECT m.record_id,m.repair_content,m.repair_time,m.repair_cost,m.result,
        t.task_id, i.infra_name, w.worker_name FROM MRT m
        JOIN TST t ON m.task_id=t.task_id JOIN IT i ON m.infra_id=i.infra_id
        JOIN WT w ON m.worker_id=w.worker_id ORDER BY m.record_id DESC LIMIT 200"""))
    return jsonify(rows)


@app.route('/api/repairs', methods=['POST'])
def add_repair():
    d = request.json
    rid = db.execute_returning_id(
        "INSERT INTO MRT(task_id,infra_id,worker_id,repair_content,repair_time,repair_cost,result) "
        "VALUES(%s,%s,%s,%s,%s,%s,%s)",
        (d['task_id'], d['infra_id'], d['worker_id'], d['repair_content'],
         d.get('repair_time'), d.get('repair_cost'), d.get('result', 1)))
    return ok('维修记录已录入', record_id=rid)


@app.route('/api/devices')
def devices():
    rows = clean(db.query("""SELECT m.device_id,m.device_name,m.device_no,m.device_type,
        m.install_loc,m.online_status,m.install_time,r.region_name FROM MDT m
        JOIN RT r ON m.region_id=r.region_id ORDER BY m.device_id"""))
    for r in rows:
        r['status_name'] = DEVICE_STATUS.get(r['online_status'], '未知')
    return jsonify(rows)


@app.route('/api/env/trend')
def env_trend():
    rows = clean(db.query("""SELECT DATE_FORMAT(collect_time,'%m-%d %H:00') h,
        ROUND(AVG(pm25),1) pm25, ROUND(AVG(pm10),1) pm10,
        ROUND(AVG(noise),1) noise, ROUND(AVG(temperature),1) temp, ROUND(AVG(humidity),1) hum
        FROM EDT GROUP BY h ORDER BY h"""))
    return jsonify(rows)


@app.route('/api/q1')
def q1():
    region = request.args.get('region', '')
    typ = request.args.get('type', '')
    sql = """SELECT i.infra_id,i.infra_type,i.infra_name,i.install_time,i.status,
        i.location,r.region_name FROM IT i JOIN RT r ON i.region_id=r.region_id WHERE 1=1"""
    args = []
    if region:
        sql += " AND r.region_name=%s"
        args.append(region)
    if typ:
        sql += " AND i.infra_type=%s"
        args.append(typ)
    sql += " ORDER BY i.infra_id"
    rows = clean(db.query(sql, args))
    for r in rows:
        r['status_name'] = INFRA_STATUS.get(r['status'], '未知')
    return jsonify(rows)


@app.route('/api/q2')
def q2():
    s = request.args.get('start', '2026-11-01')
    e = request.args.get('end', '2026-11-30')
    typ = request.args.get('type', '')
    sql = """SELECT e.event_id,e.event_type,e.event_title,e.report_time,e.event_status,
        d.dept_name dept, w.worker_name worker, r.region_name region FROM ERT e
        LEFT JOIN TST t ON e.event_id=t.event_id
        LEFT JOIN DT d ON t.dept_id=d.dept_id
        LEFT JOIN WT w ON t.worker_id=w.worker_id
        JOIN RT r ON e.region_id=r.region_id
        WHERE e.report_time BETWEEN %s AND %s"""
    args = [s, e + ' 23:59:59']
    if typ:
        sql += " AND e.event_type=%s"
        args.append(typ)
    sql += " ORDER BY e.report_time DESC LIMIT 300"
    rows = clean(db.query(sql, args))
    for r in rows:
        r['status_name'] = STATUS_MAP.get(r['event_status'], '未知')
        r['worker'] = r['worker'] or '—'
        r['dept'] = r['dept'] or '—'
    return jsonify(rows)


@app.route('/api/q3')
def q3():
    s = request.args.get('start', '2026-11-01')
    e = request.args.get('end', '2026-11-30')
    rows = clean(db.query("""SELECT w.worker_name worker, d.dept_name dept,
        COUNT(t.task_id) total,
        SUM(IF(t.task_status=3,1,0)) done,
        ROUND(SUM(IF(t.task_status=3,1,0))/COUNT(t.task_id)*100,1) rate,
        ROUND(AVG(IF(t.task_status=3 AND t.task_start IS NOT NULL AND t.task_end IS NOT NULL,
            TIMESTAMPDIFF(MINUTE,t.task_start,t.task_end),NULL)),1) avg_min
        FROM TST t JOIN WT w ON t.worker_id=w.worker_id JOIN DT d ON w.dept_id=d.dept_id
        WHERE t.task_start BETWEEN %s AND %s
        GROUP BY w.worker_id, d.dept_name ORDER BY total DESC""", [s, e + ' 23:59:59']))
    return jsonify(rows)


@app.route('/api/q4')
def q4():
    s = request.args.get('start', '2026-11-01')
    e = request.args.get('end', '2026-11-30')
    stat = clean(db.query("""SELECT r.region_name region,
        COUNT(e.event_id) total,
        SUM(IF(e.event_status=3,1,0)) done,
        ROUND(SUM(IF(e.event_status=3,1,0))/COUNT(e.event_id)*100,1) rate,
        ROUND(AVG(IF(e.event_status=3 AND t.task_end IS NOT NULL,
            TIMESTAMPDIFF(MINUTE,e.report_time,t.task_end),NULL))/60,1) avg_hour
        FROM RT r LEFT JOIN ERT e ON r.region_id=e.region_id AND e.report_time BETWEEN %s AND %s
        LEFT JOIN TST t ON e.event_id=t.event_id
        GROUP BY r.region_id ORDER BY total DESC""", [s, e + ' 23:59:59']))
    env = clean(db.query("""SELECT r.region_name region, DATE_FORMAT(ed.collect_time,'%%m-%%d') d,
        ROUND(AVG(ed.pm25),1) pm25, ROUND(AVG(ed.noise),1) noise,
        ROUND(AVG(ed.pm10),1) pm10, ROUND(AVG(ed.temperature),1) temp
        FROM EDT ed JOIN MDT m ON ed.device_id=m.device_id JOIN RT r ON m.region_id=r.region_id
        WHERE ed.collect_time BETWEEN %s AND %s
        GROUP BY r.region_id, d ORDER BY d""", [s, e + ' 23:59:59']))
    return jsonify({'stat': stat, 'env': env})


@app.route('/api/infra/<int:iid>', methods=['PUT'])
def upd_infra(iid):
    d = request.json
    db.execute(
        "UPDATE IT SET region_id=%s,infra_type=%s,infra_name=%s,location=%s,install_time=%s,status=%s WHERE infra_id=%s",
        (d['region_id'], d['infra_type'], d['infra_name'], d.get('location', ''),
         d.get('install_time'), d.get('status', 1), iid))
    return ok('设施已更新')


@app.route('/api/events/<int:eid>', methods=['PUT'])
def upd_event(eid):
    d = request.json
    db.execute(
        "UPDATE ERT SET citizen_id=%s,region_id=%s,infra_id=%s,event_title=%s,event_content=%s,event_type=%s,event_status=%s WHERE event_id=%s",
        (d['citizen_id'], d['region_id'], d.get('infra_id'), d['event_title'],
         d.get('event_content', ''), d['event_type'], d.get('event_status', 1), eid))
    return ok('事件已更新')


@app.route('/api/tasks/<int:tid>', methods=['DELETE'])
def del_task(tid):
    try:
        db.execute("DELETE FROM TST WHERE task_id=%s", (tid,))
        return ok('任务已删除')
    except Exception as e:
        return fail(db_err(e))


@app.route('/api/repairs/<int:rid>', methods=['PUT'])
def upd_repair(rid):
    d = request.json
    db.execute(
        "UPDATE MRT SET repair_content=%s,repair_cost=%s,result=%s WHERE record_id=%s",
        (d['repair_content'], d.get('repair_cost'), d.get('result', 1), rid))
    return ok('维修记录已更新')


@app.route('/api/repairs/<int:rid>', methods=['DELETE'])
def del_repair(rid):
    try:
        db.execute("DELETE FROM MRT WHERE record_id=%s", (rid,))
        return ok('维修记录已删除')
    except Exception as e:
        return fail(db_err(e))


@app.route('/api/trt')
def trt_list():
    rows = clean(db.query("""SELECT t.resource_id,t.resource_name,t.resource_type,t.resource_no,t.status,
        d.dept_name,t.dept_id FROM TRT t JOIN DT d ON t.dept_id=d.dept_id ORDER BY t.resource_id"""))
    for r in rows:
        r['status_name'] = RESOURCE_STATUS.get(r['status'], '未知')
    return jsonify(rows)


@app.route('/api/trt', methods=['POST'])
def add_trt():
    d = request.json
    rid = db.execute_returning_id(
        "INSERT INTO TRT(resource_name,resource_type,resource_no,status,dept_id) VALUES(%s,%s,%s,%s,%s)",
        (d['resource_name'], d['resource_type'], d['resource_no'], d.get('status', 1), d['dept_id']))
    return ok('资源已新增', resource_id=rid)


@app.route('/api/trt/<int:rid>', methods=['PUT'])
def upd_trt(rid):
    d = request.json
    db.execute(
        "UPDATE TRT SET resource_name=%s,resource_type=%s,resource_no=%s,status=%s,dept_id=%s WHERE resource_id=%s",
        (d['resource_name'], d['resource_type'], d['resource_no'], d.get('status', 1), d['dept_id'], rid))
    return ok('资源已更新')


@app.route('/api/trt/<int:rid>', methods=['DELETE'])
def del_trt(rid):
    try:
        db.execute("DELETE FROM TRT WHERE resource_id=%s", (rid,))
        return ok('资源已删除')
    except Exception as e:
        return fail(db_err(e))


@app.route('/api/devices', methods=['POST'])
def add_device():
    d = request.json
    rid = db.execute_returning_id(
        "INSERT INTO MDT(region_id,device_name,device_no,device_type,install_loc,online_status,install_time) "
        "VALUES(%s,%s,%s,%s,%s,%s,%s)",
        (d['region_id'], d['device_name'], d['device_no'], d['device_type'],
         d.get('install_loc', ''), d.get('online_status', 1), d.get('install_time')))
    return ok('设备已新增', device_id=rid)


@app.route('/api/devices/<int:did>', methods=['PUT'])
def upd_device(did):
    d = request.json
    db.execute(
        "UPDATE MDT SET region_id=%s,device_name=%s,device_no=%s,device_type=%s,install_loc=%s,online_status=%s WHERE device_id=%s",
        (d['region_id'], d['device_name'], d['device_no'], d['device_type'],
         d.get('install_loc', ''), d.get('online_status', 1), did))
    return ok('设备已更新')


@app.route('/api/devices/<int:did>', methods=['DELETE'])
def del_device(did):
    try:
        db.execute("DELETE FROM MDT WHERE device_id=%s", (did,))
        return ok('设备已删除')
    except Exception as e:
        return fail(db_err(e))


@app.route('/api/citizens')
def citizens():
    return jsonify(clean(db.query(
        "SELECT citizen_id,phone,real_name,email,register_time FROM CT ORDER BY citizen_id")))


@app.route('/api/citizens', methods=['POST'])
def add_citizen():
    d = request.json
    rid = db.execute_returning_id(
        "INSERT INTO CT(phone,real_name,email) VALUES(%s,%s,%s)",
        (d['phone'], d.get('real_name', ''), d.get('email', '')))
    return ok('市民已新增', citizen_id=rid)


@app.route('/api/citizens/<int:cid>', methods=['PUT'])
def upd_citizen(cid):
    d = request.json
    db.execute("UPDATE CT SET phone=%s,real_name=%s,email=%s WHERE citizen_id=%s",
               (d['phone'], d.get('real_name', ''), d.get('email', ''), cid))
    return ok('市民已更新')


@app.route('/api/citizens/<int:cid>', methods=['DELETE'])
def del_citizen(cid):
    try:
        db.execute("DELETE FROM CT WHERE citizen_id=%s", (cid,))
        return ok('市民已删除')
    except Exception as e:
        return fail(db_err(e))


@app.route('/api/depts/full')
def depts_full():
    return jsonify(clean(db.query(
        "SELECT dept_id,dept_name,dept_phone,dept_addr,manager FROM DT ORDER BY dept_id")))


@app.route('/api/depts', methods=['POST'])
def add_dept():
    d = request.json
    rid = db.execute_returning_id(
        "INSERT INTO DT(dept_name,dept_phone,dept_addr,manager) VALUES(%s,%s,%s,%s)",
        (d['dept_name'], d.get('dept_phone', ''), d.get('dept_addr', ''), d.get('manager', '')))
    return ok('部门已新增', dept_id=rid)


@app.route('/api/depts/<int:did>', methods=['PUT'])
def upd_dept(did):
    d = request.json
    db.execute("UPDATE DT SET dept_name=%s,dept_phone=%s,dept_addr=%s,manager=%s WHERE dept_id=%s",
               (d['dept_name'], d.get('dept_phone', ''), d.get('dept_addr', ''), d.get('manager', ''), did))
    return ok('部门已更新')


@app.route('/api/depts/<int:did>', methods=['DELETE'])
def del_dept(did):
    try:
        db.execute("DELETE FROM DT WHERE dept_id=%s", (did,))
        return ok('部门已删除')
    except Exception as e:
        return fail(db_err(e))


@app.route('/api/workers', methods=['POST'])
def add_worker():
    d = request.json
    rid = db.execute_returning_id(
        "INSERT INTO WT(dept_id,worker_name,worker_phone,post,hire_date) VALUES(%s,%s,%s,%s,%s)",
        (d['dept_id'], d['worker_name'], d['worker_phone'], d.get('post', '维修工'), d.get('hire_date')))
    return ok('人员已新增', worker_id=rid)


@app.route('/api/workers/<int:wid>', methods=['PUT'])
def upd_worker(wid):
    d = request.json
    db.execute("UPDATE WT SET dept_id=%s,worker_name=%s,worker_phone=%s,post=%s WHERE worker_id=%s",
               (d['dept_id'], d['worker_name'], d['worker_phone'], d.get('post', '维修工'), wid))
    return ok('人员已更新')


@app.route('/api/workers/<int:wid>', methods=['DELETE'])
def del_worker(wid):
    try:
        db.execute("DELETE FROM WT WHERE worker_id=%s", (wid,))
        return ok('人员已删除')
    except Exception as e:
        return fail(db_err(e))


if __name__ == '__main__':
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=DEBUG)