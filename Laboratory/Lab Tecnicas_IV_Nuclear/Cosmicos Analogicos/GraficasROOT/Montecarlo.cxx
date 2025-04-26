// Programa de simulación Monte Carlo en ROOT (C++) para eficiencia de detección a través de dos placas.
//
// Este programa realiza las siguientes tareas:
// 1. Lee datos experimentales desde un archivo CSV con columnas: distancia, error de distancia, tasa de cuentas, error de tasa.
// 2. Ejecuta simulaciones Monte Carlo para estimar la eficiencia (fracción de partículas detectadas en coincidencia por dos placas)
//    para dos índices de dispersión diferentes: n = 2.00 y n = 2.70. Usa N aprox 1000000 partículas simuladas en cada caso.
// 3. Calcula el chi-cuadrado entre los datos simulados y los datos reales para ambos valores de n.
// 4. Grafica los puntos experimentales con sus barras de error, junto con las eficiencias simuladas para n=2 y n=2.70 sobre los mismos puntos,
//    y traza una curva suave que representa la tendencia (mediante simulación adicional para interpolar entre puntos).
// 5. Utiliza ROOT para crear los gráficos (TGraphErrors para datos con errores, TGraph para curvas simuladas) y manejo de canvas.
// 6. Comenta el código extensivamente para explicar cada paso.
//
// Se puede compilar este código usando:
//    g++ MonteCarloSim.cpp `root-config --cflags --libs` -o MonteCarloSim
// o ejecutar directamente en ROOT (macro) con:
//    root -l -q MonteCarloSim.cxx++   (compila y ejecuta el macro con ACLiC)
//    root -l MonteCarloSim.cxx       (interpreta y ejecuta el macro (el nuestro))
//
// Notas:
// - N (número de partículas simuladas) es grande para obtener buena estadística, por lo que la ejecución puede tardar algunos segundos.
// - Si se ejecuta como programa independiente, se utiliza TApplication para visualizar el gráfico interactivo.
// - Ajuste el valor de detectorRadius según el tamaño real de las placas en el experimento (aquí asumido 10 cm de radio).
//
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <cmath>
#include <string>
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif
#include "TRandom3.h"
#include "TCanvas.h"
#include "TGraphErrors.h"
#include "TGraph.h"
#include "TLegend.h"
#include "TAxis.h"
#include "TROOT.h"
#include "TApplication.h"
#include "TString.h"

// Definir parámetros globales de la simulación
const int Nparticles = 10000000;        // Número de partículas simuladas en cada corrida Monte Carlo (N = 1,000,000)
const double detectorRadius = 10.0; // Radio de cada detector (cm). *Ajustar según el tamaño real de las placas*.



// Función para leer datos desde un archivo CSV.
// Formato esperado del CSV:
// Columna1 = distancia (d), Columna2 = incertidumbre de d (ud),
// Columna3 = tasa de cuentas real (nr), Columna4 = incertidumbre de la tasa (unr).
bool LeerDatosCSV(const char* filename,
                  std::vector<double> &dist, std::vector<double> &errDist,
                  std::vector<double> &rate, std::vector<double> &errRate)
{
    
    std::ifstream infile(filename);
    if (!infile.is_open())
    {
        std::cerr << "No se pudo abrir el archivo: " << filename << std::endl;
        return 1;
    }

    std::string linea;
    std::getline(infile, linea); // saltar cabecera

    std::vector<double> x, sx, y, sy;

    while (std::getline(infile, linea))
    {
        std::stringstream ss(linea);
        std::string campo;
        std::vector<double> fila;

        while (std::getline(ss, campo, ','))
        {
            fila.push_back(std::stod(campo));
        }

        if (fila.size() == 4)
        {
            x.push_back(fila[0]);
            sx.push_back(fila[1]);
            y.push_back(fila[2]);
            sy.push_back(fila[3]);
        }
    }

    int N = x.size();
    // Almacenar valores en los vectores de salida
    dist=x;
    errDist=sx;
    rate=y;
    errRate=sy;

return true;
}

// Función de simulación Monte Carlo que calcula la eficiencia (fracción de coincidencias)
// para un índice de dispersión dado (n) y una separación d entre detectores.
double SimularEficiencia(double n, double d, TRandom3 &randGen)
{
    long long countCoincident = 0;
    // Generar Nparticles partículas incidentes en la primera placa
    for (int i = 0; i < Nparticles; ++i)
    {
        // Generar posición aleatoria uniforme en el área de la primera placa (rectangulo de tamaño 30 x 10)
        double x1 = randGen.Uniform()*30;
        double y1 = randGen.Uniform()*10;
        double r = detectorRadius * std::sqrt(std::pow(x1,2)+std::pow(y1,2));      // distribución radial uniforme (porque P(r) dr ~ r dr)
        // Generar dirección aleatoria de la partícula conforme a la distribución angular ~ cos^n(theta).
        // Usamos la distribución condicional para partículas que atraviesan una superficie horizontal: f(cosθ) ~ cos^(n+1)(θ).
        double u2 = randGen.Uniform();
        double cosTheta = std::pow(u2, 1.0 / (n + 2.0)); // inversa de CDF para cosθ con exponente (n+1)
        double sinTheta = std::sqrt(1 - cosTheta * cosTheta);
        double phi_dir = randGen.Uniform(0, 2 * M_PI); // ángulo azimutal uniforme de la dirección
        // Calcular la posición de impacto en la segunda placa (separada una distancia d en z)
        // Suponemos placas paralelas y centradas: la partícula viaja en línea recta desde (x0, y0) en placa1 hasta (x1, y1) en placa2.
        double x2 = x1 + d * (sinTheta * std::cos(phi_dir));
        double y2 = y1 + d * (sinTheta * std::sin(phi_dir));
        // Comprobar si cae dentro del área de la segunda placa
        if ( x2 > 0 && x2 < 30 && y2 > 0 && y2 < 10)
        {
            countCoincident++;
        }
    }
    // Eficiencia = número de coincidencias / número de partículas lanzadas
    double efficiency = (double)countCoincident / (double)Nparticles;
    return efficiency;
}

