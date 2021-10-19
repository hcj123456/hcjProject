import json
import locale
import os
from datetime import datetime

import yaml
from rest_framework.response import Response

from debugtalks.models import Debugtalks
from configures.models import Configures
from reports.models import Reports
from testcases.models import Testcases
from httprunner.task import HttpRunner


def datetime_fmt():

    locale.setlocale(locale.LC_CTYPE, 'chinese')

    return '%Y年%m月%d日 %H:%M:%S'


def generate_testcase_file(instance, env, testcase_dir_path):
    testcase_list = []

    config = {
        'config': {
            'name': instance.name,
            'request': {
                'base_url': env.base_url if env else ''
            }
        }
    }
    testcase_list.append(config)

    interface_name = instance.interface.name
    project_name = instance.interface.project.name

    include = json.loads(instance.include, encoding='utf-8')
    request = json.loads(instance.request, encoding='utf-8')
    testcase_dir_path = os.path.join(testcase_dir_path, project_name)
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)

        debugtalk_obj = Debugtalks.objects.filter(project__name=project_name).first()
        debugtalk = debugtalk_obj.debugtalk if debugtalk_obj.debugtalk else ''
        with open(os.path.join(testcase_dir_path, 'debugtalk.py'), 'w', encoding='utf-8') as file:
            file.write(debugtalk)

    testcase_dir_path = os.path.join(testcase_dir_path, interface_name)
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)

    config_id = include.get('config')
    if config_id is not None:
        config_obj = Configures.objects.filter(id=config_id).first()
        if config_obj:
            config_request = json.loads(config_obj.request, encoding='utf-8')
            config_request['config']['request']['base_url'] = env.base_url if env.base_url else ''
            testcase_list[0] = config_request

    prefix_testcase_list =include.get('testcases')
    if prefix_testcase_list:
        for testcase_id in prefix_testcase_list:
            testcase_obj = Testcases.objects.filter(id=testcase_id).first()
            try:
                testcase_request = json.loads(testcase_obj.request, encoding='utf-8')
            except Exception as e:
                continue
            testcase_list.append(testcase_request)

    testcase_list.append(request)

    testcase_dir_path = os.path.join(testcase_dir_path, instance.name + '.yaml')
    with open(testcase_dir_path, 'w', encoding='utf-8') as file:
        yaml.dump(testcase_list, file, allow_unicode=True)


def generate_report(runner, instance):
    # 创建报告名称：用例名
    report_name = instance.name

    # 对时间戳进行转化
    time_stamp = int(runner.summary["time"]["start_at"])
    start_datetime = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    runner.summary['time']['start_datetime'] = start_datetime
    # duration保留3位小数
    runner.summary['time']['duration'] = round(runner.summary['time']['duration'], 3)
    report_name = report_name if report_name else start_datetime
    runner.summary['html_report_name'] = report_name

    # 将summary中的所有字节类型转化为字符串类型
    for item in runner.summary['details']:
        try:
            for record in item['records']:
                record['meta_data']['response']['content'] = record['meta_data']['response']['content']. \
                    decode('utf-8')
                record['meta_data']['response']['cookies'] = dict(record['meta_data']['response']['cookies'])

                request_body = record['meta_data']['request']['body']
                if isinstance(request_body, bytes):
                    record['meta_data']['request']['body'] = request_body.decode('utf-8')
        except Exception as e:
            continue

    summary = json.dumps(runner.summary, ensure_ascii=False)
    # result = summary.get('success')
    # count
    # success
    # html
    # 生成报告
    # report_path = runner.gen_html_report(html_report_name=)
    report_name = report_name + '_' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    report_path = runner.gen_html_report(html_report_name=report_name)

    with open(report_path, encoding='utf-8') as stream:
        reports = stream.read()

    test_report = {
        'name': report_name,
        'result': runner.summary.get('success'),
        'success': runner.summary.get('stat').get('successes'),
        'count': runner.summary.get('stat').get('testsRun'),
        'html': reports,
        'summary': summary
    }
    report_obj = Reports.objects.create(**test_report)
    return report_obj.id


def run_testcase(instance, testcase_dir_path):
    # 1、创建HttpRunner对象
    runner = HttpRunner()
    try:
        # 2、运行用例
        runner.run(testcase_dir_path)
    except Exception as e:
        res = {'msg': '用例执行失败', 'code': '0'}
        return Response(res, status=400)

    # 3、创建报告
    report_id = generate_report(runner, instance)
    return Response({'id': report_id}, status=201)