from io import BytesIO

import openpyxl
from celery import shared_task
from converter.models import Converter
from dropbox import Dropbox
from dropbox.exceptions import ApiError
from dropbox.files import UploadError

from .models import UserTask


@shared_task
def export_task(task_id):
    task = UserTask.objects.filter(id=task_id).first()
    if not task:
        task.update_task_status(
            status='Failure',
            result="Can't find the task",
        )
        return None

    task.update_task_status('Started')

    converters = Converter.objects.filter(**task.start_parameters)
    if not converters:
        task.update_task_status(
            status='Failure',
            result='There are no rates with current parameters',
        )
        return None

    create_excel(task, converters)


def create_excel(task, converters):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = f'Currencies of {task.name}'

    header = converters.first().get_field_names()
    for col_num, column_title in enumerate(header, 1):
        cell = worksheet.cell(row=1, column=col_num)
        cell.value = str(column_title)

    for row_num, row in enumerate(converters.values_list(), 1):
        for col_num, cell_value in enumerate(row, 1):
            cell = worksheet.cell(row=row_num + 1, column=col_num)
            cell.value = str(cell_value)

    file_path = f'/excel/{task.name}.xlsx'

    output = BytesIO()
    workbook.save(output)

    url = upload_to_dropbox(
        file_path=file_path,
        file=output,
    )

    task.update_task_status(
        status='Success',
        result=url,
    )


def upload_to_dropbox(file_path, file):
    # It's working only with temporary access token
    dbx = Dropbox(
        'sl.Bq2LpA7djRMSvdwAiVsylCE9_fWWLo9E_GdUMJBxw4qlarmVi_cW5J1VI2T9PLjU_i'
        '3KLKk7oKhvzm55szz67kSICy3Blt8vSYoBYxFW_30OwNGsiE_lS1N_S9-AxQL4YzjgEE2'
        'DUtjKdUKDa93W',
    )

    try:
        dbx.files_upload(
            file.getvalue(),
            file_path,
        )
        return dbx.files_get_temporary_link(file_path).link

    except ApiError as exc:
        if isinstance(exc.error, UploadError):
            dbx.files_delete(file_path)
            dbx.files_upload(
                file.getvalue(),
                file_path,
            )
            return dbx.files_get_temporary_link(file_path).link

        else:
            return str(exc)