int Montecarlo()
{
    // Nombre del archivo de datos CSV
    const char* nombreArchivo = "Distancias.csv";


    // 1. Lectura de datos experimentales desde el archivo CSV
    std::vector<double> dist, errDist, rate, errRate;
    if (!LeerDatosCSV(nombreArchivo, dist, errDist, rate, errRate))
    {
        return 1; // Terminar si falla la lectura de datos
    }
    int Npoints = dist.size();
    if (Npoints == 0)
    {
        std::cerr << "No se encontraron datos en el archivo." << std::endl;
        return 1;
    }

    // 2. Simulación de Monte Carlo para estimar la eficiencia a n = 2.00 y n = 2.70 en cada distancia medida
    TRandom3 randGen;
    randGen.SetSeed(0); // Semilla aleatoria basada en tiempo (0). Usar un valor fijo para resultados reproducibles.
    double n1 = 2.0;
    double n2 = 4.63;
    std::vector<double> eff_n1;
    std::vector<double> eff_n2;
    eff_n1.reserve(Npoints);
    eff_n2.reserve(Npoints);
    for (int i = 0; i < Npoints; ++i)
    {
        double d = dist[i];
        double eff1 = SimularEficiencia(n1, d, randGen);
        double eff2 = SimularEficiencia(n2, d, randGen);
        eff_n1.push_back(eff1);
        eff_n2.push_back(eff2);
    }

    // 3. Calcular el chi-cuadrado entre los datos simulados y los reales para n = 2.00 y n = 2.70
    // Se permite ajustar una normalización global de la simulación a los datos (ya que la tasa absoluta depende de factores experimentales).
    double chi2_n1 = 0.0, chi2_n2 = 0.0;
    double scale_n1 = 1.0, scale_n2 = 1.0;
    // Calcular factor de escala óptimo para n1 minimizando chi² = Σ[(datos - escala*simulación)^2/σ^2]
    {
        double num = 0.0, den = 0.0;
        for (int i = 0; i < Npoints; ++i)
        {
            double sigma = (errRate[i] == 0.0 ? 1.0 : errRate[i]);
            num += rate[i] * eff_n1[i] / (sigma * sigma);
            den += eff_n1[i] * eff_n1[i] / (sigma * sigma);
        }
        if (den != 0.0)
            scale_n1 = num / den;
        // Calcular chi² resultante para n1
        for (int i = 0; i < Npoints; ++i)
        {
            double sigma = (errRate[i] == 0.0 ? 1.0 : errRate[i]);
            double model = eff_n1[i] * scale_n1;
            double diff = model - rate[i];
            chi2_n1 += (diff * diff) / (sigma * sigma);
        }
    }
    // Calcular factor de escala óptimo y chi² para n2
    {
        double num = 0.0, den = 0.0;
        for (int i = 0; i < Npoints; ++i)
        {
            double sigma = (errRate[i] == 0.0 ? 1.0 : errRate[i]);
            num += rate[i] * eff_n2[i] / (sigma * sigma);
            den += eff_n2[i] * eff_n2[i] / (sigma * sigma);
        }
        if (den != 0.0)
            scale_n2 = num / den;
        for (int i = 0; i < Npoints; ++i)
        {
            double sigma = (errRate[i] == 0.0 ? 1.0 : errRate[i]);
            double model = eff_n2[i] * scale_n2;
            double diff = model - rate[i];
            chi2_n2 += (diff * diff) / (sigma * sigma);
        }
    }
    // Imprimir resultados de ajuste y chi²
    std::cout << "Resultado del ajuste:" << std::endl;
    std::cout << "  n = " << n1 << " -> escala = " << scale_n1 << ", chi-cuadrado = " << chi2_n1 << std::endl;
    std::cout << "  n = " << n2 << " -> escala = " << scale_n2 << ", chi-cuadrado = " << chi2_n2 << std::endl;

    // 4. Graficar datos experimentales y resultados simulados para ambas n
    // Preparar los datos para gráficas de ROOTcone
    // (TGraphErrors necesita punteros a arreglos de double; usamos data() de vector)
    TGraphErrors *grData = new TGraphErrors(Npoints, dist.data(), rate.data(), errDist.data(), errRate.data());
    //grData->SetTitle("");
    grData->GetXaxis()->SetTitle("d_{real} [cm]");
    grData->GetYaxis()->SetTitle("n_{r} [1/s]");
    grData->SetMarkerStyle(20); // círculo lleno
    grData->SetMarkerColor(kBlack);
    grData->SetLineColor(kBlack);
    grData->SetLineWidth(1);

    // Generar puntos adicionales para una curva suave (interpolación por simulación) de cada modelo
    int NcurvePoints = 100;
    double d_min = dist[0];
    double d_max = dist[0];
    for (double val : dist)
    {
        if (val < d_min)
            d_min = val;
        if (val > d_max)
            d_max = val;
    }
    // Reservar vectores para curva
    std::vector<double> curve_d;
    std::vector<double> curve_sim1;
    std::vector<double> curve_sim2;
    curve_d.reserve(NcurvePoints);
    curve_sim1.reserve(NcurvePoints);
    curve_sim2.reserve(NcurvePoints);
    double step = (d_max - d_min) / (NcurvePoints - 1);
    for (int j = 0; j < NcurvePoints; ++j)
    {
        double d_val = d_min + step * j;
        if (d_val < 0)
            d_val = 0.0; // asegurar no negativa, por si d_min es 0 de todos modos
        double eff1 = SimularEficiencia(n1, d_val, randGen);
        double eff2 = SimularEficiencia(n2, d_val, randGen);
        curve_d.push_back(d_val);
        curve_sim1.push_back(eff1 * scale_n1);
        curve_sim2.push_back(eff2 * scale_n2);
    }
    TGraph *grSim1 = new TGraph(NcurvePoints, curve_d.data(), curve_sim1.data());
    TGraph *grSim2 = new TGraph(NcurvePoints, curve_d.data(), curve_sim2.data());
    grSim1->SetLineColor(kRed);
    grSim1->SetLineWidth(2);
    grSim1->SetLineStyle(1); // línea sólida
    grSim2->SetLineColor(kBlue);
    grSim2->SetLineWidth(2);
    grSim2->SetLineStyle(2); // línea discontinua

    // 5. Usar ROOT para graficar en un canvas
    TCanvas *c1 = new TCanvas("c1", "Simulacion vs Datos", 800, 600);
    c1->SetGrid();
    grData->Draw("AP");     // dibujar puntos (A: ejes automáticos, P: markers con error bars)
    grSim1->Draw("L SAME"); // dibujar curva n=2 (L: línea conectando puntos simulados, SAME: en la misma gráfica)
    grSim2->Draw("L SAME"); // dibujar curva n=2.70

    // 6. Agregar una leyenda explicando cada conjunto de datos
    TLegend *legend = new TLegend(0.55, 0.7, 0.88, 0.85);
    legend->SetBorderSize(0);
    legend->SetFillColor(0);
    legend->AddEntry(grData, "Datos experimentales", "PE"); // Puntos con error
    TString label1 = TString::Format("Simulacion n=%.2f", n1);
    TString label2 = TString::Format("Simulacion n=%.2f", n2);
    legend->AddEntry(grSim1, label1.Data(), "L");
    legend->AddEntry(grSim2, label2.Data(), "L");
    legend->Draw();
    //SetEstiloPublicacion();
    //c1->SetRightMargin(0.03);   // achica el margen derecho
    //c1->SetTopMargin(0.03);     // más apretado arriba
    c1->Update(); // Actualizar el canvas para asegurar que todo esté dibujado
    c1->SaveAs("../Graficas/Montecarlo.pdf");

// Mantener la aplicación abierta (solo si es programa independiente, no macro) hasta que se cierre la ventana
#ifndef __CINT__
    std::cout << ">> Cierre la ventana del gráfico para finalizar la ejecución <<" << std::endl;
// app.Run();
#endif

    // Guardar en un CSV los resultados de tasa simulada (n_r) y su incertidumbre para cada distancia
    std::ofstream outfile("../Datos Crudos/Eficiencias.csv");
    if (!outfile.is_open()) {
        std::cerr << "No se pudo crear el archivo de salida Montecarlo_resultados.csv" << std::endl;
    } else {
        outfile << "distancia,sim_n1,err_sim_n1,sim_n2,err_sim_n2\n";
        for (int i = 0; i < Npoints; ++i) {
            double e1 = eff_n1[i];
            double e2 = eff_n2[i];
            double sim_n1 = e1 * scale_n1;
            double sim_n2 = e2 * scale_n2;
            double err_sim_n1 = scale_n1 * std::sqrt(e1 * (1.0 - e1) / Nparticles);
            double err_sim_n2 = scale_n2 * std::sqrt(e2 * (1.0 - e2) / Nparticles);
            outfile << dist[i] << "," << sim_n1 << "," << err_sim_n1 << ","
                    << sim_n2 << "," << err_sim_n2 << "\n";
        }
        outfile.close();
        std::cout << ">> Resultados guardados en Montecarlo_resultados.csv" << std::endl;
    }

    return 0;
}
