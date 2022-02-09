#ifndef SSFPACK_BASIC_INCLUDED
#define SSFPACK_BASIC_INCLUDED

enum // structural model indexes for components
{
	CMP_LEVEL, CMP_SLOPE, CMP_TREND,
	CMP_SEAS_DUMMY, CMP_SEAS_TRIG, CMP_SEAS_HS, CMP_BWCYC,
    CMP_CYC_0, CMP_CYC_1, CMP_CYC_2, CMP_CYC_3, CMP_CYC_4,
    CMP_CYC_5, CMP_CYC_6, CMP_CYC_7, CMP_CYC_8, CMP_CYC_9, 
	CMP_AR1, CMP_AR2, CMP_IRREG,
	CMP_TOTAL
};

enum // type of state estimators
{
	ST_PRED,
	ST_SMO, ST_SIM,
	DS_SMO, DS_SIM,
	ST_FIL, DS_FIL,
	DS_SIM_EPS, DS_SIM_ETA
};

#define SSFPACK_BASIC

// administration functions 

extern "ssfpack,FnSsfVersion"
	SsfVersion();

extern "ssfpack,FnSsfAbout"
	SsfAbout();

extern "ssfpack,FnSsfWarning"
	SsfWarning(const iPrint);


// model in state space functions

extern "ssfpack,FnGetSsfStsm"
    GetSsfStsm(const mInfo, const pmPhi, const pmOmega, const pmSigma, ...);
		
extern "ssfpack,FnGetSsfArma"
    GetSsfArma(const mAr, const mMa, const dStDev, const pmPhi, const pmOmega, const pmSigma);

extern "ssfpack,FnGetSsfSarima"
    GetSsfSarima(const mD, const mAr, const mMa, const dStDev, const pmPhi, const pmOmega, const pmSigma);

extern "ssfpack,FnGetSsfReg"
    GetSsfReg(const mX, const pmPhi, const pmOmega, const pmSigma, const pmJ_Phi);

extern "ssfpack,FnAddSsfReg"
    AddSsfReg(const mX, const pmPhi, const pmOmega, const pmSigma, const pmJ_Phi);

extern "ssfpack,FnGetSsfSpline"
    GetSsfSpline(const q, const mDelta, const pmPhi, const pmOmega, ...);		
	
// Kalman filter functions

extern "ssfpack,FnKalmanFil"
	KalmanFil(const mY, const mTZ, const mHG, ...);
			   
extern "ssfpack,FnKalmanInit"
	KalmanInit(const mY, const mTZ, const mHG, ...);
			   
extern "ssfpack,FnKalmanFilEx"
	KalmanFilEx(const mInit, const mY, const mTZ, const mHG, ...);

extern "ssfpack,FnKalmanFilMeanEx"
	KalmanFilMeanEx(const mKFInfo, const mY, const mTZ, const mHG, ...);

// Kalman smoothing functions

extern "ssfpack,FnKalmanSmo"
	KalmanSmo(const mKFInfo, const mTZ, const mHG, ...);

extern "ssfpack,FnKalmanSmoEx"
	KalmanSmoEx(const mKFInfo, const mTZ, const mHG, ...);

extern "ssfpack,FnKalmanSmoMeanEx"
	KalmanSmoMeanEx(const mKFInfo, const mTZ, const mHG, ...);

extern "ssfpack,FnKalmanFilSmoMeanEx"
	KalmanFilSmoMeanEx(const mKFInfo, const mY, const mTZ, const mHG, ...);

// log likelihood functions

extern "ssfpack,FnSsfLik"
    SsfLik(const adLik, const adVar, const mY, const mTZ, const mHG, ...);

extern "ssfpack,FnSsfLikEx"
    SsfLikEx(const adLik, const adVar, const mY, ...);

extern "ssfpack,FnSsfLikMulti"
    SsfLikMulti(const adLik, const adVar, const iMulti, const mY, ...);

extern "ssfpack,FnSsfLikConc"
    SsfLikConc(const adLik, const adVar, const mY, const mTZ, const mHG, ...);

extern "ssfpack,FnSsfLikConcEx"
    SsfLikConcEx(const adLik, const adVar, const mY, const mTZ, const mHG, ...);

extern "ssfpack,FnSsfLikSco"
    SsfLikSco(const adLik, ...);
	
extern "ssfpack,FnSsfLikScoEx"
    SsfLikScoEx(const adLik, ...);

// ready to use functions

extern "ssfpack,FnSsfMomentEst"
    SsfMomentEst(const iSel, const mEst, const mY, const mTZ, const mHG, ...);

extern "ssfpack,FnSsfMomentEstEx"
    SsfMomentEstEx(const iSel, const mEst, const mY, const mTZ, const mHG, ...);

extern "ssfpack,FnSsfMomentEstMulti"
    SsfMomentEstMulti(const iMulti, const mEst, const mY, const mTZ, const mHG, ...);

extern "ssfpack,FnSsfCondDens"
    SsfCondDens(const iSel, const mY, const mTZ, const mHG, ...);

extern "ssfpack,FnSsfCondDensEx"
    SsfCondDensEx(const iSel, const mY, const mTZ, const mHG, ...);

extern "ssfpack,FnSsfForecast"
    SsfForecast(const mY, const mTZ, const mHG, const mIP, ...);

extern "ssfpack,FnSsfWeightsEx"
	SsfWeightsEx(const iSel, const iPos, const mKF, const mTZ, const mHG, ...);
	
extern "ssfpack,FnSsfSimObs"
	SsfSimObs(const mErr, const mTZ, const mHG, ...);

extern "ssfpack,FnSsfSimState"
	SsfSimState(const mErr, const mTZ, const mHG, ...);

extern "ssfpack,FnSsfBootstrap"
    SsfBootstrap(const mTime, const mKF, const mTZ, const mHG, ...);

extern "ssfpack,FnSsfFreqGain"
    SsfFreqGain(const iGrid, const mFreq);

extern "ssfpack,FnSsfSignalEst"
    SsfSignalEst(const iSel, const mSel, const mY, const mTZ, const mHG, ...);

// "old" ssfpack functions
	
extern "ssfpack,FnSsfRecursion"
	SsfRecursion(const mKSInfo, const mTZ, const mHG, ...);
			   
extern "ssfpack,FnSsfWeights"
	SsfWeights(const iSel, const mYpos, const mTZ, const mHG, ...);

extern "ssfpack,FnSimSmoWgt"
	SimSmoWgt(const ivSel, const mKFInfo, const mTZ, const mHG, ...);

extern "ssfpack,FnSimSmoDraw"
    SimSmoDraw(const ivSel, const mDraw, const mWeight, const mKFInfo,
        const mTZ, const mHG, ...);

#endif // SSFPACK_BASIC_INCLUDED
