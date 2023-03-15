
MAX_VAL = 1
MIN_VAL = 0


class SomeModel:
    def predict(self, message: str) -> float:
        pass


def predict_message_mood(
    message: str,
    model: SomeModel,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    if message == '':
        return 'Empty message'
    if bad_thresholds >= MAX_VAL or bad_thresholds <= MIN_VAL:
        return 'Incorrect bad_thresholds'
    if good_thresholds >= MAX_VAL or good_thresholds <= MIN_VAL:
        return 'Incorrect good_thresholds'
    if bad_thresholds > good_thresholds:
        return 'good_thresholds < bad_thresholds'
    pred = model.predict(message)

    if MIN_VAL <= pred < bad_thresholds:
        return 'неуд'
    if bad_thresholds <= pred <= good_thresholds:
        return 'норм'
    if good_thresholds < pred <= MAX_VAL:
        return 'отл'
    return ''
