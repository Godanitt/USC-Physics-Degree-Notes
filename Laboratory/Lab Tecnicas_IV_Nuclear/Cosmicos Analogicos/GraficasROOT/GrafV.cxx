#include <TGraphErrors.h>
#include <TF1.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TStyle.h>
#include <TPaveStats.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <algorithm>
#include <TAxis.h>

void SetEstiloPublicacion() {
    gStyle->SetOptStat(0);             // Oculta el recuadro de estadísticas (media, RMS, etc.)
    gStyle->SetOptTitle(0);            // Oculta el título automático del gráfico (puedes usar uno manual)

    gStyle->SetTitleFont(42, "XYZ");   // Fuente moderna (Helvetica-like) para títulos de ejes
    gStyle->SetLabelFont(42, "XYZ");   // Fuente moderna para las etiquetas (números) de los ejes

    gStyle->SetTitleSize(0.05, "XYZ"); // Tamaño del título del eje (más grande que etiquetas)
    gStyle->SetLabelSize(0.045, "XYZ");// Tamaño de las etiquetas del eje (valores numéricos)

    gStyle->SetFrameLineWidth(1.3);      // Grosor del marco que rodea la gráfica
    gStyle->SetLineWidth(2.3);           // Grosor por defecto para líneas (funciones, bordes)
    gStyle->SetHistLineWidth(1.3);       // Grosor de líneas de histogramas (si los usas)
    gStyle->SetTickLength(0.03, "X");  // Aumenta tamaño de los ticks en X
    gStyle->SetTickLength(0.03, "Y");  // Aumenta tamaño de los ticks en Y
    gStyle->SetEndErrorSize(8);  // tamaño del "sombrerito" del error bar

}

