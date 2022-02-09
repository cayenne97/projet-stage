#include <oxstd.oxh>
#include <oxdraw.h>
#import <database>
#import <maxsqp>
#import <packages/SSF8/SSF.ox>
//#import <packages/SSF9/SSF.ox>

main()
{
	decl path_load_excess_ret="./data/concat.csv";
	decl path_saved_betas_SSF="./betas/betas_SSF.csv";
	decl names_Y={"NoDur_vw"};
	decl first_day=dayofcalendar(2010, 1, 4);
	decl last_day=dayofcalendar(2021, 10, 29);
	decl print_outputs=1;
	decl run_SSF=1;
	decl X_TV={"Mkt","SMB","HML"};

	decl args = arglist(), cargs = sizeof(args);

	println("first_day: ", first_day);
	println("last_day: ", last_day);
	println("first_day: ", "%C", first_day);
	println("last_day: ", "%C", last_day);
	println("names_Y: ", names_Y);
	println("X_TV: ", X_TV);
	if (cargs>1)
	{
		println("args:", args);

		decl idx=1;
        sscan(args[idx++], "%s", &path_load_excess_ret);
        sscan(args[idx++], "%s", &path_saved_betas_SSF);
 //       sscan(args[idx++], "%d", &first_day);
        sscan(args[idx++], "%C", &first_day);
        sscan(args[idx++], "%C", &last_day);
        sscan(args[idx++], "%s", &names_Y);
		names_Y=array(names_Y);

        sscan(args[idx++], "%v", &X_TV);

//		decl allX_TV;
// 		decl nX=cargs-idx;
//		X_TV=new array[nX];
//		for (decl i=0;i<nX;++i)
// 	    	sscan(args[idx++], "%z", &X_TV[i]);

		println("cargs=", cargs);
//		println("nX=",nX);
		println("first_day: ", "%C", first_day);
		println("last_day: ", "%C", last_day);
		println("names_Y: ", names_Y);
		println("X_TV: ", X_TV);
		
	}
	
	if (run_SSF)
	{
		println("\n*** Estimating SSF ***");
		decl dbase = new Database();
		dbase.Load(path_load_excess_ret);
		decl Date=dbase.GetVar("date");
 		decl index_first_obs_in=vecrindex(Date,first_day);
		decl index_last_obs_in=vecrindex(Date,last_day);
		decl Date_in=Date[index_first_obs_in:index_last_obs_in];
		decl Y_all=dbase.GetVar(names_Y);

//		dbase.Info();
		decl X_all=1~dbase.GetVar(X_TV);
		decl a_all_namesX={"Constant"}~X_TV;
		decl model = new SSF();
		model.s_vY=Y_all[index_first_obs_in:index_last_obs_in][];
		model.s_mX=X_all[index_first_obs_in:index_last_obs_in][];
		model.a_names_X=a_all_namesX;
		model.s_cT = rows(model.s_vY);						//Number of observations	
		model.s_sModel = 1;
		decl IC;
		decl para=model.MaxLik(print_outputs,&IC);			//State space regression model
		decl mD=model.Smoothing();							//Perform smoothing prints/draws output
		decl betas_SSF=mD[:sizer(mD)-2][]';

		for (decl i=0;i<sizerc(a_all_namesX);++i)
			DrawTMatrix(i, betas_SSF[][i]', a_all_namesX[i], Date_in',0, 0, 0, 2);
		ShowDrawWindow();
		decl db=new Database();
		db.Create(rows(betas_SSF));
		db.SetDates(Date_in);
		db.Append(betas_SSF,a_all_namesX);
		db.Save(path_saved_betas_SSF); 

		delete dbase;
		delete model;
	}
}