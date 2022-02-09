
SsfCombine(const mPhi, const mPhiAdd, const dFill)
{
	// dimension of state vectors
	decl cst = columns(mPhi);
	decl cstadd = columns(mPhiAdd);
	decl csy = rows(mPhi) - cst;

	// combining models
	decl mphi = constant(dFill, cst + cstadd + csy, cst + cstadd);
	mphi[0:][0:] = mPhi[:cst-1][];
	mphi[cst:][cst:] = mPhiAdd[:cstadd-1][];
	mphi[cst + cstadd:][0:] = mPhi[cst:][] ~ mPhiAdd[cstadd:][];

	return mphi;
}

SsfCombineSym(const mOmega, const cSt, const mOmegaAdd, const dFill)
{
	// dimension of state vectors
	decl cst = cSt;
	decl csy = rows(mOmega) - cst;
	decl cstadd = columns(mOmegaAdd) - csy;

	decl momega = constant(dFill, cst + cstadd + csy, cst + cstadd + csy);
	momega[0:][0:] = mOmega[:cst-1][:cst-1];
	momega[cst:][cst:] = mOmegaAdd[:cstadd-1][:cstadd-1];
	momega[cst + cstadd:][0:] = mOmega[cst:][:cst-1] ~ mOmegaAdd[cstadd:][:cstadd-1];
	momega[cst + cstadd:][cst + cstadd:] = mOmega[cst:][cst:];
	momega = setupper(momega, momega');

	return momega;
}
