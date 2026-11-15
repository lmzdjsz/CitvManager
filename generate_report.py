# -*- coding: utf-8 -*-
"""生成《数据库综合课程设计》期末报告 .docx（含图片）"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
import os, datetime

IMG_DIR = r'E:\demo3\report_images'
os.makedirs(IMG_DIR, exist_ok=True)

# ============================================================
#  图片生成
# ============================================================
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def draw_box(ax, x, y, w, h, text, fc='#4ECDC4', tc='white', fs=10, ec='none'):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                         facecolor=fc, edgecolor=ec or '#333', linewidth=1.2)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center',
            fontsize=fs, color=tc, fontweight='bold', wrap=True)

def draw_arrow(ax, x1, y1, x2, y2, text='', color='#555'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
    if text:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my+0.15, text, ha='center', va='bottom', fontsize=8, color=color)

# ---- 图1: 系统三层架构 ----
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis('off')
ax.set_title('图 1  系统三层架构图', fontsize=14, fontweight='bold', pad=10)
draw_box(ax, 1, 5, 8, 1.2, '表现层（前端）\nVue 3 + ECharts + Element 风格  |  单页应用  |  HTTP/Fetch', '#3498DB', fs=11)
draw_box(ax, 1, 3, 8, 1.2, '业务逻辑层（后端）\nPython Flask + Flask-CORS  |  24 个 RESTful API  |  JSON 响应', '#E67E22', fs=11)
draw_box(ax, 1, 1, 8, 1.2, '数据持久层（数据库）\nMySQL 8.4 InnoDB  |  12 张表  |  外键约束 + 事务', '#27AE60', fs=11)
draw_arrow(ax, 5, 5, 5, 4.2, 'HTTP 请求/响应', '#333')
draw_arrow(ax, 5, 3, 5, 2.2, 'SQL 查询/提交', '#333')
ax.text(5.2, 4.6, '↑ 渲染数据', fontsize=8, color='#666')
ax.text(5.2, 2.6, '↑ 结果集', fontsize=8, color='#666')
plt.tight_layout()
plt.savefig(f'{IMG_DIR}/fig1_arch.png', dpi=150, bbox_inches='tight')
plt.close()

# ---- 图2: 功能模块结构图 ----
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 14); ax.set_ylim(0, 9); ax.axis('off')
ax.set_title('图 2  系统功能模块结构图', fontsize=14, fontweight='bold', pad=10)
draw_box(ax, 5, 7.5, 4, 1, '城市管理数字化平台', '#2C3E50', fs=12)
mods = [
    (0.3, 5.5, '平台\n概览', '#3498DB'),
    (2.3, 5.5, '数据\n模型', '#3498DB'),
    (4.3, 5.5, '设施\n管理', '#E67E22'),
    (6.3, 5.5, '事件\n处理', '#E67E22'),
    (8.3, 5.5, '资源\n调度', '#E67E22'),
    (10.3, 5.5, '环境\n监测', '#27AE60'),
    (12.3, 5.5, '期末\n查询', '#E74C3C'),
]
for x, y, t, c in mods:
    draw_box(ax, x, y, 1.6, 1, t, c, fs=9)
    draw_arrow(ax, 7, 7.5, x+0.8, 6.5)
submods = [
    (0.0, 3.5, 'KPI指标卡\n趋势图表', '#5DADE2'),
    (2.0, 3.5, '12表结构\nER关系图', '#5DADE2'),
    (4.0, 3.5, '设施列表\n新增/删除', '#F39C12'),
    (6.0, 3.5, '事件上报\n任务派单', '#F39C12'),
    (8.0, 3.5, '人员管理\n资源管理', '#F39C12'),
    (10.0, 3.5, '设备监控\n趋势分析', '#58D68D'),
    (12.0, 3.5, 'Q1~Q4\n筛选+图表', '#EC7063'),
]
for i, (x, y, t, c) in enumerate(submods):
    draw_box(ax, x, y, 1.8, 1.2, t, c, fs=8)
    draw_arrow(ax, mods[i][0]+0.8, 5.5, x+0.9, 4.7)
plt.tight_layout()
plt.savefig(f'{IMG_DIR}/fig2_modules.png', dpi=150, bbox_inches='tight')
plt.close()

# ---- 图3: E-R 图 ----
fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, 14); ax.set_ylim(0, 10); ax.axis('off')
ax.set_title('图 3  数据库 E-R 关系图', fontsize=14, fontweight='bold', pad=10)
# 实体位置
entities = {
    'RT\n区域': (7, 8.5, '#3498DB'),
    'CT\n市民': (1, 6, '#E67E22'),
    'IT\n设施': (4, 6, '#E67E22'),
    'ERT\n事件': (7, 6, '#E74C3C'),
    'MDT\n设备': (10, 6, '#27AE60'),
    'DT\n部门': (1, 3.5, '#9B59B6'),
    'WT\n人员': (4, 3.5, '#9B59B6'),
    'TRT\n资源': (7, 3.5, '#9B59B6'),
    'TST\n任务': (4, 1, '#F39C12'),
    'MRT\n维修': (8, 1, '#F39C12'),
    'EDT\n环境数据': (12, 3.5, '#27AE60'),
    'ST\n统计': (12, 8.5, '#1ABC9C'),
}
for name, (x, y, c) in entities.items():
    draw_box(ax, x-0.7, y-0.4, 1.4, 0.8, name, c, fs=9)
# 关系线 (x1,y1)->(x2,y2) 标注
relations = [
    ('RT\n区域', 'IT\n设施', '1:N'),
    ('RT\n区域', 'ERT\n事件', '1:N'),
    ('RT\n区域', 'MDT\n设备', '1:N'),
    ('RT\n区域', 'ST\n统计', '1:N'),
    ('CT\n市民', 'ERT\n事件', '1:N'),
    ('IT\n设施', 'ERT\n事件', '1:N'),
    ('ERT\n事件', 'TST\n任务', '1:N'),
    ('DT\n部门', 'WT\n人员', '1:N'),
    ('DT\n部门', 'TRT\n资源', '1:N'),
    ('DT\n部门', 'TST\n任务', '1:N'),
    ('WT\n人员', 'TST\n任务', '1:N'),
    ('TRT\n资源', 'TST\n任务', '1:N'),
    ('TST\n任务', 'MRT\n维修', '1:N'),
    ('MDT\n设备', 'EDT\n环境数据', '1:N'),
]
for e1, e2, label in relations:
    x1, y1, _ = entities[e1]
    x2, y2, _ = entities[e2]
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='-', color='#888', lw=1))
    mx, my = (x1+x2)/2, (y1+y2)/2
    ax.text(mx, my, label, ha='center', va='center', fontsize=7,
            color='#E74C3C', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.1', facecolor='white', edgecolor='none', alpha=0.8))
plt.tight_layout()
plt.savefig(f'{IMG_DIR}/fig3_er.png', dpi=150, bbox_inches='tight')
plt.close()

# ---- 图4: 表依赖层级图 ----
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 14); ax.set_ylim(0, 8); ax.axis('off')
ax.set_title('图 4  数据库表外键依赖层级图', fontsize=14, fontweight='bold', pad=10)
layers = [
    (6.5, ['RT', 'CT', 'DT'], '#3498DB', '第1层（基础表，无外键）'),
    (4.5, ['IT→RT', 'WT→DT', 'TRT→DT', 'MDT→RT'], '#E67E22', '第2层（依赖基础表）'),
    (2.5, ['ERT→CT,RT,IT'], '#E74C3C', '第3层（事件核心）'),
    (0.5, ['TST→ERT,WT,TRT,DT', 'EDT→MDT', 'ST→RT'], '#27AE60', '第4层（任务/环境/统计）'),
]
y_pos = 7
for y, tables, c, label in layers:
    ax.text(0.3, y_pos+0.3, label, fontsize=9, color=c, fontweight='bold')
    total_w = len(tables) * 2.2
    start_x = (14 - total_w) / 2
    for i, t in enumerate(tables):
        draw_box(ax, start_x + i*2.2, y_pos, 2, 0.7, t, c, fs=9)
    y_pos -= 1.8
# 箭头表示依赖方向
ax.annotate('', xy=(7, 5.2), xytext=(7, 6.3),
            arrowprops=dict(arrowstyle='->', color='#555', lw=2))
ax.annotate('', xy=(7, 3.2), xytext=(7, 4.3),
            arrowprops=dict(arrowstyle='->', color='#555', lw=2))
ax.annotate('', xy=(7, 1.2), xytext=(7, 2.3),
            arrowprops=dict(arrowstyle='->', color='#555', lw=2))
ax.text(7.3, 5.8, '外键依赖', fontsize=8, color='#555')
plt.tight_layout()
plt.savefig(f'{IMG_DIR}/fig4_hierarchy.png', dpi=150, bbox_inches='tight')
plt.close()

# ---- 图5: 业务流程图 ----
fig, ax = plt.subplots(figsize=(10, 3.5))
ax.set_xlim(0, 14); ax.set_ylim(0, 4); ax.axis('off')
ax.set_title('图 5  事件处理业务流程图', fontsize=14, fontweight='bold', pad=10)
steps = [
    (0.5, '市民\n上报事件', '#3498DB'),
    (3, '系统\n生成事件', '#E67E22'),
    (5.5, '部门\n分派任务', '#9B59B6'),
    (8, '人员\n执行维修', '#E74C3C'),
    (10.5, '记录\n归档', '#27AE60'),
    (13, '统计\n汇总', '#1ABC9C'),
]
for x, t, c in steps:
    draw_box(ax, x, 1.5, 1.5, 1, t, c, fs=9)
for i in range(len(steps)-1):
    draw_arrow(ax, steps[i][0]+1.5, 2, steps[i+1][0], 2)
plt.tight_layout()
plt.savefig(f'{IMG_DIR}/fig5_flow.png', dpi=150, bbox_inches='tight')
plt.close()

print('5 张图片已生成到', IMG_DIR)

# ============================================================
#  报告生成
# ============================================================
doc = Document()

style = doc.styles['Normal']
style.font.name = '宋体'
style.font.size = Pt(12)
style._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
style.paragraph_format.line_spacing = 1.5
style.paragraph_format.space_after = Pt(0)

for i in range(1, 4):
    hs = doc.styles[f'Heading {i}']
    hs.font.name = '黑体'
    hs._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    hs.font.color.rgb = RGBColor(0, 0, 0)
    hs.font.size = Pt(16 if i == 1 else (14 if i == 2 else 12))

def add_p(text, bold=False, size=12, align=None, indent=True):
    p = doc.add_paragraph()
    if align: p.alignment = align
    if indent: p.paragraph_format.first_line_indent = Cm(0.74)
    run = p.add_run(text)
    run.font.name = '宋体'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    run.font.size = Pt(size)
    run.bold = bold
    return p

def add_code(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(1)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run(text)
    run.font.name = 'Consolas'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    run.font.size = Pt(9)

def add_table(headers, rows, col_widths=None):
    t = doc.add_table(rows=1, cols=len(headers), style='Table Grid')
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(headers):
        cell = t.rows[0].cells[j]; cell.text = h
        for para in cell.paragraphs:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in para.runs: run.bold = True; run.font.size = Pt(10)
    for row in rows:
        cells = t.add_row().cells
        for j, v in enumerate(row):
            cells[j].text = str(v)
            for para in cells[j].paragraphs:
                para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in para.runs: run.font.size = Pt(10)
    if col_widths:
        for j, w in enumerate(col_widths):
            for row in t.rows: row.cells[j].width = Cm(w)

def add_img(path, width=15):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(path, width=Cm(width))

# ===== 封面 =====
for _ in range(5): doc.add_paragraph()
for text, size in [('《数据库综合课程设计》', 28), ('期 末 报 告', 28)]:
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text); run.font.size = Pt(size); run.bold = True
    run.font.name = '黑体'; run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
doc.add_paragraph()
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('B7 城市管理数字化平台设计与实现'); run.font.size = Pt(20)
run.font.name = '黑体'; run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
for _ in range(4): doc.add_paragraph()
for label in ['课程名称：数据库综合课程设计', '项目编号：B7', '姓        名：___________',
              '学        号：___________', '班        级：___________', '指导教师：___________',
              '提交日期：2026 年 11 月 14 日']:
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(label); run.font.size = Pt(14)
    run.font.name = '宋体'; run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
doc.add_page_break()

# ===== 目录 =====
doc.add_heading('目  录', level=1)
toc = [
    '摘  要',
    '第一章  系统需求分析',
    '  1.1  项目背景与意义',
    '  1.2  功能需求分析',
    '  1.3  数据需求分析',
    '  1.4  数据流分析',
    '第二章  数据库概念结构设计',
    '  2.1  实体识别与属性分析',
    '  2.2  实体间联系分析',
    '  2.3  E-R 图设计',
    '第三章  数据库逻辑结构设计',
    '  3.1  E-R 模型向关系模式转换',
    '  3.2  关系模式定义',
    '  3.3  范式分析',
    '  3.4  表结构详细设计',
    '第四章  数据库物理实现',
    '  4.1  数据库与表创建',
    '  4.2  外键约束策略',
    '  4.3  索引设计',
    '  4.4  数据初始化',
    '第五章  系统功能实现',
    '  5.1  技术架构设计',
    '  5.2  后端 API 设计与实现',
    '  5.3  前端功能模块',
    '  5.4  关键代码实现',
    '第六章  四项期末查询设计与验证',
    '  6.1  Q1 — 区域内设施查询',
    '  6.2  Q2 — 事件处理情况查询',
    '  6.3  Q3 — 维修人员统计查询',
    '  6.4  Q4 — 区域综合分析查询',
    '第七章  总结与展望',
]
for item in toc:
    p = doc.add_paragraph(); p.paragraph_format.line_spacing = 1.5
    run = p.add_run(item); run.font.size = Pt(12)
    run.font.name = '宋体'; run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
doc.add_page_break()

# ===== 摘要 =====
doc.add_heading('摘  要', level=1)
add_p('随着我国城市化进程的不断加快，城市基础设施规模持续扩大，市政管理的复杂度日益增加。传统的人工巡检、电话接报、纸质工单等管理模式存在信息孤岛严重、响应速度滞后、数据难以统计分析、跨部门协同困难等问题，已无法满足现代城市精细化治理的需求。本项目设计并实现了一个城市管理数字化平台（City Management Platform Database，简称 CMPD），旨在通过关系数据库技术将城市管理的各类业务数据集中存储、统一管理，并借助 Web 技术实现数据的在线录入、查询、统计与分析，从而提升城市管理的数字化、智能化水平。')
add_p('本系统覆盖区域管理、基础设施档案、市民事件上报、维修任务调度、环境监测五大业务域，共设计 12 张数据库表，构建了从事件发现到任务分派、维修记录、环境监控的全闭环数据模型。系统后端采用 Python Flask 框架与 pymysql 驱动，提供 24 个 RESTful API 接口，支持数据的增删改查与统计分析；前端采用 Vue 3（CDN 引入方式）与 ECharts 图表库构建单页应用，实现了数据看板、设施管理、事件处理、资源调度、环境监测及四项期末规定查询等功能。数据库层使用 MySQL 8.4 InnoDB 存储引擎，通过外键级联约束（CASCADE、SET NULL、RESTRICT）保证参照完整性，并预置了 7 个行政区域、4 个部门、8 名维修人员、40 个基础设施、12 名市民、60 条事件上报、60 条任务调度、12 台监测设备、864 条环境数据等约 1200 条示例数据。')
add_p('本报告详细阐述了系统的需求分析、数据库概念设计与逻辑设计、物理实现、系统功能实现及四项规定查询的 SQL 设计与验证过程，完整呈现了从 E-R 模型到可运行系统的全流程。经测试验证，系统各项功能运行正常，四项规定查询结果正确，前后端数据实时同步，达到了预期设计目标。')
p = doc.add_paragraph()
run = p.add_run('关键词：'); run.bold = True; run.font.size = Pt(12)
run.font.name = '宋体'; run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
run = p.add_run('城市管理；数据库设计；E-R 模型；关系模式；MySQL；Flask；RESTful API；Vue 3')
run.font.size = Pt(12); run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
doc.add_page_break()

# ===== 第一章 =====
doc.add_heading('第一章  系统需求分析', level=1)

doc.add_heading('1.1  项目背景与意义', level=2)
add_p('城市管理是现代城市治理的核心内容，涉及道路桥梁维护、照明设施管理、环境卫生保洁、环境质量监测等多个方面。随着城市规模的扩大，市政设施数量动辄以万计，每日产生的事件上报、维修工单、环境采集数据量巨大，传统管理方式面临以下突出矛盾：')
add_p('（1）信息分散，孤岛严重。各业务科室各自维护台账，数据格式不统一，跨科室查询困难，难以形成全局视角。', indent=False)
add_p('（2）响应滞后，协同困难。市民上报事件后需人工流转至对应科室，分派维修人员依赖电话沟通，处理周期长、效率低。', indent=False)
add_p('（3）数据沉睡，分析缺失。大量历史数据以纸质或分散电子文件形式存在，无法进行统计分析，难以支撑管理决策。', indent=False)
add_p('（4）环境监测缺乏系统化手段。空气质量、噪音等环境数据采集分散，无法与区域、设施关联分析。', indent=False)
add_p('建设统一的城市管理数字化平台，将各类业务数据集中存储于关系数据库中，通过 Web 界面实现数据的在线管理与统计分析，是解决上述问题的有效途径。本项目的意义在于：以关系数据库为核心，建立区域—设施—事件—任务—维修—环境的数据闭环，实现业务数据的全生命周期管理，为城市精细化管理提供数据支撑和决策依据。')

doc.add_heading('1.2  功能需求分析', level=2)
add_p('根据城市管理业务流程，系统需满足以下功能需求：')
func_reqs = [
    ('区域管理', '支持行政区域的层级划分与信息维护，包括区域名称、上级区域、层级、位置描述等。系统预置 7 个区域：高新区、锦江区、武侯区、青羊区、成华区、金牛区、天府新区。'),
    ('基础设施管理', '记录道路、桥梁、照明、垃圾桶四类设施的位置、类型、安装时间及运行状态（正常/故障/维修中）。支持按区域和类型筛选查看，支持新增与删除操作。系统预置 40 个设施。'),
    ('市民事件上报', '市民通过电话注册（含姓名、邮箱）并上报道路损坏、设施故障、垃圾堆积、照明失效四类事件。系统记录事件标题、内容、类型、上报时间及处理状态（待处理/处理中/已完成）。支持事件的新增与删除。'),
    ('维修任务调度', '事件生成后由部门分派维修人员与维修资源执行任务，记录任务起止时间、执行状态（待执行/执行中/已完成）及备注。支持任务的派单与完成操作。'),
    ('维修记录归档', '任务完成后记录维修内容、维修时间、维修费用及维修结果，形成完整的维修档案。'),
    ('环境监测', '部署空气质量、噪音、水质、温湿度四类监测设备于各区域，设备按固定频率采集 PM2.5、PM10、噪音、温度、湿度等环境数据。支持设备清单查看与环境趋势分析。'),
    ('数据统计', '按区域和日期汇总事件总数、完成数、设施故障数及环境均值（平均噪音、平均 PM2.5），为管理决策提供数据支撑。'),
    ('四项规定查询', 'Q1 区域内设施查询、Q2 事件处理情况查询、Q3 维修人员统计查询、Q4 区域综合分析查询，支持条件筛选与结果展示。'),
]
for i, (name, desc) in enumerate(func_reqs, 1):
    add_p(f'（{i}）{name}：{desc}', indent=False)

doc.add_heading('1.3  数据需求分析', level=2)
add_p('系统需管理的数据实体按业务域分组如下：')
add_table(
    ['业务域', '实体（表）', '核心数据项', '预估数据量'],
    [
        ['区域域', '区域 RT', '区域编号、名称、上级、层级、位置', '7 条'],
        ['设施域', '基础设施 IT', '设施编号、区域、类型、名称、位置、安装时间、状态', '40 条'],
        ['事件域', '市民 CT', '市民编号、电话、姓名、邮箱、注册时间', '12 条'],
        ['事件域', '事件上报 ERT', '事件编号、市民、区域、设施、标题、内容、类型、时间、状态', '60 条'],
        ['事件域', '任务调度 TST', '任务编号、事件、人员、资源、部门、起止时间、状态', '60 条'],
        ['事件域', '维修记录 MRT', '记录编号、任务、设施、人员、内容、时间、费用、结果', '约 25 条'],
        ['资源域', '部门 DT', '部门编号、名称、电话、地址、负责人', '4 条'],
        ['资源域', '维修人员 WT', '人员编号、部门、姓名、电话、岗位、入职日期', '8 条'],
        ['资源域', '维修资源 TRT', '资源编号、名称、类型、编号、状态、归属部门', '16 条'],
        ['环境域', '监测设备 MDT', '设备编号、区域、名称、编号、类型、位置、在线状态', '12 条'],
        ['环境域', '环境数据 EDT', '数据编号、设备、PM2.5、PM10、噪音、温度、湿度、时间', '864 条'],
        ['统计域', '数据统计 ST', '统计编号、日期、区域、事件总数、完成数、故障数、均值', '84 条'],
    ],
    [2, 3, 7, 2]
)
add_p('各实体间存在大量关联关系：设施隶属于区域，事件由市民上报并关联区域与设施，任务由事件触发并分派给人员与资源，维修记录归属于任务，监测设备部署于区域并产生环境数据，统计按区域与日期聚合。这些关联关系通过外键约束在数据库层面保证参照完整性。')

doc.add_heading('1.4  数据流分析', level=2)
add_p('系统的核心数据流为"事件驱动"模式：市民上报事件 → 系统生成事件记录 → 部门分派任务 → 人员执行维修 → 记录维修结果 → 统计汇总。同时，环境监测设备持续采集数据，按区域和时间聚合后供综合分析使用。数据流经各表时，通过外键关联保持引用一致性，确保每条记录都能追溯到其来源。')
add_img(f'{IMG_DIR}/fig5_flow.png', 15)
add_p('图 5 展示了事件处理的核心业务流程，从市民上报到统计汇总共 6 个环节，每个环节对应一张数据库表的写入操作（图中标注了每步对应的 SQL 语句）。')

doc.add_page_break()

# ===== 第二章 =====
doc.add_heading('第二章  数据库概念结构设计', level=1)

doc.add_heading('2.1  实体识别与属性分析', level=2)
add_p('经需求分析，系统识别出 12 个核心实体。各实体的属性分析如下：')
add_table(
    ['实体', '主键', '核心属性', '外键属性'],
    [
        ['RT 区域', 'region_id', 'region_name, parent_id, region_level, location_desc, create_time', 'parent_id→RT（自引用）'],
        ['IT 基础设施', 'infra_id', 'infra_type, infra_name, location, install_time, status', 'region_id→RT'],
        ['CT 市民', 'citizen_id', 'phone(UNIQUE), real_name, email, register_time', '无'],
        ['DT 部门', 'dept_id', 'dept_name, dept_phone, dept_addr, manager', '无'],
        ['WT 维修人员', 'worker_id', 'worker_name, worker_phone(UNIQUE), post, hire_date', 'dept_id→DT'],
        ['TRT 维修资源', 'resource_id', 'resource_name, resource_type, resource_no, status', 'dept_id→DT'],
        ['ERT 事件上报', 'event_id', 'event_title, event_content, event_type, report_time, event_status', 'citizen_id→CT, region_id→RT, infra_id→IT'],
        ['TST 任务调度', 'task_id', 'task_start, task_end, task_status, note', 'event_id→ERT, worker_id→WT, resource_id→TRT, dept_id→DT'],
        ['MRT 维修记录', 'record_id', 'repair_content, repair_time, repair_cost, result', 'task_id→TST, infra_id→IT, worker_id→WT'],
        ['MDT 监测设备', 'device_id', 'device_name, device_no(UNIQUE), device_type, install_loc, online_status', 'region_id→RT'],
        ['EDT 环境数据', 'data_id', 'pm25, pm10, noise, temperature, humidity, collect_time', 'device_id→MDT'],
        ['ST 数据统计', 'stat_id', 'stat_date, event_total, event_finish, infra_broken, avg_noise, avg_pm25', 'region_id→RT'],
    ],
    [2, 2, 6, 4]
)

doc.add_heading('2.2  实体间联系分析', level=2)
add_p('各实体间的主要联系（均为一对多关系 1:N）如下表所示：')
add_table(
    ['联系', '父实体（1 端）', '子实体（N 端）', '删除策略', '业务含义'],
    [
        ['联系1', 'RT 区域', 'IT 基础设施', 'RESTRICT', '区域下有设施时禁止删除'],
        ['联系2', 'RT 区域', 'ERT 事件', 'RESTRICT', '区域下有事件时禁止删除'],
        ['联系3', 'RT 区域', 'MDT 设备', 'RESTRICT', '区域下有设备时禁止删除'],
        ['联系4', 'RT 区域', 'ST 统计', 'CASCADE', '区域删除时级联删除统计'],
        ['联系5', 'CT 市民', 'ERT 事件', 'CASCADE', '市民删除时级联删除其事件'],
        ['联系6', 'IT 设施', 'ERT 事件', 'SET NULL', '设施删除后事件保留，引用置空'],
        ['联系7', 'DT 部门', 'WT 人员', 'RESTRICT', '部门下有人员时禁止删除'],
        ['联系8', 'DT 部门', 'TRT 资源', 'RESTRICT', '部门下有资源时禁止删除'],
        ['联系9', 'DT 部门', 'TST 任务', 'RESTRICT', '部门下有任务时禁止删除'],
        ['联系10', 'ERT 事件', 'TST 任务', 'CASCADE', '事件删除时级联删除任务'],
        ['联系11', 'WT 人员', 'TST 任务', 'RESTRICT', '人员有任务时禁止删除'],
        ['联系12', 'TRT 资源', 'TST 任务', 'SET NULL', '资源删除后任务保留，引用置空'],
        ['联系13', 'TST 任务', 'MRT 维修', 'CASCADE', '任务删除时级联删除维修记录'],
        ['联系14', 'MDT 设备', 'EDT 环境数据', 'CASCADE', '设备删除时级联删除环境数据'],
    ],
    [1.5, 2.5, 2.5, 2.5, 5]
)

doc.add_heading('2.3  E-R 图设计', level=2)
add_p('根据上述实体与联系分析，绘制系统 E-R 关系图如下：')
add_img(f'{IMG_DIR}/fig2_er.png', 16)
add_p('图 2 中，矩形框代表实体，实体间的连线标注删除策略（CASCADE 级联删除 / SET NULL 置空引用 / RESTRICT 限制删除）。从 E-R 图可以看出，区域（RT）是系统的核心枢纽实体，向下关联基础设施（IT）、事件上报（ERT）、监测设备（MDT）和数据统计（ST）。事件上报（ERT）是业务主线实体，串联市民（CT）、区域（RT）、基础设施（IT）和任务调度（TST）。任务调度（TST）再关联维修人员（WT）、维修资源（TRT）和部门（DT），形成完整的任务执行链。维修记录（MRT）挂在任务调度（TST）之下，环境数据（EDT）由监测设备（MDT）产生。')
add_p('系统整体形成两条数据链路：')
add_p('（1）业务处理链：区域 → 设施 → 事件 → 任务 → 维修记录', indent=False)
add_p('（2）环境监测链：区域 → 设备 → 环境数据 → 统计', indent=False)

doc.add_page_break()

# ===== 第三章 =====
doc.add_heading('第三章  数据库逻辑结构设计', level=1)

doc.add_heading('3.1  E-R 模型向关系模式转换', level=2)
add_p('将 E-R 模型转换为关系模式遵循以下规则：')
add_p('（1）每个实体转换为一个关系模式，实体的属性转换为关系的属性，实体的主键转换为关系的主键。', indent=False)
add_p('（2）每个 1:N 联系通过在 N 端关系中加入 1 端关系的主键作为外键来实现。', indent=False)
add_p('（3）自引用联系（如区域的 parent_id）在同一关系中加入外键。', indent=False)
add_p('转换结果为 12 个关系模式，各模式的主键加下划线，外键以斜体标注。')

doc.add_heading('3.2  关系模式定义', level=2)
schemes = [
    'RT（<u>region_id</u>, region_name, parent_id, region_level, location_desc, create_time）',
    'IT（<u>infra_id</u>, <i>region_id</i>, infra_type, infra_name, location, install_time, status）',
    'CT（<u>citizen_id</u>, phone, real_name, email, register_time）',
    'DT（<u>dept_id</u>, dept_name, dept_phone, dept_addr, manager）',
    'WT（<u>worker_id</u>, <i>dept_id</i>, worker_name, worker_phone, post, hire_date）',
    'TRT（<u>resource_id</u>, resource_name, resource_type, resource_no, status, <i>dept_id</i>）',
    'ERT（<u>event_id</u>, <i>citizen_id</i>, <i>region_id</i>, <i>infra_id</i>, event_title, event_content, event_type, report_time, event_status）',
    'TST（<u>task_id</u>, <i>event_id</i>, <i>worker_id</i>, <i>resource_id</i>, <i>dept_id</i>, task_start, task_end, task_status, note）',
    'MRT（<u>record_id</u>, <i>task_id</i>, <i>infra_id</i>, <i>worker_id</i>, repair_content, repair_time, repair_cost, result）',
    'MDT（<u>device_id</u>, <i>region_id</i>, device_name, device_no, device_type, install_loc, online_status, install_time）',
    'EDT（<u>data_id</u>, <i>device_id</i>, pm25, pm10, noise, temperature, humidity, collect_time）',
    'ST（<u>stat_id</u>, stat_date, <i>region_id</i>, event_total, event_finish, infra_broken, avg_noise, avg_pm25, stat_create）',
]
for s in schemes:
    add_p(s, indent=False)

doc.add_heading('3.3  范式分析', level=2)
add_p('对上述关系模式进行规范化分析：')
add_p('（1）第一范式（1NF）：所有关系的属性都是原子的，不可再分。如 location 存储坐标字符串、event_content 存储文本，均为单值属性。满足 1NF。', indent=False)
add_p('（2）第二范式（2NF）：所有关系的主键均为单列自增 ID，不存在部分函数依赖。满足 2NF。', indent=False)
add_p('（3）第三范式（3NF）：各关系的非主属性对主键不存在传递依赖。例如，TST 表中的 dept_id 虽可通过 worker_id 间接确定（人员隶属于部门），但任务可直接指定执行部门，故保留 dept_id 为直接外键而非冗余——这是业务需求而非范式违例。其余关系均无传递依赖。满足 3NF。', indent=False)
add_p('（4）BCNF：所有决定因素均为候选键。各关系模式中，函数依赖的左部均为候选键，满足 BCNF。', indent=False)
add_p('综上，系统所有关系模式均满足 BCNF 范式要求，数据库设计规范化程度良好。')

doc.add_heading('3.4  表结构详细设计', level=2)
add_p('各表的字段定义如下（按建表顺序排列）：')

tables_def = [
    ('表 3.1  RT 区域表', [
        ['字段名', '数据类型', '约束', '说明'],
        ['region_id', 'INT', 'PK, AUTO_INCREMENT', '区域编号（主键）'],
        ['region_name', 'VARCHAR(50)', 'NOT NULL', '区域名称'],
        ['parent_id', 'INT', 'NULL', '上级区域编号（自引用外键）'],
        ['region_level', 'TINYINT', 'NULL', '区域层级（1=区级）'],
        ['location_desc', 'VARCHAR(200)', 'NULL', '位置描述'],
        ['create_time', 'DATETIME', 'DEFAULT CURRENT_TIMESTAMP', '创建时间'],
    ]),
    ('表 3.2  IT 基础设施表', [
        ['字段名', '数据类型', '约束', '说明'],
        ['infra_id', 'INT', 'PK, AUTO_INCREMENT', '设施编号（主键）'],
        ['region_id', 'INT', 'FK→RT, NOT NULL', '所属区域编号'],
        ['infra_type', 'VARCHAR(30)', 'NOT NULL', '设施类型（道路/桥梁/照明/垃圾桶）'],
        ['infra_name', 'VARCHAR(100)', 'NOT NULL', '设施名称'],
        ['location', 'VARCHAR(200)', 'NOT NULL', '位置坐标'],
        ['install_time', 'DATETIME', 'NULL', '安装时间'],
        ['status', 'TINYINT', 'NOT NULL DEFAULT 1', '状态（1正常/2故障/3维修中）'],
    ]),
    ('表 3.3  CT 市民表', [
        ['字段名', '数据类型', '约束', '说明'],
        ['citizen_id', 'INT', 'PK, AUTO_INCREMENT', '市民编号（主键）'],
        ['phone', 'VARCHAR(20)', 'NOT NULL UNIQUE', '电话号码（唯一）'],
        ['real_name', 'VARCHAR(30)', 'NULL', '真实姓名'],
        ['email', 'VARCHAR(100)', 'NULL', '电子邮箱'],
        ['register_time', 'DATETIME', 'DEFAULT CURRENT_TIMESTAMP', '注册时间'],
    ]),
    ('表 3.4  DT 部门表', [
        ['字段名', '数据类型', '约束', '说明'],
        ['dept_id', 'INT', 'PK, AUTO_INCREMENT', '部门编号（主键）'],
        ['dept_name', 'VARCHAR(80)', 'NOT NULL', '部门名称'],
        ['dept_phone', 'VARCHAR(20)', 'NULL', '部门联系电话'],
        ['dept_addr', 'VARCHAR(200)', 'NULL', '部门办公地址'],
        ['manager', 'VARCHAR(30)', 'NULL', '部门负责人'],
    ]),
    ('表 3.5  WT 维修人员表', [
        ['字段名', '数据类型', '约束', '说明'],
        ['worker_id', 'INT', 'PK, AUTO_INCREMENT', '人员编号（主键）'],
        ['dept_id', 'INT', 'FK→DT, NOT NULL', '所属部门编号'],
        ['worker_name', 'VARCHAR(30)', 'NOT NULL', '人员姓名'],
        ['worker_phone', 'VARCHAR(20)', 'NOT NULL UNIQUE', '联系电话（唯一）'],
        ['post', 'VARCHAR(50)', 'NULL', '岗位'],
        ['hire_date', 'DATE', 'NULL', '入职日期'],
    ]),
    ('表 3.6  TRT 维修资源表', [
        ['字段名', '数据类型', '约束', '说明'],
        ['resource_id', 'INT', 'PK, AUTO_INCREMENT', '资源编号（主键）'],
        ['resource_name', 'VARCHAR(80)', 'NOT NULL', '资源名称'],
        ['resource_type', 'VARCHAR(30)', 'NOT NULL', '资源类型（车辆/平台/工具/仪器）'],
        ['resource_no', 'VARCHAR(50)', 'NOT NULL', '资源编号'],
        ['status', 'TINYINT', 'NOT NULL DEFAULT 1', '状态（1空闲/2使用中/3维修中）'],
        ['dept_id', 'INT', 'FK→DT, NOT NULL', '归属部门编号'],
    ]),
    ('表 3.7  ERT 事件上报表', [
        ['字段名', '数据类型', '约束', '说明'],
        ['event_id', 'INT', 'PK, AUTO_INCREMENT', '事件编号（主键）'],
        ['citizen_id', 'INT', 'FK→CT ON DELETE CASCADE', '上报市民编号'],
        ['region_id', 'INT', 'FK→RT ON DELETE RESTRICT', '事件发生区域'],
        ['infra_id', 'INT', 'FK→IT ON DELETE SET NULL', '关联设施编号'],
        ['event_title', 'VARCHAR(100)', 'NOT NULL', '事件标题'],
        ['event_content', 'TEXT', 'NULL', '事件详细内容'],
        ['event_type', 'VARCHAR(30)', 'NOT NULL', '事件类型（道路损坏/设施故障/垃圾堆积/照明失效）'],
        ['report_time', 'DATETIME', 'DEFAULT CURRENT_TIMESTAMP', '上报时间'],
        ['event_status', 'TINYINT', 'NOT NULL DEFAULT 1', '状态（1待处理/2处理中/3已完成）'],
    ]),
    ('表 3.8  TST 任务调度表', [
        ['字段名', '数据类型', '约束', '说明'],
        ['task_id', 'INT', 'PK, AUTO_INCREMENT', '任务编号（主键）'],
        ['event_id', 'INT', 'FK→ERT ON DELETE CASCADE', '关联事件编号'],
        ['worker_id', 'INT', 'FK→WT ON DELETE RESTRICT', '分派维修人员'],
        ['resource_id', 'INT', 'FK→TRT ON DELETE SET NULL', '分配维修资源'],
        ['dept_id', 'INT', 'FK→DT ON DELETE RESTRICT', '执行部门'],
        ['task_start', 'DATETIME', 'NULL', '任务开始时间'],
        ['task_end', 'DATETIME', 'NULL', '任务结束时间'],
        ['task_status', 'TINYINT', 'NOT NULL DEFAULT 1', '状态（1待执行/2执行中/3已完成）'],
        ['note', 'TEXT', 'NULL', '备注'],
    ]),
    ('表 3.9  MRT 维修记录表', [
        ['字段名', '数据类型', '约束', '说明'],
        ['record_id', 'INT', 'PK, AUTO_INCREMENT', '记录编号（主键）'],
        ['task_id', 'INT', 'FK→TST ON DELETE CASCADE', '关联任务编号'],
        ['infra_id', 'INT', 'FK→IT ON DELETE SET NULL', '维修设施编号'],
        ['worker_id', 'INT', 'FK→WT ON DELETE RESTRICT', '执行维修人员'],
        ['repair_content', 'TEXT', 'NOT NULL', '维修内容描述'],
        ['repair_time', 'DATETIME', 'DEFAULT CURRENT_TIMESTAMP', '维修完成时间'],
        ['repair_cost', 'DECIMAL(10,2)', 'NULL', '维修费用（元）'],
        ['result', 'TINYINT', 'NOT NULL DEFAULT 1', '维修结果（1已修复）'],
    ]),
    ('表 3.10  MDT 监测设备表', [
        ['字段名', '数据类型', '约束', '说明'],
        ['device_id', 'INT', 'PK, AUTO_INCREMENT', '设备编号（主键）'],
        ['region_id', 'INT', 'FK→RT ON DELETE RESTRICT', '部署区域编号'],
        ['device_name', 'VARCHAR(80)', 'NOT NULL', '设备名称'],
        ['device_no', 'VARCHAR(50)', 'NOT NULL UNIQUE', '设备编号（唯一）'],
        ['device_type', 'VARCHAR(30)', 'NOT NULL', '设备类型（空气质量/噪音/水质/温湿度）'],
        ['install_loc', 'VARCHAR(200)', 'NOT NULL', '安装位置'],
        ['online_status', 'TINYINT', 'NOT NULL DEFAULT 1', '在线状态（1在线/0离线）'],
        ['install_time', 'DATETIME', 'NULL', '安装时间'],
    ]),
    ('表 3.11  EDT 环境数据表', [
        ['字段名', '数据类型', '约束', '说明'],
        ['data_id', 'BIGINT', 'PK, AUTO_INCREMENT', '数据编号（主键）'],
        ['device_id', 'INT', 'FK→MDT ON DELETE CASCADE', '采集设备编号'],
        ['pm25', 'FLOAT', 'NULL', 'PM2.5 浓度（μg/m³）'],
        ['pm10', 'FLOAT', 'NULL', 'PM10 浓度（μg/m³）'],
        ['noise', 'FLOAT', 'NULL', '噪音值（dB）'],
        ['temperature', 'FLOAT', 'NULL', '温度（℃）'],
        ['humidity', 'FLOAT', 'NULL', '湿度（%）'],
        ['collect_time', 'DATETIME', 'NOT NULL', '数据采集时间'],
    ]),
    ('表 3.12  ST 数据统计表', [
        ['字段名', '数据类型', '约束', '说明'],
        ['stat_id', 'INT', 'PK, AUTO_INCREMENT', '统计编号（主键）'],
        ['stat_date', 'DATE', 'NOT NULL', '统计日期'],
        ['region_id', 'INT', 'FK→RT ON DELETE CASCADE', '区域编号'],
        ['event_total', 'INT', 'NOT NULL', '事件总数'],
        ['event_finish', 'INT', 'NOT NULL', '已完成事件数'],
        ['infra_broken', 'INT', 'NOT NULL', '设施故障数'],
        ['avg_noise', 'FLOAT', 'NULL', '平均噪音值'],
        ['avg_pm25', 'FLOAT', 'NULL', '平均 PM2.5 值'],
        ['stat_create', 'DATETIME', 'DEFAULT CURRENT_TIMESTAMP', '统计记录生成时间'],
    ]),
]
for title, rows in tables_def:
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(6)
    run = p.add_run(title); run.bold = True; run.font.size = Pt(12)
    run.font.name = '黑体'; run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    add_table(rows[0], rows[1:], [3.5, 3, 4.5, 3.5])

doc.add_page_break()

# ===== 第四章 =====
doc.add_heading('第四章  数据库物理实现', level=1)

doc.add_heading('4.1  数据库与表创建', level=2)
add_p('数据库命名为 CMPD（City Management Platform Database），字符集采用 utf8mb4 以支持中文和 Emoji 字符，排序规则为 utf8mb4_general_ci，存储引擎为 InnoDB 以支持事务和外键约束。建表时按外键依赖顺序先建被引用表（RT、CT、DT），再建引用表，避免外键创建失败。')
add_p('数据库创建语句：')
add_code("CREATE SCHEMA IF NOT EXISTS `CMPD` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;\nUSE `CMPD`;")
add_p('核心建表 SQL（区域表、设施表、事件表——展示外键约束策略）：')
add_code("""CREATE TABLE `RT` (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;""")
add_p('其余各表按相同模式创建，完整建表脚本共 185 行，保存在 init_db.py 文件中。')

doc.add_heading('4.2  外键约束策略', level=2)
add_p('系统根据业务语义为各外键设置不同的删除策略，保证数据参照完整性：')
add_table(
    ['删除策略', '应用场景', '业务理由'],
    [
        ['CASCADE\n（级联删除）', 'CT→ERT、ERT→TST、TST→MRT、MDT→EDT、RT→ST', '子表数据完全依附于父表，父记录删除时子记录无独立存在意义，应一并删除'],
        ['SET NULL\n（置空引用）', 'IT→ERT(infra_id)、TRT→TST(resource_id)、IT→MRT(infra_id)', '设施或资源删除后，事件和任务记录仍需保留以备查，仅清除对外键的引用'],
        ['RESTRICT\n（限制删除）', 'RT→IT、RT→ERT、RT→MDT、DT→WT、DT→TRT、DT→TST、WT→TST、WT→MRT、RT→MDT', '存在依赖数据时禁止删除父记录，防止产生孤儿数据，需先删除子记录'],
    ],
    [2.5, 6, 6]
)
add_p('外键约束在数据库层面保证了参照完整性，即任何一条记录的外键值必须指向已存在的父记录或为空（SET NULL 场景）。这使得应用层无需额外编写一致性检查代码，由数据库引擎自动维护。')

doc.add_heading('4.3  索引设计', level=2)
add_p('除主键自动创建的聚簇索引外，系统在以下字段上利用 UNIQUE 约束创建了唯一索引：')
add_table(
    ['表', '字段', '索引类型', '说明'],
    [
        ['CT', 'phone', 'UNIQUE', '市民电话唯一，防止重复注册'],
        ['WT', 'worker_phone', 'UNIQUE', '人员电话唯一'],
        ['MDT', 'device_no', 'UNIQUE', '设备编号唯一'],
    ],
    [2, 3, 2.5, 6]
)
add_p('外键字段由 InnoDB 自动创建索引以加速关联查询。对于频繁筛选的字段（如 IT.status、ERT.event_status、ERT.event_type、ERT.report_time），在实际生产环境中可考虑添加普通索引以提升查询性能。')

doc.add_heading('4.4  数据初始化', level=2)
add_p('系统通过 init_db.py 脚本预置了示例数据，用于功能演示与查询验证。数据初始化遵循以下原则：')
add_p('（1）先插入无外键依赖的基础表（RT、DT、CT），再插入有外键依赖的表。', indent=False)
add_p('（2）数据之间保持业务逻辑一致性：已完成的事件对应已完成的任务，已完成的任务对应有维修记录。', indent=False)
add_p('（3）环境数据按时间序列生成，模拟真实采集频率（每 3 小时一次）。', indent=False)
add_p('各表预置数据量如下：')
add_table(
    ['表', '记录数', '数据说明'],
    [
        ['RT 区域表', '7', '高新区、锦江区、武侯区、青羊区、成华区、金牛区、天府新区'],
        ['DT 部门表', '4', '市政设施科、环境卫生科、照明管理科、桥梁养护科'],
        ['CT 市民表', '12', '市民A~市民L，含随机电话与邮箱'],
        ['WT 维修人员表', '8', '8名维修工（张明、李华、王强等）分属4个部门'],
        ['IT 基础设施表', '40', '道路、桥梁、照明、垃圾桶四类，随机分布于7个区域'],
        ['TRT 维修资源表', '16', '维修车辆、升降平台、电动工具、检测设备各4个'],
        ['ERT 事件上报表', '60', '4种事件类型，时间分布于2026年11月1~12日'],
        ['TST 任务调度表', '60', '每事件对应一个任务，状态与事件状态联动'],
        ['MRT 维修记录表', '约25', '已完成任务生成维修记录，含100~2000元随机费用'],
        ['MDT 监测设备表', '12', '空气质量、噪音、水质、温湿度四类设备各3台'],
        ['EDT 环境数据表', '864', '12设备×6天×每3小时采集=864条，含正弦波模拟日变化'],
        ['ST 数据统计表', '84', '12天×7区域的日统计汇总'],
    ],
    [3, 2, 9]
)
add_p('表依赖层级图如下，展示了各表之间的外键依赖关系和建表顺序：')
add_img(f'{IMG_DIR}/fig1_hierarchy.png', 15)
add_p('图 1 中，第 1 层为无外键依赖的基础表（RT、CT、DT），第 2 层依赖基础表（IT、WT、TRT、MDT、ST），第 3 层为事件核心表（ERT）和环境数据表（EDT），第 4 层为任务调度表（TST），第 5 层为维修记录表（MRT）。建表时必须按层级从上到下依次创建，删除时则反向操作。')

doc.add_page_break()

# ===== 第五章 =====
doc.add_heading('第五章  系统功能实现', level=1)

doc.add_heading('5.1  技术架构设计', level=2)
add_p('系统采用前后端分离的三层架构，各层职责清晰、技术选型轻量：')
add_img(f'{IMG_DIR}/fig3_arch.png', 14)
add_table(
    ['层次', '技术选型', '版本', '职责'],
    [
        ['表现层\n（前端）', 'Vue 3 + ECharts', 'Vue 3.x (CDN)\nECharts 5.x', '单页应用，数据渲染与用户交互，通过 Fetch API 调用后端接口'],
        ['业务逻辑层\n（后端）', 'Python + Flask', 'Python 3.9\nFlask 3.x', 'RESTful API 服务，业务逻辑处理，SQL 拼装与执行，JSON 响应'],
        ['数据持久层\n（数据库）', 'MySQL', 'MySQL 8.4\nInnoDB', '数据持久化存储，外键约束保证完整性，事务保证原子性'],
    ],
    [2.5, 3.5, 3, 5.5]
)
add_p('技术选型理由：')
add_p('（1）Flask：轻量级 Web 框架，无需复杂配置即可快速构建 RESTful API，适合课程设计规模的项目。', indent=False)
add_p('（2）pymysql：纯 Python 实现的 MySQL 驱动，安装简单，API 直观，支持事务和参数化查询（防止 SQL 注入）。', indent=False)
add_p('（3）Vue 3 CDN 方式：无需 Node.js 构建环境，浏览器直接加载，降低部署复杂度，同时享受 Vue 3 的响应式数据绑定和组件化开发体验。', indent=False)
add_p('（4）ECharts：功能丰富的图表库，支持折线图、饼图、柱状图等，满足数据可视化需求。', indent=False)
add_p('（5）MySQL InnoDB：支持事务、外键约束和行级锁，是关系数据库的标准存储引擎，适合需要数据一致性的业务系统。', indent=False)

doc.add_heading('5.2  后端 API 设计与实现', level=2)
add_p('后端共提供 24 个 RESTful API 接口，遵循 HTTP 语义规范：GET 用于查询，POST 用于新增，PUT 用于修改，DELETE 用于删除。所有接口返回 JSON 格式数据，成功响应包含 code=0，失败响应包含 code 非 0 和错误消息 msg。通过 Flask-CORS 中间件支持跨域访问。')
add_p('接口按功能分类如下：')
add_table(
    ['分类', '接口路径', '方法', '功能说明'],
    [
        ['概览', '/api/overview', 'GET', '平台概览 KPI 指标（事件总数、完成率、设施数、人员数）'],
        ['概览', '/api/overview/charts', 'GET', '事件趋势折线图 + 事件类型饼图数据'],
        ['区域', '/api/regions', 'GET', '获取区域列表（下拉选项）'],
        ['设施', '/api/infra', 'GET', '基础设施列表（支持区域/类型筛选）'],
        ['设施', '/api/infra/stats', 'GET', '设施统计（按类型/状态分组计数）'],
        ['设施', '/api/infra', 'POST', '新增基础设施'],
        ['设施', '/api/infra/<id>', 'PUT', '修改基础设施信息'],
        ['设施', '/api/infra/<id>', 'DELETE', '删除基础设施（受外键约束）'],
        ['事件', '/api/events', 'GET', '事件列表（支持时间/类型/状态筛选）'],
        ['事件', '/api/events/stats', 'GET', '事件统计（按类型/状态分组）'],
        ['事件', '/api/events', 'POST', '市民上报新事件'],
        ['事件', '/api/events/<id>', 'DELETE', '删除事件（级联删除任务）'],
        ['市民', '/api/citizens', 'GET/POST', '市民列表查询 / 新增市民注册'],
        ['市民', '/api/citizens/<id>', 'PUT/DELETE', '修改市民信息 / 删除市民'],
        ['部门', '/api/depts, /api/depts/full', 'GET', '部门列表（简略/含人员数）'],
        ['人员', '/api/workers', 'GET/POST', '维修人员列表 / 新增人员'],
        ['资源', '/api/resources', 'GET/POST', '维修资源列表 / 新增资源'],
        ['任务', '/api/tasks', 'GET/POST', '任务列表 / 派单（含完成操作）'],
        ['维修', '/api/repairs', 'GET/POST', '维修记录列表 / 新增维修记录'],
        ['环境', '/api/devices', 'GET', '监测设备清单'],
        ['环境', '/api/env/trend', 'GET', '环境数据趋势（PM2.5/噪音/温湿度）'],
        ['查询', '/api/q1', 'GET', 'Q1 区域内设施查询'],
        ['查询', '/api/q2', 'GET', 'Q2 事件处理情况查询'],
        ['查询', '/api/q3', 'GET', 'Q3 维修人员统计查询'],
        ['查询', '/api/q4', 'GET', 'Q4 区域综合分析查询'],
    ],
    [1.5, 5, 2.5, 5.5]
)

doc.add_heading('5.3  前端功能模块', level=2)
add_p('前端采用 Vue 3 单页应用架构，通过 CDN 引入 Vue 3 和 ECharts，无需构建工具。页面包含左侧导航栏和右侧内容区，通过 Vue 响应式数据绑定实现页面切换。系统功能模块结构如下：')
add_img(f'{IMG_DIR}/fig4_modules.png', 16)
add_p('各功能模块详细说明：')
modules_detail = [
    ('平台概览', '展示 KPI 指标卡（事件总数、完成率、设施数、人员数）和两个图表：事件数量趋势折线图（按日期）和事件类型分布饼图。数据通过 /api/overview 和 /api/overview/charts 接口获取。'),
    ('数据模型', '展示 12 张数据库表的结构信息（表名、字段、类型、约束）和 E-R 关系图，帮助理解数据库设计。'),
    ('基础设施管理', '设施列表支持按区域和类型筛选，显示设施编号、名称、类型、位置、安装时间、状态。提供统计卡片展示各类型/状态的数量分布。支持新增设施（填写区域、类型、名称、位置等信息）和删除设施（受外键约束，关联事件时无法删除）。'),
    ('事件报告处理', '事件列表支持按时间范围、事件类型、处理状态筛选。展示事件编号、标题、类型、上报时间、负责部门、处理人员、状态。支持市民上报新事件（选择区域、设施、类型，填写标题和内容）和删除事件（级联删除关联任务）。'),
    ('资源调度', '任务列表展示所有维修任务及其关联的事件、人员、资源、状态。支持派单操作（为待处理事件分派维修人员和资源）和任务完成操作（记录结束时间，生成维修记录）。'),
    ('环境监测', '设备清单展示所有监测设备的名称、编号、类型、部署区域、在线状态。环境趋势图通过 ECharts 多折线图展示 PM2.5、噪音、温度等指标随时间的变化趋势。'),
    ('市民管理', '市民列表展示所有注册市民的编号、电话、姓名、邮箱、注册时间。支持新增市民（填写电话、姓名、邮箱）和删除市民（级联删除其上报的事件）。'),
    ('部门管理', '部门列表展示所有部门的编号、名称、电话、地址、负责人。支持新增和删除部门（有人员时禁止删除）。'),
    ('人员管理', '维修人员列表展示所有人员的编号、姓名、所属部门、电话、岗位、入职日期。支持新增和删除人员。'),
    ('期末查询', 'Q1~Q4 四项查询页面，每项查询提供独立的筛选条件和结果展示区域，结果以表格形式展示，部分查询附带 ECharts 图表。'),
]
for i, (name, desc) in enumerate(modules_detail, 1):
    add_p(f'（{i}）{name}：{desc}', indent=False)

doc.add_heading('5.4  关键代码实现', level=2)
add_p('（1）数据库连接工具层（db.py）：', indent=False)
add_code("""import pymysql
from config import MYSQL

def get_conn():
    return pymysql.connect(host=MYSQL['host'], port=MYSQL['port'],
        user=MYSQL['user'], password=MYSQL['password'],
        database=MYSQL['database'], charset=MYSQL['charset'],
        cursorclass=pymysql.cursors.DictCursor)

def query(sql, args=None):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, args)
            return cur.fetchall()
    finally:
        conn.close()

