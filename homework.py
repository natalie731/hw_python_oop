class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Сформировать сообщение."""
        format_3 = '{:.3f}'
        training_type: str = self.training_type
        duration: float = format_3.format(self.duration)
        distance: float = format_3.format(self.distance)
        speed: float = format_3.format(self.speed)
        calories: float = format_3.format(self.calories)

        return(f'Тип тренировки: {training_type}; '
               f'Длительность: {duration} ч.; '
               f'Дистанция: {distance} км; '
               f'Ср. скорость: {speed} км/ч; '
               f'Потрачено ккал: {calories}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65

    @classmethod
    def get_classname(cls) -> str:
        """Получить тип тренировки."""
        training_type: str = cls.__name__
        return training_type

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
        distance: float = self.action * self.LEN_STEP / Training.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.get_classname(),
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        duration_min = self.duration * 60
        spent_calories: float = (
            (coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2)
            * self.weight / Training.M_IN_KM * duration_min
        )
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1: float = 0.035
        coeff_calorie_2: int = 2
        coeff_calorie_3: float = 0.029
        duration_min = self.duration * 60
        spent_calories: float = (
            (coeff_calorie_1 * self.weight + (
                self.get_mean_speed()**coeff_calorie_2 // self.height
            ) * coeff_calorie_3 * self.weight) * duration_min
        )
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38  # Переопределать константу суперкласса

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = (
            self.length_pool * self.count_pool
            / Swimming.M_IN_KM / self.duration
        )
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1: float = 1.1
        coeff_calorie_2: int = 2
        spent_calories: float = (
            (self.get_mean_speed() + coeff_calorie_1)
            * coeff_calorie_2 * self.weight
        )
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_workout_type = {'SWM': Swimming,
                         'RUN': Running,
                         'WLK': SportsWalking}
    new_train = dict_workout_type[workout_type](*data)
    return new_train


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
        training = read_package(workout_type, data)
        main(training)
