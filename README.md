# Closest-Relative

The closest relative program takes as input a path down the phylotree and returns a set of the closest matches it finds on
the 1kGenomes server. 

First off, clone the repo.
```https://github.com/KavinSub/Closest-Relative.git```

Then setup a virtual environment
```
virtualenv env
source env/bin/activate
pip install
```

Once that's done follow these instructions.
1. First get the raw data for your Mitochondrial DNA from 23andMe. See instructions [here](https://customercare.23andme.com/hc/en-us/articles/202907670-Accessing-your-Raw-Data).
2. Once that's been downloaded you need to convert the raw data to a VCF file. See instructions [here](https://github.com/genepi/23andme-tools).
3. Now use [Haplogrep](http://haplogrep.uibk.ac.at/) to determine the phylotree path. Click run Haplogrep, and open the VCF file you created in step 2. In the bottom right panel you'll see some bubbles containing a string of letters and numbers. Between each bubble there is a box with a number followed by a letter. In positions.txt, starting from the far right of the display, write down the numbers in order on each line. 
4. Run
```
python filter.py
```
5. The closest matches will be printed to stdout. In addition, the data is written to data.json. To see a more visual representation of the data follow the next set of instructions.

To see the data visualization follow these instructions.
1. Run
```
python server.py
```
2. Then in your browser open localhost:5000. The data visualization should show up.