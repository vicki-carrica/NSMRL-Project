package project.NSMRL;
import java.util.Scanner;

public class main {

	public static void main(String[] args) {
		/*
		 * Program that codes for SET time 
		 * Version 1.0
		 */
		Scanner scan = new Scanner(System.in);
		int fitSurv;
		int unfitSurv;
		int candles;
		int canisters;
		double pressure;
		int aftVol;
		int flood;
		int percOx;
		double oConc; //concentration of oxygen? how do you find that? const?
		double coConc;
		double oSurvTime;
		double coSurvTime;
		double remainingHr; 
		double temp;
		double coSET;
		double oSET;
		double presATA;
		double vBreath;
		/*
		 * Define more variables here
		 */
		
		
		System.out.println("Welcome to the SET Calculator!");
		System.out.print("Input the number of fit (has use of both arms and can stand upright) survivors in the submarine: ");
		fitSurv = scan.nextInt();
		System.out.print("Input the number of unfit survivors in the submarine: ");
		unfitSurv = scan.nextInt();
		System.out.print("Input the number of chlorate candles in the submarine: ");
		candles = scan.nextInt();
		System.out.print("Input the number of ExtendAir kits in the submarine: ");
		canisters = scan.nextInt();
		System.out.print("Input the pressure (in fsw) in the submarine: "); //idk what unit pressure is in? fsw?
		pressure = scan.nextDouble();
		System.out.print("Input the percentage of the submarine compartment which is flooded: ");
		flood = scan.nextInt();
		System.out.print("Input the temperature (in F) in the submarine: ");
		temp = scan.nextDouble();
		System.out.print("Input the initial concentration (in %SEV) of oxygen: "); //ask
		oConc = scan.nextDouble();
		System.out.print("Input the initial concentration (in %SEV) of carbon dioxide: "); //ask 
		coConc = scan.nextDouble();
		oSurvTime = oxSurvTime(fitSurv, unfitSurv, candles, flood, oConc, temp);
		System.out.println("Approximate survival time (O2) if depth prevents escape: " + oSurvTime); //not SEV, survival time instead, dont know what the relationship is yet
		coSurvTime = coSurvTime(canisters, fitSurv, unfitSurv, coConc, flood, temp); //wrong value, by a lot
		System.out.println("Approximate survival time (CO2) if depth prevents escape: " + coSurvTime);
		remainingHr = hourBreathing(fitSurv, unfitSurv); //wrong value, by a lot
		System.out.println("Approximate remaining escaper hours of breathing after the start of escape: " + remainingHr);
		presATA = fswToATA(pressure);
		vBreath = calcVBreath(flood, fitSurv, presATA);
		System.out.println("Approximate Vbreath: " + vBreath);
		oSET = oStartEscapeTime(candles, fitSurv, unfitSurv, flood, oConc, vBreath, temp, remainingHr);
		System.out.println("Approximate O2 Start Escape Time: " + oSET);
		coSET = coStartEscapeTime(canisters, fitSurv, unfitSurv, flood, coConc, vBreath, temp, remainingHr);
		System.out.println("Approximate CO2 Start Escape Time: " + coSET);
		if (oSET < coSET) {
			System.out.println("Time to escape: " + oSET);
		} else {
			System.out.println("Time to escape: " + coSET);
		}
		
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
		double w = (double)survivors/2.0;
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
		double tCandles = ((double)cand*115.0)/(double)survivors;
		double numerator = ((concInt*volumeCompt)-(.13*volumeBreath))*(1/.7302)*(1/temperature)-breathingHr*.0838*(1/32);
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
		double numerator = ((.06*volumeBreath)-(concInt*volumeCompt))*(1/.7302)*(1/temperature)-breathingHr*.1*(1/44);
		double denominator = (double)survivors*.1*(1.0/44.0);
		double coWaitingTime = numerator/denominator;
		double coSET = coWaitingTime + tLiOH;
		return coSET;
	}
	

}
