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

void Angulos_hacer(const char* filename, const char* pdf) {

    std::ifstream infile(filename);
    if (!infile.is_open()) {
        std::cerr << "No se pudo abrir el archivo: " << filename << std::endl;
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
    
    TCanvas* c1 = new TCanvas("c1", "Regresion Exponencial prueba", 800, 600);
    gStyle->SetOptFit(1);
    gr->Draw("AP");

    double xmin = *std::min_element(x.begin(), x.end());
    double xmax = *std::max_element(x.begin(), x.end());

    // Ajuste coseno f(x) = a * cos2(bx)
    TF1* fexp1 = new TF1("fexp1", "[0]+[1]*(cos(x*TMath::Pi()/180))**2", xmin, xmax);
    fexp1->SetParameters(0.3, 1.2);
    fexp1->SetLineColor(kRed + 1);
    fexp1->SetLineWidth(2);
    gr->Fit(fexp1, "R");
    double a = fexp1->GetParameter(0);
    double ea = fexp1->GetParError(0);
    double b = fexp1->GetParameter(1);
    double eb = fexp1->GetParError(1);
    double chi2 = fexp1->GetChisquare();
    int ndf = fexp1->GetNDF();

    // Ajuste coseno f(x) = a * cos^n(bx)

    TF1* fexp2 = new TF1("fexp2", "[0] + [1]*(4*pow(cos(x*TMath::Pi()/180), 2)+pow(cos(x*TMath::Pi()/180), [2]))", xmin, xmax);

    fexp2->SetParameters(0.3, 1.2, 2);
    fexp2->SetLineColor(kYellow + 2);
    fexp2->SetLineWidth(2);
    gr->Fit(fexp2, "R+");
    double a2 = fexp2->GetParameter(0);
    double ea2 = fexp2->GetParError(0);
    double b2 = fexp2->GetParameter(1);
    double eb2 = fexp2->GetParError(1);
    double c2 = fexp2->GetParameter(2);
    double ec2 = fexp2->GetParError(2);
    double chi22 = fexp2->GetChisquare();
    int ndf2 = fexp2->GetNDF();
    
    gStyle->SetOptFit(0);  // evita que se cree automáticamente
    gPad->Update(); // actualiza el canvas y crea el objeto stats si existe
    TPaveStats* stats = (TPaveStats*)gr->GetListOfFunctions()->FindObject("stats");
    if (stats) stats->Delete();  // borra el recuadro

    c1->Modified();
    c1->Update();


    /////// PRIMERA CAJA ///////////////

    TPaveText *fitbox = new TPaveText(0.74, 0.72, 0.97, 0.97, "NDC");  // posición en el canvas
    fitbox->SetTextAlign(12);
    fitbox->SetTextFont(42);
    fitbox->SetTextSize(0.03);
    fitbox->SetFillColor(kWhite);
    fitbox->SetBorderSize(1);

    fitbox->AddText("Ajuste a + b cos^{2} (#theta):");
    //fitbox->AddText("f(x) = a e^{bx}");
    fitbox->AddText(Form("a = %.3g #pm %.2g", a, ea));
    fitbox->AddText(Form("b = %.3g #pm %.2g", b, eb));
    fitbox->AddText(Form("#chi^{2}/ndf = %.2f / %d", chi2, ndf));

    fitbox->SetFillColor(19);
    fitbox->Draw("same");

    /////// SEGUNDA CAJA ///////////////

    TPaveText *fitbox2 = new TPaveText(0.74, 0.47, 0.97, 0.72, "NDC");  // posición en el canvas
    fitbox2->SetTextAlign(12);
    fitbox2->SetTextFont(42);
    fitbox2->SetTextSize(0.03);
    fitbox2->SetFillColor(kWhite);
    fitbox2->SetBorderSize(1);

    fitbox2->AddText("Ajuste a  + b cos^{n} (#theta):");
    //fitbox->AddText("f(x) = a e^{bx}");
    fitbox2->AddText(Form("a = %.3g #pm %.2g", a2, ea2));
    fitbox2->AddText(Form("b = %.3g #pm %.2g", b2, eb2));
    fitbox2->AddText(Form("n = %.3g #pm %.2g", c2, ec2));
    fitbox2->AddText(Form("#chi^{2}/ndf = %.2f / %d", chi22, ndf2));

    fitbox2->SetFillColor(19);
    fitbox2->Draw("same");

    ////////////////////////////////
    
    

    // Leyenda actualizada
    TLegend *legend = new TLegend(0.30, 0.80, 0.74, 0.97);
    legend->SetFillColor(kWhite);
    legend->SetBorderSize(1);
    legend->SetTextSize(0.03);
    legend->SetFillColor(19);
    legend->AddEntry(gr, "Puntos experimentales", "p");
    legend->AddEntry(fexp1, "Ajuste:a + b cos^{2}(#theta)", "l");
    legend->AddEntry(fexp2, "Ajuste:a + b (4 cos^{2}(#theta)+cos^{n}(#theta))", "l");
    legend->Draw();

    c1->SetLeftMargin(0.12);  // margen izquierdo ampliado
    c1->SetRightMargin(0.03);   // achica el margen derecho
    c1->SetTopMargin(0.03);     // más apretado arriba

    c1->Modified();
    c1->Update();
    c1->SaveAs(pdf);

    std::cout << "Gráfico guardado como GraficoU.pdf" << std::endl;
}

int Angulos_2() {
    const char* archivo1="Angulos.csv";
    const char* pdf1="../Graficas/Angulos_3.pdf";
    Angulos_hacer( archivo1,pdf1);

    const char* archivo2="Angulos_2.csv";
    const char* pdf2="../Graficas/Angulos_4.pdf";
    Angulos_hacer(archivo2,pdf2);

    return 0;
}