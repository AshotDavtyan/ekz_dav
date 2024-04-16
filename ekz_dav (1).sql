-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Апр 16 2024 г., 11:48
-- Версия сервера: 8.0.29
-- Версия PHP: 7.1.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `ekz_dav`
--

-- --------------------------------------------------------

--
-- Структура таблицы `jobs`
--

CREATE TABLE `jobs` (
  `id` int NOT NULL,
  `worker_id` int DEFAULT NULL,
  `job_name` varchar(255) NOT NULL,
  `payment` decimal(10,2) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `jobs`
--

INSERT INTO `jobs` (`id`, `worker_id`, `job_name`, `payment`, `start_date`, `end_date`) VALUES
(1, 1, '231231', '5555.00', '2024-01-01', '2024-01-10'),
(7, 1, 'adasd', '1232.00', '2024-01-21', '2025-01-21'),
(9, 1, 'вфвы', '212.00', '2024-01-20', '2025-02-20'),
(10, 1, 'da', '2222.00', '2133-02-20', '2303-01-20'),
(11, 1, '231231', '3333.00', '2020-01-20', '2021-02-20');

-- --------------------------------------------------------

--
-- Структура таблицы `tasks`
--

CREATE TABLE `tasks` (
  `id` int NOT NULL,
  `task_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `tasks`
--

INSERT INTO `tasks` (`id`, `task_name`) VALUES
(1, 'Полив');

-- --------------------------------------------------------

--
-- Структура таблицы `workers`
--

CREATE TABLE `workers` (
  `id` int NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `birth_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `workers`
--

INSERT INTO `workers` (`id`, `full_name`, `address`, `birth_date`) VALUES
(1, 'Иванов Иван Петрович', 'г. Москва, ул. Пушкина, 15', '1990-01-01');

-- --------------------------------------------------------

--
-- Структура таблицы `workertasks`
--

CREATE TABLE `workertasks` (
  `worker_id` int NOT NULL,
  `task_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `workertasks`
--

INSERT INTO `workertasks` (`worker_id`, `task_id`) VALUES
(1, 1);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `jobs`
--
ALTER TABLE `jobs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `worker_id` (`worker_id`);

--
-- Индексы таблицы `tasks`
--
ALTER TABLE `tasks`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `task_name` (`task_name`);

--
-- Индексы таблицы `workers`
--
ALTER TABLE `workers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `full_name` (`full_name`);

--
-- Индексы таблицы `workertasks`
--
ALTER TABLE `workertasks`
  ADD PRIMARY KEY (`worker_id`,`task_id`),
  ADD KEY `task_id` (`task_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `jobs`
--
ALTER TABLE `jobs`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT для таблицы `tasks`
--
ALTER TABLE `tasks`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `workers`
--
ALTER TABLE `workers`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `jobs`
--
ALTER TABLE `jobs`
  ADD CONSTRAINT `jobs_ibfk_1` FOREIGN KEY (`worker_id`) REFERENCES `workers` (`id`);

--
-- Ограничения внешнего ключа таблицы `workertasks`
--
ALTER TABLE `workertasks`
  ADD CONSTRAINT `workertasks_ibfk_1` FOREIGN KEY (`worker_id`) REFERENCES `workers` (`id`),
  ADD CONSTRAINT `workertasks_ibfk_2` FOREIGN KEY (`task_id`) REFERENCES `tasks` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
