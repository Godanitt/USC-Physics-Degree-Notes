#include <TH1F.h>
#include <TF1.h>
#include <TCanvas.h>
#include <TStyle.h>
#include <TLegend.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <TPaveText.h>

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

void SetOtros(TH1F* hist, double xmax2) {
    
    int altura = hist->GetEntries();  // estimador para la altura
    double m = hist->GetMean();       // estimador para lambda
    
    auto poisson_suave = [](double *x, double *par) {
        double mu = par[0];
        double A = par[1];
        double xx = x[0];
        // ¡No redondeamos!
        // Gamma(x+1) es factorial(x) para reales => Poisson continua
        return A * TMath::Power(mu, xx) * exp(-mu) / TMath::Gamma(xx + 1);
    };
    
    TF1 *f_poisson = new TF1("poisson", poisson_suave, 0, xmax2, 2);
    

    f_poisson->SetParameter(1, altura);
    f_poisson->FixParameter(1, altura);
    f_poisson->SetParameter(0, m);
    f_poisson->SetParName(0, "mu");
    
    f_poisson->SetNpx(1000);
    f_poisson->SetLineColor(kYellow + 1);
    f_poisson->SetLineWidth(3);
    hist->Fit(f_poisson, "R+");
    
    // Ajuste Gaussiano (con altura calculada dentro de la lambda)
    // Captura [=] para acceder a "altura" desde fuera

    auto gauss_func = [=](double *x, double *par) {
        double mu = par[0];
        double sigma = sqrt(mu);
        double A = altura / (sqrt(2 * TMath::Pi() * mu));
        double arg = (x[0] - mu) / sigma;
        return A * exp(-0.5 * arg * arg);
    };
    
    TF1 *f_gauss = new TF1("f_gauss", gauss_func, 0, xmax2, 1);
    
    
    f_gauss->SetParameter(0, m);
    f_gauss->SetParName(0, "mu");
    
    f_gauss->SetNpx(1000);
    f_gauss->SetLineColor(kRed);
    f_gauss->SetLineWidth(3);
    hist->Fit(f_gauss, "R+");
    ///////////////////////////////////////////////////////////////////////////
    // Para poner las entradas en leyenda

    int entries = hist->GetEntries();
    double mean = hist->GetMean();

    TString label = Form("Entries = %d, Mean = %.2f", entries, mean);

    ///////////////////////////////////////////////////////////////////////////
    // Legenda

    TLegend *legend = new TLegend(0.60, 0.77, 0.97, 0.97);
    legend->SetFillColor(kWhite);
    legend->SetBorderSize(1);
    legend->SetTextSize(0.03);
    legend->SetFillColor(19);
    legend->AddEntry(hist, label, "f");
    legend->AddEntry(f_gauss, "Ajuste Gaussiano", "l");
    legend->AddEntry(f_poisson, "Ajuste Poisson", "l");
    legend->Draw();

    // Caja con la chi cuadrada gaussiana

    TPaveText *fitbox1 = new TPaveText(0.69, 0.57, 0.97, 0.77, "NDC");  // posición en el canvas
    fitbox1->SetTextAlign(12);
    fitbox1->SetTextFont(42);
    fitbox1->SetTextSize(0.03);
    fitbox1->SetFillColor(kWhite);
    fitbox1->SetBorderSize(1);

    fitbox1->AddText("Ajuste Gaussiano:");
    //fitbox->AddText("f(x) = a e^{bx}");
    double a = f_gauss->GetParameter(0);
    double ea = f_gauss->GetParError(0);
    double chi2 = f_gauss->GetChisquare();
    int ndf = f_gauss->GetNDF();
    
    fitbox1->AddText(Form("#mu = %.4g #pm %.2g", a, ea));
    fitbox1->AddText(Form("#chi^{2}/ndf = %.2f / %d", chi2, ndf));

    fitbox1->SetFillColor(19);
    fitbox1->Draw("same");

    ///////////////////////////////////////////////////////////////////////////
    // Caja con la chi2 de poisson

    TPaveText *fitbox2 = new TPaveText(0.69, 0.37, 0.97, 0.57, "NDC");  // posición en el canvas
    fitbox2->SetTextAlign(12);
    fitbox2->SetTextFont(42);
    fitbox2->SetTextSize(0.03);
    fitbox2->SetFillColor(kWhite);
    fitbox2->SetBorderSize(1);

    fitbox2->AddText("Ajuste Poisson:");
    //fitbox->AddText("f(x) = a e^{bx}");
    double a2 = f_poisson->GetParameter(0);
    double ea2 = f_poisson->GetParError(0);
    double chi22 = f_poisson->GetChisquare();
    int ndf2 = f_poisson->GetNDF();
    
    fitbox2->AddText(Form("#mu = %.4g #pm %.2g", a2, ea2));
    fitbox2->AddText(Form("#chi^{2}/ndf = %.2f / %d", chi22, ndf2));

    fitbox2->SetFillColor(19);
    fitbox2->Draw("same");
    
    

}
// Función que crea y devuelve el histograma
TH1F *CrearHistogramaDesdeCSV(const char *filename, const char *histoname, const char *title,
                              int nbins, double xmin, double xmax)
{
    std::ifstream infile(filename);
    if (!infile.is_open())
    {
        std::cerr << "No se pudo abrir el archivo: " << filename << std::endl;
        return nullptr;
    }

    TH1F *hist = new TH1F(histoname, title, nbins, 0-0.5, xmax-0.5);

    hist->GetXaxis()->SetRangeUser(xmin, xmax);

    std::string linea;
    std::getline(infile, linea); // Saltar encabezado

    int bin_index = 1; // ROOT bins empiezan en
    
    while (std::getline(infile, linea))
    {
        std::stringstream ss(linea);
        std::string campo;
        int columna = 0;
        double frecuencia = 0;

        while (std::getline(ss, campo, ','))
        {
            if (columna == 2)
            { // Columna "Diferencia" ahora representa frecuencia
                try
                {
                    frecuencia = std::stod(campo);
                    hist->SetBinContent(bin_index, frecuencia);
                }
                catch (...)
                {
                    std::cerr << "Error al convertir: " << campo << std::endl;
                }
                break;
            }
            columna++;
        }
        bin_index++;
    
    }
    int total = 0;

    for (int i = 1; i <= hist->GetNbinsX(); ++i) {
        total += hist->GetBinContent(i);
    }
    
    hist->SetLineWidth(2); // puedes usar 3 o 4 si lo quieres más grueso
    hist->SetLineColor(kBlack); // opcional para cambiar color

    hist->SetEntries(total);
    hist->SetFillColorAlpha(kAzure -4, 0.35); // color + transparencia (0=transparente, 1=opaco)



    return hist;
}