def execute(sql, args=None):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, args)
        conn.commit()  # 显式提交事务
    finally:
        conn.close()""")
add_p('（2）Flask 路由与 API 实现（app.py 节选——以新增市民接口为例）：', indent=False)
add_code("""@app.route('/api/citizens', methods=['POST'])
def add_citizen():
    d = request.json  # 获取前端提交的JSON数据
    rid = db.execute_returning_id(
        "INSERT INTO CT(phone,real_name,email) VALUES(%s,%s,%s)",
        (d['phone'], d.get('real_name', ''), d.get('email', '')))
    return jsonify({'code': 0, 'msg': '市民已新增', 'citizen_id': rid})""")
add_p('（3）前端 API 调用（index.html 节选——以新增市民为例）：', indent=False)
add_code("""async function submitForm() {
    // 收集表单数据
    const data = {phone: form.phone, real_name: form.name, email: form.email};
    // 调用后端API
    const r = await post('/api/citizens', data);
    if (r.code) { showToast(r.msg, false); return; }  // 失败时显示错误
    showToast('已新增');  // 成功提示
    loadCitizens();  // 刷新列表
}""")

doc.add_page_break()

# ===== 第六章 =====
doc.add_heading('第六章  四项期末查询设计与验证', level=1)
add_p('本章详细阐述四项期末规定查询的需求分析、SQL 设计、接口实现与验证结果。四项查询分别从设施管理、事件处理、人员绩效、区域综合四个维度对数据库进行多表关联查询与统计分析。')
add_p('四项查询各自涉及的表及连接关系如下图所示：')
add_img(f'{IMG_DIR}/fig6_queries.png', 16)
add_p('图 6 展示了 Q1~Q4 四项查询各自涉及的表及连接方式（INNER JOIN / LEFT JOIN）。Q1 仅涉及 2 表内连接；Q2 涉及 5 表以 LEFT JOIN 为主；Q3 涉及 3 表内连接做分组统计；Q4 涉及 5 表，包含事件统计与环境趋势两组子查询。')

doc.add_heading('6.1  Q1 — 区域内设施查询', level=2)
add_p('【查询需求】查询指定区域内基础设施的编号、类型、名称、安装日期与运行状态，支持按设施类型进一步筛选。')
add_p('【涉及表】IT（基础设施表）、RT（区域表）', indent=False)
add_p('【连接方式】内连接（INNER JOIN），通过 region_id 关联', indent=False)
add_p('【SQL 实现】', indent=False)
add_code("""SELECT i.infra_id, i.infra_type, i.infra_name, i.install_time,
       i.status, i.location, r.region_name
