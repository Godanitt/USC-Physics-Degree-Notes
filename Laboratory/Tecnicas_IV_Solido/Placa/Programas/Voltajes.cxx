
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

// ---- FUNCIÓN ---- //
void hacerGrafico(const std::vector<double>& x, const std::vector<double>& y,
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
    
    TGraph *gr1 = new TGraph(n,x.data(),y.data()); 
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
    


    std::vector<double_t> I1 = {1.593,1.984,2.486,2.988};
    std::vector<double_t> V1 = {0.4624,0.5748,0.7210,0.8660};
    
    hacerGrafico(I1, V1, 1.4, 3.1, "Cruzado_1.pdf");

    std::vector<double_t> I2 = {1.576,1.979,2.486,2.986};
    std::vector<double_t> V2 = {0.4570,0.5733,0.7200,0.8648};
    
    hacerGrafico(I2, V2, 1.4, 3.1, "Cruzado_2.pdf");


    std::vector<double_t> V3 = {0.0009,0.0014,0.0017,0.0022};
    std::vector<double_t> I3 = {1.575,2.020,2.490,3.051};
    
    hacerGrafico(I3, V3, 1.4, 3.1, "Paralelo_1.pdf");


    std::vector<double_t> I4 = {1.609,1.970,2.576,2.963};
    std::vector<double_t> V4 = {0.0001,0.0002,0.0009,0.0013};
    
    hacerGrafico(I4, V4, 1.4, 3.1, "Paralelo_2.pdf");


    std::vector<double_t> I5 = {1.592,1.970,2.576,2.963};
    std::vector<double_t> V5 = {0.4667,0.5915,0.7491,0.8884};
    
    hacerGrafico(I5, V5, 1.4, 3.1, "Paralelo_3.pdf");


    std::vector<double_t> I6 = {1.603,2.020,2.539,3.070};
    std::vector<double_t> V6 = {0.4700,0.5908,0.7418,0.8969};
    
    hacerGrafico(I6, V6, 1.4, 3.1, "Paralelo_4.pdf");




}
