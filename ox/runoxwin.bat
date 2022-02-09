
SET pathoxl_windows_tm="C:/Program Files/OxMetrics8/ox/bin64/oxl"
SET namecode=TVB_8
SET pathdata=./data/concat.csv
SET firstday=1926-07-01
SET lastday=2021-12-31
SET namesY=NoDur_vw
SET namesX={Mkt}
SET pathbetas=./betas/betas_SFF_%firstday%_%lastday%_%namesY%_%namesX%.csv
%pathoxl_windows_tm% %namecode%.ox %pathdata% %pathbetas% %firstday% %lastday% %namesY% %namesX%

