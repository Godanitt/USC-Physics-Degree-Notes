
#include "TFile.h"
#include "TH1.h"
#include "TCanvas.h"
#include "TGraphErrors.h"
#include "TF1.h"
#include "TMultiGraph.h"
#include "TStyle.h"
#include "TLegend.h"
#include "TEfficiency.h"
#include "TGraph.h"
#include "TGraphAsymmErrors.h"
#include "TPaveStats.h"
#include <vector>
#include <TCanvas.h>
#include <TGraph.h>
#include <TF1.h>
#include <TLegend.h>
#include <vector>
#include <string>

void calcular_sV(const std::vector<double_t>& V, std::vector<double_t>& sV) {
    for (size_t i = 0; i < V.size(); ++i) {
        sV[i] = 0.005 * V[i] + 0.0002;
    }
}

void calcular_sI(const std::vector<double_t>& I, std::vector<double_t>& sI) {
    for (size_t i = 0; i < I.size(); ++i) {
        sI[i] = 0.01 * I[i] + 0.002;
    }
}


// ---- FUNCIÓN ---- //
void hacerGrafico(const std::vector<double>& x, const std::vector<double>& y,
    const std::vector<double>& sx, const std::vector<double>& sy,
    double xmin, double xmax,
    const std::string& titulo = "Ajuste lineal.pdf") {

    TCanvas *c= new TCanvas("c_ajuste","Two simple graphs",800,600);
 
    gStyle->SetOptFit(111);
    c->SetGrid();

    const Int_t n = x.size();

    // AJUSTE LINEAL 

    TF1* fun1 = new TF1("fitFunc", "pol1", 1.4, 3.1);  // límites
    fun1->SetLineColor(kBlue);


    // GRAFICAS DE PUNTOS EXPERIMENTALES

    TGraphErrors *gr1 = new TGraphErrors(n, x.data(), y.data(), sx.data(), sy.data());
    gr1->SetMarkerColor(2);
    gr1->SetMarkerStyle(21);
    gr1->SetMarkerSize(1);
    gr1->SetTitle(titulo.c_str()); //Choose title for the graph
    gr1->GetYaxis()->SetTitle("V (mV)"); //Choose title for the axis
    gr1->GetXaxis()->SetTitle("I (A)"); 
    gr1->SetLineColor(4);    
   
    gr1->Draw("ap"); //"A" draw axes, "C" = draw a smooth line    

    gr1->Fit(fun1, "RQ");  // "R" -> respeta rango, "Q"-> no dibujes la linea
    fun1->Draw("c same");  
    c->Update();
    
    TPaveStats* stats = (TPaveStats*)gr1->GetListOfFunctions()->FindObject("stats");
    if (stats) {
        stats->SetX1NDC(0.55); // coordenadas normalizadas (0-1)
        stats->SetX2NDC(0.85);
        stats->SetY1NDC(0.15);
        stats->SetY2NDC(0.4);
        //stats->SetTextColor(0); // Opcional: color del texto del recuadro
    } else {
        std::cout << "Hola" << std::endl;
    }

    c->Modified();     
    c->Update();
    

    // LEYENDA: 

    TLegend *legend = new TLegend(0.15, 0.7, 0.45, 0.85);  // x1, y1, x2, y2 (NDC)
    legend -> SetFillColor(kWhite);
    legend->SetBorderSize(1);
    legend->SetTextSize(0.03);
    legend->AddEntry(gr1, "Puntos experimentales", "p");
    legend->AddEntry(fun1, "Ajuste lineal", "lp");
    legend->Draw();   
    
    c->SaveAs(titulo.c_str());


}


void Voltajes() {   
    // ---- GRÁFICOS CON BARRAS DE ERROR ---- //

std::vector<double_t> I1 = {1.593, 1.984, 2.486, 2.988};
std::vector<double_t> V1 = {0.4624, 0.5748, 0.7210, 0.8660};
std::vector<double_t> sV1(V1.size()), sI1(I1.size());
calcular_sV(V1, sV1);
calcular_sI(I1, sI1);
hacerGrafico(I1, V1, sI1, sV1, 1.4, 3.1, "Cruzado_1.pdf");

std::vector<double_t> I2 = {1.576, 1.979, 2.486, 2.986};
std::vector<double_t> V2 = {0.4570, 0.5733, 0.7200, 0.8648};
std::vector<double_t> sV2(V2.size()), sI2(I2.size());
calcular_sV(V2, sV2);
calcular_sI(I2, sI2);
hacerGrafico(I2, V2, sI2, sV2, 1.4, 3.1, "Cruzado_2.pdf");

std::vector<double_t> I3 = {1.575, 2.020, 2.490, 3.051};
std::vector<double_t> V3 = {0.0009, 0.0014, 0.0017, 0.0022};
std::vector<double_t> sV3(V3.size()), sI3(I3.size());
calcular_sV(V3, sV3);
calcular_sI(I3, sI3);
hacerGrafico(I3, V3, sI3, sV3, 1.4, 3.1, "Paralelo_1.pdf");

std::vector<double_t> I4 = {1.609, 1.970, 2.576, 2.963};
std::vector<double_t> V4 = {0.0001, 0.0002, 0.0009, 0.0013};
std::vector<double_t> sV4(V4.size()), sI4(I4.size());
calcular_sV(V4, sV4);
calcular_sI(I4, sI4);
hacerGrafico(I4, V4, sI4, sV4, 1.4, 3.1, "Paralelo_2.pdf");

std::vector<double_t> I5 = {1.592, 2.024, 2.534, 3.034};
std::vector<double_t> V5 = {0.4667, 0.5915, 0.7491, 0.8884};
std::vector<double_t> sV5(V5.size()), sI5(I5.size());
calcular_sV(V5, sV5);
calcular_sI(I5, sI5);
hacerGrafico(I5, V5, sI5, sV5, 1.4, 3.1, "Paralelo_3.pdf");

std::vector<double_t> I6 = {1.603, 2.020, 2.539, 3.070};
std::vector<double_t> V6 = {0.4700, 0.5908, 0.7418, 0.8969};
std::vector<double_t> sV6(V6.size()), sI6(I6.size());
calcular_sV(V6, sV6);
calcular_sI(I6, sI6);
hacerGrafico(I6, V6, sI6, sV6, 1.4, 3.1, "Paralelo_4.pdf");




}