int GrafV() {
    const char* filename = "PlateuV.csv";

    TCanvas* c1 = new TCanvas("c1", "Plateu", 800, 600);

    std::ifstream infile(filename);
    if (!infile.is_open()) {
        std::cerr << "No se pudo abrir el archivo: " << filename << std::endl;
        return 1;
    }

    std::string linea;
    std::getline(infile, linea); // saltar cabecera

    std::vector<double> x, sx, y1, sy1,y2,sy2,y3,sy3;

    while (std::getline(infile, linea)) {
        std::stringstream ss(linea);
        std::string campo;
        std::vector<double> fila;

        while (std::getline(ss, campo, ',')) {
            fila.push_back(std::stod(campo));
        }

        if (fila.size() == 8) {
            x.push_back(fila[0]);
            sx.push_back(fila[1]);
            y1.push_back(fila[2]);
            sy1.push_back(fila[3]);
            y2.push_back(fila[4]);
            sy2.push_back(fila[5]);
            y3.push_back(fila[6]);
            sy3.push_back(fila[7]);
        }
    }

    int N = x.size();
    TGraphErrors* gr = new TGraphErrors(N);
    for (int i = 0; i < N; ++i) {
        gr->SetPoint(i, x[i], y1[i]);
        gr->SetPointError(i, sx[i], sy1[i]);
    }

    //gr->SetTitle("Ajuste exponencial;V;n12")
    SetEstiloPublicacion();
    
    gr->SetMarkerStyle(20);
    gr->SetMarkerColor(kBlue + 1);
    gr->SetLineColor(kBlue - 10);
    gr->SetMarkerSize(1.25);  // Tamaño del punto (1.0 es el valor por defecto)
    gr->SetLineWidth(2);         // Grosor de barras de error
    gr->SetLineColor(kBlue);   // Color de las barras (por ejemplo, negro)


    gr->Draw("AP");
    
    ////////////////////////////

    TGraphErrors* gr1 = new TGraphErrors(N);
    for (int i = 0; i < N; ++i) {
        gr1->SetPoint(i, x[i], y2[i]);
        gr1->SetPointError(i, sx[i], sy2[i]);
    }

    //gr->SetTitle("Ajuste exponencial;V;n12")
    SetEstiloPublicacion();
    
    gr1->SetMarkerStyle(20);
    gr1->SetMarkerColor(kGreen  + 1);
    gr1->SetLineColor(kGreen - 10);
    gr1->SetMarkerSize(1.25);  // Tamaño del punto (1.0 es el valor por defecto)
    gr1->SetLineColor(kGreen);   // Color de las barras (por ejemplo, negro)
    gr1->SetLineWidth(2);         // Grosor de barras de error


    gr1->Draw("P same");
    /////////////////////////////////////

    TGraphErrors* gr2 = new TGraphErrors(N);
    for (int i = 0; i < N; ++i) {
        gr2->SetPoint(i, x[i], y3[i]);
        gr2->SetPointError(i, sx[i], sy3[i]);
    }

    //gr->SetTitle("Ajuste exponencial;V;n12")
    SetEstiloPublicacion();
    
    gr2->SetMarkerStyle(20);
    gr2->SetMarkerColor(kRed + 1);
    gr2->SetLineColor(kRed - 10);
    gr2->SetMarkerSize(1.25);  // Tamaño del punto (1.0 es el valor por defecto)
    gr2->SetLineWidth(2);         // Grosor de barras de error
    gr2->SetLineColor(kRed);   // Color de las barras (por ejemplo, negro)


    gr2->Draw("P same");
    /////////////////////////////7

    double xmin = *std::min_element(x.begin(), x.end());
    double xmax = *std::max_element(x.begin(), x.end());

  //  // Ajuste exponencial f(x) = a * exp(bx)
  //  TF1* fexp1 = new TF1("fexp1", "[0]*exp([1]*x)", xmin, xmax);
  //  fexp1->SetParameters(1, 0.1);
  //  fexp1->SetLineColor(kRed + 1);
  //  fexp1->SetLineWidth(2);
  //  gr->Fit(fexp1, "R");
  //  double a = fexp1->GetParameter(0);
  //  double b = fexp1->GetParameter(1);
  //  double ea = fexp1->GetParError(0);
  //  double eb = fexp1->GetParError(1);
  //  double chi2 = fexp1->GetChisquare();
  //  int ndf = fexp1->GetNDF();
  //  
   // gStyle->SetOptFit(0);  // evita que se cree automáticamente
   // gPad->Update(); // actualiza el canvas y crea el objeto stats si existe
   // TPaveStats* stats = (TPaveStats*)gr->GetListOfFunctions()->FindObject("stats");
   // if (stats) stats->Delete();  // borra el recuadro
    


   // TPaveText *fitbox = new TPaveText(0.2, 0.42, 0.40, 0.68, "NDC");  // posición en el canvas
   // fitbox->SetTextAlign(12);
  // fitbox->SetTextFont(42);
  //  fitbox->SetTextSize(0.03);
   // fitbox->SetFillColor(kWhite);
  //  fitbox->SetBorderSize(1);

    //fitbox->AddText("Mejor Ajuste:");
    //fitbox->AddText("f(x) = a e^{bx}");
    //fitbox->AddText(Form("a = %.3g #pm %.2g", a, ea));
    //fitbox->AddText(Form("b = %.3g #pm %.2g", b, eb));
    //fitbox->AddText(Form("#chi^{2}/ndf = %.2f / %d", chi2, ndf));

   // fitbox->SetFillColor(19);
  //  fitbox->Draw("same");
    
    gr->GetXaxis()->SetTitle("V_{1} [kV]");
    gr->GetYaxis()->SetTitle("n [1/s]");

    double ymin = *std::min_element(y2.begin(), y2.end())-1;
    double ymax = *std::max_element(y1.begin(), y1.end())+1;

    gr->GetXaxis()->SetTitle("V_{1} [kV]");
    gr->GetYaxis()->SetTitle("n [1/s]");
    gr->GetYaxis()->SetRangeUser(ymin, ymax);

    // Leyenda actualizada
    TLegend *legend = new TLegend(0.2, 0.72, 0.5, 0.85);
    legend->SetFillColor(kWhite);
    legend->SetBorderSize(1);
    legend->SetTextSize(0.03);
    legend->SetFillColor(19);
    legend->AddEntry(gr, "n_{12}", "p");
    legend->AddEntry(gr1, "n_{acc}", "p");
    legend->AddEntry(gr2, "n_{r}", "p");
    //legend->AddEntry(fexp1, "Ajuste: a e^{b x}", "l");
    legend->Draw();

    c1->Modified();
    c1->Update();
    c1->SaveAs("GraficoV.pdf");

    std::cout << "Gráfico guardado como GraficoV.pdf" << std::endl;
    return 0;
}
