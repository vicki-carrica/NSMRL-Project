import javax.swing.*;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.BorderFactory;
import java.awt.GridLayout;
import java.awt.BorderLayout;
import javax.swing.JButton;
import javax.swing.JLabel;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.Dimension;
import javax.swing.JTextField;

public class GUI implements ActionListener
{
    
    JLabel label; 
    JFrame frame;
    JPanel panel;
    JTextField textField;
    JLabel label2;
    JLabel label3;
    JLabel label4;
    JLabel label5;
    JButton button;
    JLabel spacer;
    SpinnerModel model;
    int count = 0;
    int fitSurv = 0;
    int unfitSurv = 0;
    int candles = 0;
    int canisters = 0;
    double pressure = 0.0;
    int flood = 0;
    double temp = 0.0;
    double oConc = 0.0;
    double coConc = 0.0;
    String in;
    
    public GUI()
    {
        frame = new JFrame();

        button = new JButton("Enter");
        textField  = new JTextField(10);
        model = new SpinnerNumberModel(0, 0, 1000, 1);
        button.addActionListener(this);
        button.setBounds(100,100,100,50);
        textField.setPreferredSize(new Dimension(200,40));
        label = new JLabel("Input the number of fit survivors (has use of both arms and can stand upright):");
        label2 = new JLabel("");
        label2.setBounds(100,150,100,50);
        label3 = new JLabel("");
        label4 = new JLabel("");
        label5 = new JLabel("");
        
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setPreferredSize(new Dimension(500, 500));
        frame.setTitle("Our GUI");
        JPanel panel = new JPanel();
        panel.add(label);
        panel.add(textField);
        panel.add(button);
        panel.add(label2);
        panel.add(label3);
        panel.add(label4);
        panel.add(label5);
        frame.add(panel);
        frame.pack();
        frame.setVisible(true);
    }
    
    public static void main(String[] args)
    {
        new GUI();
    }
    
    @Override
    public void actionPerformed (ActionEvent e){
        
        count++;
        in = textField.getText();
        if (count==1){
            fitSurv = Integer.parseInt(in);
            label2.setText("Fit survivors: "+fitSurv);
            label.setText("Input the number of unfit survivors:");
        } else if (count == 2){
            unfitSurv = Integer.parseInt(in);
            label2.setText("Unfit survivors: "+unfitSurv);
            label.setText("Input the number of chlorate candles:");
        } else if (count == 3){
            candles = Integer.parseInt(in);
            label2.setText("Chlorate candles: "+candles);
            label.setText("Input the number of ExtendAir kits:");
        } else if (count == 4){
            canisters = Integer.parseInt(in);
            label2.setText("ExtendAir kits: "+canisters);
            label.setText("Input the pressure (in fsw):");
        } else if (count == 5){
            pressure = Double.parseDouble(in);
            label2.setText("Pressure: "+pressure);
            label.setText("Input the percentage of the compartment that is flooded:");
        } else if (count == 6){
            flood = Integer.parseInt(in);
            label2.setText("Percent flooded: "+flood);
            label.setText("Input the temperature (in Fahrenheit):");
        } else if (count == 7){
            temp = Double.parseDouble(in);
            label2.setText("Temperature: "+temp);
            label.setText("Input the initial concentration (in %SEV) of oxygen:");
        }else if (count == 8){
            oConc = Double.parseDouble(in);
            button.setText("Calculate");
            label2.setText("Oxygen concentration: "+oConc);
            label.setText("Input the initial concentration (in %SEV) of carbon dioxide:");
        } else if (count==9){
            coConc = Double.parseDouble(in);
            label2.setText("Carbon dioxide concentration: "+coConc);
            double oSurvTime = oxSurvTime(fitSurv, unfitSurv, candles, flood, oConc, temp);
            label2.setText("Oxygen survival time: " + oSurvTime + " hours");
            double coSurvTime = coSurvTime(canisters, fitSurv, unfitSurv, coConc, flood, temp);
            label3.setText("Carbon dioxide survival time: " + coSurvTime + " hours");
            double remainingHr = hourBreathing(fitSurv, unfitSurv);
            double presATA = fswToATA(pressure);
            double vBreath = calcVBreath(flood, fitSurv, presATA);
            double oSET = oStartEscapeTime(candles, fitSurv, unfitSurv, flood, oConc, vBreath, temp, remainingHr);
            label4.setText("Oxygen Start Escape Time: " + oSET + " hours");
            double coSET = coStartEscapeTime(canisters, fitSurv, unfitSurv, flood, coConc, vBreath, temp, remainingHr);
            label5.setText("Carbon dioxide Start Escape Time: " + coSET + " hours");
        }else {
            label.setText("Start Escape Times:");
        }
        textField.setText("");
    }
    
