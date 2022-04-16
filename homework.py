from dataclasses import dataclass, asdict
from typing import List, Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message = ('Тип тренировки: {}; '
               'Длительность: {:.3f} ч.; '
               'Дистанция: {:.3f} км; '
               'Ср. скорость: {:.3f} км/ч; '
               'Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:
        return self.message.format(*asdict(self).values())


class Training:
    """Базовый класс тренировки."""
    MIN_IN_H: int = 60
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 ) -> None:
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
        raise NotImplementedError(f'Для класса {self.__class__.__name__}'
                                  f'не указан метод расчета ккал')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_min = self.duration * self.MIN_IN_H
        spent_calories: float = (
            (self.COEFF_CALORIE_1 * self.get_mean_speed()
             - self.COEFF_CALORIE_2) * self.weight
            / self.M_IN_KM * duration_min
        )
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: int = 2
    COEFF_CALORIE_3: float = 0.029

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_min = self.duration * self.MIN_IN_H
        spent_calories: float = (
            (self.COEFF_CALORIE_1 * self.weight + (
                self.get_mean_speed()**self.COEFF_CALORIE_2 // self.height
            ) * self.COEFF_CALORIE_3 * self.weight) * duration_min
        )
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_CALORIE_1: float = 1.1
    COEFF_CALORIE_2: int = 2

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories: float = (
            (self.get_mean_speed() + self.COEFF_CALORIE_1)
            * self.COEFF_CALORIE_2 * self.weight
        )
        return spent_calories


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_workout_type: Dict[str, Type[Training]]
    dict_workout_type = {'SWM': Swimming,
                         'RUN': Running,
                         'WLK': SportsWalking}

    if workout_type in dict_workout_type:
        return dict_workout_type[workout_type](*data)

    raise ValueError('В базе отсутствует новый тип тренировки,'
                     'полученной с датчиков.')


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()

    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        data_float = list(map(float, data))
        training = read_package(workout_type, data_float)
        main(training)