FROM IT i
JOIN RT r ON i.region_id = r.region_id
WHERE r.region_name = %s        -- 区域名称参数
  AND i.infra_type = %s          -- 设施类型参数（可选）
ORDER BY i.infra_id;""")
add_p('【接口】GET /api/q1?region=高新区&type=道路', indent=False)
add_p('【前端交互】提供区域下拉选择框和设施类型下拉选择框，用户选择后点击查询按钮，结果以表格形式展示，状态字段映射为"正常/故障/维修中"的中文显示。', indent=False)
add_p('【验证】以"高新区"为例，查询该区域所有设施，结果返回该区域内的道路、桥梁、照明、垃圾桶等设施的详细信息，数据与数据库实际记录一致。', indent=False)

doc.add_heading('6.2  事件处理情况查询', level=2)
add_p('【查询需求】查询指定时间范围内事件的类型、报告时间、负责部门、处理人员与处理状态，支持按事件类型筛选，结果按报告时间降序排列。')
add_p('【涉及表】ERT（事件上报表）、TST（任务调度表）、DT（部门表）、WT（人员表）、RT（区域表）', indent=False)
add_p('【连接方式】LEFT JOIN 为主，ERT 与 RT 之间使用 INNER JOIN', indent=False)
add_p('【SQL 实现】', indent=False)
add_code("""SELECT e.event_id, e.event_type, e.event_title, e.report_time,
       e.event_status, d.dept_name AS dept, w.worker_name AS worker,
       r.region_name AS region
