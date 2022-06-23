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
		double presFSW;
		int aftVol;
		int flood;
		int percOx;
		double conc; //concentration? how do you find that? const?
		double oSurvTime;
		double remainingHr; 
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
		System.out.print("Input the pressure (in fsw) in the submarine: ");
		presFSW = scan.nextDouble();
		System.out.print("Input the percentage of the submarine compartment which is flooded: ");
		flood = scan.nextInt();
		System.out.print("Input the initial concentration of oxygen: "); //ask jeff
		conc = scan.nextDouble();
		oSurvTime = oxSurvTime(fitSurv, unfitSurv, candles, presFSW, flood, conc);
		System.out.println("Approximate survival time (O2) if depth prevents escape: " + oSurvTime); //not SEV, survival time instead, dont know what the relationship is yet
		
		

	}
	
	static double oxSurvTime(int fitSurv, int unfitSurv, int candles, double presFSW, int flood, double conc) {
		/*
		 * Function calculates approximate survival time based on oxygen if depth prevents escape
		 */
		int fit = fitSurv;
		int unfit = unfitSurv;
		int cand = candles;
		double pres = presFSW;
		int percentFlood = flood;
		double oxygenConcentration = conc;
		int survivors = fit + unfit; //ask if the calculations want total survivors or fit?
		//volume calculation:
		double volumeCompt = (100-percentFlood)*79800/100;
		//candle time calculation:
		int candleSCF = cand * 115; //unit: SCF
		int survivorSCF = survivors; //unit: SCF/hr
		double tOCandles = (double)candleSCF/(double)survivorSCF; //unit: hrs
		//O2 time calculation:
		double numerator = (1.0/.7302)*volumeCompt*(oxygenConcentration-0.13);
		double denominator = .0838/32;
		double tOThirteen = numerator/denominator;
		//total survival time calculation
		double OSurvivalTime = tOCandles - tOThirteen;
		
		return OSurvivalTime;
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

}
