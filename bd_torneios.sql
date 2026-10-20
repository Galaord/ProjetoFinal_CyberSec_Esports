-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 19-Out-2026 às 06:02
-- Versão do servidor: 10.4.32-MariaDB-log
-- versão do PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `bd_torneios`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `equipas`
--

CREATE TABLE `equipas` (
  `id` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `tag` varchar(10) NOT NULL,
  `pais` varchar(60) DEFAULT NULL,
  `vitorias` int(11) NOT NULL DEFAULT 0,
  `derrotas` int(11) NOT NULL DEFAULT 0
) ;

--
-- Extraindo dados da tabela `equipas`
--

INSERT INTO `equipas` (`id`, `nome`, `tag`, `pais`, `vitorias`, `derrotas`) VALUES
(1, 'Lusitanos Gaming', 'LUS', 'Portugal', 3, 1),
(2, 'Brazil Storm', 'BST', 'Brasil', 2, 2),
(3, 'European Wolves', 'EW', 'Alemanha', 4, 1),
(4, 'Atlantic Five', 'ATF', 'Portugal', 1, 2);

-- --------------------------------------------------------

--
-- Estrutura da tabela `estatisticas_jogador`
--

CREATE TABLE `estatisticas_jogador` (
  `id` int(11) NOT NULL,
  `partida_mapa_id` int(11) NOT NULL,
  `jogador_id` int(11) NOT NULL,
  `kills` int(11) NOT NULL DEFAULT 0,
  `deaths` int(11) NOT NULL DEFAULT 0,
  `assists` int(11) NOT NULL DEFAULT 0,
  `mvps` int(11) NOT NULL DEFAULT 0,
  `dano_total` int(11) NOT NULL DEFAULT 0
) ;

--
-- Extraindo dados da tabela `estatisticas_jogador`
--

INSERT INTO `estatisticas_jogador` (`id`, `partida_mapa_id`, `jogador_id`, `kills`, `deaths`, `assists`, `mvps`, `dano_total`) VALUES
(1, 1, 1, 24, 12, 5, 3, 2450),
(2, 1, 2, 20, 14, 4, 2, 2100),
(3, 1, 3, 18, 15, 6, 1, 1850),
(4, 1, 6, 16, 17, 3, 1, 1700),
(5, 1, 7, 21, 16, 2, 1, 2200),
(6, 2, 1, 17, 16, 4, 1, 1750),
(7, 2, 2, 19, 15, 3, 2, 2000),
(8, 2, 6, 25, 13, 5, 3, 2600),
(9, 2, 7, 22, 14, 4, 2, 2300),
(10, 3, 1, 26, 10, 6, 4, 2800),
(11, 3, 2, 21, 12, 5, 2, 2250),
(12, 3, 3, 19, 13, 7, 1, 1950),
(13, 3, 6, 14, 18, 4, 0, 1450),
(14, 3, 7, 17, 16, 3, 1, 1800),
(15, 6, 1, 28, 17, 5, 3, 2950),
(16, 6, 2, 23, 18, 4, 2, 2400),
(17, 6, 6, 20, 21, 6, 1, 2150),
(18, 6, 7, 19, 22, 3, 1, 2000);

-- --------------------------------------------------------

--
-- Estrutura da tabela `inscricoes_torneio`
--

CREATE TABLE `inscricoes_torneio` (
  `id` int(11) NOT NULL,
  `torneio_id` int(11) NOT NULL,
  `equipa_id` int(11) NOT NULL,
  `data_inscricao` date NOT NULL,
  `posicao_final` int(11) DEFAULT NULL,
  `pontos` int(11) NOT NULL DEFAULT 0
) ;

--
-- Extraindo dados da tabela `inscricoes_torneio`
--

INSERT INTO `inscricoes_torneio` (`id`, `torneio_id`, `equipa_id`, `data_inscricao`, `posicao_final`, `pontos`) VALUES
(1, 1, 1, '2026-09-20', NULL, 6),
(2, 1, 2, '2026-09-21', NULL, 3),
(3, 1, 3, '2026-09-22', NULL, 9),
(4, 1, 4, '2026-09-23', NULL, 0),
(5, 2, 1, '2026-09-25', NULL, 0),
(6, 2, 2, '2026-09-26', NULL, 0),
(7, 2, 3, '2026-09-27', NULL, 0),
(8, 3, 1, '2026-08-20', 2, 6),
(9, 3, 2, '2026-08-21', 3, 3),
(10, 3, 3, '2026-08-22', 1, 9);

