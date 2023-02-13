from dataclasses import asdict
from typing import Type, Dict


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
        self.MESSAGE: str = (f'Тип тренировки: {training_type}; '
                             f'Длительность: {duration:.3f} ч.;'
                             f' Дистанция: {distance:.3f} км; '
                             f'Ср. скорость: {speed:.3f} км/ч; '
                             f'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(*asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    M_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * self.duration * self.M_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WEIGHT_MULTIPLIER: float = 0.035
    PRIVATE_SQUARE_FACTOR: float = 0.029
    TRANSFER_MULTIPLIER_SPEED: float = 0.278
    TRANSFER_MULTIPLIER_HEIGHT: int = 100
    EX_CAL: int = 2

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (((self.WEIGHT_MULTIPLIER * self.weight
                  + ((self.get_mean_speed() * self.TRANSFER_MULTIPLIER_SPEED)
                     ** self.EX_CAL
                     / (self.height / self.TRANSFER_MULTIPLIER_HEIGHT))
                  * self.PRIVATE_SQUARE_FACTOR * self.weight)
                 * self.duration * self.M_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""
    AVERAGE_SPEED_OFFSET: float = 1.1
    SPEED_MULTIPLIER: float = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        return self.length_pool * self.count_pool \
            / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (self.get_mean_speed() + self.AVERAGE_SPEED_OFFSET) \
            * self.SPEED_MULTIPLIER * self.weight * self.duration


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    train_dict: Dict[str, Type[Training]] = {'SWM': Swimming,
                                             'RUN': Running,
                                             'WLK': SportsWalking}
    if workout_type in train_dict:
        return train_dict[workout_type](*data)
    raise KeyError


def main(training: Training) -> None:
    """Главная функция."""
    information = training.show_training_info()
    print(information.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
