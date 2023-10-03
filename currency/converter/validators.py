from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta


def validate_source_date(source_date):
    if source_date < datetime.now() - timedelta(days=30):
        raise ValidationError(
            _("%(date) must not to be earlier than month from now'"),
            params={"source_date": source_date},
        )