-- --------------------------------------------------------

--
-- Estrutura da tabela `jogadores`
--

CREATE TABLE `jogadores` (
  `id` int(11) NOT NULL,
  `nickname` varchar(50) NOT NULL,
  `nome_real` varchar(100) DEFAULT NULL,
  `pais` varchar(60) DEFAULT NULL,
  `steam_id` varchar(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Extraindo dados da tabela `jogadores`
--

INSERT INTO `jogadores` (`id`, `nickname`, `nome_real`, `pais`, `steam_id`) VALUES
(1, 'ShadowPT', 'João Silva', 'Portugal', '76561198000000001'),
(2, 'Frost', 'Pedro Costa', 'Portugal', '76561198000000002'),
(3, 'Viper', 'Miguel Santos', 'Portugal', '76561198000000003'),
(4, 'Blaze', 'André Martins', 'Portugal', '76561198000000004'),
(5, 'Sn1per', 'Tiago Ferreira', 'Portugal', '76561198000000005'),
(6, 'Ace', 'Lucas Oliveira', 'Brasil', '76561198000000006'),
(7, 'Ghost', 'Rafael Lima', 'Brasil', '76561198000000007'),
(8, 'Raptor', 'Daniel Alves', 'Brasil', '76561198000000008'),
(9, 'Nova', 'Martin Novak', 'República Checa', '76561198000000009'),
(10, 'Hunter', 'Lukas Meyer', 'Alemanha', '76561198000000010'),
(11, 'Echo', 'David Müller', 'Alemanha', '76561198000000011'),
(12, 'Reaper', 'Alex Turner', 'Reino Unido', '76561198000000012');

-- --------------------------------------------------------

--
-- Estrutura da tabela `jogador_equipa`
--

CREATE TABLE `jogador_equipa` (
  `id` int(11) NOT NULL,
  `jogador_id` int(11) NOT NULL,
  `equipa_id` int(11) NOT NULL,
  `funcao` enum('IGL','AWPer','Entry Fragger','Rifler','Support','Coach') NOT NULL DEFAULT 'Rifler',
  `data_entrada` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Extraindo dados da tabela `jogador_equipa`
--

INSERT INTO `jogador_equipa` (`id`, `jogador_id`, `equipa_id`, `funcao`, `data_entrada`) VALUES
(1, 1, 1, 'IGL', '2026-01-10'),
(2, 2, 1, 'AWPer', '2026-01-10'),
(3, 3, 1, 'Entry Fragger', '2026-01-10'),
(4, 4, 1, 'Rifler', '2026-01-10'),
(5, 5, 1, 'Support', '2026-01-10'),
(6, 6, 2, 'IGL', '2026-02-01'),
(7, 7, 2, 'AWPer', '2026-02-01'),
(8, 8, 2, 'Entry Fragger', '2026-02-01'),
(9, 9, 3, 'IGL', '2026-03-01'),
(10, 10, 3, 'Rifler', '2026-03-01'),
(11, 11, 3, 'AWPer', '2026-03-01'),
(12, 12, 4, 'Rifler', '2026-04-01');

-- --------------------------------------------------------

--
-- Estrutura da tabela `mapas`
--

CREATE TABLE `mapas` (
  `id` int(11) NOT NULL,
  `nome` varchar(50) NOT NULL,
  `ativo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Extraindo dados da tabela `mapas`
--

INSERT INTO `mapas` (`id`, `nome`, `ativo`) VALUES
(1, 'Mirage', 1),
(2, 'Inferno', 1),
(3, 'Dust2', 1),
(4, 'Nuke', 1),
(5, 'Ancient', 1),
(6, 'Anubis', 1),
(7, 'Overpass', 0);

-- --------------------------------------------------------

--
-- Estrutura da tabela `partidas_torneio`
--

CREATE TABLE `partidas_torneio` (
  `id` int(11) NOT NULL,
  `torneio_id` int(11) NOT NULL,
  `equipa1_id` int(11) NOT NULL,
  `equipa2_id` int(11) NOT NULL,
  `vencedor_id` int(11) DEFAULT NULL,
  `data_jogo` datetime NOT NULL,
  `fase` varchar(50) NOT NULL,
  `formato` enum('BO1','BO3','BO5') NOT NULL DEFAULT 'BO3',
  `estado` enum('Agendada','Em andamento','Concluida','Cancelada') NOT NULL DEFAULT 'Agendada',
  `mapas_equipa1` int(11) NOT NULL DEFAULT 0,
  `mapas_equipa2` int(11) NOT NULL DEFAULT 0
) ;

--
-- Extraindo dados da tabela `partidas_torneio`
--

INSERT INTO `partidas_torneio` (`id`, `torneio_id`, `equipa1_id`, `equipa2_id`, `vencedor_id`, `data_jogo`, `fase`, `formato`, `estado`, `mapas_equipa1`, `mapas_equipa2`) VALUES
(1, 1, 1, 2, 1, '2026-10-02 15:00:00', 'Fase de grupos', 'BO3', 'Concluida', 2, 1),
(2, 1, 3, 4, 3, '2026-10-03 17:00:00', 'Fase de grupos', 'BO3', 'Concluida', 2, 0),
(3, 1, 1, 3, NULL, '2026-10-12 18:00:00', 'Meia-final', 'BO3', 'Agendada', 0, 0),
(4, 2, 2, 3, NULL, '2026-11-02 16:00:00', 'Fase de grupos', 'BO3', 'Agendada', 0, 0),
(5, 3, 1, 2, 1, '2026-09-10 14:00:00', 'Final', 'BO1', 'Concluida', 1, 0);

-- --------------------------------------------------------

--
-- Estrutura da tabela `partida_mapa`
--

CREATE TABLE `partida_mapa` (
  `id` int(11) NOT NULL,
  `partida_id` int(11) NOT NULL,
  `mapa_id` int(11) NOT NULL,
  `numero_mapa` int(11) NOT NULL,
  `rondas_equipa1` int(11) NOT NULL DEFAULT 0,
  `rondas_equipa2` int(11) NOT NULL DEFAULT 0,
  `vencedor_id` int(11) DEFAULT NULL,
  `lado_inicial_equipa1` enum('CT','T') DEFAULT NULL,
  `overtime` tinyint(1) NOT NULL DEFAULT 0
) ;

--
-- Extraindo dados da tabela `partida_mapa`
--

INSERT INTO `partida_mapa` (`id`, `partida_id`, `mapa_id`, `numero_mapa`, `rondas_equipa1`, `rondas_equipa2`, `vencedor_id`, `lado_inicial_equipa1`, `overtime`) VALUES
(1, 1, 1, 1, 13, 9, 1, 'CT', 0),
(2, 1, 2, 2, 10, 13, 2, 'T', 0),
(3, 1, 5, 3, 13, 7, 1, 'CT', 0),
(4, 2, 3, 1, 13, 6, 3, 'T', 0),
(5, 2, 4, 2, 13, 8, 3, 'CT', 0),
(6, 5, 1, 1, 16, 12, 1, 'CT', 1);

-- --------------------------------------------------------

--
-- Estrutura da tabela `torneios`
--

CREATE TABLE `torneios` (
  `id` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `jogo` varchar(30) NOT NULL DEFAULT 'CS2',
  `data_inicio` date NOT NULL,
  `data_fim` date DEFAULT NULL,
  `formato` varchar(10) NOT NULL DEFAULT 'BO3',
  `estado` enum('Planeado','Em andamento','Concluido','Cancelado') NOT NULL DEFAULT 'Planeado'
) ;

--
-- Extraindo dados da tabela `torneios`
--

INSERT INTO `torneios` (`id`, `nome`, `jogo`, `data_inicio`, `data_fim`, `formato`, `estado`) VALUES
(1, 'CS2 Portugal Cup 2026', 'CS2', '2026-10-01', '2026-10-15', 'BO3', 'Em andamento'),
(2, 'Lisbon Esports Masters', 'CS2', '2026-11-01', '2026-11-10', 'BO3', 'Planeado'),
(3, 'CS:GO Legends Cup', 'CS:GO', '2026-09-01', '2026-09-20', 'BO1', 'Concluido');

--
-- Índices para tabelas despejadas
--

--
-- Índices para tabela `equipas`
--
ALTER TABLE `equipas`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nome` (`nome`),
  ADD UNIQUE KEY `tag` (`tag`);

--
-- Índices para tabela `estatisticas_jogador`
--
ALTER TABLE `estatisticas_jogador`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `partida_mapa_id` (`partida_mapa_id`,`jogador_id`),
  ADD KEY `jogador_id` (`jogador_id`);

--
-- Índices para tabela `inscricoes_torneio`
--
ALTER TABLE `inscricoes_torneio`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `torneio_id` (`torneio_id`,`equipa_id`),
  ADD KEY `equipa_id` (`equipa_id`);

--
-- Índices para tabela `jogadores`
--
ALTER TABLE `jogadores`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nickname` (`nickname`),
  ADD UNIQUE KEY `steam_id` (`steam_id`);

--
-- Índices para tabela `jogador_equipa`
--
ALTER TABLE `jogador_equipa`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `jogador_id` (`jogador_id`),
  ADD KEY `equipa_id` (`equipa_id`);

--
-- Índices para tabela `mapas`
--
ALTER TABLE `mapas`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nome` (`nome`);

--
-- Índices para tabela `partidas_torneio`
--
ALTER TABLE `partidas_torneio`
  ADD PRIMARY KEY (`id`),
  ADD KEY `torneio_id` (`torneio_id`),
  ADD KEY `equipa1_id` (`equipa1_id`),
  ADD KEY `equipa2_id` (`equipa2_id`),
  ADD KEY `vencedor_id` (`vencedor_id`);

--
-- Índices para tabela `partida_mapa`
--
ALTER TABLE `partida_mapa`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `partida_id` (`partida_id`,`numero_mapa`),
  ADD KEY `mapa_id` (`mapa_id`),
  ADD KEY `vencedor_id` (`vencedor_id`);

--
-- Índices para tabela `torneios`
--
ALTER TABLE `torneios`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `equipas`
--
ALTER TABLE `equipas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `estatisticas_jogador`
--
ALTER TABLE `estatisticas_jogador`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `inscricoes_torneio`
--
ALTER TABLE `inscricoes_torneio`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `jogadores`
--
ALTER TABLE `jogadores`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de tabela `jogador_equipa`
--
ALTER TABLE `jogador_equipa`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de tabela `mapas`
--
ALTER TABLE `mapas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de tabela `partidas_torneio`
--
ALTER TABLE `partidas_torneio`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `partida_mapa`
--
ALTER TABLE `partida_mapa`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `torneios`
--
ALTER TABLE `torneios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restrições para despejos de tabelas
--

--
-- Limitadores para a tabela `estatisticas_jogador`
--
ALTER TABLE `estatisticas_jogador`
  ADD CONSTRAINT `estatisticas_jogador_ibfk_1` FOREIGN KEY (`partida_mapa_id`) REFERENCES `partida_mapa` (`id`),
  ADD CONSTRAINT `estatisticas_jogador_ibfk_2` FOREIGN KEY (`jogador_id`) REFERENCES `jogadores` (`id`);

--
-- Limitadores para a tabela `inscricoes_torneio`
--
ALTER TABLE `inscricoes_torneio`
  ADD CONSTRAINT `inscricoes_torneio_ibfk_1` FOREIGN KEY (`torneio_id`) REFERENCES `torneios` (`id`),
  ADD CONSTRAINT `inscricoes_torneio_ibfk_2` FOREIGN KEY (`equipa_id`) REFERENCES `equipas` (`id`);

--
-- Limitadores para a tabela `jogador_equipa`
--
ALTER TABLE `jogador_equipa`
  ADD CONSTRAINT `jogador_equipa_ibfk_1` FOREIGN KEY (`jogador_id`) REFERENCES `jogadores` (`id`),
  ADD CONSTRAINT `jogador_equipa_ibfk_2` FOREIGN KEY (`equipa_id`) REFERENCES `equipas` (`id`);

--
-- Limitadores para a tabela `partidas_torneio`
--
ALTER TABLE `partidas_torneio`
  ADD CONSTRAINT `partidas_torneio_ibfk_1` FOREIGN KEY (`torneio_id`) REFERENCES `torneios` (`id`),
  ADD CONSTRAINT `partidas_torneio_ibfk_2` FOREIGN KEY (`equipa1_id`) REFERENCES `equipas` (`id`),
  ADD CONSTRAINT `partidas_torneio_ibfk_3` FOREIGN KEY (`equipa2_id`) REFERENCES `equipas` (`id`),
  ADD CONSTRAINT `partidas_torneio_ibfk_4` FOREIGN KEY (`vencedor_id`) REFERENCES `equipas` (`id`);

--
-- Limitadores para a tabela `partida_mapa`
--
ALTER TABLE `partida_mapa`
  ADD CONSTRAINT `partida_mapa_ibfk_1` FOREIGN KEY (`partida_id`) REFERENCES `partidas_torneio` (`id`),
  ADD CONSTRAINT `partida_mapa_ibfk_2` FOREIGN KEY (`mapa_id`) REFERENCES `mapas` (`id`),
  ADD CONSTRAINT `partida_mapa_ibfk_3` FOREIGN KEY (`vencedor_id`) REFERENCES `equipas` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
