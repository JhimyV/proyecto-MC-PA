-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 10-06-2025 a las 05:42:18
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `hotel_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id_cliente` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `telefono` varchar(10) NOT NULL,
  `dni` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id_cliente`, `nombre`, `email`, `telefono`, `dni`) VALUES
(4, 'bryan', 'nose@nose.com', '1324567890', '1324567890'),
(5, 'manu', 'manucho@outlook.com', '0912345678', '0912345678'),
(6, 'luiss', 'va@hotmail.com', '0987654123', '0987654123'),
(9, 'pablo', 'pato@gmail.com', '1234567890', '1234567890'),
(10, 'luis', 'lucho@gmail.com', '0987654123', '0987654321'),
(11, 'lo', 'lo@gmail.com', '0987654321', '0912345678'),
(12, 'jose', 'jose1@gmail.com', '1230987654', '1230987654'),
(14, 'pepe', 'pep2@outlook.com', '1234509876', '1234509876'),
(15, 'juan', '11juan@gmail.com', '0912345876', '0912345876'),
(16, 'ney ', 'ney@gmail.com', '1234567899', '1234567899'),
(17, 'jose', 'pato@gmail.com', '1230987654', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `habitaciones`
--

CREATE TABLE `habitaciones` (
  `id_habitacion` int(11) NOT NULL,
  `numero` varchar(10) NOT NULL,
  `tipo` enum('Individual','Doble','Suite') NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `estado` enum('Disponible','Ocupada','Mantenimiento') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `habitaciones`
--

INSERT INTO `habitaciones` (`id_habitacion`, `numero`, `tipo`, `precio`, `estado`) VALUES
(1, '11', 'Doble', 100.00, 'Ocupada'),
(2, '10', '', 50.40, 'Ocupada'),
(3, '5', '', 40.49, 'Ocupada'),
(4, '09', 'Doble', 80.50, 'Ocupada'),
(6, '2', 'Doble', 50.40, 'Ocupada'),
(7, '100', 'Doble', 50.00, 'Ocupada'),
(8, '100', 'Doble', 100.00, 'Ocupada'),
(9, '200', 'Doble', 30.00, 'Disponible');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pagos`
--

CREATE TABLE `pagos` (
  `id_pago` int(11) NOT NULL,
  `reserva_id` int(11) NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `fecha_pago` date NOT NULL,
  `metodo_pago` enum('Efectivo','Tarjeta','Transferencia') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `pagos`
--

INSERT INTO `pagos` (`id_pago`, `reserva_id`, `monto`, `fecha_pago`, `metodo_pago`) VALUES
(1, 1, 95.50, '2025-05-31', 'Transferencia'),
(2, 2, 40.49, '2025-06-01', 'Transferencia'),
(3, 4, 80.50, '2025-06-02', 'Transferencia'),
(4, 5, 50.40, '2025-06-02', 'Transferencia'),
(5, 6, 50.00, '2025-06-03', 'Transferencia');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reservas`
--

CREATE TABLE `reservas` (
  `id_reserva` int(11) NOT NULL,
  `cliente_id` int(11) NOT NULL,
  `habitacion_id` int(11) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `estado` enum('Activa','Cancelada','Finalizada') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `reservas`
--

INSERT INTO `reservas` (`id_reserva`, `cliente_id`, `habitacion_id`, `fecha_inicio`, `fecha_fin`, `estado`) VALUES
(1, 4, 2, '2025-06-02', '2025-06-05', 'Activa'),
(2, 5, 3, '2025-06-05', '2025-06-10', 'Activa'),
(3, 4, 1, '2025-06-03', '2025-06-04', 'Activa'),
(4, 11, 4, '2025-06-20', '2025-06-23', 'Activa'),
(5, 14, 6, '2025-06-03', '2025-06-04', 'Activa'),
(6, 15, 7, '2025-06-04', '2025-06-10', 'Activa'),
(7, 16, 2, '2025-06-17', '2025-06-19', 'Activa');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre_usuario` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `rol` enum('admin','usuario') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre_usuario`, `password`, `rol`) VALUES
(1, 'admin', 'admin02', 'admin'),
(3, 'ney', '1234', 'usuario'),
(8, 'mama', '12345678', 'admin'),
(9, 'teme', 'pato', 'usuario');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id_cliente`);

--
-- Indices de la tabla `habitaciones`
--
ALTER TABLE `habitaciones`
  ADD PRIMARY KEY (`id_habitacion`);

--
-- Indices de la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD PRIMARY KEY (`id_pago`),
  ADD KEY `fk_pagos_reserva` (`reserva_id`);

--
-- Indices de la tabla `reservas`
--
ALTER TABLE `reservas`
  ADD PRIMARY KEY (`id_reserva`),
  ADD KEY `fk_reservas_cliente` (`cliente_id`),
  ADD KEY `fk_reservas_habitacion` (`habitacion_id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `habitaciones`
--
ALTER TABLE `habitaciones`
  MODIFY `id_habitacion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `pagos`
--
ALTER TABLE `pagos`
  MODIFY `id_pago` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `reservas`
--
ALTER TABLE `reservas`
  MODIFY `id_reserva` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD CONSTRAINT `fk_pagos_reserva` FOREIGN KEY (`reserva_id`) REFERENCES `reservas` (`id_reserva`);

--
-- Filtros para la tabla `reservas`
--
ALTER TABLE `reservas`
  ADD CONSTRAINT `fk_reservas_cliente` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id_cliente`),
  ADD CONSTRAINT `fk_reservas_habitacion` FOREIGN KEY (`habitacion_id`) REFERENCES `habitaciones` (`id_habitacion`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