    static double oxSurvTime(int fitSurv, int unfitSurv, int candles, int flood, double oConc, double temp) { //is temp needed?
        /*
         * Function calculates approximate survival time based on oxygen if depth prevents escape
         */
        int fit = fitSurv;
        int unfit = unfitSurv;
        int cand = candles;
        int percentFlood = flood;
        double oxygenConcentration = oConc/100.0;
        double temperature = temp + 459.67;
        int survivors = fit + unfit; //ask if the calculations want total survivors or fit?
        //volume calculation:
        double volumeCompt = (100-percentFlood)*62800/100;
        //candle time calculation:
        int candleSCF = cand * 115; //unit: SCF
        int survivorSCF = survivors; //unit: SCF/hr
        double tOCandles = (double)candleSCF/(double)survivorSCF; //unit: hrs
        //O2 time calculation:
        double numerator = (1.0/.7302)*volumeCompt*(oxygenConcentration-0.13)*(1.0/temperature);
        double denominator = (survivors*.0838)/32;
        double tOThirteen = numerator/denominator;
        //total survival time calculation
        double OSurvivalTime = tOCandles + tOThirteen;
        
        return OSurvivalTime;
    }
    static double coSurvTime(int canisters, int fitSurv, int unfitSurv, double coConc, int flood, double temp) {
	/*
	 * Function calculates approximate survival time based on carbon dioxide if depth prevents escape
	 */
	int fit = fitSurv;
	int unfit = unfitSurv;
	int cani = canisters;
	int percentFlood = flood;
	double coConcentration = coConc/100.0;
	double temperature = temp + 459.67;
	double volumeCompt = (100-percentFlood)*62800/100;
	int survivors = fit + unfit;
	double tLiOH = (cani*73)/survivors;
	double numerator = (1.0/.7302)*volumeCompt*(.06 - coConcentration)*(1.0/temperature);
	double denominator = (survivors * 0.1)/44;
	double tCO = numerator/denominator;
	
	double coSurvivalTime = tLiOH + tCO;
	return coSurvivalTime;
    }
    static double hourBreathing(int fitSurv, int unfitSurv) {
        /*
         * Function calculates the total remaining escaper hours of breathing after the start of escape 
         */
        int fit = fitSurv;
        int unfit = unfitSurv;
        int survivors = fit + unfit;
        double w = (double)fit/2.0;
        int escapeCycles = (int) Math.round(w);
        double escaperHr = escapeCycles*.25*(fit - (2*(escapeCycles + 1)/2));
        double nonEscaperHr = (survivors-fit)*fit/(1/.25 * 2);
        double g = escaperHr + nonEscaperHr;
        return g;
    }
    static double calcVBreath(int flood, int fitSurv, double presATA) {
        /*
         * Calculates the volume (Vbreath) in the equations
         */
        int percentFlooded = flood;
        int fit = fitSurv;
        double pressure = presATA;
        double vCompt = (100-percentFlooded)* pressure* 62800/100; //this equation is different for vcompt than before
        double vBreath = vCompt - 214 - (fit*53.5);
        return vBreath;
    }
    static double fswToATA(double pressure) {
        /*
         * Converts pressure from fsw to ATA
         */
        double fsw = pressure;
        double ata = (fsw+33)/33;
        return ata;
    }
    static double oStartEscapeTime(int candles, int fitSurv, int unfitSurv, int flood, double oConc, double vBreath, double temp, double g) {
        /*
         * Function that calculates the start escape time based on the O2 
         */
        int fit = fitSurv;
        int unfit = unfitSurv;
        int cand = candles;
        int percentFlood = flood;
        double concInt = oConc/100.0;
        double volumeBreath = vBreath;
        double breathingHr = g;
        double temperature = temp + 459.67;
        double volumeCompt = (100-percentFlood)*62800/100;
        int survivors = fit + unfit;
        double tCandles = ((double)cand*115.0 - breathingHr)/(double)survivors;
        double numerator1 = ((concInt*volumeCompt)-(.13*volumeBreath))*(1/.7302)*(1/temperature);
        double numerator2 = breathingHr*.0838*(1/32.0);
        double numerator = numerator1-numerator2;
        double denominator = (double)survivors*.0838*(1/32.0);
        double oWaitTime = numerator/denominator;
        double oSET = oWaitTime+tCandles;
        return oSET;
    }
    static double coStartEscapeTime(int canisters, int fitSurv, int unfitSurv, int flood, double coConc, double vBreath, double temp, double g) {
        /*
         * Function that calculates the start escape time based on the CO2 
         */
        int fit = fitSurv;
        int unfit = unfitSurv;
        int cani = canisters;
        int percentFlood = flood;
        double concInt = coConc/100.0;
        double volumeBreath = vBreath;
        double breathingHr = g;
        double temperature = temp + 459.67;
        double volumeCompt = (100-percentFlood)*62800/100;
        int survivors = fit + unfit;
        double tLiOH = (cani*73)/survivors;
        double numerator = ((.06*volumeBreath)-(concInt*volumeCompt))*(1/.7302)*(1/temperature)-breathingHr*.1*(1/44.0);
        double denominator = (double)survivors*.1*(1.0/44.0);
        double coWaitingTime = numerator/denominator;
        double coSET = coWaitingTime + tLiOH;
        return coSET;
    }
}
