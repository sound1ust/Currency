import os
from datetime import datetime

import openpyxl
from celery import shared_task
from converter.models import Converter

from .models import UserTask
from .models import UserTaskResult
from currency import settings


@shared_task
def export_task(task_id):
    time_before = datetime.now()
    task = UserTask.objects.filter(id=task_id).first()
    if not task:
        # task.update_task_status(
        #     status='Failure',
        #     result="Can't find the task",
        # )
        return None

    # task.update_task_status('Started')
    start_parameters = {
        'created_at__gte': task.date_from,
        'created_at__lte': task.date_to,
        'input_ticker__in': task.input_tickers,
        'output_ticker__in': task.output_tickers,
        'value__gte': task.value_from,
        'value__lte': task.value_to,
        'source__in': task.sources,
        'updated_by': task.updated_by,
    }
    start_parameters = {
        key: value for key, value in start_parameters.items() if value
    }

    task_result = UserTaskResult.objects.create(
        name=f"{'_'.join(task.name.split())}",
        user=task.user,
        start_date=time_before,
        start_parameters=start_parameters,
    )

    converters = Converter.objects.filter(**start_parameters)
    if not converters:
        task_result.status = 'FAILURE'
        task_result.save()
        return None

    task_result.save()
    create_excel(task_result, converters)


def create_excel(task_result, converters):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = f'Currencies of {task_result.name}'

    header = converters.first().get_field_names()
    for col_num, column_title in enumerate(header, 1):
        cell = worksheet.cell(row=1, column=col_num)
        cell.value = str(column_title)

    for row_num, row in enumerate(converters.values_list(), 1):
        for col_num, cell_value in enumerate(row, 1):
            cell = worksheet.cell(row=row_num + 1, column=col_num)
            cell.value = str(cell_value)

    file_name = f'{task_result.name}.xlsx'
    try:
        os.mkdir(f'{settings.BASE_DIR}/excel')
    except FileExistsError:
        pass

    file_path = os.path.join(settings.BASE_DIR, f'excel/{file_name}')
    workbook.save(file_path)

    task_result.result_link = file_path
    task_result.status = 'SUCCEED'
    time_after = datetime.now()
    task_result.duration = time_after - task_result.start_date
    task_result.save()
