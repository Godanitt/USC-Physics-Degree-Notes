%% Clase personalizada para libros de apuntes

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{apuntesbook}[2025/04/26 Clase personalizada para libros de apuntes]

%----------------------------------------------------------------------------
% BASE DE DOCUMENTO
%----------------------------------------------------------------------------

\LoadClass[12pt]{book}

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
\RequirePackage{fancyhdr}
\RequirePackage{geometry}
\RequirePackage{lastpage}		
\RequirePackage{array}			 % Para fjar tamaño de columnas
\RequirePackage{tikz}
\RequirePackage{subcaption}
\RequirePackage{caption}
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
\RequirePackage{wrapfig}
\RequirePackage{booktabs}
\RequirePackage{float} % en el preámbulo
\RequirePackage{lipsum}
\RequirePackage{adjustbox} % en el preámbulo
\RequirePackage{etoolbox} % asegúrate de incluir esto
\RequirePackage{tocloft} % Para incluir código fuente
\RequirePackage{minitoc} % para hacer tableofcontents de ejercicios

%----------------------------------------------------------------------------
% ÍNDICE PERSONALIZADO
%----------------------------------------------------------------------------

\addto\captionsspanish{\renewcommand{\contentsname}{Índice general}}
\let\oldtableofcontents\tableofcontents
\renewcommand{\tableofcontents}{\begingroup\oldtableofcontents\endgroup}

%----------------------------------------------------------------------------
% Tamaño de secciones y subsecciones 
%----------------------------------------------------------------------------

\RequirePackage{sectsty}
\chapterfont{\Huge}
\sectionfont{\Large}
\subsectionfont{\large}
\subsubsectionfont{\normalsize}


%----------------------------------------------------------------------------
% CAPTIONS
%----------------------------------------------------------------------------
\captionsetup{font=small, justification=centering, skip=6pt, labelfont={bf,small}, textfont={small}}

%----------------------------------------------------------------------------
% CONFIGURACIÓN DE Minitoc
%----------------------------------------------------------------------------

%\setcounter{minitocdepth}{1} % Define la profundidad que quieres (secciones, subsecciones...)
%\setcounter{secttocdepth}{2} % Esto es importante para las secciones
\dominitoc % Activa las minitoc (chapter)
%\dosecttoc % Activa las minitoc (section)


%----------------------------------------------------------------------------
% CONFIGURACIÓN DE TIKZ
%----------------------------------------------------------------------------

\usetikzlibrary{arrows.meta, calc, positioning, shapes.geometric, shapes.misc, shapes.symbols, decorations.pathreplacing, decorations.pathmorphing, decorations.text, 3d}
\usetikzlibrary{backgrounds, fit, shapes, arrows, shadows.blur, shadows, patterns, fadings}
\usetikzlibrary{decorations.pathreplacing, calligraphy, shapes.geometric, shapes.symbols, calc, positioning, arrows.meta}

% ----------------------------------------------------------------------------
% CONFIGURACIÓN DE PGFPLOTS
% ----------------------------------------------------------------------------
\pgfplotsset{compat=1.18}
\pgfplotsset{every axis/.append style={
    title style={font=\normalsize},
    xlabel style={font=\normalsize},
    ylabel style={font=\normalsize},
    legend style={font=\normalsize},
    tick label style={font=\small},
    label style={font=\small},
    width=0.8\textwidth,
    height=0.4\textwidth,
}}
\pgfplotsset{every axis label/.append style={font=\normalsize}}

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

\newtcolorbox{mybox}{colback=black!5!white, colframe=black!75!black}
\newtcolorbox{Anotacion}{colback=red!5!white, colframe=red!75!red}


% ----------------------------------------------------------------------------
% CONFIGURACIÓN DE BIBLATEX
% ----------------------------------------------------------------------------

\usepackage{biblatex} %Imports biblatex packag


%----------------------------------------------------------------------------
% GEOMETRÍA
%----------------------------------------------------------------------------
\geometry{a4paper, left=20mm, top=30mm, right=30mm, bottom=25mm}

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

\RequirePackage{newtxtext,newtxmath} % Times
%\usepackage{helvet} % Helvetica
%\usepackage{newpxtext,newpxmath} % Palatino
%\usepackage{lmodern} % Latin Modern

% ----------------------------------------------------------------------------
% CONFIGURACIÓN DE CAPÍTULOS
% ----------------------------------------------------------------------------

%\usepackage[lmodern]{quotchap}
%\usepackage[options]{fncychap}
% Configuración de la imagen de fondo solo para la portada


%----------------------------------------------------------------------------
% FORMATO DE PÁGINA
%----------------------------------------------------------------------------
% Cambia el título grande del índice
\renewcommand{\contentsname}{\sffamily\bfseries Índice general}