FROM ERT e
LEFT JOIN TST t ON e.event_id = t.event_id       -- 事件关联任务
LEFT JOIN DT d ON t.dept_id = d.dept_id           -- 任务关联部门
LEFT JOIN WT w ON t.worker_id = w.worker_id       -- 任务关联人员
JOIN RT r ON e.region_id = r.region_id            -- 事件关联区域
WHERE e.report_time BETWEEN %s AND %s             -- 时间范围参数
  AND e.event_type = %s                            -- 事件类型参数（可选）
ORDER BY e.report_time DESC
LIMIT 300;""")
add_p('【接口】GET /api/q2?start=2026-11-01&end=2026-11-12&type=', indent=False)
add_p('【设计要点】使用 LEFT JOIN 连接 TST、DT、WT，因为并非所有事件都已分派任务（待处理事件无关联任务记录）。通过 LEFT JOIN 保证所有事件都能显示，未分派的事件其部门和人员字段显示为"—"。', indent=False)
add_p('【验证】查询 2026-11-01 至 2026-11-12 期间所有事件，结果包含 60 条记录，涵盖四种事件类型。已完成事件显示对应的部门和人员，待处理事件的部门和人员显示为"—"，数据正确。', indent=False)

doc.add_heading('6.3  维修人员统计查询', level=2)
add_p('【查询需求】统计各维修人员在指定时间范围内的任务总数、已完成任务数、任务完成率（%）与平均处理时长（分钟），结果按任务数降序排列。')
add_p('【涉及表】TST（任务调度表）、WT（人员表）、DT（部门表）', indent=False)
add_p('【连接方式】INNER JOIN，通过 worker_id 和 dept_id 关联', indent=False)
add_p('【SQL 实现】', indent=False)
add_code("""SELECT w.worker_name AS worker, d.dept_name AS dept,
       COUNT(t.task_id) AS total,                              -- 任务总数
       SUM(IF(t.task_status=3,1,0)) AS done,                   -- 已完成数
       ROUND(SUM(IF(t.task_status=3,1,0))/COUNT(t.task_id)*100,1) AS rate,  -- 完成率
       ROUND(AVG(                                              -- 平均处理时长
           IF(t.task_status=3 AND t.task_start IS NOT NULL
              AND t.task_end IS NOT NULL,
              TIMESTAMPDIFF(MINUTE,t.task_start,t.task_end),
              NULL)), 1) AS avg_min
