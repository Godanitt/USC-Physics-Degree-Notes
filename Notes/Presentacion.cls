\ProvidesClass{presentacion}[2025/04/26 Clase personalizada para libros de apuntes]

%----------------------------------------------------------------------------
% BASE DE DOCUMENTO
%----------------------------------------------------------------------------

\LoadClass[9pt]{beamer}% Puedes definir un tema por defecto si quieres:
\PassOptionsToClass{presentation}{beamer}


%----------------------------------------------------------------------------
% PAQUETES BÁSICOS
%----------------------------------------------------------------------------
\RequirePackage[spanish,es-tabla,es-nodecimaldot]{babel}
\RequirePackage{amsmath} % Para usar el entorno de ecuaciones
\RequirePackage{amsthm} % Para usar el entorno de teoremas
\RequirePackage{amsfonts} % 
\RequirePackage{amssymb} % 
\RequirePackage{makeidx}
\RequirePackage{graphicx}
\RequirePackage{lmodern}
\RequirePackage[dvipsnames]{xcolor} 
\RequirePackage{array}			 % Para fjar tamaño de columnas
\RequirePackage{tikz}
\RequirePackage{pgfplots} % Para controlar la perspectiva
\RequirePackage{siunitx}
\RequirePackage{extramarks} % Para poder usar firstleftmarks
\RequirePackage[version=4]{mhchem} % Para poder usar formulas de reacciones nucleares
\RequirePackage{chemfig}
\RequirePackage{xcolor}
\RequirePackage[most]{tcolorbox}
\RequirePackage{enumitem}
\RequirePackage{physics} 
\RequirePackage{eso-pic} % Para insertar imágenes de fondo específicas
\RequirePackage[absolute,overlay]{textpos} % Paquete para colocar elementos en posiciones absolutas
\RequirePackage{booktabs}
\RequirePackage{float} % en el preámbulo
\RequirePackage{lipsum}
\RequirePackage{adjustbox} % en el preámbulo
\RequirePackage{etoolbox} % asegúrate de incluir esto

% ----------------------------------------------------------------------------
% CONFIGURACIÓN DE Tcolorbox 
% ----------------------------------------------------------------------------

\newtcolorbox{Enunciado}{
  colback=Gray!40,    % Color de fondo
  colframe=Gray!40,   % Color del borde
  sharp corners,      % Esquinas cuadradas
  boxrule=0pt,        % Grosor del borde (0pt para que desaparezca)
  left=5pt,           % Margen izquierdo interno
  right=5pt,          % Margen derecho interno
  top=5pt,            % Margen superior interno
  bottom=5pt          % Margen inferior interno
}

% ----------------------------------------------------------------------------
% CONFIGURACIÓN DE BIBLATEX
% ----------------------------------------------------------------------------
\RequirePackage{csquotes} % Required by biblatex
\RequirePackage{filecontents} % Required by biblatex
\RequirePackage{filecontents} % Required by biblatex
\RequirePackage[ 	backend=biber, % Use the biber backend for compiling the bibliography
	citestyle=numeric, % In-text citation style
	bibstyle=numeric, % Bibliography style
	sorting=none, % Order references in the order in which they are used in the document
]{biblatex}


%----------------------------------------------------------------------------
% SIUNITX CONFIGURACIÓN
%----------------------------------------------------------------------------
\sisetup{output-decimal-marker={.},
	% exponentes ------------------------
	exponent-mode=threshold,
	exponent-thresholds=-3:4, % non usar exponentes 10^{-2,-1, 0, 1,2,3}
	% redondear -------------------------
	% round-mode=figures, % cifras sig
	% round-mode=places, % cantos decimales
	round-mode=uncertainty, % cifras sig da incerteza (necesario usar erro)
	round-precision=2,
	%uncertainty-mode = separate,
	print-unity-mantissa=false,
	% unidades --------------------------
	inter-unit-product = \ensuremath{{}\cdot{}}, % separacion entre unidades
	% per-mode=power-positive-first, % so furrula con metodo interpretado puro
	inline-per-mode=single-symbol,
	display-per-mode=fraction,
}
% ----------------------------------------------------------------------------
% FUENTES
% ----------------------------------------------------------------------------

%\RequirePackage{newtxtext,newtxmath} % Times

\newcommand{\Ecal}{\mathcal{E}}