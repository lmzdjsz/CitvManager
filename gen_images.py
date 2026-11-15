# -*- coding: utf-8 -*-
"""生成6张完全正确的图表（基于实际外键关系）"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import os

IMG = r'E:\demo3\report_images'
os.makedirs(IMG, exist_ok=True)
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

C = {'blue':'#3498DB','orange':'#E67E22','red':'#E74C3C','green':'#27AE60',
     'purple':'#9B59B6','teal':'#1ABC9C','dark':'#2C3E50','yellow':'#F39C12',
     'lightblue':'#5DADE2','lightorange':'#F8C471','lightgreen':'#58D68D',
     'lightred':'#EC7063','gray':'#7F8C8D'}

def box(ax, x, y, w, h, text, fc, tc='white', fs=10, lw=1.2):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.03",
        facecolor=fc,edgecolor='#333',linewidth=lw))
    ax.text(x+w/2, y+h/2, text, ha='center', va='center',
            fontsize=fs, color=tc, fontweight='bold', linespacing=1.3)

def arrow(ax, x1, y1, x2, y2, color='#555', lw=1.5, style='->'):
    ax.annotate('', xy=(x2,y2), xytext=(x1,y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw))

def line(ax, x1, y1, x2, y2, color='#888', lw=1, label='', lpos=0.5):
    ax.plot([x1,x2],[y1,y2],color=color,lw=lw,zorder=1)
    if label:
        mx,my = x1+(x2-x1)*lpos, y1+(y2-y1)*lpos
        ax.text(mx,my,label,ha='center',va='center',fontsize=7,color=color,
                fontweight='bold',bbox=dict(boxstyle='round,pad=0.15',
                facecolor='white',edgecolor='none',alpha=0.9),zorder=3)

# ============================================================
# 图1: 表外键依赖层级图（5层，完全正确）
# ============================================================
fig, ax = plt.subplots(figsize=(13, 7.5))
ax.set_xlim(0, 14); ax.set_ylim(0, 9); ax.axis('off')
ax.set_title('图 1  数据库表外键依赖层级图', fontsize=15, fontweight='bold', pad=12)

# 5层，每层标注表名和外键引用
layers = [
    (7.8, '第 1 层（基础表，无外键依赖）', [
        ('RT\n区域', 2, C['blue']),
        ('CT\n市民', 6, C['orange']),
        ('DT\n部门', 10, C['purple']),
    ]),
    (5.8, '第 2 层（依赖第1层）', [
        ('IT\n设施\n→RT', 0.5, C['orange']),
        ('WT\n人员\n→DT', 3.5, C['purple']),
        ('TRT\n资源\n→DT', 6.5, C['purple']),
        ('MDT\n设备\n→RT', 9.5, C['green']),
        ('ST\n统计\n→RT', 12.5, C['teal']),
    ]),
    (3.5, '第 3 层（依赖第1-2层）', [
        ('ERT\n事件\n→CT,RT,IT', 3.5, C['red']),
        ('EDT\n环境数据\n→MDT', 9.5, C['green']),
    ]),
    (1.5, '第 4 层（依赖第1-3层）', [
        ('TST\n任务\n→ERT,WT,\nTRT,DT', 5.5, C['yellow']),
    ]),
    (-0.5, '第 5 层（依赖第1-4层）', [
        ('MRT\n维修记录\n→TST,IT,WT', 5.5, C['dark']),
    ]),
]
positions = {}
for y, label, tables in layers:
    ax.text(0.3, y+0.55, label, fontsize=9, color='#333', fontweight='bold')
    for name, x, color in tables:
        w, h = 1.8, 1.0
        box(ax, x-w/2, y, w, h, name, color, fs=8)
        positions[name.split('\n')[0]] = (x, y+h/2)

# 层间依赖箭头
deps = [
    ('RT','IT'),('RT','MDT'),('RT','ST'),('RT','ERT'),
    ('DT','WT'),('DT','TRT'),('DT','TST'),
    ('CT','ERT'),('IT','ERT'),
    ('ERT','TST'),('WT','TST'),('TRT','TST'),
    ('MDT','EDT'),
    ('TST','MRT'),('IT','MRT'),('WT','MRT'),
]
for p, c in deps:
    x1,y1 = positions[p]; x2,y2 = positions[c]
    if y1 > y2:
        line(ax, x1, y1-0.5, x2, y2+0.5, color='#AAA', lw=0.8)

plt.tight_layout()
plt.savefig(f'{IMG}/fig1_hierarchy.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================================
# 图2: E-R 实体关系图（12实体 + 16条外键，标注删除策略）
# ============================================================
fig, ax = plt.subplots(figsize=(14, 9))
ax.set_xlim(0, 16); ax.set_ylim(0, 11); ax.axis('off')
ax.set_title('图 2  E-R 实体关系图（12 实体 · 16 外键）', fontsize=15, fontweight='bold', pad=12)

ents = {
    'RT':(8,9.5,C['blue'],'区域'),
    'CT':(1.5,7,C['orange'],'市民'),
    'DT':(14.5,7,C['purple'],'部门'),
    'IT':(4.5,7,C['orange'],'设施'),
    'ERT':(8,7,C['red'],'事件'),
    'MDT':(11.5,7,C['green'],'设备'),
    'WT':(12.5,4.5,C['purple'],'人员'),
    'TRT':(15,4.5,C['purple'],'资源'),
    'ST':(1.5,4.5,C['teal'],'统计'),
    'TST':(8,4.5,C['yellow'],'任务'),
    'EDT':(14.5,2,C['green'],'环境数据'),
    'MRT':(5,2,C['dark'],'维修记录'),
}
for k,(x,y,c,name) in ents.items():
    box(ax, x-0.85, y-0.45, 1.7, 0.9, f'{k}\n{name}', c, fs=8)

# 16条外键关系 (子表, 父表, 删除策略)
fk = [
    ('IT','RT','RESTRICT'),('WT','DT','RESTRICT'),('TRT','DT','RESTRICT'),
    ('ERT','CT','CASCADE'),('ERT','RT','RESTRICT'),('ERT','IT','SET NULL'),
    ('TST','ERT','CASCADE'),('TST','WT','RESTRICT'),('TST','TRT','SET NULL'),('TST','DT','RESTRICT'),
    ('MRT','TST','CASCADE'),('MRT','IT','SET NULL'),('MRT','WT','RESTRICT'),
    ('MDT','RT','RESTRICT'),('EDT','MDT','CASCADE'),('ST','RT','CASCADE'),
]
colors = {'CASCADE':'#E74C3C','SET NULL':'#F39C12','RESTRICT':'#3498DB'}
for c, p, rule in fk:
    x1,y1 = ents[c][0],ents[c][1]; x2,y2 = ents[p][0],ents[p][1]
    line(ax, x1, y1, x2, y2, color=colors[rule], lw=1.2, label=rule, lpos=0.5)

# 图例
for i,(r,co) in enumerate([('CASCADE 级联删除',C['red']),('SET NULL 置空引用',C['yellow']),('RESTRICT 限制删除',C['blue'])]):
    ax.plot([0.5+i*4.5, 1+i*4.5],[10.5,10.5],color=co,lw=2)
    ax.text(1.1+i*4.5, 10.5, r, fontsize=8, va='center')

plt.tight_layout()
plt.savefig(f'{IMG}/fig2_er.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================================
# 图3: 系统三层架构图
# ============================================================
fig, ax = plt.subplots(figsize=(9, 5))
ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis('off')
ax.set_title('图 3  系统三层架构图', fontsize=15, fontweight='bold', pad=12)

box(ax, 1, 5.2, 8, 1.3, '表现层（前端）\nVue 3 (CDN) + ECharts 5.x  |  单页应用  |  Fetch API 调用后端', C['blue'], fs=10)
box(ax, 1, 3, 8, 1.3, '业务逻辑层（后端）\nPython 3.9 + Flask 3.x + Flask-CORS  |  24 个 RESTful API  |  JSON 响应', C['orange'], fs=10)
box(ax, 1, 0.8, 8, 1.3, '数据持久层（数据库）\nMySQL 8.4 + InnoDB  |  12 张表  |  16 个外键约束  |  事务 ACID', C['green'], fs=10)
arrow(ax, 5, 5.2, 5, 4.3, lw=2); arrow(ax, 5, 3, 5, 2.1, lw=2)
arrow(ax, 5.3, 4.3, 5.3, 5.2, lw=2, style='->'); arrow(ax, 5.3, 2.1, 5.3, 3, lw=2, style='->')
ax.text(4.7, 4.75, 'HTTP 请求', fontsize=8, ha='right', color='#555')
ax.text(5.5, 4.75, 'JSON 响应 →', fontsize=8, ha='left', color='#555')
ax.text(4.7, 2.55, 'SQL 查询', fontsize=8, ha='right', color='#555')
ax.text(5.5, 2.55, '结果集 →', fontsize=8, ha='left', color='#555')

plt.tight_layout()
plt.savefig(f'{IMG}/fig3_arch.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================================
# 图4: 功能模块层次图
# ============================================================
fig, ax = plt.subplots(figsize=(13, 7))
ax.set_xlim(0, 14); ax.set_ylim(0, 8); ax.axis('off')
ax.set_title('图 4  系统功能模块层次图', fontsize=15, fontweight='bold', pad=12)

box(ax, 5, 6.5, 4, 1, '城市管理数字化平台 CMPD', C['dark'], fs=12)

m1 = [
    (0.3,'平台\n概览',C['blue'],['KPI指标卡','事件趋势图','类型饼图']),
    (2.3,'数据\n模型',C['blue'],['12表结构','ER关系图']),
    (4.3,'设施\n管理',C['orange'],['设施列表','新增/删除','统计卡片']),
    (6.3,'事件\n处理',C['red'],['事件列表','事件上报','删除事件']),
    (8.3,'资源\n调度',C['yellow'],['任务列表','派单','完成操作']),
    (10.3,'环境\n监测',C['green'],['设备清单','PM2.5趋势','温湿度图']),
    (12.3,'期末\n查询',C['purple'],['Q1设施查询','Q2事件查询','Q3人员统计','Q4区域分析']),
]
for x,t,c,subs in m1:
    box(ax, x, 4.5, 1.6, 1, t, c, fs=9)
    arrow(ax, 7, 6.5, x+0.8, 5.5)
    for i,s in enumerate(subs):
        box(ax, x-0.1, 3-i*0.9, 1.8, 0.7, s, c, fs=7, tc='white')
        arrow(ax, x+0.8, 4.5, x+0.8, 3-i*0.9+0.7, lw=1)

plt.tight_layout()
plt.savefig(f'{IMG}/fig4_modules.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================================
# 图5: 事件处理业务流程图（标注每步对应的表操作）
# ============================================================
fig, ax = plt.subplots(figsize=(13, 4))
ax.set_xlim(0, 14); ax.set_ylim(0, 4.5); ax.axis('off')
ax.set_title('图 5  事件处理业务流程图（标注表操作）', fontsize=15, fontweight='bold', pad=12)

steps = [
    (0.3,'①市民注册','INSERT INTO CT',C['orange']),
    (2.6,'②上报事件','INSERT INTO ERT',C['red']),
    (4.9,'③分派任务','INSERT INTO TST',C['yellow']),
    (7.2,'④执行维修','UPDATE TST',C['purple']),
    (9.5,'⑤记录归档','INSERT INTO MRT',C['dark']),
    (11.8,'⑥统计汇总','INSERT INTO ST',C['teal']),
]
for x,t,sql,c in steps:
    box(ax, x, 2, 2, 1.2, t, c, fs=9)
    box(ax, x, 0.5, 2, 0.8, sql, C['gray'], fs=7)
    arrow(ax, x+1, 2, x+1, 1.3, lw=1)
for i in range(len(steps)-1):
    arrow(ax, steps[i][0]+2, 2.6, steps[i+1][0], 2.6, lw=2)

plt.tight_layout()
plt.savefig(f'{IMG}/fig5_flow.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================================
# 图6: 四项查询表关联图
# ============================================================
fig, ax = plt.subplots(figsize=(13, 8))
ax.set_xlim(0, 14); ax.set_ylim(0, 9); ax.axis('off')
ax.set_title('图 6  四项期末查询表关联图', fontsize=15, fontweight='bold', pad=12)

queries = [
    (7.5, 'Q1 区域内设施查询', C['blue'], [
        ('IT 设施', 1.5, 6, C['orange']),
        ('RT 区域', 4.5, 6, C['blue']),
    ], [('IT','RT','INNER JOIN\nON region_id')]),
    (7.5, 'Q2 事件处理情况查询', C['red'], [
        ('ERT 事件', 7.5, 6, C['red']),
        ('TST 任务', 9.5, 6, C['yellow']),
        ('DT 部门', 11.5, 6, C['purple']),
        ('WT 人员', 9.5, 4.5, C['purple']),
        ('RT 区域', 7.5, 4.5, C['blue']),
    ], [('ERT','TST','LEFT JOIN'),('TST','DT','LEFT JOIN'),('TST','WT','LEFT JOIN'),('ERT','RT','INNER JOIN')]),
    (2.5, 'Q3 维修人员统计查询', C['yellow'], [
        ('TST 任务', 1.5, 2.5, C['yellow']),
        ('WT 人员', 4, 2.5, C['purple']),
        ('DT 部门', 4, 0.8, C['purple']),
    ], [('TST','WT','INNER JOIN'),('WT','DT','INNER JOIN')]),
    (2.5, 'Q4 区域综合分析查询', C['green'], [
        ('RT 区域', 8, 2.5, C['blue']),
        ('ERT 事件', 10, 2.5, C['red']),
        ('TST 任务', 12, 2.5, C['yellow']),
        ('EDT 环境数据', 10, 0.8, C['green']),
        ('MDT 设备', 12, 0.8, C['green']),
    ], [('RT','ERT','LEFT JOIN'),('ERT','TST','LEFT JOIN'),('EDT','MDT','INNER JOIN'),('MDT','RT','INNER JOIN')]),
]

# 画Q1
ax.text(3, 8.2, 'Q1 — 区域内设施查询', fontsize=11, fontweight='bold', color=C['blue'])
q1t = {'IT':(1.5,6.5),'RT':(4.5,6.5)}
box(ax, 0.6, 6, 1.8, 1, 'IT\n设施', C['orange'], fs=9)
box(ax, 3.6, 6, 1.8, 1, 'RT\n区域', C['blue'], fs=9)
line(ax, 2.4, 6.5, 3.6, 6.5, color=C['blue'], lw=2, label='INNER JOIN\nON region_id')

# 画Q2
ax.text(9.5, 8.2, 'Q2 — 事件处理情况查询', fontsize=11, fontweight='bold', color=C['red'])
box(ax, 6.6, 6, 1.8, 1, 'ERT\n事件', C['red'], fs=9)
box(ax, 8.8, 6, 1.8, 1, 'TST\n任务', C['yellow'], fs=9)
box(ax, 11, 6, 1.8, 1, 'DT\n部门', C['purple'], fs=9)
box(ax, 8.8, 4.3, 1.8, 1, 'WT\n人员', C['purple'], fs=9)
box(ax, 6.6, 4.3, 1.8, 1, 'RT\n区域', C['blue'], fs=9)
line(ax, 8.4, 6.5, 8.8, 6.5, color=C['red'], lw=1.5, label='LEFT JOIN')
line(ax, 10.6, 6.5, 11, 6.5, color=C['red'], lw=1.5, label='LEFT JOIN')
line(ax, 9.7, 6, 9.7, 5.3, color=C['red'], lw=1.5, label='LEFT JOIN')
line(ax, 7.5, 6, 7.5, 5.3, color=C['red'], lw=1.5, label='INNER JOIN')

# 画Q3
ax.text(3, 3.3, 'Q3 — 维修人员统计查询', fontsize=11, fontweight='bold', color=C['yellow'])
box(ax, 0.6, 1.8, 1.8, 1, 'TST\n任务', C['yellow'], fs=9)
box(ax, 3.6, 1.8, 1.8, 1, 'WT\n人员', C['purple'], fs=9)
box(ax, 3.6, 0.2, 1.8, 1, 'DT\n部门', C['purple'], fs=9)
line(ax, 2.4, 2.3, 3.6, 2.3, color=C['yellow'], lw=2, label='INNER JOIN')
line(ax, 4.5, 1.8, 4.5, 1.2, color=C['yellow'], lw=2, label='INNER JOIN')

# 画Q4
ax.text(10, 3.3, 'Q4 — 区域综合分析查询', fontsize=11, fontweight='bold', color=C['green'])
box(ax, 7.1, 1.8, 1.8, 1, 'RT\n区域', C['blue'], fs=9)
box(ax, 9.3, 1.8, 1.8, 1, 'ERT\n事件', C['red'], fs=9)
box(ax, 11.5, 1.8, 1.8, 1, 'TST\n任务', C['yellow'], fs=9)
box(ax, 9.3, 0.2, 1.8, 1, 'EDT\n环境数据', C['green'], fs=9)
box(ax, 11.5, 0.2, 1.8, 1, 'MDT\n设备', C['green'], fs=9)
line(ax, 8.9, 2.3, 9.3, 2.3, color=C['green'], lw=1.5, label='LEFT JOIN')
line(ax, 11.1, 2.3, 11.5, 2.3, color=C['green'], lw=1.5, label='LEFT JOIN')
line(ax, 10.2, 1.2, 11.5, 1.8, color=C['green'], lw=1.5, label='INNER JOIN')
line(ax, 12.4, 1.8, 12.4, 1.2, color=C['green'], lw=1.5, label='INNER JOIN')

plt.tight_layout()
plt.savefig(f'{IMG}/fig6_queries.png', dpi=150, bbox_inches='tight')
plt.close()

print('6 张图片已生成:')
for i, name in enumerate(['fig1_hierarchy','fig2_er','fig3_arch','fig4_modules','fig5_flow','fig6_queries'], 1):
    p = f'{IMG}/{name}.png'
    print(f'  图{i}: {p} ({os.path.getsize(p)} 字节)')