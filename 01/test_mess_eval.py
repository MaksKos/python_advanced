from unittest import TestCase, mock

import mess_eval as me
from mess_eval import predict_message_mood as pmm


class TestMessEval(TestCase):
    def setUp(self):
        self.model = me.SomeModel()
        self.mess = 'text'

    def test_message(self):
        self.assertEqual(pmm('', self.model), 'Empty message')

    def test_bad_thresholds(self):
        ret = 'Incorrect bad_thresholds'
        self.assertEqual(pmm(self.mess, self.model, bad_thresholds=-0.5), ret)
        self.assertEqual(pmm(self.mess, self.model, bad_thresholds=1.1), ret)
        self.assertEqual(pmm(self.mess, self.model, bad_thresholds=me.MAX_VAL), ret)
        self.assertEqual(pmm(self.mess, self.model, bad_thresholds=me.MIN_VAL), ret)

    def test_good_thresholds(self):
        ret = 'Incorrect good_thresholds'
        self.assertEqual(pmm(self.mess, self.model, good_thresholds=-0.5), ret)
        self.assertEqual(pmm(self.mess, self.model, good_thresholds=1.1), ret)
        self.assertEqual(pmm(self.mess, self.model, good_thresholds=me.MAX_VAL), ret)
        self.assertEqual(pmm(self.mess, self.model, good_thresholds=me.MIN_VAL), ret)

    def test_thresholds(self):
        ret = 'good_thresholds < bad_thresholds'
        self.assertEqual(pmm(self.mess, self.model, bad_thresholds=0.5, good_thresholds=0.4), ret)

    def test_model(self):
        with mock.patch('mess_eval.SomeModel', spec=True) as mock_model:
            instance = mock_model.return_value
            instance.predict.side_effect = 0, 0.2, 0.3, 0.5, 0.8, 0.99, 1, 1.5, -1
            bad = 0.3
            good = 0.8

            self.assertEqual(pmm(self.mess, instance, bad, good), 'неуд')
            self.assertEqual(pmm(self.mess, instance, bad, good), 'неуд')

            self.assertEqual(pmm(self.mess, instance, bad, good), 'норм')
            self.assertEqual(pmm(self.mess, instance, bad, good), 'норм')
            self.assertEqual(pmm(self.mess, instance, bad, good), 'норм')

            self.assertEqual(pmm(self.mess, instance, bad, good), 'отл')
            self.assertEqual(pmm(self.mess, instance, bad, good), 'отл')

            self.assertEqual(pmm(self.mess, instance, bad, good), '')
            self.assertEqual(pmm(self.mess, instance, bad, good), '')

            self.assertEqual(instance.predict.call_count, 9)
            args = [mock.call(self.mess)]*9
            self.assertEqual(instance.predict.call_args_list, args)