FROM TST t
JOIN WT w ON t.worker_id = w.worker_id
JOIN DT d ON w.dept_id = d.dept_id
WHERE t.task_start BETWEEN %s AND %s
GROUP BY w.worker_id, d.dept_name
ORDER BY total DESC;""")
add_p('【接口】GET /api/q3?start=2026-11-01&end=2026-11-12', indent=False)
add_p('【设计要点】使用 IF 条件表达式在聚合函数内进行条件计数：SUM(IF(task_status=3,1,0)) 统计已完成任务数。使用 TIMESTAMPDIFF(MINUTE,...) 计算任务处理时长（分钟）。AVG 函数仅对已完成任务（task_status=3 且有起止时间）计算平均时长，未完成任务用 NULL 排除。ROUND 函数保留一位小数。', indent=False)
add_p('【验证】查询 2026-11-01 至 2026-11-12 期间各维修人员的统计信息，结果按任务数降序排列，展示 8 名维修人员的任务数、完成数、完成率与平均处理时长。完成率最高的人员达到 100%，平均处理时长在数十分钟到数小时不等，数据合理。', indent=False)

doc.add_heading('6.4  区域综合分析查询', level=2)
add_p('【查询需求】统计各区域在指定时间范围内的事件总数、完成数、完成率、平均处理时长（小时），并关联环境监测数据（PM2.5、噪音、PM10、温度）的变化趋势，进行区域综合治理情况分析。')
add_p('【涉及表】RT（区域表）、ERT（事件表）、TST（任务表）、EDT（环境数据表）、MDT（设备表）', indent=False)
add_p('【SQL 实现——区域统计部分】', indent=False)
add_code("""SELECT r.region_name AS region,
       COUNT(e.event_id) AS total,                              -- 事件总数
       SUM(IF(e.event_status=3,1,0)) AS done,                   -- 完成数
       ROUND(SUM(IF(e.event_status=3,1,0))/COUNT(e.event_id)*100,1) AS rate,
       ROUND(AVG(                                               -- 平均处理时长(小时)
           IF(e.event_status=3 AND t.task_end IS NOT NULL,
              TIMESTAMPDIFF(MINUTE,e.report_time,t.task_end),
              NULL)) / 60, 1) AS avg_hour