void histo2(const char *archivo, const char *pdf,  int xmax1=15, double xmin=0, double xmax2=15) {

    const char *nombreHistograma = archivo;
    const char *titulo = "Histograma de Diferencia;Diferencia;Frecuencia";


    TH1F *hist = CrearHistogramaDesdeCSV(archivo, nombreHistograma, titulo, xmax1, xmin, xmax2);


    // Crear canvas y dibujar
    TCanvas *c1 = new TCanvas(pdf, "Histograma Diferencia", 800, 600);
    c1->SetLeftMargin(0.15);  // margen izquierdo ampliado
    SetEstiloPublicacion();
    hist->Draw();
    SetOtros(hist,xmax2);
    c1->SetRightMargin(0.03);   // achica el margen derecho
    c1->SetTopMargin(0.03);     // más apretado arriba
    
    c1->Modified();
    c1->Update();
    c1->SaveAs(pdf);

}

// Función principal
int Histo()
{

    const char *archivo1 = "Histo_1ms.csv";
    const char *pdf1 = "../Graficas/Histo_1ms.pdf";

    histo2(archivo1,pdf1,10,0,10);


    const char *archivo2 = "Histo_2ms.csv";
    const char *pdf2 = "../Graficas/Histo_2ms.pdf";

    histo2(archivo2,pdf2,12,0,12);


    const char *archivo3 = "Histo_5ms.csv";
    const char *pdf3 = "../Graficas/Histo_5ms.pdf";

    histo2(archivo3,pdf3,18,0,18);
    const char *archivo8 = "Histo_7ms.csv";
    const char *pdf8= "../Graficas/Histo_7ms.pdf";

    histo2(archivo8,pdf8,19,0,19);


    const char *archivo4 = "Histo_1s.csv";
    const char *pdf4 = "../Graficas/Histo_1s.pdf";

    histo2(archivo4,pdf4,20,0,20);


    const char *archivo5 = "Histo_2s.csv";
    const char *pdf5 = "../Graficas/Histo_2s.pdf";

    histo2(archivo5,pdf5,40,0,40);


    const char *archivo6 = "Histo_5s.csv";
    const char *pdf6 = "../Graficas/Histo_5s.pdf";

    histo2(archivo6 ,pdf6 ,80,10,80);


    const char *archivo7 = "Histo_10s.csv";
    const char *pdf7 = "../Graficas/Histo_10s.pdf";

    histo2(archivo7,pdf7,140,40,140);







    return 0;
}