% Redefinimos el índice
\makeatletter
\renewcommand{\tableofcontents}{%
  \cleardoublepage
  \phantomsection
  \markboth{Indice general}{} % Ponemos 'Indice general' en la cabecera
  {\centering\Large\sffamily\bfseries Índice general\par} % Título grande
  \vspace{1cm}
  \@starttoc{toc}
}
\makeatother

\renewcommand{\cftchapfont}{\large\bfseries}
\renewcommand{\cftchappagefont}{\large\bfseries}
\renewcommand{\cftsecfont}{}
\renewcommand{\cftsecpagefont}{}

\makeatletter
\renewcommand{\chaptermark}[1]{%
  \if@mainmatter
    \markboth{\chaptername\ \thechapter.\ #1}{}
  \else
    \markboth{#1}{}
  \fi
}
\makeatother

\renewcommand{\sectionmark}[1]{\markright{\thesection.\ #1}}


\setlength{\headsep}{27pt}
\setlength{\footskip}{30pt}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[LE]{\leftmark}
\fancyhead[RO]{\rightmark}
\fancyhead[LO,RE]{Daniel Vázquez Lago}
\fancyfoot[LE,RO]{\thepage}
\renewcommand{\headrulewidth}{1pt}
\renewcommand{\footrulewidth}{0pt}

\setlength{\parindent}{0pt}

%----------------------------------------------------------------------------
% HIPERVÍNCULOS
%----------------------------------------------------------------------------
\RequirePackage{hyperref}
\RequirePackage{cleveref}
\hypersetup{colorlinks=true, linkcolor=blue, citecolor=ForestGreen, urlcolor=BrickRed}
\crefname{figure}{fig.}{figs.}
\crefname{table}{tab.}{tabs.}
\crefname{subsection}{subsec.}{subsecs.}

%----------------------------------------------------------------------------
% LISTINGS CONFIGURACIÓN
%----------------------------------------------------------------------------
\definecolor{mygreen}{rgb}{0,0.6,0}
\definecolor{mygray}{rgb}{0.5,0.5,0.5}
\definecolor{mymauve}{rgb}{0.58,0,0.82}
\lstset{
  backgroundcolor=\color{white},
  basicstyle=\footnotesize\ttfamily,
  breaklines=true,
  captionpos=b,
  commentstyle=\color{mygreen},
  frame=single,
  keepspaces=true,
  keywordstyle=\color{blue},
  language=Python,
  numbers=left,
  numbersep=5pt,
  numberstyle=\tiny\color{mygray},
  rulecolor=\color{black},
  showstringspaces=false,
  stringstyle=\color{mymauve},
  tabsize=2,
  title=\lstname
}

%----------------------------------------------------------------------------
% COMANDOS PERSONALIZADOS
%----------------------------------------------------------------------------


\newcommand{\parentesis}[1]{\left( #1  \right)}
\newcommand{\parciales}[2]{\frac{\partial #1}{\partial #2}}
\newcommand{\pparciales}[2]{\parentesis{\parciales{#1}{#2}}}
\newcommand{\ccorchetes}[1]{\left[ #1  \right]}
\newcommand{\D}{\mathrm{d}}
\newcommand{\derivadas}[2]{\frac{\D #1}{\D #2}}

\newcommand{\tquad}{\quad \quad \quad}
%\newcommand{\vnabla}{\vec{\nabla}}

\newcommand{\Ocal}{\mathcal{O}}
\newcommand{\Jcal}{\mathcal{J}}
\newcommand{\Mcal}{\mathcal{M}}
\newcommand{\Fcal}{\mathcal{F}}
\newcommand{\Hcal}{\mathcal{H}}
\newcommand{\Ecal}{\mathcal{E}}
\newcommand{\Ncal}{\mathcal{N}}

\newcommand{\cmm}{\text{cm}^{-1}}
\newcommand{\fcc}{\textit{fcc}}
\newcommand{\bcc}{\textit{bcc}}
\renewcommand{\sc}{\textit{sc}}
\newcommand{\hcp}{\textit{hcp}}


\newcommand{\PZB}{\text{{\tiny PZB}}}
\newcommand{\gap}{\text{{\tiny gap}}}
\newcommand{\SZB}{\text{{\tiny SZB}}}
\newcommand{\inicial}{\text{{\tiny inicial}}}
\newcommand{\final}{\text{{\tiny final}}}
\newcommand{\atomico}{\text{{\tiny atómico}}}

\newcommand{\arctanh}{\text{{arctanh}}}

\newcommand{\Vbi}{V_{\text{bi}}}



\newcommand{\Namas}{\text{Na}^+}
\newcommand{\Clmenos}{\text{Cl}^-}

\newcommand{\cm}{\text{cm}}
\newcommand{\eV}{\text{eV}}

\newcommand{\arr}{\text{arr}}
\newcommand{\diff}{\text{diff}}

\newcommand{\er}{$^{\text{er}}$}
\newcommand{\cte}{\text{cte}}


% Comandos vectoriales

\newcommand{\an}{\mathbf{a}}
\newcommand{\bn}{\mathbf{b}}
\newcommand{\dn}{\mathbf{d}}
\newcommand{\fn}{\mathbf{f}}
\newcommand{\jn}{\mathbf{j}}
\newcommand{\kn}{\mathbf{k}}
\newcommand{\pn}{\mathbf{p}}
\newcommand{\qn}{\mathbf{q}}
\newcommand{\rn}{\mathbf{r}}
\newcommand{\sn}{\mathbf{s}}
\newcommand{\un}{\mathbf{u}}
\newcommand{\vn}{\mathbf{v}}
\newcommand{\xn}{\mathbf{x}}
\newcommand{\wn}{\mathbf{w}}
\newcommand{\yn}{\mathbf{y}}
\newcommand{\qndot}{\dot{\qn}}


\newcommand{\alphan}{\boldsymbol{\alpha}}
\newcommand{\sigman}{\boldsymbol{\sigma}}
\newcommand{\pin}{\boldsymbol{\pi}}
\newcommand{\rhon}{\boldsymbol{\rho}}
\newcommand{\epsilonn}{\boldsymbol{\epsilon}}
\newcommand{\omegan}{\boldsymbol{\omega}}
\newcommand{\mun}{\boldsymbol{\mu}}



\newcommand{\An}{\mathbf{A}}
\newcommand{\Bn}{\mathbf{B}}
\newcommand{\En}{\mathbf{E}}
\newcommand{\Fn}{\mathbf{F}}
\newcommand{\Jn}{\mathbf{J}}
\newcommand{\Hn}{\mathbf{H}}
\newcommand{\Gn}{\mathbf{G}}
\newcommand{\Kn}{\mathbf{K}}
\newcommand{\Ln}{\mathbf{L}}
\newcommand{\Mn}{\mathbf{M}}
\newcommand{\Pn}{\mathbf{P}}
\newcommand{\Sn}{\mathbf{S}}
\newcommand{\Tn}{\mathbf{T}}
\newcommand{\In}{\mathbf{1}}
\newcommand{\Encal}{\boldsymbol{\mathcal{E}}}

\newcommand{\hnn}{\hat{\mathbf{n}}}
\newcommand{\hnr}{\hat{\mathbf{r}}}
\newcommand{\hnz}{\hat{\mathbf{z}}}
\newcommand{\hnv}{\hat{\mathbf{v}}}
\newcommand{\hnx}{\hat{\mathbf{x}}}
\newcommand{\hny}{\hat{\mathbf{y}}} 
\newcommand{\hnu}{\hat{\mathbf{u}}}
\newcommand{\hnR}{\hat{\mathbf{R}}}
\newcommand{\hnp}{\hat{\mathbf{p}}}
\newcommand{\hnk}{\hat{\mathbf{k}}}
\newcommand{\hni}{\hat{\mathbf{i}}}
\newcommand{\hnj}{\hat{\mathbf{j}}}
\renewcommand{\hnk}{\hat{\mathbf{k}}}

%----------------------------------------------------------------------------
% TEOREMAS
%----------------------------------------------------------------------------
\theoremstyle{theorem}
\newtheorem{definition}{Definición}[chapter]
\newtheorem{definition_equivalente}{Definición equivalente}[definition]
\newtheorem{theorem}{Teorema}[chapter]

\numberwithin{equation}{section}
\numberwithin{figure}{chapter}

%----------------------------------------------------------------------------
% PREFACIO AUTOMÁTICO
%----------------------------------------------------------------------------
\newcommand{\prefacio}{%
  \cleardoublepage
  \phantomsection
  \addcontentsline{toc}{chapter}{Prefacio}
  \chapter*{Prefacio}Estos apuntes han sido elaborados con el propósito de servir como guía de estudio y consulta para la asignatura de Física. Su contenido intenta recoger, de forma clara y estructurada, los principales conceptos, desarrollos teóricos, ejercicios y aplicaciones que conforman el temario de la materia.

  Sin embargo, lejos de considerarse un material cerrado o definitivo, estos apuntes están pensados como un proyecto abierto y en continua evolución. He creado un repositorio en \href{https://github.com/Godanitt/USC-Physics-Degree-Notes}{github}. donde se encuentra todo el contenido en formato editable. Cualquier persona interesada puede contribuir: ya sea corrigiendo errores, ampliando explicaciones, añadiendo ejemplos, mejorando las figuras o proponiendo nuevas secciones. Las aportaciones pueden ser compartidas conmigo para seguir mejorando colectivamente estos apuntes o, si lo prefieres, puedes trabajar de forma independiente y adaptarlos a tus propias necesidades. El objetivo es construir entre todos unos buenos apuntes de Física, accesibles, claros y útiles.
  
  Espero que este material te resulte útil, y te animo a colaborar o a utilizarlo como base para tus propios proyectos. ¡Buen estudio!
}


\endinput
