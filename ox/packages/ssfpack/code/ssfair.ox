#include <oxstd.h>
#import <maximize>
#include <packages/ssfpack/ssfpack.h>

static decl fconc = TRUE;
#include "airlincl.ox"

main()
{
    decl vp, ir, dlik, dvar, my, mdy;

    my = log(loadmat("Airline.mat"));	// log(airline)
	mdy = diff0(my, 1)[1:][];			// Dlog(airline)
    s_mY = diff0(mdy, 12)[12:][]';	  	// D12D(log(airline))
	s_cT = columns(s_mY);				// no of observations

	vp = <0.5;0.5>;						// starting values
	if (!fconc)
	{
	 vp |= 0.0;							// estimate sigma too
	 SetAirlineParameters(vp);			// map parameters 
	 ArmaLogLik(s_mY, &dlik, &dvar);	// evaluate
	 vp[sizerc(vp)-1] = 0.5 * log(dvar);// update log(sigma)
	}

    MaxControl(-1, 5, 1);				// get some output
	MaxControlEps(1e-7, 1e-5);			// tight cvg criteria
    ir = MaxBFGS(Likelihood, &vp, &dlik, 0, TRUE);
    
    println("\n", MaxConvergenceMsg(ir),
          " using numerical derivatives",
          "\nLog-likelihood = ", "%.8g", dlik * s_cT,
		  "; variance = ", sqr(s_dSigma),
		  "; n = ", s_cT, "; dVar = ", s_dVar);
	print("parameters with standard errors:",
		"%cf", {"%12.5g", "  (%7.5f)"}, vp ~ ArmaStderr(vp));
}
