from django.db import transaction
from django.conf import settings
from celery import shared_task

import os
import shutil

import oj
from main.judge import DefaultJudge
from main.models import Submit


@shared_task
def judge_submit(submit_pk):
    submit = Submit.objects.get(pk=submit_pk)
    problem = submit.problem
    JudgeClass = DefaultJudge

    # 初始化工作目录
    work_dir = os.path.join(settings.JUDGE_BASE_DIR, str(submit.id))
    if os.path.exists(work_dir):
        shutil.rmtree(work_dir)
    os.mkdir(work_dir)
    source_code = os.path.join(work_dir, 'source%s' % submit.get_codefile_suffix())
    with open(source_code, 'w') as f:
        f.write(submit.code)

    judge = JudgeClass(
        problem_id=str(problem.id),
        work_dir=work_dir,
        source_code=source_code,)

    # 开始判题
    with transaction.atomic():
        submit.judge_status = Submit.JUDGE_JUDGING
        submit.save()
    (compile_status, results) = judge.run()

    # 删除工作目录
    shutil.rmtree(work_dir)

    # 统计结果
    with transaction.atomic():
        if compile_status == oj.consts.COMPILE_OK:
            submit.compile_status = Submit.COMPILE_OK
            submit.run_results = [list(tp) for tp in results]
            total = len(submit.run_results)
            accepted = len([status for (status, _, _) in submit.run_results
                            if status == oj.consts.ACCEPTED])
            if total == 0:
                submit.score = 0.0
            else:
                submit.score = 100.0 * (accepted / total)
        elif compile_status == oj.consts.COMPILE_ERROR:
            submit.compile_status = Submit.COMPILE_ERROR
            submit.error_message = results
            submit.score = 0.0
        submit.judge_status = Submit.JUDGE_COMPLETED
        submit.save()
