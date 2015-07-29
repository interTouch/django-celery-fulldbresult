import json

from djcelery.backends.database import DatabaseBackend

from django_celery_fulldbresult.models import TaskResultMeta


class DatabaseResultBackend(DatabaseBackend):
    """Database backend that stores enough task metadata to retry the task.
    """

    TaskModel = TaskResultMeta

    def _store_result(self, task_id, result, status, traceback, request=None):
        if request:
            # TODO Use celery json serializer
            args = json.dumps(request.args)
            kwargs = json.dumps(request.kwargs)
            task = request.task
            expires = request.expires
            delivery_info = request.delivery_info or {}
            routing_key = delivery_info.get("routing_key")
            exchange = delivery_info.get("exchange")
            hostname = request.hostname
            date_submitted = getattr(request, "date_submitted", None)
            eta = request.eta
        else:
            args = []
            kwargs = {}
            task = ""
            expires = None
            routing_key = None
            exchange = None
            hostname = None
            date_submitted = None
            eta = None
        self.TaskModel._default_manager.store_result(
            task_id, result, status,
            traceback=traceback, children=self.current_task_children(request),
            task=task, args=args, kwargs=kwargs, expires=expires,
            routing_key=routing_key, exchange=exchange, hostname=hostname,
            date_submitted=date_submitted, eta=eta)
        return result