FROM RT r
LEFT JOIN ERT e ON r.region_id = e.region_id
    AND e.report_time BETWEEN %s AND %s
LEFT JOIN TST t ON e.event_id = t.event_id
GROUP BY r.region_id
ORDER BY total DESC;""")
add_p('【SQL 实现——环境趋势部分】', indent=False)
add_code("""SELECT r.region_name AS region,
       DATE_FORMAT(ed.collect_time, '%%m-%%d') AS d,            -- 日期(月-日)
       ROUND(AVG(ed.pm25), 1) AS pm25,
       ROUND(AVG(ed.noise), 1) AS noise,
       ROUND(AVG(ed.pm10), 1) AS pm10,
       ROUND(AVG(ed.temperature), 1) AS temp
FROM EDT ed
JOIN MDT m ON ed.device_id = m.device_id
JOIN RT r ON m.region_id = r.region_id
WHERE ed.collect_time BETWEEN %s AND %s
GROUP BY r.region_id, d
ORDER BY d;""")
add_p('【接口】GET /api/q4?start=2026-11-01&end=2026-11-12', indent=False)
add_p('【设计要点】该查询返回两组数据：stat（区域统计）和 env（环境趋势）。区域统计部分以 RT 为左表 LEFT JOIN ERT，保证所有区域都显示（即使无事件）。平均处理时长计算从事件上报时间到任务结束时间的总耗时（小时）。环境趋势部分通过 EDT→MDT→RT 三表关联，按区域和日期分组计算各环境指标的日均值，DATE_FORMAT 格式化日期为"月-日"显示。', indent=False)
add_p('【前端展示】区域统计以表格形式展示各区域的事件数、完成数、完成率、平均时长。环境趋势以 ECharts 多折线图展示，X 轴为日期，Y 轴为环境指标值，不同区域用不同颜色曲线表示，支持 PM2.5、噪音、PM10、温度指标切换。', indent=False)
add_p('【验证】查询 2026-11-01 至 2026-11-12 期间数据，7 个区域均有统计记录。事件数最多的区域约 10~15 条，完成率在 60%~100% 之间，平均处理时长 2~8 小时不等。环境趋势图显示各区域 PM2.5 在 30~60 μg/m³ 之间波动，噪音在 50~65 dB 之间，温度在 15~25℃ 之间，符合城市环境数据的合理范围。', indent=False)

doc.add_page_break()

# ===== 第七章 =====
doc.add_heading('第七章  总结与展望', level=1)

doc.add_heading('7.1  工作总结', level=2)
add_p('本项目完成了一个城市管理数字化平台的数据库设计与系统实现，主要工作包括以下六个方面：')
add_p('（1）需求分析：深入分析了城市管理业务中区域管理、设施维护、事件处理、维修调度、环境监测等环节的数据需求与功能需求，识别出 12 个核心实体，梳理了各实体间的 14 组关联关系，为数据库设计奠定了基础。', indent=False)
add_p('（2）概念设计：绘制了系统 E-R 模型，明确了实体间的联系类型（均为一对多关系）及基数，根据业务语义确定了 CASCADE、SET NULL、RESTRICT 三种外键删除策略，保证了数据参照完整性。', indent=False)
add_p('（3）逻辑设计：将 E-R 模型转换为 12 个关系模式，定义了各表的主键、外键及字段约束，进行了范式分析，确认所有关系模式均满足 BCNF 范式要求。', indent=False)
add_p('（4）物理实现：在 MySQL 8.4 上创建数据库与 12 张表，设置了外键约束和唯一索引，通过 init_db.py 脚本预置了约 1200 条示例数据，覆盖全部业务场景，为功能测试和查询验证提供了数据基础。', indent=False)
add_p('（5）系统开发：使用 Flask 构建 24 个 RESTful API 接口，使用 Vue 3 + ECharts 构建前端单页应用，实现了平台概览、设施管理、事件处理、资源调度、环境监测、市民/部门/人员管理及四项期末查询等全部功能模块。', indent=False)
add_p('（6）查询验证：设计并实现了四项期末规定查询的 SQL 语句，涵盖多表连接（INNER JOIN、LEFT JOIN）、条件聚合（IF + SUM/AVG）、时间差计算（TIMESTAMPDIFF）、日期格式化（DATE_FORMAT）等 SQL 技术要点，并通过实际执行验证了查询结果的正确性。', indent=False)

doc.add_heading('7.2  遇到的问题与解决方案', level=2)
add_p('在项目开发过程中，遇到了以下主要问题并逐一解决：')
add_p('（1）外键删除冲突：初始设计中所有外键均设为 RESTRICT，导致删除有关联数据的记录时报错。解决方案：根据业务语义区分——子数据完全依附于父数据的用 CASCADE（如删除市民级联删除其事件），子数据需独立保留的用 SET NULL（如删除设施后事件保留但引用置空），需要人工确认的用 RESTRICT。', indent=False)
add_p('（2）前端写操作状态判断：前端提交表单后未检查后端返回的 code 字段，操作失败时仍显示"成功"，导致用户误以为数据已写入。解决方案：前端所有写操作均检查返回的 code 字段，非 0 时显示红色错误提示，避免误导用户。', indent=False)
add_p('（3）浏览器缓存问题：修改前端代码后浏览器可能缓存旧版本，导致用户操作使用的是旧代码。解决方案：前端 Fetch 请求添加 cache: "no-store" 参数禁用缓存，并提示用户使用 Ctrl+F5 强制刷新。', indent=False)
add_p('（4）后端请求追踪：排查前后端数据同步问题时缺乏请求日志，难以定位问题。解决方案：在 Flask 中添加 before_request 和 after_request 钩子，记录每个 API 请求的方法、路径、请求体和响应状态码，便于调试和问题定位。', indent=False)

doc.add_heading('7.3  项目展望', level=2)
add_p('本项目作为课程设计，已实现了城市管理数字化的基本功能，但在以下方面仍有改进空间：')
add_p('（1）安全性增强：当前系统未实现用户认证与权限管理，实际部署需增加登录认证、角色权限控制、SQL 注入防护（已使用参数化查询）等安全机制。', indent=False)
add_p('（2）性能优化：对于大数据量场景，可添加更多索引（如 ERT.report_time、ERT.event_type）、使用分页查询、引入缓存机制（如 Redis）提升查询性能。', indent=False)
add_p('（3）功能扩展：可增加文件上传（事件现场照片）、消息通知（事件分派短信通知）、GIS 地图集成（设施位置可视化）、数据导出（Excel/PDF 报表）等功能。', indent=False)
add_p('（4）架构升级：当前前端使用 CDN 方式引入 Vue，适合原型开发。生产环境可迁移至 Vue CLI/Vite 构建工具，采用组件化开发和 TypeScript 类型检查，提升代码可维护性。', indent=False)

doc.add_heading('7.4  学习体会', level=2)
add_p('通过本项目，深入实践了数据库设计的全流程——从需求分析到 E-R 建模、关系模式转换、范式分析、物理实现与查询优化，对关系数据库的核心概念（主键、外键、参照完整性、范式、事务）有了更深刻的理解。同时，通过 Flask Web 后端与 Vue 前端的全栈开发，掌握了 RESTful API 设计、前后端数据交互、JSON 数据格式、CORS 跨域处理等 Web 开发技能。特别是在四项期末查询的设计中，综合运用了多表连接、条件聚合、时间函数等 SQL 高级技术，提升了 SQL 编写能力。项目开发过程中遇到的外键约束、前端缓存、数据同步等问题，也锻炼了问题定位与解决的能力。')

# ===== 保存 =====
out = r'E:\demo3\B7城市管理平台_期末报告_含图.docx'
doc.save(out)
print(f'报告已生成: {out}')
print(f'文件大小: {os.path.getsize(out)} 字节')
print(f'图片数量: 5 张')