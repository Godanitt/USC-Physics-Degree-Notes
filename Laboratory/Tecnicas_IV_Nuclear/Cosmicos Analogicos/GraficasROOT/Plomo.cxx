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

int Plomo() {
    const char* filename = "PlomoCeltia.csv";

    std::ifstream infile(filename);
    if (!infile.is_open()) {
        std::cerr << "No se pudo abrir el archivo: " << filename << std::endl;
        return 1;
    }

    std::string linea;
    std::getline(infile, linea); // saltar cabecera

    std::vector<double> x, sx, y, sy;

    while (std::getline(infile, linea)) {
        std::stringstream ss(linea);
        std::string campo;
        std::vector<double> fila;

        while (std::getline(ss, campo, ',')) {
            fila.push_back(std::stod(campo));
        }

        if (fila.size() == 4) {
            x.push_back(fila[0]);
            sx.push_back(fila[1]);
            y.push_back(fila[2]);
            sy.push_back(fila[3]);
        }
    }

    int N = x.size();

    TGraphErrors* gr = new TGraphErrors(N);
    for (int i = 0; i < N; ++i) {
        gr->SetPoint(i, x[i], y[i]);
        gr->SetPointError(i, sx[i], sy[i]);
    }

    //gr->SetTitle("Ajuste exponencial;V;n12")
    SetEstiloPublicacion();
    
    gr->SetMarkerStyle(20);
    gr->SetMarkerColor(kBlue + 1);
    gr->SetLineColor(kBlue - 10);
    gr->SetMarkerSize(1.25);  // Tamaño del punto (1.0 es el valor por defecto)
    gr->SetLineWidth(2);         // Grosor de barras de error
    gr->SetLineColor(kBlue);   // Color de las barras (por ejemplo, negro)
    
    TCanvas* c1 = new TCanvas("c1", "Regresion Exponencial", 800, 600);
    gStyle->SetOptFit(1);
    gr->Draw("AP");

    double xmin = *std::min_element(x.begin(), x.end());
    double xmax = *std::max_element(x.begin(), x.end());

    // Ajuste exponencial f(x) = a * exp(bx)
    TF1* fexp1 = new TF1("fexp1", "[0]*exp(-[1]*x)", xmin, xmax);
    fexp1->SetParameters(1, 0.1);
    fexp1->SetLineColor(kRed + 1);
    fexp1->SetLineWidth(2);
    gr->Fit(fexp1, "R");
    double a = fexp1->GetParameter(0);
    double b = fexp1->GetParameter(1);
    double ea = fexp1->GetParError(0);
    double eb = fexp1->GetParError(1);
    double chi2 = fexp1->GetChisquare();
    int ndf = fexp1->GetNDF();
    
    gStyle->SetOptFit(0);  // evita que se cree automáticamente
    gPad->Update(); // actualiza el canvas y crea el objeto stats si existe
    TPaveStats* stats = (TPaveStats*)gr->GetListOfFunctions()->FindObject("stats");
    if (stats) stats->Delete();  // borra el recuadro
    


    TPaveText *fitbox = new TPaveText(0.69, 0.65, 0.97, 0.85, "NDC");  // posición en el canvas
    fitbox->SetTextAlign(12);
    fitbox->SetTextFont(42);
    fitbox->SetTextSize(0.03);
    fitbox->SetFillColor(kWhite);
    fitbox->SetBorderSize(1);

    fitbox->AddText("Mejor Ajuste:");
    //fitbox->AddText("f(x) = a e^{bx}");
    fitbox->AddText(Form("a = %.3g #pm %.2g", a, ea));
    fitbox->AddText(Form("b = %.3g #pm %.2g", b, eb));
    fitbox->AddText(Form("#chi^{2}/ndf = %.2f / %d", chi2, ndf));

    fitbox->SetFillColor(19);
    fitbox->Draw("same");
    
    gr->GetXaxis()->SetTitle("x [mm]");
    gr->GetYaxis()->SetTitle("n_{r} [1/s]");
    

    // Leyenda actualizada
    TLegend *legend = new TLegend(0.60, 0.85, 0.97, 0.97);
    legend->SetFillColor(kWhite);
    legend->SetBorderSize(1);
    legend->SetTextSize(0.03);
    legend->SetFillColor(19);
    legend->AddEntry(gr, "Puntos experimentales", "p");
    legend->AddEntry(fexp1, "Ajuste: a e^{-b x}", "l");
    legend->Draw();

    gr->GetXaxis()->SetLimits(-2, 1000);
    c1->SetLeftMargin(0.12);  // margen izquierdo ampliado
    c1->SetRightMargin(0.03);   // achica el margen derecho
    c1->SetTopMargin(0.03);     // más apretado arriba

    c1->Modified();
    c1->Update();
    c1->SaveAs("../Graficas/PlomoCeltia.pdf");

    std::cout << "Gráfico guardado como GraficoU.pdf" << std::endl;
    return 0;
}
