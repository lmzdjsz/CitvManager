"""
初始化数据库：建表 + 插入示例数据
用法：  python init_db.py

12 张表覆盖 5 大业务域：
  区域域:  RT  区域表
  设施域:  IT  基础设施表
  事件域:  CT  市民表 / ERT 事件上报表 / TST 任务调度表 / MRT 维修记录表
  资源域:  DT  部门表 / WT  维修人员表 / TRT 维修资源表
  环境域:  MDT 监测设备表 / EDT 环境数据表
  统计域:  ST  数据统计表
"""
import pymysql
import random
import datetime
import math
from config import MYSQL

SCHEMA_SQL = """
CREATE SCHEMA IF NOT EXISTS `CMPD` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `CMPD`;

DROP TABLE IF EXISTS `ST`;
DROP TABLE IF EXISTS `EDT`;
DROP TABLE IF EXISTS `MDT`;
DROP TABLE IF EXISTS `MRT`;
DROP TABLE IF EXISTS `TST`;
DROP TABLE IF EXISTS `ERT`;
DROP TABLE IF EXISTS `TRT`;
DROP TABLE IF EXISTS `WT`;
DROP TABLE IF EXISTS `DT`;
DROP TABLE IF EXISTS `CT`;
DROP TABLE IF EXISTS `IT`;
DROP TABLE IF EXISTS `RT`;

CREATE TABLE `RT` (
  `region_id` INT NOT NULL AUTO_INCREMENT,
  `region_name` VARCHAR(50) NOT NULL,
  `parent_id` INT NULL,
  `region_level` TINYINT NULL,
  `location_desc` VARCHAR(200) NULL,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`region_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `IT` (
  `infra_id` INT NOT NULL AUTO_INCREMENT,
  `region_id` INT NOT NULL,
  `infra_type` VARCHAR(30) NOT NULL,
  `infra_name` VARCHAR(100) NOT NULL,
  `location` VARCHAR(200) NOT NULL,
  `install_time` DATETIME NULL,
  `status` TINYINT NOT NULL DEFAULT 1,
  PRIMARY KEY (`infra_id`),
  FOREIGN KEY (`region_id`) REFERENCES `RT`(`region_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `CT` (
  `citizen_id` INT NOT NULL AUTO_INCREMENT,
  `phone` VARCHAR(20) NOT NULL UNIQUE,
  `real_name` VARCHAR(30) NULL,
  `email` VARCHAR(100) NULL,
  `register_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`citizen_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `DT` (
  `dept_id` INT NOT NULL AUTO_INCREMENT,
  `dept_name` VARCHAR(80) NOT NULL,
  `dept_phone` VARCHAR(20) NULL,
  `dept_addr` VARCHAR(200) NULL,
  `manager` VARCHAR(30) NULL,
  PRIMARY KEY (`dept_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `WT` (
  `worker_id` INT NOT NULL AUTO_INCREMENT,
  `dept_id` INT NOT NULL,
  `worker_name` VARCHAR(30) NOT NULL,
  `worker_phone` VARCHAR(20) NOT NULL UNIQUE,
  `post` VARCHAR(50) NULL,
  `hire_date` DATE NULL,
  PRIMARY KEY (`worker_id`),
  FOREIGN KEY (`dept_id`) REFERENCES `DT`(`dept_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `TRT` (
  `resource_id` INT NOT NULL AUTO_INCREMENT,
  `resource_name` VARCHAR(80) NOT NULL,
  `resource_type` VARCHAR(30) NOT NULL,
  `resource_no` VARCHAR(50) NOT NULL,
  `status` TINYINT NOT NULL DEFAULT 1,
  `dept_id` INT NOT NULL,
  PRIMARY KEY (`resource_id`),
  FOREIGN KEY (`dept_id`) REFERENCES `DT`(`dept_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `ERT` (
  `event_id` INT NOT NULL AUTO_INCREMENT,
  `citizen_id` INT NOT NULL,
  `region_id` INT NOT NULL,
  `infra_id` INT NULL,
  `event_title` VARCHAR(100) NOT NULL,
  `event_content` TEXT NULL,
  `event_type` VARCHAR(30) NOT NULL,
  `report_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `event_status` TINYINT NOT NULL DEFAULT 1,
  PRIMARY KEY (`event_id`),
  FOREIGN KEY (`citizen_id`) REFERENCES `CT`(`citizen_id`) ON DELETE CASCADE,
  FOREIGN KEY (`region_id`) REFERENCES `RT`(`region_id`) ON DELETE RESTRICT,
  FOREIGN KEY (`infra_id`) REFERENCES `IT`(`infra_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `TST` (
  `task_id` INT NOT NULL AUTO_INCREMENT,
  `event_id` INT NOT NULL,
  `worker_id` INT NOT NULL,
  `resource_id` INT NULL,
  `dept_id` INT NOT NULL,
  `task_start` DATETIME NULL,
  `task_end` DATETIME NULL,
  `task_status` TINYINT NOT NULL DEFAULT 1,
  `note` TEXT NULL,
  PRIMARY KEY (`task_id`),
  FOREIGN KEY (`event_id`) REFERENCES `ERT`(`event_id`) ON DELETE CASCADE,
  FOREIGN KEY (`worker_id`) REFERENCES `WT`(`worker_id`) ON DELETE RESTRICT,
  FOREIGN KEY (`resource_id`) REFERENCES `TRT`(`resource_id`) ON DELETE SET NULL,
  FOREIGN KEY (`dept_id`) REFERENCES `DT`(`dept_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `MRT` (
  `record_id` INT NOT NULL AUTO_INCREMENT,
  `task_id` INT NOT NULL,
  `infra_id` INT NULL,
  `worker_id` INT NOT NULL,
  `repair_content` TEXT NOT NULL,
  `repair_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `repair_cost` DECIMAL(10,2) NULL,
  `result` TINYINT NOT NULL DEFAULT 1,
  PRIMARY KEY (`record_id`),
  FOREIGN KEY (`task_id`) REFERENCES `TST`(`task_id`) ON DELETE CASCADE,
  FOREIGN KEY (`infra_id`) REFERENCES `IT`(`infra_id`) ON DELETE SET NULL,
  FOREIGN KEY (`worker_id`) REFERENCES `WT`(`worker_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `MDT` (
  `device_id` INT NOT NULL AUTO_INCREMENT,
  `region_id` INT NOT NULL,
  `device_name` VARCHAR(80) NOT NULL,
  `device_no` VARCHAR(50) NOT NULL UNIQUE,
  `device_type` VARCHAR(30) NOT NULL,
  `install_loc` VARCHAR(200) NOT NULL,
  `online_status` TINYINT NOT NULL DEFAULT 1,
  `install_time` DATETIME NULL,
  PRIMARY KEY (`device_id`),
  FOREIGN KEY (`region_id`) REFERENCES `RT`(`region_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `EDT` (
  `data_id` BIGINT NOT NULL AUTO_INCREMENT,
  `device_id` INT NOT NULL,
  `pm25` FLOAT NULL,
  `pm10` FLOAT NULL,
  `noise` FLOAT NULL,
  `temperature` FLOAT NULL,
  `humidity` FLOAT NULL,
  `collect_time` DATETIME NOT NULL,
  PRIMARY KEY (`data_id`),
  FOREIGN KEY (`device_id`) REFERENCES `MDT`(`device_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `ST` (
  `stat_id` INT NOT NULL AUTO_INCREMENT,
  `stat_date` DATE NOT NULL,
  `region_id` INT NOT NULL,
  `event_total` INT NOT NULL,
  `event_finish` INT NOT NULL,
  `infra_broken` INT NOT NULL,
  `avg_noise` FLOAT NULL,
  `avg_pm25` FLOAT NULL,
  `stat_create` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`stat_id`),
  FOREIGN KEY (`region_id`) REFERENCES `RT`(`region_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

REGIONS = ['高新区', '锦江区', '武侯区', '青羊区', '成华区', '金牛区', '天府新区']
INFRA_TYPES = ['道路', '桥梁', '照明', '垃圾桶']
EVENT_TYPES = ['道路损坏', '设施故障', '垃圾堆积', '照明失效']
DEPTS = [('市政设施科', '028-85001'), ('环境卫生科', '028-85002'),
         ('照明管理科', '028-85003'), ('桥梁养护科', '028-85004')]
WORKERS = ['张明', '李华', '王强', '赵敏', '刘洋', '陈静', '杨光', '周磊']


def rnd(a, b):
    return random.randint(a, b)


def pad(n):
    return f'{n:02d}'


def main():
    cfg = dict(MYSQL)
    cfg.pop('database', None)
    cfg.pop('charset', None)
    conn = pymysql.connect(**cfg, charset='utf8mb4',
                           cursorclass=pymysql.cursors.Cursor)
    cur = conn.cursor()
    for stmt in SCHEMA_SQL.split(';'):
        s = stmt.strip()
        if s:
            cur.execute(s)
    conn.commit()
    cur.close()
    conn.close()
    print('[1/12] 建表完成')

    import db

    db.executemany(
        "INSERT INTO RT(region_name,parent_id,region_level,location_desc) VALUES(%s,NULL,1,%s)",
        [(r, f'{r}辖区') for r in REGIONS])

    db.executemany(
        "INSERT INTO DT(dept_name,dept_phone,dept_addr,manager) VALUES(%s,%s,%s,%s)",
        [(n, p, f'城管大楼{idx+1}层', WORKERS[idx]) for idx, (n, p) in enumerate(DEPTS)])

    citizens = [(f'138{rnd(10000000, 99999999)}', f'市民{chr(65+i)}',
                 f'user{i+1}@city.gov') for i in range(12)]
    db.executemany(
        "INSERT INTO CT(phone,real_name,email) VALUES(%s,%s,%s)", citizens)

    db.executemany(
        "INSERT INTO WT(dept_id,worker_name,worker_phone,post,hire_date) VALUES(%s,%s,%s,%s,%s)",
        [((i % 4) + 1, WORKERS[i], f'139{rnd(10000000, 99999999)}', '维修工',
          f'202{rnd(0, 3)}-0{rnd(1, 9)}-1{rnd(0, 8)}') for i in range(len(WORKERS))])

    for i in range(40):
        db.execute(
            "INSERT INTO IT(region_id,infra_type,infra_name,location,install_time,status) VALUES(%s,%s,%s,%s,%s,%s)",
            (rnd(1, 7), random.choice(INFRA_TYPES), f'设施-{1001+i}',
             f'(30.{rnd(50, 70)},104.{rnd(0, 20)})',
             f'202{rnd(0, 4)}-{pad(rnd(1, 12))}-{pad(rnd(1, 28))} {pad(rnd(0, 23))}:00:00',
             rnd(1, 3)))

    rtypes = [('维修车辆', '车辆'), ('升降平台', '平台'),
              ('电动工具', '工具'), ('检测设备', '仪器')]
    for i in range(16):
        t = random.choice(rtypes)
        db.execute(
            "INSERT INTO TRT(resource_name,resource_type,resource_no,status,dept_id) VALUES(%s,%s,%s,%s,%s)",
            (f'{t[0]}-{i+1}', t[1], f'R-{pad(i+1)}', rnd(1, 3), rnd(1, 4)))

    for i in range(60):
        ev_status = rnd(1, 3)
        report_day = rnd(1, 12)
        report_time = f'2026-11-{pad(report_day)} {pad(rnd(8, 20))}:{pad(rnd(0, 59))}:00'
        rid = rnd(1, 7)
        ev_type = random.choice(EVENT_TYPES)
        eid = db.execute_returning_id(
            "INSERT INTO ERT(citizen_id,region_id,infra_id,event_title,event_content,event_type,report_time,event_status) "
            "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
            (rnd(1, 12), rid, rnd(1, 40), f'{ev_type}报告#{i+1}',
             '现场情况待核实', ev_type, report_time, ev_status))

        t_status = 3 if ev_status == 3 else (2 if ev_status == 2 else 1)
        wid = rnd(1, 8)
        did = rnd(1, 4)
        ts = f'2026-11-{pad(report_day)} {pad(rnd(9, 18))}:30:00'
        if t_status == 3:
            end_day = report_day + rnd(0, 1)
            if end_day > 12:
                end_day = 12
            te = f'2026-11-{pad(end_day)} {pad(rnd(14, 20))}:00:00'
        else:
            te = None
        tid = db.execute_returning_id(
            "INSERT INTO TST(event_id,worker_id,resource_id,dept_id,task_start,task_end,task_status,note) "
            "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
            (eid, wid, rnd(1, 16), did, ts, te, t_status, ''))

        if t_status == 3:
            db.execute(
                "INSERT INTO MRT(task_id,infra_id,worker_id,repair_content,repair_time,repair_cost,result) "
                "VALUES(%s,%s,%s,%s,%s,%s,%s)",
                (tid, rnd(1, 40), wid, '已完成维修', te,
                 round(random.uniform(100, 2000), 2), 1))

    dtypes = ['空气质量', '噪音', '水质', '温湿度']
    for i in range(12):
        db.execute(
            "INSERT INTO MDT(region_id,device_name,device_no,device_type,install_loc,online_status,install_time) "
            "VALUES(%s,%s,%s,%s,%s,%s,%s)",
            (rnd(1, 7), f'监测仪-{i+1}', f'MD-{pad(i+1)}', random.choice(dtypes),
             f'(30.{rnd(50, 70)},104.{rnd(0, 20)})',
             1 if random.random() > 0.15 else 0,
             f'202{rnd(0, 3)}-0{rnd(1, 9)}-1{rnd(0, 8)} 00:00:00'))

    for did in range(1, 13):
        for day in range(8, 14):
            for h in range(0, 24, 3):
                ct = f'2026-11-{pad(day)} {pad(h)}:00:00'
                db.execute(
                    "INSERT INTO EDT(device_id,pm25,pm10,noise,temperature,humidity,collect_time) "
                    "VALUES(%s,%s,%s,%s,%s,%s,%s)",
                    (did, round(40 + 15 * math.sin(h / 3) + rnd(-5, 5), 1),
                     round(65 + 20 * math.sin(h / 3) + rnd(-8, 8), 1),
                     round(55 + 10 * math.sin(h / 4) + rnd(-4, 4), 1),
                     round(18 + 8 * math.sin((h - 6) / 4) + rnd(-1, 1), 1),
                     round(60 + 10 * math.cos(h / 4) + rnd(-3, 3), 1), ct))

    for d in range(1, 13):
        for rid in range(1, 8):
            total = rnd(5, 20)
            fin = rnd(int(total * 0.6), total)
            db.execute(
                "INSERT INTO ST(stat_date,region_id,event_total,event_finish,infra_broken,avg_noise,avg_pm25) "
                "VALUES(%s,%s,%s,%s,%s,%s,%s)",
                (f'2026-11-{pad(d)}', rid, total, fin, rnd(0, 5),
                 round(50 + rnd(-10, 10), 1), round(40 + rnd(-10, 10), 1)))

    print('[2/12] 示例数据插入完成')
    print('初始化完成！可运行  python app.py  启动后端')


if __name__ == '__main__':
    main()