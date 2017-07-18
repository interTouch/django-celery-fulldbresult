# from django.test import TestCase
import unittest
from models import TaskResultMeta


class TestModels(unittest.TestCase):
     def test_task_result_meta_indexes(self):
         self.assertEqual(TaskResultMeta._meta.index_together, ((u'status', u'date_done'),))

