
SET pathoxl_windows_tm="C:/Program Files/OxMetrics8/ox/bin64/oxl"
SET namecode=TVB_8
SET pathdata=./data/concat5factors.csv
SET firstday=1963-07-05
SET lastday=2021-11-30
SET namesY=Manuf_vw
SET namesX={Mkt}
SET pathbetas=./betas1/betas1_SFF_%firstday%_%lastday%_%namesY%_%namesX%.csv
%pathoxl_windows_tm% %namecode%.ox %pathdata% %pathbetas% %firstday% %lastday% %namesY% %namesX%
