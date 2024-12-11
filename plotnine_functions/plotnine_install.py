
pip install plotnine==0.12.4

pip install matplotlib==3.7.1

# pip show matplotlib 
# pip show plotnine 

dbutils.library.restartPython() 

from plotnine import *
from plotnine.data import mtcars
# import matplotlib 

(ggplot(mtcars, aes("wt", "mpg")) + 
 geom_point())