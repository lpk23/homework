class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        message = (f"Тип тренировки: {self.training_type}; "
                   f"Длительность: {self.duration:.3f} ч.; "
                   f"Дистанция: {self.distance:.3f} км; "
                   f"Ср. скорость: {self.speed:.3f} км/ч; "
                   f"Потрачено ккал: {self.calories:.3f}.")
        return message


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    LEN_STROKE = 1.38
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        if self.action >= 0:
            if isinstance(self, Swimming):
                distance = self.action * self.LEN_STROKE / self.M_IN_KM
            else:
                distance = self.action * self.LEN_STEP / self.M_IN_KM
            return distance
        return 0

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        if self.duration > 0:
            return self.get_distance() / self.duration
        return 0

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для бега."""
        if self.duration > 0:
            return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                     * self.get_mean_speed()
                     + self.CALORIES_MEAN_SPEED_SHIFT)
                    * self.weight / self.M_IN_KM * (self.duration * 60))
        return 0


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_COEFFICIENT = 0.035
    CALORIES_SPEED_COEFFICIENT = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: int,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для спортивной ходьбы."""
        if self.duration > 0:
            speed_in_meters_per_sec = self.get_mean_speed() / 3.6
            return ((self.CALORIES_WEIGHT_COEFFICIENT
                     * self.weight
                     + (speed_in_meters_per_sec ** 2 / self.height)
                     * self.CALORIES_SPEED_COEFFICIENT * self.weight)
                    * (self.duration * 60))
        return 0


class Swimming(Training):
    """Тренировка: плавание."""
    CALORIES_MEAN_SPEED_SHIFT = 1.1

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float):
        super().__init__(action, duration, weight)
        self.length_pool, self.count_pool = length_pool, count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость плаванья."""
        if self.duration > 0:
            return (self.length_pool
                    * self.count_pool
                    / self.M_IN_KM
                    / self.duration)
        return 0

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для плаванья."""
        if self.duration > 0:
            return ((self.get_mean_speed()
                     + self.CALORIES_MEAN_SPEED_SHIFT) * 2
                    * self.weight * self.duration)
        return 0


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_class = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return type_class[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
