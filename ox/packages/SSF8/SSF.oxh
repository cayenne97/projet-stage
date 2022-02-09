#include <oxstd.oxh>
#include <oxfloat.oxh>
#import <maximize>
#include <packages/ssfpack/ssfpack.h>


class SSF
{                                    // constructor
	public:
	decl s_dVar, s_mPhi, s_mOmega, s_mSigma, s_mJPhi, s_vY, s_mX, s_cT, s_sModel;
	decl a_names_X;

	SSF();
	Likelihood(const vP, const pdLik, const pvSco, const pmHes);	
	Get_Info_Criteria_SSF(const LogL, const n, const q);
	MaxLik(const print_output, const IC);
	MaxLik_eval(const para);
	Smoothing();
	GetSeries();
}